# ⚡ 5min Tech Talk Archive

A dedicated space for weekly 5-minute technical insights and knowledge sharing between teammates.

## 📝 Document Template

Please use the [provided template](./docs/template.md).
For learning-note style talks, see the [learning note template](./docs/template_learning.md).

---
## 📚 Seminar Index

| Date | Presenter | Topic | Summary Doc | Additional Materials |
| :---: | :---: | :--- | :---: | :---: |
| 2026-11-04 | Sujee Cho | Rendering Optimization for Large-Scale Visualization Data | [🔗](./docs/20261104_rendering_optimization_for_large_scale_visualization.md) | - |
| 2026-11-04 | Olivia Lee | Web Deployment Part 1: How My Code Reaches an https:// URL | [🔗](./docs/20261104_web_deployment_part1_from_code_to_url.md) | - |
| 2026-11-12 | Sujee Cho | Handling Time in Global Services | [🔗](./docs/20261112_handling_time_in_global_services.md) | - |
| 2026-11-12 | Olivia Lee | Web Deployment Part 2: Safer Requests, Automated Deploys | [🔗](./docs/20261112_web_deployment_part2_cloudflare_tunnel_and_cicd.md) | - |
| 2026-11-20 | Sujee Cho | Multilingual OTA & White-Labeling Architecture in Global Services | [🔗](./docs/20261120_multilingual_ota_white_labeling_architecture_in_global_services.md) | - |
| 2026-11-25 | Olivia Lee | Inside the Server: Ports, localhost, and Redis | [🔗](./docs/20261125_inside_the_server_ports_localhost_redis.md) | - |
| 2026-11-25 | Sujee Cho | Dissecting Python `dict` & The Two Faces of Hash | [🔗](./docs/20261125_dissecting_python_dict_the_two_faces_of_hash.md) | [example1](./examples/20261125_01_realworld_hash_demo.py), [example2](./examples/20261125_02_mini_hash_table.py) |

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
