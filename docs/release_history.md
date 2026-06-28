# Release History

## Status

This document summarizes the internal version history of `news-md`.

Current status:

- Project status: **Internal Validation / Portfolio-ready documentation**
- Latest archived version: `v0.4.1 archived`
- Latest archived outcome: `human-review quality fix passed with known limitations`
- This history is not a Public Release changelog.

This is a public-facing summary of internal development milestones. It explains how the project evolved from an early local extraction workflow into a documented, validation-backed portfolio project.

## Version Timeline

| Version | Focus | Main change | Validation meaning |
|---|---|---|---|
| v0.1 | Early local CLI prototype | Established the single-URL to Markdown workflow. | Proved the basic local workflow shape. |
| v0.2 | Structured extraction workflow | Added more useful Markdown output, metadata, fallback behavior, and quality fields. | Made output easier to review and reuse for AI translation, summarization, and research. |
| v0.2.2 / v0.2.2-hotfix | Narrow cleanup stage | Improved observed beginning and tail noise cleanup while preserving conservative quality labels. | Showed that small, sample-backed cleanup rules could improve usability without claiming broad site coverage. |
| v0.3 | Manual validation baseline | Expanded validation to 30 real Korean news URLs across approximately 26 media sites. | Established the first broader manual validation baseline: 21 Pass / 4 Partial / 5 Fail. |
| v0.3.1 | Hotfix archived with caveat | Addressed selected tail-noise, list-like contamination, and empty-body concerns. | Improved some known failure modes, but kept caveats for partial or uncertain outputs. |
| v0.4 | Lightweight regression runner | Added a local batch runner to record repeated validation more efficiently. | Improved validation discipline without changing the product scope from a single-URL CLI tool. |
| v0.4.1 | Human-review quality fix | Refined quality interpretation for list-like output, media-heavy pages, paragraph-loss risk, interview formatting, and tail cleanup. | Archived as `human-review quality fix passed with known limitations`. |
| v0.5 | Documentation preparation | Prepares GitHub-ready / Portfolio-ready public documentation. | Documents project scope, validation evidence, limitations, and safe public positioning. |

## Version Notes

### v0.1 / Early Prototype

The earliest stage established the core idea:

```text
single Korean news URL -> extract article body -> save Markdown
```

This was a lightweight local command-line workflow, not a platform. The goal was practical: paste one Korean news link and get one Markdown file that could be reviewed later.

Known limits at this stage included minimal fallback behavior, limited quality classification, and limited noise handling.

### v0.2 / Early Extraction Workflow

v0.2 made the extraction workflow more structured and useful for repeated personal use.

The stage added or stabilized:

- primary article-to-Markdown extraction
- fallback extraction for selected cases
- Markdown frontmatter
- metadata fields such as title, source, publication time, extraction method, and quality signals
- quality statuses such as usable, partial, empty, or uncertain output states

This made the output more suitable for later AI translation, AI summarization, content research, and source review.

The stage still did not claim broad Korean media support. Extraction quality remained dependent on page structure, access behavior, and the available fallback output.

### v0.2.2 / Hotfix Stage

v0.2.2 and the following hotfix focused on observed cleanup problems.

The stage addressed issues such as:

- obvious leading page noise
- duplicate or repeated body fragments
- reporter signatures and email-like residue
- submission or copyright-style leftovers
- short promotion fragments
- related-article or recommendation-style tail blocks

These cleanup rules were intentionally narrow. They were based on observed samples and were not presented as a universal cleanup system.

Important limitation:

- Some media-heavy or short-body articles could remain conservatively labeled as partial or noisy rather than forced into a clean success status.

### v0.3 Manual Validation

v0.3 moved the project from small regression checks into broader manual validation.

Validation scope:

- 30 real Korean news URLs
- approximately 26 media sites
- manual review of generated Markdown outputs

Aggregate result:

| Result | Count |
|---|---:|
| Pass | 21 |
| Partial | 4 |
| Fail | 5 |

This became the first broader validation baseline.

The validation showed that `news-md` could produce useful Markdown for many real samples, but it also exposed repeated limitation categories:

- recommendation or list-like content mixed into output
- empty-body or failed extraction cases
- missing metadata in otherwise usable outputs
- fallback output that was useful but thinner than ideal
- site access or extraction failures outside the scope of simple cleanup

The project remained in Internal Validation after this stage.

### v0.3.1 Archived with Caveat

v0.3.1 targeted known issues discovered during v0.3.

The stage focused on:

- tail-noise cleanup
- recommendation and ranking block residue
- list-like contamination
- safer handling of empty-body fallback output

Some selected cases improved. Empty-body handling became safer, and some obvious tail residues were reduced.

The stage was archived with caveat because not every output became fully resolved. Some content remained partial or uncertain, and the project avoided turning into an endless site-specific hotfix loop.

This stage helped clarify an important project principle: fix repeated, clearly observed problems, but do not expand the tool into a general crawler or open-ended site repair system.

### v0.4 Regression Runner

v0.4 introduced a lightweight regression runner for internal validation.

The runner helped:

- process a list of real Korean news URLs in sequence
- continue after individual failures
- collect structured result summaries
- preserve review evidence more consistently

This was validation infrastructure, not a change in product scope.

`news-md` remained a local single-URL CLI tool. The runner existed to reduce manual repetition during validation, not to turn the project into a crawler platform, monitoring system, or formal test service.

v0.4 also included a 50-sample content quality review. That review found many usable outputs, but also confirmed that script-level success does not always equal human-confirmed article quality.

### v0.4.1 Human-review Quality Fix

v0.4.1 refined how output quality is interpreted for human review.

The stage improved:

- false-positive guards for recommendation or list-like output
- classification of media-heavy and partial content
- warnings for possible paragraph loss around media blocks
- interview Q&A marker formatting
- conservative cleanup of large trailing aggregation blocks

Latest archived status:

```text
human-review quality fix passed with known limitations
```

This means the quality labels became more useful for review. It does not mean extraction became perfect.

Known limitations remained, especially for media-heavy pages, possible paragraph loss, metadata gaps, access failures, and cases where fallback extraction keeps small residual links or noise.

### v0.5 Documentation Preparation

v0.5 is the current phase.

The goal is GitHub-ready / Portfolio-ready documentation preparation.

This phase focuses on:

- project boundary
- limitations
- validation summary
- release history
- public-safe presentation
- careful separation between internal evidence and public documentation

v0.5 is not feature expansion. It is not a Public Release. It does not add a dashboard, hosted service, crawler platform, monitoring system, database, GUI, or automatic translation system.

## Development Pattern

The project followed a deliberately small development pattern:

1. Start from a real personal workflow need.
2. Build a lightweight local CLI around one URL at a time.
3. Validate against real Korean news pages.
4. Identify repeated failure and noise categories.
5. Apply narrow fixes only when supported by observed samples.
6. Archive stages with caveats instead of overstating reliability.
7. Stop feature expansion before scope creep.
8. Prepare public-safe documentation for portfolio review.

This pattern kept the project focused on its actual use case: producing reviewable Markdown drafts for later AI-assisted reading and research.

## Current Boundary

`news-md` is a lightweight local CLI tool.

It is useful for:

- extracting article-like body text from a single Korean news URL
- saving reviewable Markdown
- preparing cleaner input for AI translation and summarization
- supporting personal content research and archive review

It still requires human review for archive-quality use.

It should not be described as:

- a universal Korean news crawler
- a news monitoring platform
- a hosted service
- an automatic translation system
- a dashboard
- a Public Release package

The current project state is best summarized as:

```text
Internal Validation / Portfolio-ready documentation
```
