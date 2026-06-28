from __future__ import annotations

import argparse
import os
import re
import subprocess
from datetime import datetime
from pathlib import Path

import requests
from bs4 import BeautifulSoup


RELATED_NEWS_MARKERS = [
    "실시간 뉴스",
    "실시간 주요 뉴스",
    "가장 많이 본 뉴스",
    "많이 본 뉴스",
    "많이본뉴스",
    "인기 뉴스",
    "인기뉴스",
    "추천 뉴스",
    "관련 뉴스",
    "관련기사",
    "함께 보면 좋은 뉴스",
    "실시간 인기",
    "랭킹뉴스",
    "주요 뉴스",
    "주요뉴스",
    "시선집중",
]

RECOMMENDATION_BLOCK_MARKERS = [
    "실시간 주요 뉴스",
    "시선집중",
    "많이 본 뉴스",
    "많이본뉴스",
    "인기뉴스",
    "인기 뉴스",
    "주요 뉴스",
    "주요뉴스",
    "관련기사",
    "관련 뉴스",
    "추천기사",
    "추천 뉴스",
    "최신기사",
    "랭킹뉴스",
]

TAIL_AGGREGATION_MARKERS = [
    "실시간 주요 뉴스",
    "실시간 인기 기사",
    "실시간 인기",
    "많이 본 뉴스",
    "많이 본 기사",
    "인기뉴스",
    "인기 뉴스",
    "인기 기사",
    "주요 뉴스",
    "주요뉴스",
    "관련기사",
    "관련 뉴스",
    "추천 뉴스",
    "추천기사",
    "최신 기사",
    "최신기사",
    "랭킹뉴스",
    "주간 인기",
]

TAIL_CATEGORY_MARKERS = {
    "연예",
    "스포츠",
    "게임",
}

INTERVIEW_SPEAKER_WORDS = {
    "Q",
    "A",
    "질문",
    "답변",
    "문",
    "답",
    "기자",
    "배우",
    "감독",
    "작가",
    "진행",
    "에디터",
    "인터뷰어",
}

NOISE_MARKERS = [
    "ADVERTISEMENT",
    "Copyright",
    "copyright",
    "©",
    "ⓒ",
    "무단전재",
    "무단 전재",
    "재배포 금지",
    "기사제보",
    "보도자료",
    "기자 이메일",
]

LEADING_VIDEO_MARKERS = [
    "✔ 채널 안내",
    "mydaily studio",
    "✔ 음원 출처",
    "Music provided by",
    "브금대통령",
    "영상",
    "포토월",
]


def fetch_html(url: str) -> str:
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        ),
        "Accept-Language": "ko-KR,ko;q=0.9,en;q=0.8,zh-CN;q=0.7",
    }

    try:
        response = requests.get(url, headers=headers, timeout=20)
        response.raise_for_status()
        response.encoding = response.apparent_encoding or "utf-8"
        return response.text
    except Exception:
        return ""


def fetch_html_with_requests(url: str) -> str:
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        ),
        "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8",
        "Connection": "close",
    }

    try:
        response = requests.get(url, headers=headers, timeout=20)
        response.raise_for_status()
        response.encoding = response.apparent_encoding or "utf-8"
        return response.text
    except Exception as exc:
        print(f"requests fallback 获取失败：{exc}")
        return ""


def extract_published_at_from_html(html: str) -> str:
    if not html:
        return ""

    soup = BeautifulSoup(html, "html.parser")

    meta_rules = [
        ("property", "article:published_time"),
        ("property", "og:article:published_time"),
        ("name", "article:published_time"),
        ("name", "pubdate"),
        ("name", "publishdate"),
        ("name", "date"),
        ("name", "DC.date.issued"),
        ("itemprop", "datePublished"),
    ]

    for attr, value in meta_rules:
        tag = soup.find("meta", attrs={attr: value})
        if tag and tag.get("content"):
            return clean_date(tag["content"])

    time_tag = soup.find("time")
    if time_tag:
        if time_tag.get("datetime"):
            return clean_date(time_tag["datetime"])
        text = time_tag.get_text(" ", strip=True)
        if text:
            return clean_date(text)

    text = soup.get_text("\n", strip=True)

    patterns = [
        r"입력\s*[:：]?\s*(\d{4}[.-]\d{1,2}[.-]\d{1,2}\s+\d{1,2}:\d{2})",
        r"승인\s*[:：]?\s*(\d{4}[.-]\d{1,2}[.-]\d{1,2}\s+\d{1,2}:\d{2})",
        r"등록\s*[:：]?\s*(\d{4}[.-]\d{1,2}[.-]\d{1,2}\s+\d{1,2}:\d{2})",
        r"기사입력\s*[:：]?\s*(\d{4}[.-]\d{1,2}[.-]\d{1,2}\s+\d{1,2}:\d{2})",
        r"최종수정\s*[:：]?\s*(\d{4}[.-]\d{1,2}[.-]\d{1,2}\s+\d{1,2}:\d{2})",
        r"(\d{4}[.-]\d{1,2}[.-]\d{1,2}\s+\d{1,2}:\d{2})",
        r"(\d{4}년\s*\d{1,2}월\s*\d{1,2}일\s*\d{1,2}시\s*\d{1,2}분)",
    ]

    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            return clean_date(match.group(1))

    return ""


def clean_date(value: str) -> str:
    value = value.strip()
    value = re.sub(r"\s+", " ", value)
    value = value.replace("입력", "").replace("승인", "").replace("등록", "").strip(" :：")
    return value


def run_url2md4ai(url: str) -> str:
    result = subprocess.run(
        ["url2md4ai", "--no-links", url],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )

    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "url2md4ai 执行失败")

    return result.stdout


def run_trafilatura_fallback(url: str) -> str:
    try:
        import trafilatura

        downloaded = trafilatura.fetch_url(url)
        if not downloaded:
            return ""

        return (
            trafilatura.extract(
                downloaded,
                output_format="markdown",
                include_comments=False,
                include_tables=True,
                favor_recall=True,
            )
            or ""
        )
    except Exception as exc:
        print(f"trafilatura fallback 失败：{exc}")
        return ""


def run_trafilatura_from_html(url: str) -> str:
    html = fetch_html_with_requests(url)
    if not html:
        return ""

    try:
        import trafilatura

        return (
            trafilatura.extract(
                html,
                url=url,
                output_format="markdown",
                include_comments=False,
                include_tables=True,
                favor_recall=True,
            )
            or ""
        )
    except Exception as exc:
        print(f"requests + trafilatura fallback 失败：{exc}")
        return ""


def has_korean(text: str) -> bool:
    return bool(re.search(r"[가-힣]", text))


def is_image_line(line: str) -> bool:
    return bool(re.match(r"^\s*!\[[^\]]*\]\([^)]+\)\s*$", line.strip()))


def strip_markdown_syntax(line: str) -> str:
    line = re.sub(r"!\[[^\]]*\]\([^)]+\)", "", line)
    line = re.sub(r"\[[^\]]+\]\([^)]+\)", "", line)
    line = re.sub(r"^[#>*\-\s`|]+", "", line)
    line = re.sub(r"[*_`~]", "", line)
    return re.sub(r"\s+", " ", line).strip()


def split_frontmatter(markdown: str) -> tuple[str, str]:
    lines = markdown.splitlines()
    if len(lines) < 2 or lines[0].strip() != "---":
        return "", markdown

    for index in range(1, len(lines)):
        if lines[index].strip() == "---":
            prefix = "\n".join(lines[: index + 1]).strip() + "\n\n"
            body = "\n".join(lines[index + 1 :])
            return prefix, body

    return "", markdown


def is_reporter_email_line(line: str) -> bool:
    text = strip_markdown_syntax(line)
    email_pattern = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"

    if len(text) < 120 and re.search(email_pattern, text):
        return True

    if re.fullmatch(r"/\s*[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", text):
        return True

    if "@" in text and len(text) < 100 and "기자" in text:
        return True

    if "@" in text and len(text) < 100 and re.search(r"(뉴스엔|텐아시아|마이데일리|스포츠조선)", text):
        return True

    if re.fullmatch(email_pattern, text):
        return True

    return bool(re.fullmatch(r"[가-힣]{2,4}\s*기자\s*" + email_pattern, text))


def is_noise_line(line: str) -> bool:
    text = strip_markdown_syntax(line)
    if not text:
        return False

    if is_reporter_email_line(text):
        return True

    if text == "AD":
        return True

    if text.startswith("- ⓒ") or text.startswith("ⓒ"):
        return True

    if len(text) < 120 and re.search(r"ⓒ\s*[가-힣A-Za-z]+\(www\.[^)]+\)", text):
        return True

    short_noise_markers = [
        "이미지 확대 보기",
        "제보를 받습니다",
        "기사제보",
        "보도자료",
        "언론사로 이동합니다",
        "더 많은 컨텐츠를 만나보세요",
        "더 많은 콘텐츠를 만나보세요",
        "사이트에서 더 많은",
        "직접 확인하세요",
    ]

    if len(text) < 140 and any(marker in text for marker in short_noise_markers):
        return True

    if len(text) < 100 and re.match(r"^\[?사진\]?\s+", text):
        return True

    if len(text) < 80 and text == "제보":
        return True

    if any(marker in text for marker in NOISE_MARKERS):
        if len(text) < 90 or not any(quote in text for quote in ['"', "'", "“", "”", "‘", "’"]):
            return True

    return False


def has_hashtag_stack(text: str) -> bool:
    return len(re.findall(r"#[\w가-힣]+", text)) >= 2


def is_related_news_heading(text: str) -> bool:
    return any(marker == text or marker in text for marker in RELATED_NEWS_MARKERS)


def is_recommendation_block_marker(text: str) -> bool:
    normalized = re.sub(r"\s+", "", text).lower()
    return any(re.sub(r"\s+", "", marker).lower() in normalized for marker in RECOMMENDATION_BLOCK_MARKERS)


def is_long_article_paragraph(line: str) -> bool:
    text = strip_markdown_syntax(line)
    return (
        len(text) > 80
        and has_korean(text)
        and not line.lstrip().startswith("- ")
        and not is_related_news_heading(text)
        and not has_hashtag_stack(text)
    )


def is_short_news_title_line(line: str) -> bool:
    text = strip_markdown_syntax(line)
    if not text or not has_korean(text):
        return False

    return line.lstrip().startswith("- ") or (8 <= len(text) <= 85 and not text.endswith((".", "다", "요")))


def is_probable_speaker_marker(value: str) -> bool:
    speaker = strip_markdown_syntax(value).strip(" :：.·")
    if not speaker or len(speaker) > 12:
        return False

    if speaker in INTERVIEW_SPEAKER_WORDS:
        return True

    if re.fullmatch(r"[A-Z]{1,4}", speaker):
        return True

    return bool(re.fullmatch(r"[가-힣]{1,6}(기자|배우|감독|작가|진행|에디터)", speaker))


def count_bold_speaker_markers(text: str) -> int:
    return sum(
        1
        for match in re.finditer(r"\*\*([^*\n]{1,16})\*\*", text)
        if is_probable_speaker_marker(match.group(1))
    )


def normalize_interview_qa_markers(markdown: str) -> str:
    def replace_marker(match: re.Match[str]) -> str:
        speaker = match.group(2)
        if not is_probable_speaker_marker(speaker):
            return match.group(0)
        marker = f"**{speaker.strip()}**"
        return f"\n\n{marker}\n"

    normalized = re.sub(r"\s*(\*\*([^*\n]{1,16})\*\*)\s*", lambda m: replace_marker(m), markdown)
    normalized = re.sub(r"\n{3,}", "\n\n", normalized)
    return normalized.strip() + "\n" if normalized.strip() else ""


def clean_leading_related_news_block(markdown: str) -> str:
    lines = markdown.splitlines()
    first_text_index = None

    for index, line in enumerate(lines):
        if strip_markdown_syntax(line):
            first_text_index = index
            break

    if first_text_index is None:
        return markdown

    heading_index = None
    for index in range(first_text_index, min(len(lines), first_text_index + 8)):
        text = strip_markdown_syntax(lines[index])
        if is_related_news_heading(text):
            heading_index = index
            break

    if heading_index is None:
        return markdown

    title_count = 0
    article_start = None

    for index in range(heading_index + 1, len(lines)):
        line = lines[index]
        text = strip_markdown_syntax(line)

        if not text:
            continue

        if is_long_article_paragraph(line):
            article_start = index
            break

        if is_short_news_title_line(line):
            title_count += 1
            continue

        if title_count >= 3:
            continue

        break

    if article_start is not None and title_count >= 2:
        return "\n".join(lines[article_start:]).lstrip() + "\n"

    return markdown


def is_article_lead_line(line: str) -> bool:
    text = strip_markdown_syntax(line)
    if re.match(r"^\[[^\]]+\s*=\s*[^]]*기자\]", text):
        return True
    if re.search(r"마이데일리\s*=\s*[^,\]]+\s*기자", text):
        return True
    if re.match(r"^\[[^\]]+\s+기자\]", text):
        return True
    return bool(len(text) > 100 and "기자" in text and re.search(r"\d{1,2}일|오전|오후|서울|부산|인천|경기", text))


def clean_leading_video_or_channel_block(markdown: str) -> str:
    lines = markdown.splitlines()
    first_text_index = None

    for index, line in enumerate(lines):
        if strip_markdown_syntax(line):
            first_text_index = index
            break

    if first_text_index is None:
        return markdown

    lead_index = None
    for index in range(first_text_index, min(len(lines), first_text_index + 40)):
        if is_article_lead_line(lines[index]):
            lead_index = index
            break

    if lead_index is None or lead_index <= first_text_index:
        return markdown

    leading_text = "\n".join(strip_markdown_syntax(line) for line in lines[first_text_index:lead_index])
    marker_count = sum(1 for marker in LEADING_VIDEO_MARKERS if marker in leading_text)
    hashtag_count = len(re.findall(r"#[\w가-힣]+", leading_text))

    if marker_count >= 1 or hashtag_count >= 2:
        return "\n".join(lines[lead_index:]).lstrip() + "\n"

    return markdown


def normalize_text_paragraph(paragraph: str) -> str:
    lines = [strip_markdown_syntax(line) for line in paragraph.splitlines()]
    text = " ".join(line for line in lines if line)
    return re.sub(r"\s+", " ", text).strip()


def paragraph_is_only_images(paragraph: str) -> bool:
    lines = [line for line in paragraph.splitlines() if line.strip()]
    return bool(lines) and all(is_image_line(line) for line in lines)


def dedupe_markdown_paragraphs(markdown: str) -> str:
    paragraphs = re.split(r"\n\s*\n", markdown.strip())
    seen = set()
    kept = []

    for paragraph in paragraphs:
        if not paragraph.strip():
            continue

        if paragraph_is_only_images(paragraph):
            kept.append(paragraph.strip())
            continue

        normalized = normalize_text_paragraph(paragraph)
        if normalized and len(normalized) > 30:
            if normalized in seen:
                continue
            seen.add(normalized)

        kept.append(paragraph.strip())

    return "\n\n".join(kept).strip() + "\n" if kept else ""


def is_trailing_block_start(line: str) -> bool:
    text = strip_markdown_syntax(line)
    trailing_markers = [
        "이데일리에서 직접 확인하세요",
        "언론사로 이동합니다",
        "더 많은 컨텐츠를 만나보세요",
        "더 많은 콘텐츠를 만나보세요",
        "사이트에서 더 많은",
        "제보를 받습니다",
    ]

    return len(text) < 140 and any(marker in text for marker in trailing_markers)


def is_tail_recommendation_marker(line: str) -> bool:
    text = strip_markdown_syntax(line)
    if not text or len(text) > 120:
        return False

    markers = [
        "추천기사",
        "최신기사",
        "인기 기사",
        "인기기사",
        "실시간 인기",
        "실시간 주요 뉴스",
        "주간 인기",
        "주요뉴스",
        "많이 본 뉴스",
        "PEOPLE NOW",
        "BEAUTY TREND",
        "뷰티 트렌드",
        "통합검색",
    ]

    return any(marker.lower() in text.lower() for marker in markers)


def is_tail_aggregation_marker_line(line: str) -> bool:
    text = strip_markdown_syntax(line)
    if not text or len(text) > 80:
        return False

    normalized = re.sub(r"\s+", "", text).lower()
    if any(re.sub(r"\s+", "", marker).lower() in normalized for marker in TAIL_AGGREGATION_MARKERS):
        return True

    return text.strip("[]()<>:：|·ㆍ ") in TAIL_CATEGORY_MARKERS


def is_numbered_or_bullet_title_line(line: str) -> bool:
    text = strip_markdown_syntax(line)
    if not text or not has_korean(text):
        return False

    has_list_prefix = bool(re.match(r"^\s*(?:[-*+]|\d{1,2}[.)]|[①-⑳])\s*", line))
    return has_list_prefix and 4 <= len(text) <= 100


def has_enough_body_before_tail_marker(lines: list[str], marker_index: int) -> bool:
    before = "\n".join(lines[:marker_index])
    stats = get_content_stats(before)

    standard_article_body = (
        marker_index >= 8
        and stats["content_line_count"] >= 3
        and stats["korean_chars"] >= 300
    )

    xports_style_short_body = (
        marker_index >= 16
        and stats["content_line_count"] >= 5
        and stats["korean_chars"] >= 120
    )

    return standard_article_body or xports_style_short_body


def tail_after_marker_looks_aggregated(lines: list[str], marker_index: int) -> bool:
    short_title_count = 0
    list_title_count = 0
    long_paragraph_count = 0
    marker_count = 0
    scanned_text_count = 0

    for line in lines[marker_index + 1 : marker_index + 31]:
        text = strip_markdown_syntax(line)
        if not text or is_image_line(line) or is_noise_line(line):
            continue

        scanned_text_count += 1
        if is_tail_aggregation_marker_line(line) or is_recommendation_block_marker(text):
            marker_count += 1
            continue

        if is_numbered_or_bullet_title_line(line):
            list_title_count += 1
            continue

        if is_short_news_title_line(line):
            short_title_count += 1
            continue

        if is_long_article_paragraph(line):
            long_paragraph_count += 1

    if scanned_text_count <= 1:
        return True

    list_like_count = short_title_count + list_title_count
    return (
        long_paragraph_count <= 1
        and (
            marker_count >= 1
            or list_title_count >= 3
            or short_title_count >= 4
            or (list_like_count >= 3 and list_like_count >= long_paragraph_count + 3)
        )
    )


def get_tail_cleanup_reason(line: str) -> str:
    text = strip_markdown_syntax(line)
    if re.search(r"랭킹|순위|많이\s*본|인기", text):
        return "TAIL_RANKING_LIST_REMOVED"
    if re.search(r"추천|관련", text):
        return "TAIL_RECOMMENDATION_BLOCK_REMOVED"
    return "TAIL_AGGREGATION_BLOCK_REMOVED"


def find_tail_aggregation_block_start(lines: list[str]) -> tuple[int | None, str]:
    if len(lines) < 10:
        return None, ""

    first_text_indexes = [index for index, line in enumerate(lines) if strip_markdown_syntax(line)]
    if not first_text_indexes:
        return None, ""

    first_text_index = first_text_indexes[0]
    scan_start = max(first_text_index + 6, len(lines) // 3)

    for index in range(scan_start, len(lines)):
        if not is_tail_aggregation_marker_line(lines[index]):
            continue

        before = "\n".join(lines[:index])
        before_stats = get_content_stats(before)
        marker_in_late_body = index >= len(lines) // 2
        enough_body_before = (
            before_stats["content_line_count"] >= 5
            and before_stats["long_article_paragraph_count"] >= 3
            and before_stats["korean_chars"] >= 450
        )
        enough_long_body_before = (
            before_stats["content_line_count"] >= 8
            and before_stats["korean_chars"] >= 800
        )

        if not (marker_in_late_body or enough_long_body_before):
            continue
        if not enough_body_before:
            continue
        if not tail_after_marker_looks_aggregated(lines, index):
            continue

        return index, get_tail_cleanup_reason(lines[index])

    return None, ""


def clean_trailing_promo_or_related_block(markdown: str) -> str:
    lines = markdown.splitlines()
    if not lines:
        return markdown

    scan_start = max(0, len(lines) - 45)

    for index in range(scan_start, len(lines)):
        if is_trailing_block_start(lines[index]):
            return "\n".join(lines[:index]).rstrip() + "\n"

        if (
            is_tail_recommendation_marker(lines[index])
            and has_enough_body_before_tail_marker(lines, index)
            and tail_after_marker_looks_aggregated(lines, index)
        ):
            return "\n".join(lines[:index]).rstrip() + "\n"

    trailing_list_start = None
    trailing_list_count = 0
    for index in range(len(lines) - 1, scan_start - 1, -1):
        text = strip_markdown_syntax(lines[index])
        if not text:
            continue

        if lines[index].lstrip().startswith("- ") and 8 <= len(text) <= 90 and has_korean(text):
            trailing_list_start = index
            trailing_list_count += 1
            continue

        break

    if trailing_list_start is not None and trailing_list_count >= 3:
        return "\n".join(lines[:trailing_list_start]).rstrip() + "\n"

    cleaned_lines = list(lines)
    while cleaned_lines:
        text = strip_markdown_syntax(cleaned_lines[-1])
        if not text:
            cleaned_lines.pop()
            continue

        if is_noise_line(cleaned_lines[-1]):
            cleaned_lines.pop()
            continue

        break

    return "\n".join(cleaned_lines).rstrip() + "\n" if cleaned_lines else ""


def dedupe_adjacent_short_lines(markdown: str) -> str:
    lines = markdown.splitlines()
    kept = []
    last_text = ""

    for line in lines:
        text = strip_markdown_syntax(line)
        if text and text == last_text and len(text) <= 80 and not is_image_line(line):
            continue

        kept.append(line)
        if text:
            last_text = text

    return "\n".join(kept).rstrip() + "\n" if kept else ""


def get_content_stats(markdown: str) -> dict:
    lines = markdown.splitlines()
    content_lines = []
    ad_marker_count = 0
    related_news_marker_count = 0
    recommendation_marker_count = 0
    short_title_line_count = 0
    long_article_paragraph_count = 0
    nonempty_text_line_count = 0
    collapsed_interview_marker_lines = 0
    speaker_marker_line_count = 0
    image_count = 0

    for line in lines:
        text = strip_markdown_syntax(line)

        if is_image_line(line):
            image_count += 1
            continue

        if text:
            nonempty_text_line_count += 1

        if (
            "ADVERTISEMENT" in line
            or strip_markdown_syntax(line) == "AD"
            or any(marker in line for marker in ("Copyright", "copyright", "©", "ⓒ", "무단전재", "무단 전재"))
        ):
            ad_marker_count += 1

        if any(marker in text for marker in RELATED_NEWS_MARKERS):
            related_news_marker_count += 1
        if is_recommendation_block_marker(text):
            recommendation_marker_count += 1

        if is_short_news_title_line(line):
            short_title_line_count += 1
        if is_long_article_paragraph(line):
            long_article_paragraph_count += 1
        if count_bold_speaker_markers(line) >= 4:
            collapsed_interview_marker_lines += 1
        if count_bold_speaker_markers(line) == 1 and re.fullmatch(r"\*\*[^*\n]{1,16}\*\*", line.strip()):
            speaker_marker_line_count += 1

        if any(marker in text for marker in RELATED_NEWS_MARKERS):
            continue

        if is_noise_line(line):
            continue

        if len(text) > 25 and has_korean(text):
            content_lines.append(text)

    plain_text = "\n".join(content_lines)

    return {
        "total_chars": len(markdown or ""),
        "korean_chars": len(re.findall(r"[가-힣]", plain_text)),
        "content_line_count": len(content_lines),
        "image_count": image_count,
        "ad_marker_count": ad_marker_count,
        "related_news_marker_count": related_news_marker_count,
        "recommendation_marker_count": recommendation_marker_count,
        "short_title_line_count": short_title_line_count,
        "long_article_paragraph_count": long_article_paragraph_count,
        "nonempty_text_line_count": nonempty_text_line_count,
        "collapsed_interview_marker_lines": collapsed_interview_marker_lines,
        "speaker_marker_line_count": speaker_marker_line_count,
    }


def count_related_title_lines_after_marker(lines: list[str], marker_index: int) -> int:
    count = 0
    scanned = 0

    for line in lines[marker_index + 1 : marker_index + 14]:
        text = strip_markdown_syntax(line)
        if not text:
            continue

        scanned += 1
        if is_image_line(line) or is_noise_line(line):
            continue

        looks_like_title = has_korean(text) and 8 <= len(text) <= 85
        if looks_like_title:
            count += 1
        elif scanned <= 3:
            continue
        else:
            break

    return count


def has_leading_video_channel_noise(markdown: str) -> bool:
    _, body = split_frontmatter(markdown)
    body_lines = body.splitlines()
    first_text_index = None

    for index, line in enumerate(body_lines):
        if strip_markdown_syntax(line):
            first_text_index = index
            break

    if first_text_index is None:
        return False

    lead_index = None
    for index in range(first_text_index, min(len(body_lines), first_text_index + 20)):
        if is_article_lead_line(body_lines[index]):
            lead_index = index
            break

    check_end = lead_index if lead_index is not None else min(len(body_lines), first_text_index + 12)
    leading_text = "\n".join(strip_markdown_syntax(line) for line in body_lines[first_text_index:check_end])

    if not leading_text.strip():
        return False

    strong_marker_count = 0
    if re.search(r"채널\s*(안내|구독)|구독|좋아요", leading_text):
        strong_marker_count += 1
    if re.search(r"음원\s*출처|Music provided|브금대통령|music source", leading_text, re.IGNORECASE):
        strong_marker_count += 1
    if re.search(r"영상\s*(설명|출처|제공)", leading_text):
        strong_marker_count += 1
    if "mydaily studio" in leading_text:
        strong_marker_count += 1

    hashtag_count = len(re.findall(r"#[\w가-힣]+", leading_text))
    if hashtag_count >= 2 or "해시태그" in leading_text:
        strong_marker_count += 1

    return strong_marker_count >= 1


def get_list_like_quality_reasons(stats: dict) -> list[str]:
    if stats["recommendation_marker_count"] <= 0:
        return []

    text_lines = max(stats["nonempty_text_line_count"], 1)
    short_title_ratio = stats["short_title_line_count"] / text_lines
    too_few_article_paragraphs = stats["long_article_paragraph_count"] <= 1
    list_like_content = (
        stats["short_title_line_count"] >= 4
        or (stats["short_title_line_count"] >= 3 and short_title_ratio >= 0.45)
        or short_title_ratio >= 0.6
    )

    if not (too_few_article_paragraphs and list_like_content):
        return []

    reasons = [
        "ARTICLE_BODY_MISSING",
        "LIST_LIKE_CONTENT",
        "POSSIBLE_RECOMMENDATION_BLOCK",
    ]
    if too_few_article_paragraphs:
        reasons.append("TOO_FEW_ARTICLE_PARAGRAPHS")
    return reasons


def has_possible_media_paragraph_loss(stats: dict) -> bool:
    if stats["image_count"] < 2:
        return False

    return (
        stats["content_line_count"] <= 8
        or stats["long_article_paragraph_count"] <= 4
        or stats["image_count"] >= stats["content_line_count"]
    )


def assess_markdown_quality(markdown: str) -> tuple[str, list[str]]:
    if not markdown or not markdown.strip():
        return "empty", ["正文为空"]

    reasons = []
    lines = markdown.splitlines()
    stats = get_content_stats(markdown)
    info_reasons = []

    if stats["speaker_marker_line_count"] >= 2:
        info_reasons.append("INTERVIEW_QA_FORMAT_NORMALIZED")
    if stats["collapsed_interview_marker_lines"] > 0:
        reasons.append("INTERVIEW_QA_FORMAT_COLLAPSED")

    list_like_reasons = get_list_like_quality_reasons(stats)
    if list_like_reasons:
        return "wrong_content", list_like_reasons

    for index, line in enumerate(lines):
        text = strip_markdown_syntax(line)
        if any(marker in text for marker in RELATED_NEWS_MARKERS):
            title_count = count_related_title_lines_after_marker(lines, index)
            marker_near_start = index <= 12
            marker_in_body = stats["content_line_count"] <= 4 or stats["long_article_paragraph_count"] <= 1
            if title_count >= 3 and (marker_near_start or marker_in_body):
                return "wrong_content", [
                    "ARTICLE_BODY_MISSING",
                    "LIST_LIKE_CONTENT",
                    "POSSIBLE_RECOMMENDATION_BLOCK",
                    f"疑似推荐/热门新闻区块：{text}",
                ]

    if stats["content_line_count"] == 0 and stats["korean_chars"] == 0:
        return "empty", ["未发现有效韩文正文段落"]

    if stats["ad_marker_count"] > 0:
        reasons.append("包含广告/版权/转载噪声")

    if any(marker in markdown for marker in NOISE_MARKERS if marker != "ADVERTISEMENT"):
        reasons.append("包含版权/转载/投稿等噪声")

    if has_leading_video_channel_noise(markdown):
        reasons.append("疑似前置视频/频道宣传块")

    trailing_lines = lines[max(0, len(lines) - 30) :]
    if any(is_trailing_block_start(line) for line in trailing_lines):
        reasons.append("疑似尾部推广/相关新闻块")

    if stats["image_count"] >= 3 and stats["content_line_count"] <= 5:
        reasons.append("多张 Markdown 图片但有效正文段落较少")

    if reasons:
        if has_possible_media_paragraph_loss(stats):
            reasons.extend(["POSSIBLE_PARAGRAPH_LOSS", "BODY_INCOMPLETE_AFTER_MEDIA_BLOCK"])
        return "partial_with_noise", reasons

    if has_possible_media_paragraph_loss(stats):
        return "possible_partial_content", [
            "POSSIBLE_PARAGRAPH_LOSS",
            "BODY_INCOMPLETE_AFTER_MEDIA_BLOCK",
            "正文中间有多个图片块且图片前后正文偏少",
        ]

    if stats["content_line_count"] < 2 or stats["korean_chars"] < 120:
        return "too_short_uncertain", ["正文较短，无法确定是否为原文长度"]

    return "ok", info_reasons


def has_minimum_article_body(markdown: str) -> bool:
    stats = get_content_stats(markdown)
    return stats["content_line_count"] >= 1 and stats["korean_chars"] >= 120


def clean_markdown_noise_with_reasons(markdown: str) -> tuple[str, list[str]]:
    frontmatter, body = split_frontmatter(markdown)
    cleaned_lines = []
    last_caption = ""
    cleanup_reasons = []

    for line in body.splitlines():
        stripped = line.strip()
        text = strip_markdown_syntax(line)

        if not stripped:
            cleaned_lines.append(line)
            continue

        if is_noise_line(line):
            continue

        is_short_caption = has_korean(text) and len(text) <= 35 and not re.search(r"[.!?。]$", text)
        if is_short_caption and text == last_caption:
            continue
        if is_short_caption:
            last_caption = text

        cleaned_lines.append(line)

    cleaned = "\n".join(cleaned_lines)
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned).strip()
    cleaned = cleaned + "\n" if cleaned else ""
    cleaned = normalize_interview_qa_markers(cleaned)
    cleaned = clean_leading_related_news_block(cleaned)
    cleaned = clean_leading_video_or_channel_block(cleaned)
    cleaned = dedupe_markdown_paragraphs(cleaned)
    cleaned = dedupe_adjacent_short_lines(cleaned)

    tail_lines = cleaned.splitlines()
    tail_start, tail_reason = find_tail_aggregation_block_start(tail_lines)
    if tail_start is not None:
        cleaned = "\n".join(tail_lines[:tail_start]).rstrip() + "\n"
        cleanup_reasons.append(tail_reason)

    cleaned = clean_trailing_promo_or_related_block(cleaned)
    return (frontmatter + cleaned if cleaned else frontmatter), cleanup_reasons


def clean_markdown_noise(markdown: str) -> str:
    cleaned, _ = clean_markdown_noise_with_reasons(markdown)
    return cleaned


def is_fallback_clearly_more_complete(primary_stats: dict, fallback_stats: dict) -> bool:
    return (
        fallback_stats["content_line_count"] >= primary_stats["content_line_count"] + 2
        or fallback_stats["korean_chars"] >= primary_stats["korean_chars"] * 1.25 + 100
    )


def merge_quality_reasons(*reason_groups: list[str]) -> list[str]:
    merged = []
    for reasons in reason_groups:
        for reason in reasons:
            if reason and reason not in merged:
                merged.append(reason)
    return merged


def choose_best_markdown(primary: str, fallback: str) -> tuple[str, str, str, list[str]]:
    primary_clean, primary_cleanup_reasons = clean_markdown_noise_with_reasons(primary)
    fallback_clean, fallback_cleanup_reasons = clean_markdown_noise_with_reasons(fallback)

    primary_status, primary_reasons = assess_markdown_quality(primary_clean)
    fallback_status, fallback_reasons = assess_markdown_quality(fallback_clean)
    primary_reasons = merge_quality_reasons(primary_cleanup_reasons, primary_reasons)
    fallback_reasons = merge_quality_reasons(fallback_cleanup_reasons, fallback_reasons)
    primary_stats = get_content_stats(primary_clean)
    fallback_stats = get_content_stats(fallback_clean)

    if primary_status == "wrong_content" and fallback_status not in ("wrong_content", "empty"):
        return fallback_clean, "trafilatura_fallback", fallback_status, fallback_reasons

    if fallback_status in ("wrong_content", "empty"):
        return primary_clean, "url2md4ai", primary_status, primary_reasons

    if (
        primary_status == "partial_with_noise"
        and fallback_stats["content_line_count"] > primary_stats["content_line_count"]
        and fallback_status != "wrong_content"
    ):
        return fallback_clean, "trafilatura_fallback", fallback_status, fallback_reasons

    if primary_status == "possible_partial_content" and is_fallback_clearly_more_complete(
        primary_stats, fallback_stats
    ):
        return fallback_clean, "trafilatura_fallback", fallback_status, fallback_reasons

    if (
        primary_status in ("partial_with_noise", "possible_partial_content")
        and primary_stats["image_count"] >= 2
        and not is_fallback_clearly_more_complete(primary_stats, fallback_stats)
    ):
        return primary_clean, "url2md4ai", primary_status, primary_reasons

    if (
        primary_status not in ("wrong_content", "empty")
        and fallback_status not in ("wrong_content", "empty")
        and is_fallback_clearly_more_complete(primary_stats, fallback_stats)
    ):
        return fallback_clean, "trafilatura_fallback", fallback_status, fallback_reasons

    quality_rank = {
        "empty": 0,
        "wrong_content": 1,
        "partial_with_noise": 2,
        "possible_partial_content": 3,
        "too_short_uncertain": 4,
        "ok": 5,
    }

    if fallback_clean and quality_rank.get(fallback_status, 0) > quality_rank.get(primary_status, 0):
        return fallback_clean, "trafilatura_fallback", fallback_status, fallback_reasons

    return primary_clean, "url2md4ai", primary_status, primary_reasons


def inject_published_at(markdown: str, published_at: str) -> str:
    if not published_at:
        return markdown

    lines = markdown.splitlines()

    if len(lines) >= 2 and lines[0].strip() == "---":
        end_index = None

        for i in range(1, len(lines)):
            if lines[i].strip() == "---":
                end_index = i
                break

        if end_index is not None:
            frontmatter = lines[:end_index]
            rest = lines[end_index:]

            if not any(line.startswith("published_at:") for line in frontmatter):
                insert_at = len(frontmatter)

                for idx, line in enumerate(frontmatter):
                    if line.startswith("source:"):
                        insert_at = idx + 1
                        break

                frontmatter.insert(insert_at, f'published_at: "{published_at}"')

            return "\n".join(frontmatter + rest) + "\n"

    return f'---\npublished_at: "{published_at}"\n---\n\n{markdown}'


def yaml_quote(value: str) -> str:
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'


def format_yaml_list(values: list[str]) -> str:
    if not values:
        return "[]"

    return "[" + ", ".join(yaml_quote(value) for value in values) + "]"


def inject_extraction_metadata(
    markdown: str,
    extraction_method: str,
    quality_status: str,
    quality_reasons: list[str],
) -> str:
    fields = {
        "extraction_method": yaml_quote(extraction_method),
        "quality_status": yaml_quote(quality_status),
        "quality_reasons": format_yaml_list(quality_reasons),
    }

    lines = markdown.splitlines()

    if len(lines) >= 2 and lines[0].strip() == "---":
        end_index = None
        for i in range(1, len(lines)):
            if lines[i].strip() == "---":
                end_index = i
                break

        if end_index is not None:
            frontmatter = lines[:end_index]
            rest = lines[end_index:]
            frontmatter = [
                line
                for line in frontmatter
                if not any(line.startswith(f"{field}:") for field in fields)
            ]

            for field, value in fields.items():
                frontmatter.append(f"{field}: {value}")

            return "\n".join(frontmatter + rest) + "\n"

    metadata = ["---"] + [f"{field}: {value}" for field, value in fields.items()] + ["---"]
    return "\n".join(metadata) + "\n\n" + markdown


def main():
    parser = argparse.ArgumentParser(description="Extract clean news markdown with published_at.")
    parser.add_argument("url", nargs="?", help="新闻链接")
    parser.add_argument(
        "-o",
        "--output-dir",
        default=os.environ.get("NEWS_MD_OUTPUT_DIR", "outputs"),
        help="Markdown 保存目录，默认 outputs；可用 NEWS_MD_OUTPUT_DIR 覆盖",
    )
    parser.add_argument(
        "--print",
        action="store_true",
        help="不保存文件，直接输出到终端",
    )

    args = parser.parse_args()

    if not args.url:
        args.url = input("请输入新闻链接：").strip()

    if not args.url:
        print("未输入新闻链接，已退出")
        return

    html = fetch_html(args.url)
    published_at = extract_published_at_from_html(html)

    extraction_method = "url2md4ai"

    try:
        primary_markdown = run_url2md4ai(args.url)
        fallback_markdown = run_trafilatura_fallback(args.url)
        markdown, extraction_method, quality_status, quality_reasons = choose_best_markdown(
            primary_markdown, fallback_markdown
        )
    except RuntimeError as exc:
        message = str(exc)
        if "UNEXPECTED_EOF_WHILE_READING" not in message:
            raise

        print("抓取失败：FETCH_FAILED_SSL")
        print("原因：网站 HTTPS 连接被提前中断")
        print("建议：优先尝试 Naver News 链接，或稍后重试")
        markdown, cleanup_reasons = clean_markdown_noise_with_reasons(run_trafilatura_from_html(args.url))
        extraction_method = "requests_trafilatura"
        quality_status, quality_reasons = assess_markdown_quality(markdown)
        quality_reasons = merge_quality_reasons(cleanup_reasons, quality_reasons)

    if extraction_method in ("trafilatura_fallback", "requests_trafilatura") and not has_minimum_article_body(markdown):
        quality_status = "empty_body"
        quality_reasons = ["fallback produced no usable article body"]
        failed_markdown = inject_extraction_metadata(
            markdown,
            extraction_method,
            quality_status,
            quality_reasons,
        )

        if args.print:
            print(failed_markdown)
            return

        print("抓取失败：EMPTY_BODY")
        print(f"抽取方式：{extraction_method}")
        print(f"正文质量：{quality_status}")
        print("质量原因：" + "；".join(quality_reasons))
        return

    markdown = inject_published_at(markdown, published_at)
    markdown = inject_extraction_metadata(
        markdown,
        extraction_method,
        quality_status,
        quality_reasons,
    )

    if args.print:
        print(markdown)
        return

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    filename = f"news_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    output_path = output_dir / filename

    output_path.write_text(markdown, encoding="utf-8")

    print(f"已保存：{output_path}")
    print(f"抽取方式：{extraction_method}")
    print(f"正文质量：{quality_status}")
    if quality_reasons:
        print("质量原因：" + "；".join(quality_reasons))

    if published_at:
        print(f"发布时间：{published_at}")
    else:
        print("发布时间：未提取到")


if __name__ == "__main__":
    main()
