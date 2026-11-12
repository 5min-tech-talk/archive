# ⚡ 5min Tech Talk Archive

A dedicated space for weekly 5-minute technical insights and knowledge sharing between teammates.

## 📝 Document Template

Please use the [provided template](./docs/template.md).

---
## 📚 Seminar Index

| Round | Date | Presenter | Topic | Summary Doc | Additional Materials |
| :---: | :---: | :---: | :--- | :---: | :---: |
| 1 | 2026-11-04 | Sujee Cho | Rendering Optimization for Large-Scale Visualization Data | [docs](./docs/20261104_rendering_optimization_for_large_scale_visualization.md) | - |
| 2 | - | - | - | - | - |
| 3 | - | - | - | - | - |
| 4 | - | - | - | - | - |
| 5 | - | - | (Upcoming Session) | - | - |

---

## 📂 Repository Structure

To keep the repository clean as sessions accumulate, files are categorized into flat directories:
* `docs/`: Markdown (`.md`) summary documents for each session.
* `assets/`: Static resources such as diagrams, screenshots, or presentation PDFs (`.pdf`, `.png`).
* `examples/`: Source code or practical examples associated with the seminar topics.

---

## 🛠️ Contribution & Commit Guidelines

1. **Naming Convention:** 
   * **Docs:** `YYYYMMDD_topic_name.md`
     (e.g., `20261104_rendering_optimization_for_large_scale_visualization.md`)
   * **Assets:** `YYYYMMDD_title.ext`, using the same prefix as the related doc
     (e.g., `20261104_quadtree.jpeg`)
   * Use lowercase letters and underscores only — no spaces or Korean characters, so links don't break.
2. **Asset Guidelines:**
   * Resize images to around 1200–1600px wide and compress them before uploading (WebP recommended).
   * Commit only final versions — deleted or replaced files still remain in Git history.
3. **Gitmoji Conventions:** Use emoji prefixes in commit messages to keep the history intuitive:
   * ✨ `:sparkles:` for adding new seminar documents
   * 📝 `:memo:` for revising or fixing summaries
   * 🎨 `:art:` for uploading diagrams or presentation assets
   * 🚀 `:rocket:` for adding example code
   * 🐛 `:bug:` for fixing bugs in example code or broken links/paths
