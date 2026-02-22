# 贡献者指南

欢迎加入 Windows R-tools box 的开发！
---
## 🏷 样式与界面开发规范
- 所有前端界面/工具请统一引用根目录 styles.css，保证整个项目风格一致。
- 请优先使用 styles.css 已有的 class（如 .btn、.card 等）与变量。
- 如需扩展全局样式，须补充详细中文注释，或在本地用 rtools-xxx- 前缀命名，避免干扰全局。
- 禁止随意覆盖主按钮、字体、色彩、圆角等基础样式。

示例：
```html
<link rel="stylesheet" href="../styles.css">
<button class="btn btn-success">启动</button>
<div class="card">标准卡片样式</div>
```
---
## 📝 代码与样式贡献流程
1. Fork 本仓库
2. 创建新分支（如 feature/my-awesome-tool）
3. 遵循本规范进行开发，确保样式、交互统一
4. Commit & Push 你的更改
5. 发起 Pull Request，简要描述你的更改及影响范围

> 建议每次贡献配合完善文档、注释，新增样式需写入 styles.css 并加中文说明。
---
## 🚦 代码与提交规范
- Python：推荐 PEP8 风格，变量与函数需见名知意，有必要时补注释
- 前端 JS 建议缩进两空格，变量/函数见名知意
- CSS 样式请严格按 styles.css 命名规范和注释
- commit 信息需简明清楚，例如 feat: 新增XX工具、fix: 修复XXX
---
## 🧩 样式/组件补充
- 全局新增 class，建议写在 styles.css 末尾并加中文用途注释
- 尽量避免命名冲突和重复定义
- 本地自用样式请加前缀“rtools-xxx-”
---
## 📣 贡献守则
- 尊重开源氛围，提交前请自测功能和样式一致性
- 所有贡献按 AGPL v3 协议授权
如有疑问请 [提交 Issue](https://github.com/Regulus-forteen/Windows-R-tools-box/issues) 或在 PR 中留言。
---
# Contributor Guide (English)

Welcome to contributing to Windows R-tools box!
---
## 🏷 UI & Style Guide
- All tools and UI pages must include the root-level styles.css for unified project style.
- Always use existing classes in styles.css (such as .btn, .card etc.) and variables.
- For new global styles, add detailed English comments; for tool-specific overrides, use the rtools-xxx- prefix to avoid global conflicts.
- Do not arbitrarily override core colors, border, font, or button classes.

Example:
```html
<link rel="stylesheet" href="../styles.css">
<button class="btn btn-success">RUN</button>
<div class="card">Sample Card Style</div>
```
---
## 📝 How to contribute
1. Fork the repository
2. Create a new branch (e.g., feature/my-awesome-tool)
3. Develop following this guide, ensuring UI/UX consistency
4. Commit & push your changes
5. Open a Pull Request and describe your changes and impacts

> Please also improve docs/comments as contributing; add new styles with comments in styles.css.
---
## 🚦 Code and Commit Standards
- Python: follow PEP8 conventions, meaningful names for variables/functions, annotate when needed
- Frontend JS: use 2-space indentation, clear variable/function names
- CSS: strictly follow naming/comment conventions in styles.css
- Commit messages must be clear and descriptive, e.g. feat: add X tool, fix: fix Y bug.
---
## 🧩 Extending UI or Styles
- For new global classes, add at the end of styles.css and add an English usage comment
- Avoid duplicates/conflicts in naming
- For local styles use the prefix “rtools-xxx-”
---
## 📣 Code of Conduct
- Respect the open-source spirit, please test your changes for style and functional consistency before submitting.
- By contributing, you agree to license under AGPL v3.
If you have questions, please open an Issue (https://github.com/Regulus-forteen/Windows-R-tools-box/issues) or comment in your PR.
