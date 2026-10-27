<p align="center">
  <img src="docs/assets/ovobrowser-banner.png" width="640" alt="Ovobrowser">
</p>

<p align="center">
  <a href="https://github.com/ovobrowsersupport/ovobrowser/releases"><img src="https://img.shields.io/github/v/release/ovobrowsersupport/ovobrowser" alt="Release"></a>
  <a href="LICENSE"><img src="https://img.shields.io/github/license/ovobrowsersupport/ovobrowser" alt="License"></a>
  <a href="https://github.com/ovobrowsersupport/ovobrowser/commits/main"><img src="https://img.shields.io/github/last-commit/ovobrowsersupport/ovobrowser" alt="Last Commit"></a>
  <br>
  <a href="https://github.com/ovobrowsersupport/ovobrowser/stargazers"><img src="https://img.shields.io/github/stars/ovobrowsersupport/ovobrowser" alt="Stars"></a>
  <a href="https://github.com/ovobrowsersupport/ovobrowser/releases"><img src="https://img.shields.io/github/downloads/ovobrowsersupport/ovobrowser/total" alt="Downloads"></a>
</p>

<p align="center">
  <a href="README.en.md">English</a> · <strong>中文</strong>
</p>

<h3 align="center">源码级 Chromium 指纹内核-指纹浏览器器-跨境电商浏览器</h3>

源码级修改的 Chromium 指纹内核。不是 JS 注入，不是 `playwright-stealth` 那套运行时补丁——指纹在 C++ 里改完再编译进二进制。检测站看到的是普通 Chrome，因为它本来就是 Chromium。

当前便携包：**Windows x64** · 内核 **138 / 144 / 150** · 产品名 **ovobrowser**（UA / Client Hints 仍报 Chrome，避免被判未知浏览器）

- 5 类独立噪声：Canvas / WebGL / Audio / ClientRects / Font（可关可固定种子）
- UA-CH、平台、核数、内存、屏幕、DPR、电池、DNT、语音列表
- WebGL vendor/renderer、隐藏 WebGPU / 蓝牙、WebRTC 不漏内网 IP
- 时区 / `lang` / `accept-lang` 与出口 IP 对齐
- 任意语言：拼命令行 → 拉起 `chrome.exe`（Python / Node / Go / C# / PowerShell / Java / Rust 示例都在本页）

### 普通用户客户端

针对普通用户，我们已经开发了图形化指纹浏览器客户端：装好就能管理环境、代理、团队和窗口同步，不必自己拼命令行。中英双语说明与软件截图见 **[ovobrowser-manger](https://github.com/ovobrowsersupport/ovobrowser-manger)**。官网下载：[ovobrowser.com](https://ovobrowser.com/)。

**下载最新包** → [Releases v1.0.0](https://github.com/ovobrowsersupport/ovobrowser/releases/tag/v1.0.0)

---

## 目录

- [检测通过的网站列表](#检测通过的网站列表)
- [普通用户客户端](#普通用户客户端)
- [下载](#下载)
- [30 秒上手](#30-秒上手)
- [为什么自己编译](#为什么自己编译)
- [可修改的指纹（全表）](#可修改的指纹全表)
- [分类噪声](#分类噪声)
- [屏幕必须和 DPR 成对](#屏幕必须和-dpr-成对)
- [多语言调用](#多语言调用)
- [代理（带账密）](#代理带账密)
- [详细文档](#详细文档)
- [许可](#许可)
- [联系我们](#联系我们)
- [Star History](#star-history)

---

## 检测通过的网站列表

- [demo.fingerprint.com](https://demo.fingerprint.com/playground)
- 
https://github.com/user-attachments/assets/18958668-6489-44f5-9b7e-91d897c3ce86

- [browserscan.net](https://www.browserscan.net/)


https://github.com/user-attachments/assets/ef4b4520-d504-430c-84c8-129208074986



- [scrapingcourse.com](https://scrapingcourse.com)

- [deviceandbrowserinfo.com](https://deviceandbrowserinfo.com/are_you_a_bot)


https://github.com/user-attachments/assets/3ee4751f-d6bc-4684-8c6e-58f815927029



- [bot.sannysoft.com](https://bot.sannysoft.com/)


https://github.com/user-attachments/assets/61f3f519-991e-40af-ab76-70e4a5db9d13



- [bot-detector.rebrowser.net](https://bot-detector.rebrowser.net/)

- [abrahamjuliot.github.io](https://abrahamjuliot.github.io/creepjs/)

- [fingerprint-scan.com](https://fingerprint-scan.com/)

---

## 下载

解压 zip，里面的 `chrome.exe` 就是内核。

| 内核 | 版本 | 下载 |
|---|---|---|
| **150**（推荐） | `150.0.7871.124` | [ovobrowser-150-…-win64-portable.zip](https://github.com/ovobrowsersupport/ovobrowser/releases/download/v1.0.0/ovobrowser-150-150.0.7871.124-win64-portable.zip) |
| 144 | `144.0.7559.132` | [ovobrowser-144-…-win64-portable.zip](https://github.com/ovobrowsersupport/ovobrowser/releases/download/v1.0.0/ovobrowser-144-144.0.7559.132-win64-portable.zip) |
| 138 | `138.0.7204.183` | [ovobrowser-138-…-win64-portable.zip](https://github.com/ovobrowsersupport/ovobrowser/releases/download/v1.0.0/ovobrowser-138-138.0.7204.183-win64-portable.zip) |

150 对 FingerprintJS 的 ML 更友好；三套开关基本一致（144/150 的 audio 噪声更完整，canvas 主线程与 Worker 已对齐）。

环境变量（下面所有示例通用）：

```bat
set OVO_CHROME=D:\ovobrowser-150\chrome.exe
set OVO_PROFILE=D:\ovobrowser-profiles\acc01
set OVO_URL=https://demo.fingerprint.com/playground
```

---

## 30 秒上手

把路径换成你解压出来的 `chrome.exe`：

```bat
chrome.exe --user-data-dir=D:\ovobrowser-profiles\acc01 --no-first-run --no-default-browser-check --disable-quic --fingerprint-platform=windows --fingerprint-brand=Chrome --fingerprint-brand-version=150.0.7871.124 --fingerprint-platform-version=10.0.0 --user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36" --fingerprint-screen=1536x864 --fingerprint-device-scale-factor=1.25 --fingerprint-screen-color-depth=24 --fingerprint-hardware-concurrency=8 --fingerprint-device-memory=8 --timezone=America/New_York --lang=en-US --accept-lang=en-US,en --webrtc-ip-handling-policy=disable_non_proxied_udp https://demo.fingerprint.com/playground
```

这套是 **FingerprintJS Pro 全绿骨架**（不开噪声、不伪装 GPU 串）。时区/语言请改成你的**出口 IP 所在地**。

---

## 为什么自己编译

| | 注入式工具 | ovobrowser |
|---|---|---|
| 改指纹的位置 | JS / CDP / 启动参数拼装 | Chromium **C++ 源码**，编进二进制 |
| 典型代表 | playwright-stealth、puppeteer-extra | 本仓库便携包 |
| 检测站看到什么 | 补丁痕迹、`Function.toString` 异常、CDP 特征 | 普通 Chrome API |
| 升级 | Chrome 一更就碎 | 跟内核版本一起 rebase |

产品名改成 ovobrowser（任务管理器、关于页、默认 User Data 目录）。**UA 和 Client Hints 故意仍是 Chrome**——改成 ovobrowser 会被直接判未知浏览器。

规则：**不传开关 = 真机/上游默认**；**传入 = 按你给的值伪装或加噪**。

---

## 可修改的指纹（全表）

### Navigator / UA-CH / 硬件

| 开关 | 改什么 | 示例 | 不传 |
|---|---|---|---|
| `--user-agent=` | `navigator.userAgent` + 请求头 | `…Chrome/150.0.0.0 Safari/537.36` | 内核自带 UA |
| `--fingerprint-brand=` | UA-CH `brands` | `Chrome` | Chromium / Google Chrome |
| `--fingerprint-brand-version=` | UA-CH **完整补丁号** | `150.0.7871.124` | 内核版本 |
| `--fingerprint-platform=` | `navigator.platform` + UA-CH | `windows` / `macos` / `linux` / `android` / `ios` | 真机 OS |
| `--fingerprint-platform-version=` | UA-CH `platformVersion` | `10.0.0`（Win11 用 `13.0.0+`） | 真机 |
| `--fingerprint-hardware-concurrency=` | `navigator.hardwareConcurrency` | `8` | 真机核数 |
| `--fingerprint-device-memory=` | `navigator.deviceMemory` | `0.25/0.5/1/2/4/8` | 默认 `8` |
| `--fingerprint-dnt=` | `navigator.doNotTrack` | `1` / `0` / `unspecified` | `null` |
| `--fingerprint-battery=` | `getBattery()` | `1,1.0,0,Infinity` | 真实电池 |
| `--fingerprint-disable-speech-voices` | `speechSynthesis.getVoices()` | 传入即空列表 | 真实语音 |

`platform=ios` 时自动隐藏 `navigator.userAgentData`（真机 Safari 没有这个 API）。GREASE 品牌由内核按主版本生成，不用手写。

UA 里的版本位必须是 **`主版本.0.0.0`**。完整补丁号只放 `--fingerprint-brand-version`。写成 `Chrome/150.0.7871.124` → BrowserScan **Different browser version −5%**。

### 屏幕

| 开关 | 改什么 | 示例 | 不传 |
|---|---|---|---|
| `--fingerprint-screen=` | `screen.width/height/avail*`（**CSS 逻辑像素**） | `1536x864` | 真机分辨率 |
| `--fingerprint-device-scale-factor=` | `devicePixelRatio`、CSS `resolution`、`Sec-CH-DPR` | `1.25` | **宿主机缩放**（会泄露真机） |
| `--fingerprint-screen-color-depth=` | `colorDepth` / `pixelDepth` | `24` | 真机 |
| `--fingerprint-screen-width=` / `-height=` | 144/150 分量写法 | 等价于 screen | — |

### GPU / WebRTC / 隐藏接口

| 开关 | 改什么 | 示例 | 不传 |
|---|---|---|---|
| `--fingerprint-gpu-vendor=` | `UNMASKED_VENDOR_WEBGL` | `Qualcomm` | 真机 vendor |
| `--fingerprint-gpu-renderer=` | `UNMASKED_RENDERER_WEBGL` | `ANGLE (Qualcomm, Adreno (TM) 730, OpenGL ES 3.2)` | 真机 renderer |
| `--fingerprint-webgpu=disable` | `navigator.gpu = null` | 传入即隐藏 | 暴露适配器 |
| `--fingerprint-disable-bluetooth` | `navigator.bluetooth = null` | 传入即隐藏 | 真实蓝牙 API |
| `--webrtc-ip-handling-policy=` | ICE 候选 | `disable_non_proxied_udp`（推荐，默认） | 同默认 |

vendor 和 renderer 必须是**同一块真实 GPU** 的成套字符串。手机 UA + 桌面 RTX/D3D11 = 一眼假。

### 时区 / 语言

| 开关 | 改什么 | 示例 | 不传 |
|---|---|---|---|
| `--timezone=` | JS `Intl` / `Date` | `America/New_York` | 系统时区 |
| `--lang=` | UI + `navigator.language` + Intl locale | `en-US` | 系统语言 |
| `--accept-lang=` | 请求头 + `navigator.languages` | `en-US,en`（**不要 `q=`**） | 系统默认 |

三个都要跟**出口 IP** 对齐，否则 BrowserScan：Different time zones −10%、Language mismatch −10%。`--lang` 和 `--accept-lang` **必须都传**。

### 行为类（不是指纹，但常用）

| 开关 | 作用 |
|---|---|
| `--blink-settings=imagesEnabled=false` | 不加载图片 |
| `--max-image-size-kb=300` | 丢掉过大的图 |
| `--autoplay-policy=document-user-activation-required` | 禁自动播放 |
| `--mute-audio` | 静音 |
| `--disable-save-password` | 关掉保存密码气泡（默认会保存） |
| `--block-notifications` | 只拒通知 |
| `--deny-permission-prompts` | 拒全部权限弹窗 |
| `--disable-quic` | SOCKS 场景必须关，否则 https 常 `ERR_SSL_PROTOCOL_ERROR` |
| `--user-data-dir=` | 持久化 Cookie / 密码；不传则像临时档案 |

无开关、默认生效：ClientRects 噪声跨调用一致；144/150 canvas 主线程与 Worker 一致；UA 与内核主版本自洽；地址栏默认搜索已从 ungoogled 的「No Search」改回 Google。

---

## 分类噪声

传入 = 该类加噪；不传 = 原生输出（FingerprintJS 全绿请全部不传）。

| 开关 | 作用面 |
|---|---|
| `--fingerprint-canvas[=种子]` | `toDataURL` / `getImageData` / `measureText` |
| `--fingerprint-webgl[=种子]` | WebGL `readPixels` |
| `--fingerprint-audio[=种子]` | AudioContext 波形 / 采样率 |
| `--fingerprint-rects[=种子]` | `getClientRects` / `getBoundingClientRect` |
| `--fingerprint-font[=种子]` | 字体度量 / 字体列表 |
| `--fingerprint-random` | 五类一起开（各随机种子） |

- 裸开关：本次启动随机种子，**同一次运行跨标签一致**
- `=8842`：固定种子，一个账号一套
- `--fingerprint=数字` 只是缺省种子回退，**单独传不会开噪声**

138 的 audio 只有帧数微扰；144/150 才有完整采样率噪声。

开噪声或 `--fingerprint-gpu-*` → FingerprintJS Pro 容易报 **Browser Tampering**。要换 visitor 就开；要全绿就关。

---

## 屏幕必须和 DPR 成对

`--fingerprint-screen` 填的是逻辑像素。检测站显示的物理分辨率 = `screen.width × devicePixelRatio`。

只传 screen 不传 DPR，会乘上**宿主机真实缩放**，算出不存在的分辨率。

| screen | DPR | 真实硬件 |
|---|---|---|
| `1920x1080` | `1` | 1080p @100% |
| `1536x864` | `1.25` | 1080p 笔记本 @125%（最常见） |
| `1280x720` | `1.5` | 1080p @150% |
| `2560x1440` | `1` | 2K @100% |
| `2048x1152` | `1.25` | 2K 笔记本 @125% |
| `1920x1080` | `2` | 4K @200% |
| `1280x800` | `2` | MacBook Pro 13" Retina |
| `412x915` | `2.625` | Pixel 7 |
| `393x852` | `3` | iPhone 14 Pro |

macOS 只有 `1` / `2`；Windows 用 `1/1.25/1.5/1.75/2/2.25`，不要编 `1.33`。

Console 自检：

```js
console.table({
  logical: `${screen.width}x${screen.height}`,
  dpr: devicePixelRatio,
  physical: `${screen.width * devicePixelRatio}x${screen.height * devicePixelRatio}`,
  media: matchMedia(`(resolution: ${devicePixelRatio}dppx)`).matches,
});
```

---

## 多语言调用

内核**没有 HTTP SDK**。所有语言做同一件事：拼 argv → spawn `chrome.exe`。把 `OVO_CHROME` 指到解压后的 exe。可运行文件也在 [`examples/`](examples/)。

### Python

```python
import os, subprocess
from pathlib import Path

chrome = os.environ.get("OVO_CHROME", r"D:\ovobrowser-150\chrome.exe")
profile = os.environ.get("OVO_PROFILE", r"D:\ovobrowser-profiles\py")
Path(profile).mkdir(parents=True, exist_ok=True)

subprocess.Popen([
    chrome,
    f"--user-data-dir={profile}",
    "--no-first-run", "--no-default-browser-check", "--disable-quic",
    "--fingerprint-platform=windows",
    "--fingerprint-brand=Chrome",
    "--fingerprint-brand-version=150.0.7871.124",
    "--fingerprint-platform-version=10.0.0",
    "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36",
    "--fingerprint-hardware-concurrency=8",
    "--fingerprint-device-memory=8",
    "--fingerprint-screen=1536x864",
    "--fingerprint-device-scale-factor=1.25",
    "--fingerprint-screen-color-depth=24",
    "--fingerprint-battery=1,1.0,0,Infinity",
    "--webrtc-ip-handling-policy=disable_non_proxied_udp",
    "--timezone=America/New_York",
    "--lang=en-US",
    "--accept-lang=en-US,en",
    "https://demo.fingerprint.com/playground",
])
```

### Python + Playwright

`pip install playwright`。用 **persistent context**，不要 `launch()` 隐身窗（BrowserScan 会扣 Incognito）。

```python
from playwright.sync_api import sync_playwright

CHROME = r"D:\ovobrowser-150\chrome.exe"
PROFILE = r"D:\ovobrowser-profiles\pw"
ARGS = [
    "--no-first-run", "--no-default-browser-check", "--disable-quic",
    "--fingerprint-platform=windows", "--fingerprint-brand=Chrome",
    "--fingerprint-brand-version=150.0.7871.124",
    "--fingerprint-platform-version=10.0.0",
    "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36",
    "--fingerprint-screen=1536x864", "--fingerprint-device-scale-factor=1.25",
    "--fingerprint-screen-color-depth=24",
    "--fingerprint-hardware-concurrency=8", "--fingerprint-device-memory=8",
    "--timezone=America/New_York", "--lang=en-US", "--accept-lang=en-US,en",
    "--webrtc-ip-handling-policy=disable_non_proxied_udp",
]

with sync_playwright() as p:
    ctx = p.chromium.launch_persistent_context(
        user_data_dir=PROFILE,
        executable_path=CHROME,
        headless=False,
        args=ARGS,
        ignore_default_args=["--enable-automation", "--no-sandbox"],
        chromium_sandbox=True,
        no_viewport=True,
    )
    page = ctx.pages[0] if ctx.pages else ctx.new_page()
    page.goto("https://demo.fingerprint.com/playground")
    input("检查完回车…")
    ctx.close()
```

### Node.js

```js
const { spawn } = require("child_process");
const fs = require("fs");

const chrome = process.env.OVO_CHROME || "D:\\ovobrowser-150\\chrome.exe";
const profile = process.env.OVO_PROFILE || "D:\\ovobrowser-profiles\\node";
fs.mkdirSync(profile, { recursive: true });

spawn(chrome, [
  `--user-data-dir=${profile}`,
  "--no-first-run", "--no-default-browser-check", "--disable-quic",
  "--fingerprint-platform=windows", "--fingerprint-brand=Chrome",
  "--fingerprint-brand-version=150.0.7871.124",
  "--fingerprint-platform-version=10.0.0",
  "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36",
  "--fingerprint-hardware-concurrency=8", "--fingerprint-device-memory=8",
  "--fingerprint-screen=1536x864", "--fingerprint-device-scale-factor=1.25",
  "--fingerprint-screen-color-depth=24",
  "--fingerprint-battery=1,1.0,0,Infinity",
  "--webrtc-ip-handling-policy=disable_non_proxied_udp",
  "--timezone=America/New_York", "--lang=en-US", "--accept-lang=en-US,en",
  "https://demo.fingerprint.com/playground",
], { detached: true, stdio: "ignore" }).unref();
```

### Go

```go
chrome := `D:\ovobrowser-150\chrome.exe`
profile := `D:\ovobrowser-profiles\go`
cmd := exec.Command(chrome,
    "--user-data-dir="+profile,
    "--no-first-run", "--no-default-browser-check", "--disable-quic",
    "--fingerprint-platform=windows", "--fingerprint-brand=Chrome",
    "--fingerprint-brand-version=150.0.7871.124",
    "--fingerprint-platform-version=10.0.0",
    "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36",
    "--fingerprint-hardware-concurrency=8", "--fingerprint-device-memory=8",
    "--fingerprint-screen=1536x864", "--fingerprint-device-scale-factor=1.25",
    "--fingerprint-screen-color-depth=24",
    "--webrtc-ip-handling-policy=disable_non_proxied_udp",
    "--timezone=America/New_York", "--lang=en-US", "--accept-lang=en-US,en",
    "https://demo.fingerprint.com/playground",
)
cmd.Start()
```

### C#

```csharp
Process.Start(new ProcessStartInfo {
    FileName = @"D:\ovobrowser-150\chrome.exe",
    Arguments = string.Join(" ", new[] {
        "--user-data-dir=\"D:\\ovobrowser-profiles\\cs\"",
        "--no-first-run", "--no-default-browser-check", "--disable-quic",
        "--fingerprint-platform=windows", "--fingerprint-brand=Chrome",
        "--fingerprint-brand-version=150.0.7871.124",
        "--fingerprint-platform-version=10.0.0",
        "--user-agent=\"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36\"",
        "--fingerprint-screen=1536x864", "--fingerprint-device-scale-factor=1.25",
        "--timezone=America/New_York", "--lang=en-US", "--accept-lang=en-US,en",
        "--webrtc-ip-handling-policy=disable_non_proxied_udp",
        "https://demo.fingerprint.com/playground",
    }),
    UseShellExecute = true,
});
```

### PowerShell

```powershell
$chrome  = $env:OVO_CHROME;  if (-not $chrome)  { $chrome  = "D:\ovobrowser-150\chrome.exe" }
$profile = $env:OVO_PROFILE; if (-not $profile) { $profile = "D:\ovobrowser-profiles\ps" }
New-Item -ItemType Directory -Force -Path $profile | Out-Null
Start-Process $chrome -ArgumentList @(
  "--user-data-dir=$profile",
  "--no-first-run","--no-default-browser-check","--disable-quic",
  "--fingerprint-platform=windows","--fingerprint-brand=Chrome",
  "--fingerprint-brand-version=150.0.7871.124",
  "--fingerprint-platform-version=10.0.0",
  "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36",
  "--fingerprint-screen=1536x864","--fingerprint-device-scale-factor=1.25",
  "--fingerprint-hardware-concurrency=8","--fingerprint-device-memory=8",
  "--timezone=America/New_York","--lang=en-US","--accept-lang=en-US,en",
  "--webrtc-ip-handling-policy=disable_non_proxied_udp",
  "https://demo.fingerprint.com/playground"
)
```

### Java

```java
List<String> cmd = new ArrayList<>();
cmd.add("D:\\ovobrowser-150\\chrome.exe");
cmd.add("--user-data-dir=D:\\ovobrowser-profiles\\java");
cmd.add("--no-first-run"); cmd.add("--disable-quic");
cmd.add("--fingerprint-platform=windows");
cmd.add("--fingerprint-brand=Chrome");
cmd.add("--fingerprint-brand-version=150.0.7871.124");
cmd.add("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36");
cmd.add("--fingerprint-screen=1536x864");
cmd.add("--fingerprint-device-scale-factor=1.25");
cmd.add("--timezone=America/New_York");
cmd.add("--lang=en-US"); cmd.add("--accept-lang=en-US,en");
cmd.add("https://demo.fingerprint.com/playground");
new ProcessBuilder(cmd).start();
```

### Rust

```rust
Command::new(r"D:\ovobrowser-150\chrome.exe")
    .args([
        "--user-data-dir=D:\\ovobrowser-profiles\\rust",
        "--no-first-run", "--disable-quic",
        "--fingerprint-platform=windows",
        "--fingerprint-brand=Chrome",
        "--fingerprint-brand-version=150.0.7871.124",
        "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36",
        "--fingerprint-screen=1536x864",
        "--fingerprint-device-scale-factor=1.25",
        "--timezone=America/New_York",
        "--lang=en-US", "--accept-lang=en-US,en",
        "https://demo.fingerprint.com/playground",
    ])
    .spawn()?;
```

---

## 代理（带账密）

Chromium `--proxy-server` **不支持用户名密码**。住宅代理请：

```
浏览器 → 本地无认证 SOCKS5 桥 →（国内再经本机梯子，如 7890）→ 上游认证代理
```

`--proxy-server=socks5://127.0.0.1:本地桥端口`

走 SOCKS 时务必 `--disable-quic`。时区/语言要在**启动前**按出口 IP 填好，启动后再改 `--timezone` 无效。

---

## 详细文档

| 文档 | 中文 | English |
|---|---|---|
| 启动参数完整说明 | [FLAGS.md](docs/zh/FLAGS.md) | [FLAGS.md](docs/en/FLAGS.md) |
| 指纹修改面与实现说明 | [FINGERPRINT.md](docs/zh/FINGERPRINT.md) | [FINGERPRINT.md](docs/en/FINGERPRINT.md) |
| 推荐启动配方 | [RECIPES.md](docs/zh/RECIPES.md) | [RECIPES.md](docs/en/RECIPES.md) |
| 仓库目录结构 | [STRUCTURE.md](docs/STRUCTURE.md) | — |

### 版本更新说明

<details>
<summary><strong>点击展开：v1.0.0 之后的内核更新（2026-08-26 ～ 2026-10-20）</strong></summary>

<br>

<details>
<summary><strong>2026-10-20</strong> · 对照商业指纹浏览器补齐 11 处细节、Google 首页登录态（138 / 144 / 150 / 155）</summary>

把我们的内核、某商业指纹浏览器、正版 Chrome 155 放在一起逐项对比，下面这些地方原来和正版不一样，可能被识别，现已对齐：

- **`measureText` 修复**：开 `--fingerprint-font` 等噪声后，文字宽度会变成接近 0，现在只做极小的偏移。
- **WebGL 参数**：真机是 NVIDIA、伪装成 Intel / AMD 时，`MAX_VERTEX_UNIFORM_VECTORS` 等 3 个参数原来露出 NVIDIA 特有的 4095，现在按伪装的厂商返回 4096 / 16384 / 212992。
- **WebGPU 厂商与架构**：伪装显卡时，`adapter.info` 返回和正版一样的短名，如 `intel` / `gen-9`、`amd` / `rdna-2`、`nvidia` / `ampere`，原来是 `Google Inc. (Intel)`、架构为空。
- **WebGPU 特性**：不再按种子隐藏可选特性，改报本机真实的全部特性。
- **WebGL 噪声**：`readPixels`、`toDataURL`、`drawImage(webglCanvas)` 三种读取方式结果完全一致，原来只有 `readPixels` 加了噪声，一比对就能看出来。
- **语音列表**：补上正版 Chrome 自带的 19 个 Google 在线语音（加上系统语音共 22 个），名称和正版逐字相同。
- **`outerWidth` / `outerHeight`**：返回真实窗口尺寸，原来等于内视口，真实浏览器不会这样。打开开发者工具导致差值异常时，才回退成「内视口 + 正常边框」，反调试仍然有效。
- **ClientRects 噪声**：整数坐标的元素不再加小数偏移（正版返回 `10, 20`，不会是 `9.9998, 19.9992`），带小数的坐标照常加噪声。
- **书签栏**：默认不再常驻。原来网页可视高度比正版矮 33px，现在和正版一样只在新标签页显示。
- **Widevine**：便携包里带上了 Widevine 组件，`com.widevine.alpha` 可用，Netflix 等 DRM 视频能播放。
- **新参数 `--fingerprint-max-touch-points=<0~10>`**：用于桌面平台，改 `navigator.maxTouchPoints`，并同步 `any-pointer: coarse`。普通台式机传 `0`。不传则跟随宿主机，触屏笔记本会报 10。
- **Google 首页登录态**：登录后新标签页打开的 Google 首页能正常显示头像，原来始终显示「登录」按钮。

验证结果：四个内核的 lies 均为 0，BrowserScan 不论是否伪装 GPU 都是 100%。

</details>

<details>
<summary><strong>2026-10-18</strong> · AMD 显卡 Canvas 报红、Google 登录校验头、deviceMemory（138 / 144 / 150 / 155）</summary>

- **AMD 显卡 Canvas 报红**：在 AMD 显卡上开画布噪声，BrowserScan 会报 Canvas Tampering。新的画布噪声只改抗锯齿边缘半透明像素的 alpha 最低位，不动 RGB 和纯色区域，同一画面处理两遍结果不变。`getImageData`、`toDataURL`、`toBlob`、子区域读取的结果彼此一致。
- **Google 登录校验头**：发往 Google 域名的请求补上正版 Chrome 才有的 `x-browser-channel / year / validation / copyright` 四个请求头，按 UA 主版本取值，和同版本正版逐字节一致，登录 Google 账号更不容易被风控。
- **deviceMemory**：`navigator.deviceMemory` 与请求头 `Sec-CH-Device-Memory` 统一成同一个值，原来请求头报的是真机内存。取值范围也按各版本正版：138 / 144 为 0.25～8；150 / 155 桌面为 2～32、移动端为 1～8。

</details>

<details>
<summary><strong>2026-10-13</strong> · 新增 155 内核</summary>

- 新增 `155.0.8059.39` 内核（基于 ungoogled-chromium 155），参数和 150 完全相同。
- 155 内核 BrowserScan 100%；FingerprintJS Pro 的 Bot、Tampering、DevTools、VM、Incognito 均为 Not detected，与 150 一致。

</details>

<details>
<summary><strong>2026-10-09</strong> · Chrome 应用商店可以安装扩展（138 / 144）</summary>

- 原来在 Chrome 应用商店点「添加至 Chrome」，144 会一直转圈，138 会显示「目前无法获取该产品」，现在都能正常下载安装。
- 后台自动更新扩展仍然是关闭的，浏览器不会主动连 Google 检查扩展更新。

</details>

<details>
<summary><strong>2026-10-07</strong> · 移动端设备控制条</summary>

- **设备控制条**：平台设为 android / ios 并传了 `--fingerprint-screen` 时，窗口顶部出现类似 DevTools 设备模式的控制条，可以：
  - 切换机型预设或自定义宽高；
  - 旋转横竖屏；
  - 调整显示比例；
  - 设置网络限速。
- **手机画面显示**：手机画面居中显示，窗口较小时按比例整体缩小，网页看到的视口和 DPR 仍是设备的值。原来网页贴在左上角，窗口小了还会被裁掉。

</details>

<details>
<summary><strong>2026-10-05</strong> · 移动端一致性修复</summary>

- **中文字体**：切到 Android / iOS 并开 `--fingerprint-font` 时，中文不再显示成方框，雅黑、宋体、苹方等中日韩字体会保留。
- **平台信息一致**：页面、Worker、网络请求三处的平台信息保持一致，`userAgentData`、`Sec-CH-UA-Platform`、`Sec-CH-UA-Mobile` 都会跟着改成 Android。iOS 不再发送 Client Hints 请求头。
- **触控、指针和屏幕方向**：移动端的 `maxTouchPoints` 为 5，`pointer: coarse`，`hover: none`，竖屏时 `screen.orientation` 为 `portrait-primary`。
- **WebGL 报错**：移动端伪装 GPU 后，BrowserScan 不再扣「WebGL exception」分。
- **新标签页**：新标签页默认打开 Google 首页（原来是空白页），安卓 UA 下打开 Google 也不会 404。

</details>

<details>
<summary><strong>2026-08-26</strong> · 反调试默认开启</summary>

- 网页里的 `debugger` 语句（包括字面量、`eval`、`new Function`）默认不再让页面暂停，防止站点借此卡死页面或检测开发者工具。
- 需要自己调试时，传 `--fingerprint-allow-debugger` 恢复原生行为。

</details>

</details>

---

## 许可

文档与示例：本仓库 [LICENSE](LICENSE)（MIT）。内核二进制遵循 Chromium / ungoogled-chromium 上游许可。

---

## 联系我们

- QQ 群：`1108811142`
- Telegram：[t.me/ovobrowser_group](https://t.me/ovobrowser_group)
- 邮箱：[support@ovobrowser.com](mailto:support@ovobrowser.com)

---

## Star History

<a href="https://www.star-history.com/#ovobrowsersupport/ovobrowser&Date">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=ovobrowsersupport/ovobrowser&type=Date&theme=dark" />
    <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=ovobrowsersupport/ovobrowser&type=Date" />
    <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=ovobrowsersupport/ovobrowser&type=Date" width="600" />
  </picture>
</a>
