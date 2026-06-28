# news-md | Korean News Article Cleaner

[中文](README.md)

## Overview

`news-md` is a lightweight local CLI tool that turns a single Korean news article URL into cleaner, reviewable Markdown.

The project came from my own content research workflow. When reading Korean news, I often need to extract the article body first, then use it for AI translation, summarization, content analysis, or archive review. Giving the URL directly to an AI tool is not always reliable, and manual copying often brings in ads, related-news blocks, copyright text, reporter information, and site navigation.

`news-md` solves a small but frequent problem: prepare one Korean news page as a more reliable Markdown input for later review and AI-assisted work.

It is not a large platform or a general-purpose crawler. It is a focused local workflow tool with clear boundaries.

## Why this tool exists

**1. If AI tools exist, why not just give them the link?**

News pages are not just article text. They may involve redirects, SSL issues, dynamic loading, access restrictions, or noisy page modules around the real article body. An AI tool may not always read the intended content reliably.

**2. If the page opens in a browser, why not copy it manually?**

Manual copying works once, but it does not scale well as a repeated research habit. Copied text often includes ads, recommendation lists, copyright blocks, reporter emails, navigation text, or duplicated fragments.

**3. If extraction tools already exist, why build this?**

General extraction tools provide a useful starting point, but my workflow needed Korean-news-specific cleanup, metadata retention, Markdown output, and regression-style review. `news-md` keeps those needs scoped to a small local tool instead of expanding into a platform.

## Workflow

```text
Korean news URL
  -> article body extraction
  -> visible noise cleanup
  -> Markdown output
  -> AI translation / summarization / content research / archive review
```

## Main features

- Accepts a single Korean news article URL.
- Extracts article-like body content.
- Cleans obvious page noise where possible.
- Saves Markdown output.
- Records basic metadata such as title, source, published time, extraction method, and quality status.
- Supports review through regression samples and human inspection.

## AI-assisted development

This project is also an AI-assisted development case, but it is not presented as an “AI platform.” AI was used in concrete, reviewable parts of the work.

- GPT helped with requirement breakdown, scope decisions, README structure, validation ideas, and public documentation decisions.
- Codex helped with code edits, local fixes, conflict resolution, GitHub upload preparation, and documentation cleanup.
- I remained responsible for judging whether the need was real, whether outputs were usable, whether the scope was expanding, and what materials were safe to publish.

## Project highlights

- **Real workflow problem**: The project starts from a repeated content research task, not from an abstract AI demo idea.
- **Lightweight tool design**: The workflow stays focused on one URL to Markdown, using a CLI to reduce repetitive cleanup.
- **AI-assisted development**: GPT and Codex supported planning, editing, debugging, and documentation while human judgment controlled scope and quality.
- **Testing and human review**: Outputs were reviewed across sample sets using categories such as pass, partial, problem, and failed.
- **Public/private boundary awareness**: Public docs keep aggregate summaries and limitations, while real URL lists, raw logs, and internal review materials stay private.

## Usage

The tool is designed for local Windows / PowerShell usage, either through the batch wrapper or the local CLI prompt.

Example:

```powershell
news-md "https://example.com/korean-news-article"
```

The result is saved as Markdown. The output location can be adjusted through command options or local environment configuration.

## Current boundaries

`news-md` is suitable as a lightweight tool for personal content research and portfolio demonstration, but it should not be treated as a general released product.

It is not:

- a general-purpose crawler
- a news monitoring system
- an automatic translation system
- a dashboard
- a server or hosted service
- a Public Release
- a complete extraction solution for every website or layout

It also does not guarantee perfect extraction for every Korean news article. Important materials should still be checked against the original page.

## Tech stack

- Python
- Windows batch / PowerShell local usage
- `url2md4ai` as the primary extraction approach
- `trafilatura` fallback
- BeautifulSoup-based metadata parsing
- Markdown output with quality status signals

## Related documents

- [Chinese README](README.md)
- [Project Overview](docs/project_overview.md)
- [Limitations](docs/limitations.md)
- [Validation Summary](docs/validation_summary.md)
- [Release History](docs/release_history.md)
