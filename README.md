# news-md

[English](README.en.md)

一个轻量级的韩语新闻正文提取工具。

## 这个项目是什么

`news-md` 是一个本地 CLI 小工具，用来把单条韩网新闻链接整理成相对干净、可复核的 Markdown 文本。

它的目标不是“自动翻译新闻”，而是先把网页里的新闻正文提取出来，尽量减少广告、推荐新闻、版权说明、记者邮箱、站点导航等噪声，方便后续交给 AI 做翻译、摘要或内容研究。

## 为什么要做这个工具

直接把新闻链接交给 AI 并不总是稳定。新闻网页可能会遇到反爬、SSL、跳转、动态加载、页面结构复杂等问题，AI 工具不一定能稳定拿到正文。

手动复制网页正文也很费时间。复制出来的内容经常混入广告、推荐新闻、版权块、记者邮箱、站点导航或重复内容，后续还需要人工清理。

对个人内容研究来说，更可控的流程是：先把网页整理成 Markdown，再交给 AI 翻译、摘要或分析。这样输入内容更清楚，也更方便复核。

## 基本流程

```text
韩网新闻 URL
  -> 提取正文
  -> 清理明显噪声
  -> 输出 Markdown
  -> 用于 AI 翻译 / 摘要 / 内容研究 / 归档复核
```

## 当前能做什么

- 输入单条韩语新闻 URL。
- 提取类似新闻正文的内容。
- 尽量清理明显页面噪声。
- 输出 Markdown 文件。
- 记录标题、来源、发布时间、抽取方式、正文质量状态等基础信息。
- 通过回归样本和人工 review 记录验证效果。

## 当前不做什么

- 不是通用爬虫平台。
- 不是新闻监控系统。
- 不是自动翻译系统。
- 不是 dashboard。
- 不是 server / hosted service。
- 不是 Public Release。
- 不保证适配所有韩网新闻站点。
- 不保证每篇文章都能完美抽取。

## 验证方式

项目曾用多批真实韩网新闻样本做验证，并按 pass / partial / problem / failed 等类别记录结果。

公开文档只保留聚合后的验证总结和限制说明，不公开真实 URL、完整样本正文、PowerShell 原始日志或内部人审记录。

详细英文验证总结见：

- [docs/validation_summary.md](docs/validation_summary.md)
- [docs/limitations.md](docs/limitations.md)

## 项目状态

- 当前状态：`v0.5.1 portfolio-ready repository uploaded to GitHub`
- 英文 GitHub / Portfolio 文档已准备完成。
- 中文说明用于帮助中文面试官快速理解项目。
- 当前仍不是 Public Release。
- 项目仍处于 Internal Validation / Portfolio-ready documentation 状态。

## 这个项目体现的能力

这个项目来自一个具体的个人内容研究流程：需要反复把韩语新闻网页整理成后续可读、可翻译、可复核的文本。

它体现的重点不是“大而全”，而是把一个重复、容易出错的步骤拆成轻量 CLI 工具，并围绕真实样本做验证、质量标注和版本归档。

开发过程中使用了 AI / Codex 辅助实现和整理，但项目边界、质量判断、公开材料和 private/internal 材料的区分仍然保留人工控制。

作为作品集项目，它展示了问题定义、轻量工具设计、回归验证意识、文档整理能力，以及对公开安全边界的处理。

## Related Docs

- [README.en.md](README.en.md)
- [docs/project_overview.md](docs/project_overview.md)
- [docs/limitations.md](docs/limitations.md)
- [docs/validation_summary.md](docs/validation_summary.md)
- [docs/release_history.md](docs/release_history.md)
