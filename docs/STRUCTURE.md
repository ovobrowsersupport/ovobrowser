# 目录说明：每个文件做什么

本项目是 **ovobrowser 源码级 Chromium 指纹内核** 的 **GitHub 文档 + 启动示例**。
改过的浏览器本体是 `chrome.exe`（在 Releases 的便携 zip 里），**不在这份源码树中**。

---

## 根目录

| 路径 | 做什么 |
|---|---|
| `README.md` | **仓库首页（中文）**：介绍、检测站列表、下载表、30 秒上手、指纹开关总表、多语言启动示例、代理说明 |
| `README.en.md` | 同上的英文版，和中文页互相链接 |
| `LICENSE` | 文档与示例的 MIT 许可。内核二进制仍遵循 Chromium / ungoogled-chromium 上游许可 |
| `.gitignore` | 忽略环境文件、浏览器二进制、Release 压缩包、profile 与各语言编译产物 |
| `.gitattributes` | 统一文本换行符，并把图片/压缩包标记为二进制文件 |

---

## `docs/` 文档（比首页更细）

| 路径 | 做什么 |
|---|---|
| `docs/zh/FLAGS.md` | **启动参数说明书（中文）**：每个 `--fingerprint-*` 改什么、不传时的默认、138/144/150 差异 |
| `docs/en/FLAGS.md` | 启动参数说明书（英文） |
| `docs/zh/FINGERPRINT.md` | **内核改了哪些指纹面（中文）**：噪声、UA-CH、屏幕/DPR、WebRTC 等实现说明 |
| `docs/en/FINGERPRINT.md` | 指纹改动说明（英文） |
| `docs/zh/RECIPES.md` | **推荐启动配方（中文）**：FingerprintJS 全绿、BrowserScan 骨架、换 visitor 开噪声 |
| `docs/en/RECIPES.md` | 推荐配方（英文） |
| `docs/STRUCTURE.md` | 本仓库的目录结构与文件用途 |
| `docs/assets/ovobrowser-banner.png` | 首页横幅原图（猫头鹰 + 字标，1280×420） |
| `docs/assets/ovobrowser-logo.png` | 官方猫头鹰 logo 原图 |

读文档的顺序建议：`README.md` → `docs/zh/FLAGS.md` → 需要原理再看 `FINGERPRINT.md` → 抄命令看 `RECIPES.md`。

---

## `examples/` 可运行启动脚本

把环境变量 `OVO_CHROME` 指到解压后的 `chrome.exe` 即可跑。

| 路径 | 做什么 |
|---|---|
| `examples/README.md` | 示例目录说明（中文） |
| `examples/README.en.md` | 示例目录说明（英文） |
| `examples/python/launch.py` | 用 `subprocess` 直接拉起 `chrome.exe`（全绿骨架、无 Playwright） |
| `examples/python/launch_playwright.py` | 用 Playwright **persistent context** 驱动同一套参数（不要用 `launch()` 隐身窗） |
| `examples/nodejs/launch.js` | Node 拼 argv 启动 |
| `examples/go/main.go` + `go.mod` | Go 启动 |
| `examples/csharp/Program.cs` | C# 启动 |
| `examples/java/Launch.java` | Java 启动 |
| `examples/powershell/Launch.ps1` | PowerShell 启动 |
| `examples/rust/src/main.rs` + `Cargo.toml` | Rust 启动 |

---

## `video/`

留给 README 演示动画/录屏。仓库里目前只有占位文件 `.gitkeep`（Git 不能提交空文件夹）。把 `.mp4` / `.gif` 放这里即可。

---

## `kernels-放到-Releases/`（仅在交接包里，默认不进 git）

| 文件 | 做什么 |
|---|---|
| `ovobrowser-150-150.0.7871.124-win64-portable.zip` | **推荐内核** Windows x64 便携包，解压得 `chrome.exe` |
| `ovobrowser-144-144.0.7559.132-win64-portable.zip` | 144 内核便携包 |
| `ovobrowser-138-138.0.7204.183-win64-portable.zip` | 138 内核便携包 |

三套开关大体一致；150 对 FingerprintJS 更友好。用户解压后只需运行其中的 `chrome.exe`，并加上 README「30 秒上手」里的参数。

---

## 刻意没有放进本仓库的

- Chromium **C++ 源码树**（体积极大，编译用；本包只含编好的便携 zip）
- 旧 GitHub 账号的 `.git` 历史（避免关联被封账号）
- 代理密码、本地 profile 目录
