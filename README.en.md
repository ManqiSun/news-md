# news-md

[中文说明](README.md)

A lightweight CLI tool for extracting Korean news article text into Markdown.

## Overview

`news-md` is a small local CLI workflow for turning a single Korean news article URL into cleaned Markdown.

It is intended for personal content research workflows where extracted article text may later be used for AI translation, summarization, review, or archival notes. The project is currently in portfolio-ready documentation and internal validation preparation. It is not presented as a Public Release.

## Why This Project Exists

Directly giving news URLs to AI tools is not always reliable. News pages may involve blocking, SSL issues, redirects, dynamic loading, or noisy page structure.

Manually copying article text is repetitive and often includes ads, related articles, copyright blocks, reporter emails, or site navigation noise.

A lightweight local workflow makes extraction more repeatable, reviewable, and easier to feed into downstream AI-assisted research steps.

## Core Workflow

```text
Korean news URL
  -> article extraction
  -> visible noise cleanup
  -> Markdown output
  -> AI translation / summarization / research archive
```

## What It Does

- Accepts a single Korean news article URL.
- Extracts article-like content.
- Cleans obvious page noise where possible.
- Saves Markdown output.
- Records basic metadata where available, such as title, source, published time, extraction method, and quality status.
- Supports validation through curated regression samples.

## What It Does Not Do

- It is not a general-purpose crawler.
- It is not a monitoring system.
- It is not an automatic translation system.
- It is not a dashboard.
- It is not a hosted service or server.
- It is not presented as a Public Release.
- It does not guarantee perfect extraction for every Korean news site.

## Project Status

- Current stage: v0.5 documentation preparation.
- Latest archived implementation state: v0.4.1 archived.
- Status: human-review quality fix passed with known limitations.
- Current purpose: GitHub-ready / portfolio-ready documentation.
- Release posture: not Public Release.

## Validation Summary

Validation was performed across multiple Korean news sites and real-world article samples. Results were reviewed by category, including pass, partial, problem, and failed cases.

Known limitations are documented separately. Raw URL lists, PowerShell logs, and internal review notes are intentionally kept private.

See:

- [Validation Summary](docs/validation_summary.md)
- [Limitations](docs/limitations.md)

## Documentation

Public-facing documentation:

- [Project Overview](docs/project_overview.md): project scope, positioning, and workflow summary.
- [Limitations](docs/limitations.md): known extraction limits and cases requiring human review.
- [Validation Summary](docs/validation_summary.md): public-safe validation summary.
- [Release History](docs/release_history.md): archived version notes and documentation-stage status.

## Repository Safety Note

A public-safe example regression file is provided at [tests/regression_urls.example.txt](tests/regression_urls.example.txt).

Real regression URL lists and internal notes are excluded from public tracking. Local outputs, logs, caches, and private notes are ignored through `.gitignore`.

## Usage

The tool is designed for local PowerShell usage, either by passing a URL or following the local CLI prompt, depending on the configured batch wrapper.

```powershell
news-md "https://example.com/korean-news-article"
```

## Tech Stack

- Python
- PowerShell / Windows batch wrapper
- `url2md4ai` as the primary extraction approach
- `trafilatura` fallback
- BeautifulSoup-based metadata parsing

## Portfolio Relevance

This project demonstrates practical problem framing, lightweight CLI workflow design, AI-assisted development, validation and regression thinking, public/private boundary control, and documentation discipline.
