from __future__ import annotations

import argparse
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT_FILE = PROJECT_ROOT / "notes" / "regression_urls.txt"
NEWS_MD_SCRIPT = PROJECT_ROOT / "scripts" / "news_md.py"


def read_urls(input_file: Path) -> list[str]:
    urls = []
    for line in input_file.read_text(encoding="utf-8").splitlines():
        value = line.strip()
        if not value or value.startswith("#"):
            continue
        urls.append(value)
    return urls


def append_log(log_file: Path, message: str = "") -> None:
    print(message)
    with log_file.open("a", encoding="utf-8") as handle:
        handle.write(message + "\n")


def find_output_file(text: str) -> str:
    matches = re.findall(r"[A-Za-z]:\\[^\r\n]+?\.md", text)
    return matches[-1].strip() if matches else ""


def find_first_known_value(text: str, values: list[str]) -> str:
    for value in values:
        if value in text:
            return value
    return "unknown"


def result_from_quality(quality: str, return_code: int, error: str) -> str:
    if return_code != 0 or error:
        return "ERROR" if return_code != 0 else "FAIL"
    if quality == "ok":
        return "OK"
    if quality == "partial_with_noise":
        return "PARTIAL"
    if quality in {"failed", "empty", "empty_body", "wrong_content"}:
        return "FAIL"
    return "TBD"


def markdown_escape(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ").strip()


def run_one_url(index: int, total: int, url: str, log_file: Path) -> dict[str, str | int]:
    append_log(log_file, f"[{index}/{total}] Running: {url}")

    try:
        completed = subprocess.run(
            [sys.executable, str(NEWS_MD_SCRIPT), url],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
    except Exception as exc:
        error = f"{type(exc).__name__}: {exc}"
        append_log(log_file, error)
        append_log(log_file)
        return {
            "no": index,
            "url": url,
            "status": "ERROR",
            "quality": "unknown",
            "method": "unknown",
            "output_file": "",
            "error": error,
            "exit_code": "not_started",
        }

    stdout = completed.stdout.strip()
    stderr = completed.stderr.strip()
    combined_output = "\n".join(part for part in [stdout, stderr] if part)

    append_log(log_file, "--- stdout ---")
    append_log(log_file, stdout if stdout else "(empty)")
    append_log(log_file, "--- stderr ---")
    append_log(log_file, stderr if stderr else "(empty)")
    append_log(log_file, f"exit code: {completed.returncode}")

    method = find_first_known_value(
        combined_output,
        ["url2md4ai", "trafilatura_fallback", "requests_trafilatura"],
    )
    quality = find_first_known_value(
        combined_output,
        [
            "partial_with_noise",
            "possible_partial_content",
            "too_short_uncertain",
            "empty_body",
            "wrong_content",
            "failed",
            "empty",
            "ok",
        ],
    )
    output_file = find_output_file(combined_output)
    error = ""

    if completed.returncode != 0:
        error = stderr or stdout or "process exited with non-zero code"
    elif not output_file:
        error = stderr or "no output file detected"

    status = result_from_quality(quality, completed.returncode, error)
    summary = f"{status} | quality={quality} | method={method} | file={output_file or 'unknown'}"
    if error:
        summary += f" | error={error}"

    append_log(log_file, summary)
    append_log(log_file)

    return {
        "no": index,
        "url": url,
        "status": status,
        "quality": quality,
        "method": method,
        "output_file": output_file,
        "error": error,
        "exit_code": completed.returncode,
    }


def write_result_report(result_file: Path, run_time: str, urls: list[str], results: list[dict[str, str | int]]) -> None:
    counts = {
        "OK": 0,
        "PARTIAL": 0,
        "FAIL": 0,
        "ERROR": 0,
        "TBD": 0,
    }
    for result in results:
        counts[str(result["status"])] = counts.get(str(result["status"]), 0) + 1

    lines = [
        "# news-md v0.4 Batch Validation Result",
        "",
        f"Run time: {run_time}",
        f"URL count: {len(urls)}",
        "",
        "## Summary",
        "",
        f"- Total: {len(urls)}",
        f"- OK: {counts.get('OK', 0)}",
        f"- Partial: {counts.get('PARTIAL', 0)}",
        f"- Fail: {counts.get('FAIL', 0)}",
        f"- Error: {counts.get('ERROR', 0)}",
        f"- TBD: {counts.get('TBD', 0)}",
        "",
        "## Results",
        "",
        "| # | URL | Status | Quality | Method | Output File | Error |",
        "|---|-----|--------|---------|--------|-------------|-------|",
    ]

    for result in results:
        lines.append(
            "| {no} | {url} | {status} | {quality} | {method} | {output_file} | {error} |".format(
                no=result["no"],
                url=markdown_escape(str(result["url"])),
                status=markdown_escape(str(result["status"])),
                quality=markdown_escape(str(result["quality"])),
                method=markdown_escape(str(result["method"])),
                output_file=markdown_escape(str(result["output_file"] or "unknown")),
                error=markdown_escape(str(result["error"] or "")),
            )
        )

    lines.extend(
        [
            "",
            "## Notes",
            "",
            "- This batch runner is for internal validation only.",
            "- It does not change extraction logic.",
            "- It does not prove universal Korean news extraction support.",
            "- It only helps evaluate whether news-md is stable enough for personal workflow and portfolio presentation.",
        ]
    )

    result_file.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Run news-md against a simple URL list.")
    parser.add_argument(
        "-i",
        "--input",
        default=str(DEFAULT_INPUT_FILE),
        help="URL list file. Empty lines and lines starting with # are skipped.",
    )
    args = parser.parse_args()

    input_file = Path(args.input).resolve()
    if not input_file.exists():
        print(f"Input file not found: {input_file}")
        return 1

    urls = read_urls(input_file)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    run_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    result_file = PROJECT_ROOT / "notes" / f"regression_results_{timestamp}.md"
    log_file = PROJECT_ROOT / "notes" / f"powershell_run_log_{timestamp}.txt"

    append_log(log_file, f"batch start time: {run_time}")
    append_log(log_file, f"input file path: {input_file}")
    append_log(log_file, f"total URL count: {len(urls)}")
    append_log(log_file)

    results = []
    for index, url in enumerate(urls, start=1):
        results.append(run_one_url(index, len(urls), url, log_file))

    write_result_report(result_file, run_time, urls, results)

    append_log(log_file, f"batch finish time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    append_log(log_file, f"structured result file: {result_file}")
    append_log(log_file)
    append_log(log_file, "Batch finished.")
    append_log(log_file, f"Result saved to: {result_file}")
    append_log(log_file, f"Run log saved to: {log_file}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
