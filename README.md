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

<h3 align="center">源码级 Chromium 指纹内核。</h3>

源码级修改的 Chromium 指纹内核。不是 JS 注入，不是 `playwright-stealth` 那套运行时补丁——指纹在 C++ 里改完再编译进二进制。检测站看到的是普通 Chrome，因为它本来就是 Chromium。

当前便携包：**Windows x64** · 内核 **138 / 144 / 150** · 产品名 **ovobrowser**（UA / Client Hints 仍报 Chrome，避免被判未知浏览器）

- 5 类独立噪声：Canvas / WebGL / Audio / ClientRects / Font（可关可固定种子）
- UA-CH、平台、核数、内存、屏幕、DPR、电池、DNT、语音列表
- WebGL vendor/renderer、隐藏 WebGPU / 蓝牙、WebRTC 不漏内网 IP
- 时区 / `lang` / `accept-lang` 与出口 IP 对齐
- 任意语言：拼命令行 → 拉起 `chrome.exe`（Python / Node / Go / C# / PowerShell / Java / Rust 示例都在本页）

**下载最新包** → [Releases v1.0.0](https://github.com/ovobrowsersupport/ovobrowser/releases/tag/v1.0.0)

---

## 目录

- [检测通过的网站列表](#检测通过的网站列表)
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

---

## 检测通过的网站列表

- [demo.fingerprint.com](https://demo.fingerprint.com/playground)
<video src="https://raw.githubusercontent.com/ovobrowsersupport/ovobrowser/main/video/fingerprint-pro.mp4" controls="controls" width="100%">
</video>

- [browserscan.net](https://www.browserscan.net/)
<video src="https://raw.githubusercontent.com/ovobrowsersupport/ovobrowser/main/video/browserscan.mp4" controls="controls" width="100%">
</video>

- [scrapingcourse.com](https://scrapingcourse.com)

- [deviceandbrowserinfo.com](https://deviceandbrowserinfo.com/are_you_a_bot)
<video ssrc="https://raw.githubusercontent.com/ovobrowsersupport/ovobrowser/main/video/device-browser-info.mp4" controls="controls" width="100%">
</video>

- [bot.sannysoft.com](https://bot.sannysoft.com/)
<video ssrc="https://raw.githubusercontent.com/ovobrowsersupport/ovobrowser/main/video/bot-sannysoft.mp4" controls="controls" width="100%">
</video>

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

---

## 许可

文档与示例：本仓库 [LICENSE](LICENSE)（MIT）。内核二进制遵循 Chromium / ungoogled-chromium 上游许可。
