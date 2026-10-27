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
  <a href="README.md">中文</a> · <strong>English</strong>
</p>

<h3 align="center">Source-level Chromium fingerprint kernel.</h3>

Source-level Chromium fingerprint kernel. Not JS injection, not `playwright-stealth` — fingerprints are patched in C++ and compiled into the binary. Detection sites see a normal Chrome because it *is* Chromium.

Portable builds: **Windows x64** · kernels **138 / 144 / 150 / 155** · product name **ovobrowser** (UA / Client Hints still report Chrome so you are not scored as an unknown browser)

- 5 independent noise classes: Canvas / WebGL / Audio / ClientRects / Font (off by default; optional fixed seeds)
- UA-CH, platform, cores, memory, screen, DPR, battery, DNT, speech voices
- WebGL vendor/renderer, hide WebGPU / Bluetooth, WebRTC without LAN IPs
- Timezone / `lang` / `accept-lang` aligned to the exit IP
- Any language: build argv → spawn `chrome.exe` (Python / Node / Go / C# / PowerShell / Java / Rust on this page)

### Client for everyday users

For everyday users we already ship a GUI fingerprint-browser client: install it, then manage profiles, proxies, teams, and window sync — no command line. Bilingual docs and screenshots: **[ovobrowser-manger](https://github.com/ovobrowsersupport/ovobrowser-manger)**. Download: [ovobrowser.com](https://ovobrowser.com/).

**Download** → [Releases](https://github.com/ovobrowsersupport/ovobrowser/releases/latest)

---

## Contents

- [Sites that pass](#sites-that-pass)
- [Client for everyday users](#client-for-everyday-users)
- [Download](#download)
- [30-second start](#30-second-start)
- [Why a custom build](#why-a-custom-build)
- [What you can change](#what-you-can-change)
- [Category noise](#category-noise)
- [Screen + DPR must be paired](#screen--dpr-must-be-paired)
- [Launch from any language](#launch-from-any-language)
- [Authenticated proxies](#authenticated-proxies)
- [Documentation](#documentation)
- [License](#license)
- [Contact](#contact)
- [Star History](#star-history)

---

## Sites that pass

- [demo.fingerprint.com](https://demo.fingerprint.com/playground)
- [browserscan.net](https://www.browserscan.net/)
- [bot.incolumitas.com](https://bot.incolumitas.com/)
- [deviceandbrowserinfo.com](https://deviceandbrowserinfo.com/are_you_a_bot)
- [bot.sannysoft.com](https://bot.sannysoft.com/)
- [bot-detector.rebrowser.net](https://bot-detector.rebrowser.net/)
- [abrahamjuliot.github.io](https://abrahamjuliot.github.io/creepjs/)
- [fingerprint-scan.com](https://fingerprint-scan.com/)

---

## Download

Unzip; `chrome.exe` is the kernel.

| Kernel | Version | Asset |
|---|---|---|
| 155 (latest) | `155.0.8059.39` | [ovobrowser-155-…-win64-portable.zip](https://github.com/ovobrowsersupport/ovobrowser/releases/latest/download/ovobrowser-155-155.0.8059.39-win64-portable.zip) |
| **150** (recommended) | `150.0.7871.124` | [ovobrowser-150-…-win64-portable.zip](https://github.com/ovobrowsersupport/ovobrowser/releases/latest/download/ovobrowser-150-150.0.7871.124-win64-portable.zip) |
| 144 | `144.0.7559.132` | [ovobrowser-144-…-win64-portable.zip](https://github.com/ovobrowsersupport/ovobrowser/releases/latest/download/ovobrowser-144-144.0.7559.132-win64-portable.zip) |
| 138 | `138.0.7204.183` | [ovobrowser-138-…-win64-portable.zip](https://github.com/ovobrowsersupport/ovobrowser/releases/latest/download/ovobrowser-138-138.0.7204.183-win64-portable.zip) |

150 is friendliest to FingerprintJS ML. 155 is the newest kernel, with exactly the same flags as 150. Flag sets are the same; 144 / 150 / 155 have fuller audio noise and canvas main/Worker alignment. All four portable builds bundle Widevine for DRM video.

```bat
set OVO_CHROME=D:\ovobrowser-150\chrome.exe
set OVO_PROFILE=D:\ovobrowser-profiles\acc01
set OVO_URL=https://demo.fingerprint.com/playground
```

---

## 30-second start

```bat
chrome.exe --user-data-dir=D:\ovobrowser-profiles\acc01 --no-first-run --no-default-browser-check --disable-quic --fingerprint-platform=windows --fingerprint-brand=Chrome --fingerprint-brand-version=150.0.7871.124 --fingerprint-platform-version=10.0.0 --user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36" --fingerprint-screen=1536x864 --fingerprint-device-scale-factor=1.25 --fingerprint-screen-color-depth=24 --fingerprint-hardware-concurrency=8 --fingerprint-device-memory=8 --timezone=America/New_York --lang=en-US --accept-lang=en-US,en --webrtc-ip-handling-policy=disable_non_proxied_udp https://demo.fingerprint.com/playground
```

This is the **FingerprintJS Pro green** skeleton (no noise, no GPU-string spoof). Change timezone/language to the **exit IP region**.

---

## Why a custom build

| | Injected tools | ovobrowser |
|---|---|---|
| Where fingerprints change | JS / CDP / flag soup | Chromium **C++**, baked into the binary |
| Typical names | playwright-stealth, puppeteer-extra | this portable zip |
| What sites see | patch tells, `Function.toString` lies, CDP | stock Chrome APIs |
| Updates | break on every Chrome bump | rebase with the kernel |

Product name is ovobrowser (Task Manager, About, default User Data dir). **UA and Client Hints stay Chrome** on purpose.

Rule: **omit a flag = real hardware / upstream default**. **Pass a flag = spoof or noise as specified**.

---

## What you can change

### Navigator / UA-CH / hardware

| Flag | Effect | Example | If omitted |
|---|---|---|---|
| `--user-agent=` | UA string + header | `…Chrome/150.0.0.0 Safari/537.36` | kernel UA |
| `--fingerprint-brand=` | UA-CH `brands` | `Chrome` | Chromium / Google Chrome |
| `--fingerprint-brand-version=` | UA-CH **full patch** | `150.0.7871.124` | kernel version |
| `--fingerprint-platform=` | platform + UA-CH | `windows` / `macos` / `linux` / `android` / `ios` | real OS |
| `--fingerprint-platform-version=` | UA-CH `platformVersion` | `10.0.0` (Win11: `13.0.0+`) | real |
| `--fingerprint-hardware-concurrency=` | hardwareConcurrency | `8` | real cores |
| `--fingerprint-device-memory=` | deviceMemory + `Sec-CH-Device-Memory` header | 138/144: `0.25/0.5/1/2/4/8`; 150/155 desktop: `2/4/8/16/32`, mobile: `1/2/4/8` (invalid values snap to the nearest step) | default `8` (JS and header match) |
| `--fingerprint-max-touch-points=` | `navigator.maxTouchPoints` + `any-pointer` | `0`–`10` (`0` for a regular desktop) | follows the host; fixed at 5 on android / ios |
| `--fingerprint-dnt=` | doNotTrack | `1` / `0` / `unspecified` | `null` |
| `--fingerprint-battery=` | getBattery | `1,1.0,0,Infinity` | real battery |
| `--fingerprint-disable-speech-voices` | empty voice list | flag only | real voices |

`platform=ios` hides `navigator.userAgentData`. GREASE brands are generated for you.

UA version **must** be `MAJOR.0.0.0`. Full patch goes only in `--fingerprint-brand-version`. `Chrome/150.0.7871.124` → BrowserScan **Different browser version −5%**.

### Screen

| Flag | Effect | Example | If omitted |
|---|---|---|---|
| `--fingerprint-screen=` | `screen.*` (**CSS logical px**) | `1536x864` | real screen |
| `--fingerprint-device-scale-factor=` | DPR / CSS resolution / `Sec-CH-DPR` | `1.25` | **host scale** (leaks the machine) |
| `--fingerprint-screen-color-depth=` | colorDepth | `24` | real |
| `--fingerprint-screen-width=` / `-height=` | 144 / 150 / 155 split form | same as screen | — |

### GPU / WebRTC / hide APIs

| Flag | Effect | Example | If omitted |
|---|---|---|---|
| `--fingerprint-gpu-vendor=` | UNMASKED_VENDOR_WEBGL | `Qualcomm` | real vendor |
| `--fingerprint-gpu-renderer=` | UNMASKED_RENDERER_WEBGL | Adreno/ANGLE string | real renderer |
| `--fingerprint-webgpu=disable` | `navigator.gpu = null` | flag only | real WebGPU |
| `--fingerprint-disable-bluetooth` | `navigator.bluetooth = null` | flag only | real |
| `--webrtc-ip-handling-policy=` | ICE candidates | `disable_non_proxied_udp` (default) | same |

Vendor + renderer must be one real GPU. Mobile UA + desktop RTX is an instant lie.

### Timezone / language

| Flag | Effect | Example | If omitted |
|---|---|---|---|
| `--timezone=` | Intl / Date | `America/New_York` | host zone |
| `--lang=` | UI + `navigator.language` + Intl locale | `en-US` | host language |
| `--accept-lang=` | header + `navigator.languages` | `en-US,en` (**no `q=`**) | host default |

All three must match the **exit IP**. Pass **both** lang flags.

### Behavior (not fingerprints)

| Flag | Effect |
|---|---|
| `--blink-settings=imagesEnabled=false` | no images |
| `--max-image-size-kb=300` | drop large images |
| `--autoplay-policy=document-user-activation-required` | no autoplay |
| `--mute-audio` | mute |
| `--disable-save-password` | no save-password bubble (default is on) |
| `--block-notifications` | notifications only |
| `--deny-permission-prompts` | all permission prompts |
| `--disable-quic` | required with SOCKS or HTTPS often fails |
| `--user-data-dir=` | persist cookies/passwords |

Always on: ClientRects consistency (integer coordinates are not noised); 144 / 150 / 155 canvas main/Worker match; anti-debugging on by default (pass `--fingerprint-allow-debugger` to debug yourself); bookmark bar not shown permanently; `outerWidth/Height` report the real window size; UA aligned with kernel major; default search restored to Google.

---

## Category noise

Pass = noise on; omit = native (keep all off for FingerprintJS green).

| Flag | Surface |
|---|---|
| `--fingerprint-canvas[=seed]` | toDataURL / getImageData / measureText |
| `--fingerprint-webgl[=seed]` | WebGL `readPixels` / `toDataURL` / `drawImage` (all three match) |
| `--fingerprint-audio[=seed]` | AudioContext |
| `--fingerprint-rects[=seed]` | ClientRects |
| `--fingerprint-font[=seed]` | font metrics / list |
| `--fingerprint-random` | all five, random seeds |

Bare flag = random seed for this process, stable across tabs. `=8842` = reproducible. `--fingerprint=N` is fallback only and does **not** enable noise by itself.

Noise or `--fingerprint-gpu-*` → FingerprintJS Pro **Browser Tampering**. Pick uniqueness or “green”, not both.

---

## Screen + DPR must be paired

`screen` is logical pixels. Sites show `screen.width × devicePixelRatio`.

| screen | DPR | Hardware |
|---|---|---|
| `1920x1080` | `1` | 1080p @100% |
| `1536x864` | `1.25` | 1080p laptop @125% |
| `1280x720` | `1.5` | 1080p @150% |
| `2560x1440` | `1` | 1440p @100% |
| `1920x1080` | `2` | 4K @200% |
| `412x915` | `2.625` | Pixel 7 |
| `393x852` | `3` | iPhone 14 Pro |

macOS: `1` or `2` only. Windows: `1/1.25/1.5/1.75/2/2.25`.

```js
console.table({
  logical: `${screen.width}x${screen.height}`,
  dpr: devicePixelRatio,
  physical: `${screen.width * devicePixelRatio}x${screen.height * devicePixelRatio}`,
  media: matchMedia(`(resolution: ${devicePixelRatio}dppx)`).matches,
});
```

---

## Launch from any language

No HTTP SDK. Spawn `chrome.exe` with the same flags. Runnable copies live in [`examples/`](examples/).

### Python

```python
import os, subprocess
from pathlib import Path

chrome = os.environ.get("OVO_CHROME", r"D:\ovobrowser-150\chrome.exe")
profile = os.environ.get("OVO_PROFILE", r"D:\ovobrowser-profiles\py")
Path(profile).mkdir(parents=True, exist_ok=True)

subprocess.Popen([
    chrome, f"--user-data-dir={profile}",
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
])
```

### Python + Playwright

Use **persistent context**, not `launch()` (incognito is scored).

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    ctx = p.chromium.launch_persistent_context(
        user_data_dir=r"D:\ovobrowser-profiles\pw",
        executable_path=r"D:\ovobrowser-150\chrome.exe",
        headless=False,
        args=[
            "--no-first-run", "--disable-quic",
            "--fingerprint-platform=windows", "--fingerprint-brand=Chrome",
            "--fingerprint-brand-version=150.0.7871.124",
            "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36",
            "--fingerprint-screen=1536x864", "--fingerprint-device-scale-factor=1.25",
            "--timezone=America/New_York", "--lang=en-US", "--accept-lang=en-US,en",
            "--webrtc-ip-handling-policy=disable_non_proxied_udp",
        ],
        ignore_default_args=["--enable-automation", "--no-sandbox"],
        chromium_sandbox=True,
        no_viewport=True,
    )
    page = ctx.pages[0] if ctx.pages else ctx.new_page()
    page.goto("https://demo.fingerprint.com/playground")
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
  "--no-first-run", "--disable-quic",
  "--fingerprint-platform=windows", "--fingerprint-brand=Chrome",
  "--fingerprint-brand-version=150.0.7871.124",
  "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36",
  "--fingerprint-screen=1536x864", "--fingerprint-device-scale-factor=1.25",
  "--timezone=America/New_York", "--lang=en-US", "--accept-lang=en-US,en",
  "--webrtc-ip-handling-policy=disable_non_proxied_udp",
  "https://demo.fingerprint.com/playground",
], { detached: true, stdio: "ignore" }).unref();
```

### Go

```go
cmd := exec.Command(`D:\ovobrowser-150\chrome.exe`,
    "--user-data-dir=D:\\ovobrowser-profiles\\go",
    "--no-first-run", "--disable-quic",
    "--fingerprint-platform=windows", "--fingerprint-brand=Chrome",
    "--fingerprint-brand-version=150.0.7871.124",
    "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36",
    "--fingerprint-screen=1536x864", "--fingerprint-device-scale-factor=1.25",
    "--timezone=America/New_York", "--lang=en-US", "--accept-lang=en-US,en",
    "--webrtc-ip-handling-policy=disable_non_proxied_udp",
    "https://demo.fingerprint.com/playground",
)
cmd.Start()
```

### C#

```csharp
Process.Start(new ProcessStartInfo {
    FileName = @"D:\ovobrowser-150\chrome.exe",
    Arguments = "--user-data-dir=\"D:\\ovobrowser-profiles\\cs\" --no-first-run --disable-quic --fingerprint-platform=windows --fingerprint-brand=Chrome --fingerprint-brand-version=150.0.7871.124 --user-agent=\"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36\" --fingerprint-screen=1536x864 --fingerprint-device-scale-factor=1.25 --timezone=America/New_York --lang=en-US --accept-lang=en-US,en --webrtc-ip-handling-policy=disable_non_proxied_udp https://demo.fingerprint.com/playground",
    UseShellExecute = true,
});
```

### PowerShell

```powershell
Start-Process "D:\ovobrowser-150\chrome.exe" -ArgumentList @(
  "--user-data-dir=D:\ovobrowser-profiles\ps",
  "--no-first-run","--disable-quic",
  "--fingerprint-platform=windows","--fingerprint-brand=Chrome",
  "--fingerprint-brand-version=150.0.7871.124",
  "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36",
  "--fingerprint-screen=1536x864","--fingerprint-device-scale-factor=1.25",
  "--timezone=America/New_York","--lang=en-US","--accept-lang=en-US,en",
  "--webrtc-ip-handling-policy=disable_non_proxied_udp",
  "https://demo.fingerprint.com/playground"
)
```

### Java

```java
new ProcessBuilder(
    "D:\\ovobrowser-150\\chrome.exe",
    "--user-data-dir=D:\\ovobrowser-profiles\\java",
    "--no-first-run", "--disable-quic",
    "--fingerprint-platform=windows", "--fingerprint-brand=Chrome",
    "--fingerprint-brand-version=150.0.7871.124",
    "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36",
    "--fingerprint-screen=1536x864", "--fingerprint-device-scale-factor=1.25",
    "--timezone=America/New_York", "--lang=en-US", "--accept-lang=en-US,en",
    "https://demo.fingerprint.com/playground"
).start();
```

### Rust

```rust
Command::new(r"D:\ovobrowser-150\chrome.exe")
    .args([
        "--user-data-dir=D:\\ovobrowser-profiles\\rust",
        "--no-first-run", "--disable-quic",
        "--fingerprint-platform=windows", "--fingerprint-brand=Chrome",
        "--fingerprint-brand-version=150.0.7871.124",
        "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36",
        "--fingerprint-screen=1536x864", "--fingerprint-device-scale-factor=1.25",
        "--timezone=America/New_York", "--lang=en-US", "--accept-lang=en-US,en",
        "https://demo.fingerprint.com/playground",
    ])
    .spawn()?;
```

---

## Authenticated proxies

Chromium `--proxy-server` has **no user:pass**. Bridge locally:

```
browser → local unauthenticated SOCKS5 → (optional ladder :7890) → upstream
```

`--proxy-server=socks5://127.0.0.1:<bridge>` plus `--disable-quic`. Set timezone/lang **before** launch.

---

## Documentation

| Topic | English | 中文 |
|---|---|---|
| Complete flag reference | [FLAGS.md](docs/en/FLAGS.md) | [FLAGS.md](docs/zh/FLAGS.md) |
| Fingerprint surfaces and implementation | [FINGERPRINT.md](docs/en/FINGERPRINT.md) | [FINGERPRINT.md](docs/zh/FINGERPRINT.md) |
| Recommended launch recipes | [RECIPES.md](docs/en/RECIPES.md) | [RECIPES.md](docs/zh/RECIPES.md) |
| Repository structure | [STRUCTURE.md](docs/STRUCTURE.md) | — |

### Changelog

<details>
<summary><strong>Click to expand: kernel updates since v1.0.0 (2026-08-26 – 2026-10-20)</strong></summary>

<br>

<details>
<summary><strong>2026-10-20</strong> · 11 details aligned against a commercial fingerprint browser, plus Google homepage sign-in (138 / 144 / 150 / 155)</summary>

We compared our kernel side by side with a commercial fingerprint browser and genuine Chrome 155. The items below used to differ from genuine Chrome and could be detected. They now match:

- **`measureText` fix**: With noise flags such as `--fingerprint-font`, text widths could collapse to almost 0. Now only a tiny offset is applied.
- **WebGL parameters**: On an NVIDIA host spoofed as Intel / AMD, three parameters such as `MAX_VERTEX_UNIFORM_VECTORS` used to leak NVIDIA's 4095. They now report 4096 / 16384 / 212992 to match the spoofed vendor.
- **WebGPU vendor and architecture**: When the GPU is spoofed, `adapter.info` returns the same short names as genuine Chrome, such as `intel` / `gen-9`, `amd` / `rdna-2`, `nvidia` / `ampere`. It used to return `Google Inc. (Intel)` with an empty architecture.
- **WebGPU features**: Optional features are no longer hidden per seed. All features the host really supports are reported.
- **WebGL noise**: `readPixels`, `toDataURL` and `drawImage(webglCanvas)` now return identical results. Before, only `readPixels` was noised, so a simple cross-check exposed it.
- **Speech voices**: The 19 Google online voices that genuine Chrome ships are added (22 voices with the system ones), with names identical to genuine Chrome.
- **`outerWidth` / `outerHeight`**: Return the real window size. They used to equal the inner viewport, which a real browser never does. Only when the gap is abnormal (for example DevTools is open) do they fall back to "inner viewport + normal frame", so anti-debugging still works.
- **ClientRects noise**: Elements with integer coordinates no longer get fractional offsets. Genuine Chrome returns `10, 20`, never `9.9998, 19.9992`. Fractional coordinates are still noised.
- **Bookmark bar**: No longer shown permanently by default. The visible page height used to be 33px shorter than genuine Chrome. Now, as in genuine Chrome, it appears only on the New Tab page.
- **Widevine**: The portable builds bundle the Widevine component. `com.widevine.alpha` is available, so DRM video such as Netflix plays.
- **New flag `--fingerprint-max-touch-points=<0~10>`**: For desktop platforms. It sets `navigator.maxTouchPoints` and keeps `any-pointer: coarse` in sync. Pass `0` for a regular desktop. If omitted it follows the host, so a touchscreen laptop reports 10.
- **Google homepage sign-in**: After you sign in, the Google homepage opened in a new tab shows your avatar. It used to always show the "Sign in" button.

Verified: lies are 0 on all four kernels, and BrowserScan scores 100% with or without GPU spoofing.

</details>

<details>
<summary><strong>2026-10-18</strong> · AMD canvas warning, Google sign-in validation headers, deviceMemory (138 / 144 / 150 / 155)</summary>

- **AMD canvas warning**: With canvas noise on an AMD GPU, BrowserScan reported Canvas Tampering. The new canvas noise only flips the lowest alpha bit of semi-transparent anti-aliased edge pixels. It leaves RGB and solid areas untouched, and running the same image through it twice gives the same result. `getImageData`, `toDataURL`, `toBlob` and sub-region reads are consistent with each other.
- **Google sign-in validation headers**: Requests to Google domains now carry the four headers only genuine Chrome sends: `x-browser-channel / year / validation / copyright`. Values are picked by the UA major version and are byte-identical to genuine Chrome of the same version, which lowers the risk-control friction when signing in to Google.
- **deviceMemory**: `navigator.deviceMemory` and the `Sec-CH-Device-Memory` request header now report the same value. The header used to leak the real memory. Allowed ranges follow each genuine version: 138 / 144 use 0.25–8; 150 / 155 use 2–32 on desktop and 1–8 on mobile.

</details>

<details>
<summary><strong>2026-10-13</strong> · New 155 kernel</summary>

- New `155.0.8059.39` kernel, based on ungoogled-chromium 155, with exactly the same flags as 150.
- The 155 kernel scores 100% on BrowserScan. On FingerprintJS Pro, Bot, Tampering, DevTools, VM and Incognito are all Not detected, the same as 150.

</details>

<details>
<summary><strong>2026-10-09</strong> · Extensions install from the Chrome Web Store (138 / 144)</summary>

- Clicking "Add to Chrome" on the Chrome Web Store used to spin forever on 144 and show "This item is currently unavailable" on 138. Both now download and install normally.
- Background extension auto-update is still disabled; the browser does not contact Google on its own to check for extension updates.

</details>

<details>
<summary><strong>2026-10-07</strong> · Mobile device toolbar</summary>

- **Device toolbar**: With platform set to android / ios and `--fingerprint-screen` passed, a toolbar similar to the DevTools device mode appears at the top of the window. You can:
  - switch device presets or set a custom width and height;
  - rotate between portrait and landscape;
  - change the display scale;
  - set network throttling.
- **Phone view**: The phone view is centered and shrinks proportionally when the window is small. The page still sees the device viewport and DPR. It used to stick to the top-left corner and get cropped in small windows.

</details>

<details>
<summary><strong>2026-10-05</strong> · Mobile consistency fixes</summary>

- **CJK fonts**: On Android / iOS with `--fingerprint-font`, Chinese text no longer renders as boxes. CJK fonts such as Microsoft YaHei, SimSun and PingFang are kept.
- **Consistent platform info**: The page, Workers and network requests report the same platform. `userAgentData`, `Sec-CH-UA-Platform` and `Sec-CH-UA-Mobile` all switch to Android. iOS no longer sends Client Hints headers.
- **Touch, pointer and orientation**: On mobile, `maxTouchPoints` is 5, with `pointer: coarse` and `hover: none`. In portrait, `screen.orientation` is `portrait-primary`.
- **WebGL error**: After spoofing the GPU on mobile, BrowserScan no longer deducts for "WebGL exception".
- **New Tab page**: The New Tab page opens the Google homepage by default (it used to be blank), and Google no longer returns 404 under an Android UA.

</details>

<details>
<summary><strong>2026-08-26</strong> · Anti-debugging on by default</summary>

- `debugger` statements in pages (literals, `eval`, `new Function`) no longer pause the page by default. This stops sites from freezing the page with them or using them to detect DevTools.
- When you need to debug yourself, pass `--fingerprint-allow-debugger` to restore the native behavior.

</details>

</details>

---

## License

Docs/examples: [LICENSE](LICENSE) (MIT). Binaries: Chromium / ungoogled-chromium.

---

## Contact

- QQ group: `1108811142`
- Telegram: [t.me/ovobrowser_group](https://t.me/ovobrowser_group)
- Email: [support@ovobrowser.com](mailto:support@ovobrowser.com)

---

## Star History

<a href="https://www.star-history.com/#ovobrowsersupport/ovobrowser&Date">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=ovobrowsersupport/ovobrowser&type=Date&theme=dark" />
    <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=ovobrowsersupport/ovobrowser&type=Date" />
    <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=ovobrowsersupport/ovobrowser&type=Date" width="600" />
  </picture>
</a>
