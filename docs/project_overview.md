# Project Overview

## What is news-md?

`news-md` is a lightweight local CLI tool for extracting Korean news article bodies into reviewable Markdown.

Core workflow:

```text
single Korean news URL -> article body extraction -> obvious noise cleanup -> Markdown output
```

The generated Markdown is intended as a draft for human review, AI translation, AI summarization, content research, and archive review. It is not meant to be treated as a final authoritative copy without checking the source.

## Why this project exists

Directly giving a news link to an AI tool is not always reliable. Korean news pages can include surrounding content that is useful on the website but distracting in a research workflow, such as:

- ads or promotional blocks
- recommendation modules
- ranking and popular-news lists
- reporter signatures
- copyright or submission text
- image and video modules
- dynamically loaded or hard-to-access article bodies

Manual copy-paste cleanup is repetitive and inconsistent. A local CLI workflow gives more control over what is captured, what is cleaned, and what still needs review.

The project exists to support a practical personal workflow: turn one Korean news article at a time into a Markdown file that can be inspected before being used for downstream AI-assisted reading or research.

## Core Workflow

A typical high-level workflow is:

1. The user runs the local CLI command.
2. The user provides one Korean news URL.
3. The tool extracts article-like body content.
4. The tool removes obvious noise where it can do so conservatively.
5. The tool writes Markdown output with metadata and quality signals where available.
6. The user reviews the Markdown before using it for AI translation, summarization, research, or archive.

The review step is part of the intended workflow. `news-md` helps prepare cleaner input, but it does not replace human judgment.

## What the tool does

`news-md` currently focuses on a narrow set of local CLI tasks:

- Extracts article-like body text from a single Korean news URL.
- Produces Markdown output for review.
- Includes metadata and quality status where available.
- Uses fallback extraction where supported by the implementation.
- Applies narrow cleanup rules for observed noise patterns.
- Adds quality signals that help separate usable, partial, uncertain, and failed outputs.
- Supports internal regression validation through a separate runner.

The regression runner is a validation support tool. It helps record repeated internal checks, but it is not the product identity and does not turn `news-md` into a crawler or monitoring system.

## What the tool does not do

`news-md` is not:

- a universal Korean news crawler
- a news monitoring system
- an automatic translation system
- a dashboard
- a hosted service
- a Public Release package
- a large-scale extraction platform

It does not guarantee:

- perfect extraction
- complete metadata
- successful access to every news site
- complete removal of all page noise
- final archive-quality text without review

The output should be read as a structured draft that still needs human inspection.

## Validation approach

Validation used real Korean news samples, but raw evidence remains internal.

The public validation summary is deliberately aggregate and cautious:

- v0.3 established a broader manual baseline using 30 real Korean news URLs across approximately 26 media sites.
- v0.4 added a lightweight regression runner for repeatable internal records.
- v0.4 included a 50-sample human content-quality review.
- v0.4.1 refined human-review quality interpretation and was archived as `human-review quality fix passed with known limitations`.

Raw URL lists, raw logs, detailed internal review notes, and local environment details are not included in public documentation.

For details, see:

- [Validation Summary](validation_summary.md)
- [Limitations](limitations.md)
- [Release History](release_history.md)

## Current project status

Current status:

- Project status: **Internal Validation / Portfolio-ready documentation**
- Latest archived version: `v0.4.1 archived`
- Latest archived outcome: `human-review quality fix passed with known limitations`
- Current phase: `v0.5 documentation preparation`

This means the project has enough evidence to be presented as a personal workflow and portfolio project. It should not be represented as a universal crawler, unattended extraction system, hosted service, or Public Release package.

## Portfolio relevance

From a portfolio perspective, `news-md` demonstrates:

- identifying a real workflow problem
- designing a scoped local tool instead of overbuilding
- integrating extraction, cleanup, metadata, and review signals
- validating against real-world samples
- keeping regression records
- documenting limitations honestly
- preventing scope creep

The project is intentionally small. Its value comes from matching a concrete workflow, recording validation evidence, and keeping its boundaries clear.

## Related documents

- [Limitations](limitations.md)
- [Validation Summary](validation_summary.md)
- [Release History](release_history.md)
