# Limitations

## Project status

`news-md` is currently in **Internal Validation / Portfolio-ready documentation** status.

The current archived project state is:

- `news-md v0.4.1 archived`
- `status: human-review quality fix passed with known limitations`
- `v0.5: GitHub-ready / Portfolio-ready documentation preparation`

This is not a Public Release. The tool is not guaranteed to work on every Korean news site, every article layout, or every media-heavy page. Human review is recommended before using the output for archive-quality research, citation, or final reference.

## What news-md can help with

`news-md` is designed for a narrow local workflow:

```text
single Korean news URL -> extract article body -> clean obvious noise -> save Markdown
```

It can help with:

- Turning a single Korean news article link into a reviewable Markdown file.
- Removing obvious page noise such as large recommendation, ranking, or aggregation blocks when they are detected safely.
- Producing cleaner input for later AI translation, summarization, and close reading.
- Supporting personal content research and archive review.
- Adding quality signals that make the output easier to inspect before reuse.

The goal is not perfect automated extraction. The goal is a lightweight preprocessing step that makes human review and downstream AI work easier.

## What news-md does not guarantee

`news-md` does not guarantee that:

- Every Korean news site can be accessed or extracted successfully.
- Every article body will be complete.
- Every recommendation, popular-news, ranking, copyright, reporter, or related-link block will be removed.
- Every title, source, or publication time will be detected.
- `quality_status: ok` means the output is perfect.
- The generated Markdown can be used as final reference text without human review.

The output should be treated as a structured draft for review, not as an authoritative copy of the original article.

## Known limitation categories

### 1. Site access and page structure variation

Korean news sites vary widely in HTML structure, embedded media layout, metadata conventions, and access behavior. A page that works today may change later if the site updates its layout.

Some failures are caused by access or loading conditions rather than article-cleaning logic, including:

- blocked requests
- redirects
- SSL or network errors
- no extractable content
- dynamically loaded article bodies
- pages that require behavior closer to a browser session

In these cases, `news-md` may fail, return an empty body, or produce only partial content.

### 2. Media-heavy articles

Video-heavy or image-heavy articles can be difficult to extract reliably. Some pages contain video captions, image descriptions, embedded titles, or related article links near the real article body.

In this category, the extractor may capture:

- video notes instead of the main body
- image captions without enough surrounding article text
- headline-like fragments from nearby content blocks
- unrelated article titles from page modules

The v0.4.1 quality fix improved classification for this class of issue. In particular, outputs that look like media fragments or unrelated lists should no longer be treated too easily as clean `ok` results. However, the underlying extraction may still be incomplete.

### 3. Possible paragraph loss around media blocks

Articles with many images or embedded media blocks may lose paragraphs near the middle of the article. This can happen when the source page interleaves article text, images, captions, and layout modules in a way that is hard to separate.

The v0.4.1 validation identified this as a known risk. The tool may mark the output with warning-like quality reasons such as:

- `POSSIBLE_PARAGRAPH_LOSS`
- `BODY_INCOMPLETE_AFTER_MEDIA_BLOCK`

These signals do not recover the missing text by themselves. They are intended to tell the reader that the article should be checked against the original page before being archived or quoted.

### 4. Recommendation / ranking / list-like contamination

Many news pages include content modules such as:

- real-time news
- popular news
- recommended articles
- ranking lists
- category lists
- related article blocks

These blocks can sometimes be mixed into the extracted Markdown, especially when fallback extraction is used.

v0.4.1 added stronger false-positive guards and tail cleanup rules for list-like output. The goal is to avoid treating recommendation or ranking content as clean article body, and to remove large trailing aggregation blocks when there is enough article body before them.

This cleanup is intentionally conservative. Some lightweight recommendation links may still remain in fallback output, for example short bullet links that begin with a marker such as `- ▶ ...`. These should be checked during review.

### 5. Interview formatting issues

Interview articles often use speaker markers, question labels, or publication-specific abbreviations. These markers can be collapsed into the same paragraph during extraction, making the Markdown harder to read.

v0.4.1 improved formatting for common interview markers such as:

- `**GQ**`
- `**EK**`
- `**Q**`
- `**A**`

The improvement is formatting-oriented. It is meant to separate collapsed speaker markers more clearly without rewriting the article. Different sites may use different interview formats, so interview output still needs human inspection.

### 6. Metadata completeness

`news-md` tries to extract useful metadata such as title, source, and publication time. These fields are helpful for review, but they should not be treated as perfectly reliable.

Known metadata limitations include:

- some sites may not expose publication time in a consistent way
- fallback extraction may produce incomplete title or source fields
- page metadata may differ from the visible article page
- publication and update times may be hard to distinguish

For important articles, metadata should be verified against the original page.

## How to read quality_status and quality_reasons

`quality_status` is a risk signal, not an absolute quality judgment.

General interpretation:

- `ok` means no obvious automated warning was found. It does not mean the output is perfect or complete.
- `partial_with_noise`, `possible_partial_content`, warning-like statuses, or failure statuses mean the output needs closer review.
- `failed` or empty-body outcomes mean the tool did not produce usable article content.

`quality_reasons` explain why the output should be used carefully. They may point to risks such as list-like content, possible recommendation blocks, paragraph loss, incomplete media-heavy extraction, or tail cleanup.

These fields are meant to support human review. They should not replace it.

## Recommended human review workflow

For archive-quality use, a practical review flow is:

1. Run `news-md` on one article URL.
2. Open the generated Markdown.
3. Check the title, source, and publication time.
4. Read the first and last body paragraphs.
5. Check the middle of the article for missing transitions or media-block gaps.
6. Look for recommendation, ranking, copyright, reporter, email, or submission-tip residue.
7. For important articles, compare the Markdown against the original webpage.
8. Confirm the output manually before quoting, archiving, translating, or summarizing it.

This workflow keeps `news-md` in its intended role: a lightweight preprocessing tool, not a final authority.

## Non-goals

`news-md` is not:

- a universal Korean news crawler
- a news monitor
- a summarizer
- a translation system
- a dashboard
- a server or hosted service
- a large-scale extraction platform
- a Public Release

It does not try to solve every page layout, access restriction, or content-completeness problem.

## Current conclusion

`news-md v0.4.1` passed human-review quality fix validation with known limitations.

At its current stage, the tool is suitable as a lightweight preprocessing tool for a personal content research workflow. It is useful for producing reviewable Markdown before AI translation, summarization, content research, or archive review.

It is not suitable as an unattended large-scale extraction system, and it should not be used as final reference text without human review.
