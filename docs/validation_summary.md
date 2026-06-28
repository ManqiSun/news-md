# Validation Summary

## Status

This document summarizes internal validation for `news-md` up to `v0.4.1`.

Current status:

- Project status: **Internal Validation / Portfolio-ready documentation**
- Latest archived version: `v0.4.1 archived`
- Validation outcome: `human-review quality fix passed with known limitations`
- This is not a Public Release certification.

The purpose of this summary is to explain what has been validated, what the validation suggests, and where the known limits remain. It is a public-facing summary derived from internal notes, not a raw validation log.

## Validation Scope

Validation focused on the core `news-md` workflow:

```text
single Korean news URL -> extract article body -> remove obvious noise -> output Markdown
```

The validation covered:

- article body extraction from real Korean news pages
- obvious noise removal
- Markdown output suitability for later AI translation and summarization
- quality status classification
- fallback behavior
- regression tracking across versions
- human review of selected outputs

The validation did not attempt to prove universal support for all Korean media sites. It also did not attempt to turn `news-md` into a crawler platform, monitoring system, hosted service, or automated translation system.

## Validation History

### v0.3 Manual Validation

v0.3 established the first broader manual validation baseline.

Scope:

- 30 real Korean news URLs
- approximately 26 media sites
- manual review of generated Markdown outputs

Aggregate result:

| Result | Count |
|---|---:|
| Pass | 21 |
| Partial | 4 |
| Fail | 5 |

Interpretation:

- **Pass** meant the output contained usable article-body content with acceptable cleanup for the intended workflow.
- **Partial** meant the output was useful, but had caveats such as short body text, metadata gaps, residual noise, or media-related uncertainty.
- **Fail** meant extraction failed, produced empty content, or produced output that was not usable enough for the intended workflow.

This phase was a baseline, not a marketing claim. It showed that the CLI could produce useful Markdown across a mixed real-world sample, while also exposing repeated limitation categories such as access failures, empty-body cases, metadata gaps, and recommendation/list contamination.

### v0.3.1 Hotfix Validation

v0.3.1 focused on specific issues observed during v0.3.

The validation checked whether narrow quality fixes improved:

- recommendation, ranking, and list-like tail contamination
- misleading empty-body outputs
- selected residual noise patterns

Outcome:

- Some selected tail-noise cases improved.
- Empty-body handling became safer.
- The stage was archived with caveat because some outputs remained partial or uncertain rather than fully resolved.

This phase did not establish full site-level support. It was a narrow validation improvement, not a claim that every affected site or layout was solved.

### v0.4 Regression Runner

v0.4 added a lightweight regression runner to make repeated validation easier to record.

This was validation infrastructure, not extraction-quality expansion. The runner helped:

- process a list of real Korean news URLs in order
- continue after individual URL failures
- record result status and quality signals
- preserve repeatable evidence for later review

One recorded v0.4 batch run covered 30 URLs and produced this aggregate result:

| Status | Count |
|---|---:|
| OK | 25 |
| Partial | 1 |
| Fail | 1 |
| Error | 3 |
| TBD | 0 |

The runner supported validation discipline without changing the identity of the project. `news-md` remained a single-URL local CLI tool; the runner was a support tool for internal review.

### v0.4 Content Quality Review

v0.4 also included a broader human content-quality review over 50 real Korean news samples.

Aggregate result:

| Review result | Count |
|---|---:|
| Good | 24 |
| Usable with caveat | 16 |
| Problem | 3 |
| Failed | 7 |

Interpretation:

- Most usable outputs were suitable as drafts for AI translation or summarization after review.
- Caveat cases included metadata gaps, thinner fallback metadata, small tail artifacts, image-heavy uncertainty, or residual page noise.
- Problem cases showed that script-level success does not always mean human-quality article extraction.
- Failed cases were generally tied to access, extraction, network, or empty-body limitations.

This review reinforced a key project rule: automated status is helpful, but it should not replace human review for archive-quality use.

### v0.4.1 Human-review Quality Fix

v0.4.1 refined the human-review quality interpretation.

Archived status:

```text
human-review quality fix passed with known limitations
```

Main validation focus:

- stronger false-positive guards for recommendation/list-like output
- clearer classification of media-heavy or partial content
- warning signals for possible paragraph loss around media blocks
- interview Q&A marker normalization
- conservative tail cleanup when large aggregation blocks appear after a sufficient article body

Problem-sample recheck:

| Recheck group | Result |
|---|---:|
| Passed or became usable | 3 / 5 |
| Remained known limitations | 2 / 5 |

Good-sample regression:

| Recheck group | Result |
|---|---:|
| No obvious regression | 5 / 5 |

Interpretation:

- v0.4.1 made the quality labels more useful for human review.
- Some previously misleading outputs were no longer treated as clean article-body success.
- Some known limitations remained, especially around media-heavy pages and possible paragraph loss.
- The validation did not mean extraction became perfect.

## What the Validation Demonstrates

The validation supports these measured conclusions:

- The CLI workflow can process a real Korean news URL and generate reviewable Markdown.
- The tool can produce usable article-body drafts across a mixed sample of Korean media pages.
- The quality status system is useful for separating usable, partial, warning, and failed outputs.
- Human review improves interpretation of the generated Markdown.
- Regression records help prevent undocumented behavior changes.
- The project is suitable as a personal content research workflow component and portfolio project.

## What the Validation Does Not Demonstrate

The validation does not show that:

- `news-md` supports every Korean news website.
- Every article body will be extracted completely.
- Noise removal is perfect.
- Metadata is always complete or fully accurate.
- `quality_status: ok` means the output is final or flawless.
- Human review can be skipped for archive-quality use.
- The project is certified as Public Release ready.
- The tool is a crawler, monitoring system, hosted service, or automated translation system.

These limits are intentional and are consistent with the project scope described in `docs/limitations.md`.

## Evidence Handling

The validation was based on real internal samples and human review notes, but the raw evidence is not included in public documentation.

The following materials remain internal/private:

- full real URL lists
- raw PowerShell logs
- raw validation logs
- raw human review notes
- local environment details
- generated article outputs used for manual inspection

Public documentation uses sanitized aggregate summaries instead:

- sample counts
- result categories
- validation phases
- known limitation categories
- cautious conclusions

This keeps the public documentation useful for GitHub and portfolio review without exposing private validation data or local environment details.

## Current Interpretation

`news-md` has enough validation evidence to be presented as an **Internal Validation / Portfolio-ready local CLI tool**, with clear caveats and known limitations.

It should be described as a lightweight Korean news article body extraction workflow:

```text
single URL -> article body extraction -> obvious noise cleanup -> reviewable Markdown
```

It should not be described as a universal crawler, unattended extraction system, monitoring platform, hosted service, automated translation system, or Public Release package.
