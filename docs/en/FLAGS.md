# ovobrowser kernel launch flags

Chinese: [FLAGS.md](../zh/FLAGS.md)

Documents every extra flag on the three self-built kernels (**138 / 144 / 150**): what it changes, example values, and the default if omitted. Fingerprint patches, product icon, and OS spoofing are the same across kernels; differences are a few legacy switches and audio-noise depth.

---

## 1. Kernel overview

| Kernel | Full version | Baseline | Portable zip |
|---|---|---|---|
| **138** | `138.0.7204.183` | fingerprint-chromium 138 (ungoogled) | `ovobrowser-138-138.0.7204.183-win64-portable.zip` |
| **144** | `144.0.7559.132` | ungoogled 144 | `ovobrowser-144-144.0.7559.132-win64-portable.zip` |
| **150** | `150.0.7871.124` | ungoogled 150 | `ovobrowser-150-150.0.7871.124-win64-portable.zip` |

All three include:

- Independent noise: canvas / audio / webgl / rects / font
- Extra fingerprints: deviceMemory / screen / colorDepth / DNT / battery / speechVoices
- WebGL vendor/renderer spoof
- Hide WebGPU (`--fingerprint-webgpu=disable` → `navigator.gpu=null`)
- Hide Bluetooth (`--fingerprint-disable-bluetooth` → `navigator.bluetooth=null`)
- WebRTC IP policy (`--webrtc-ip-handling-policy`)
- Behavior flags (images, autoplay, mute, save-password, notifications, random fingerprint)
- `navigator.platform` / UA-CH platform spoof (including Android / iOS); iOS hides `navigator.userAgentData`
- ClientRects consistency; (144/150) canvas main-thread vs Worker consistency
- UA / UA-CH aligned with the real kernel version

### Product name is ovobrowser (no flag required)

| Surface | Before | After |
|---|---|---|
| Task Manager / exe properties | Chromium | **ovobrowser** |
| `chrome://version` | Chromium 150.0.7871.124 | **ovobrowser** 150.0.7871.124 |
| About / Settings | Chromium | ovobrowser |
| AppUserModelID | Chromium | ovobrowser |
| Default user-data dir | `%LOCALAPPDATA%\Chromium\User Data` | `%LOCALAPPDATA%\ovobrowser\User Data` |

**UA and Client Hints are intentionally still Chrome/Chromium.** Renaming those would be detected as an unknown browser.

If you previously launched without `--user-data-dir`, copy `%LOCALAPPDATA%\Chromium\User Data` to the ovobrowser directory.

Legal copy still credits The Chromium Authors.

---

## 2. Category noise

Pass the flag = noise on; omit = native output.

| Flag | Effect | On | Off |
|---|---|---|---|
| `--fingerprint-canvas[=seed]` | Canvas 2D pixels / `measureText` | Randomized (fixed if seeded) | Native |
| `--fingerprint-webgl[=seed]` | WebGL `readPixels` | Randomized | Native |
| `--fingerprint-audio[=seed]` | AudioContext stats | Randomized | Native |
| `--fingerprint-rects[=seed]` | ClientRects sub-pixel offset | Randomized | Native |
| `--fingerprint-font[=seed]` | Font metrics / list | Randomized | Native |

- Bare flag: random seed for this process, consistent across tabs
- `=8842`: reproducible seed
- `--fingerprint-random`: all five at once
- `--fingerprint=<n>`: fallback seed only; does not enable noise by itself

| Class | 138 | 144 | 150 |
|---|---|---|---|
| canvas / webgl / rects / font | yes | yes | yes |
| audio | frame-count only | frame + sample rate | frame + sample rate |
| canvas main/Worker match | no | yes | yes |

Turning noise on is the usual FingerprintJS Pro “Browser Tampering” trigger.

---

## 3. Common flags (all kernels)

Omit = real machine / default. Pass = spoof.

| Flag | JS / network field | Example | If omitted |
|---|---|---|---|
| category noise | see §2 | `--fingerprint-canvas=8842` | native |
| `--fingerprint=<n>` | fallback seed | `20260720` | each class picks its own |
| `--user-agent=` | UA string + header | see warning | kernel UA |
| `--fingerprint-brand=` | UA-CH brands | `Chrome` | Chromium / Google Chrome |
| `--fingerprint-brand-version=` | **full** patch in UA-CH | `150.0.7871.124` | kernel version |
| `--fingerprint-platform=` | platform + UA-CH | `windows` / `macos` / `linux` / `android` / `ios` | real OS |
| `--fingerprint-platform-version=` | UA-CH platformVersion | `10.0.0` | real |
| `--fingerprint-hardware-concurrency=` | hardwareConcurrency | `8` | real cores |
| `--fingerprint-device-memory=` | deviceMemory | `0.25/0.5/1/2/4/8` | default `8` |
| `--fingerprint-screen=` | screen W×H (CSS px) | `1920x1080` | real screen |
| `--fingerprint-screen-color-depth=` | colorDepth | `24` | real |
| `--fingerprint-device-scale-factor=` | DPR / CSS resolution / `Sec-CH-DPR` | `1.25` | **host** scale (leaks the machine) |
| `--fingerprint-dnt=` | doNotTrack | `1` / `0` / `unspecified` | `null` |
| `--fingerprint-battery=` | getBattery | `1,1.0,0,Infinity` | real battery |
| `--fingerprint-disable-speech-voices` | empty voice list | flag only | real voices |
| `--fingerprint-gpu-vendor=` | UNMASKED_VENDOR_WEBGL | `Qualcomm` | real vendor |
| `--fingerprint-gpu-renderer=` | UNMASKED_RENDERER_WEBGL | Adreno/ANGLE string | real renderer |
| `--fingerprint-webgpu=disable` | `navigator.gpu=null` | flag only | real WebGPU |
| `--fingerprint-disable-bluetooth` | `navigator.bluetooth=null` | flag only | real |
| `--webrtc-ip-handling-policy=` | ICE IPs | `disable_non_proxied_udp` | same (kernel default) |
| `--timezone=` | Intl / Date | `Asia/Tokyo` | host zone |
| `--lang=` | UI + `navigator.language` | `en-US` | host language |
| `--accept-lang=` | Accept-Language + `navigator.languages` | `en-US,en` (**no `q=`**) | host |

### UA must use the reduced form

Real Chrome UA Reduction reports only `MAJOR.0.0.0` in UA; the full patch lives in Client Hints.

| UA version | `--fingerprint-brand-version` | BrowserScan |
|---|---|---|
| `150.0.7871.124` | same | Different browser version −5% |
| `150.0.0.0` | `150.0.7871.124` | 100% |

Correct:

```
--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36
--fingerprint-brand=Chrome
--fingerprint-brand-version=150.0.7871.124
```

- UA major and brand-version major must match
- Keep `Windows NT 10.0` even on Win11; Win11 is `platform-version` ≥ `13.0.0`
- Prefer the kernel’s real major (150). Other majors can fool BrowserScan’s UA check but TLS/JS still reveal the binary

GREASE (`Not;A=Brand`) is generated automatically.

### DPR must be paired with screen

`--fingerprint-screen` is **logical CSS pixels** = physical ÷ scale. 1920×1080 laptop at 125% is `1536x864` + DPR `1.25`, not `1920x1080`.

| `--fingerprint-screen` | `--fingerprint-device-scale-factor` | Hardware |
|---|---|---|
| `1920x1080` | `1` | 1080p @100% |
| `1536x864` | `1.25` | 1080p laptop @125% (most common) |
| `1280x720` | `1.5` | 1080p @150% |
| `2560x1440` | `1` | 1440p @100% |
| `2048x1152` | `1.25` | 1440p laptop @125% |
| `1366x768` | `1` | old 1366 panel |
| `1920x1080` | `2` | 4K @200% |
| `1280x800` | `2` | MacBook Pro 13" Retina |
| `1512x982` | `2` | MacBook Pro 14" |
| `1728x1117` | `2` | MacBook Pro 16" |

macOS only `1` or `2`. Windows uses `1/1.25/1.5/1.75/2/2.25`. Do not invent `1.33`.

Mobile: iPhone DPR `3`, Pixel `2.625`.

This flag does **not** resize the window (unlike Chromium `--force-device-scale-factor`).

Console check:

```js
console.table({
  logical: `${screen.width}x${screen.height}`,
  dpr: devicePixelRatio,
  physical: `${screen.width * devicePixelRatio}x${screen.height * devicePixelRatio}`,
  media: matchMedia(`(resolution: ${devicePixelRatio}dppx)`).matches,
});
```

---

## 4. WebRTC / WebGPU / Bluetooth / geolocation

| Capability | How |
|---|---|
| WebRTC | `--webrtc-ip-handling-policy=disable_non_proxied_udp` |
| WebGPU hide | `--fingerprint-webgpu=disable` |
| Bluetooth hide | `--fingerprint-disable-bluetooth` |
| Geolocation | launcher-level (CDP / Playwright), not a kernel flag |
| Device name / MAC | not exposed to web JS; no kernel flag |

---

## 5. Behavior flags

| Ability | Flag | If omitted |
|---|---|---|
| Block images | `--blink-settings=imagesEnabled=false` | load images |
| Max image KB | `--max-image-size-kb=300` | unlimited |
| Block autoplay | `--autoplay-policy=document-user-activation-required` | allow |
| Mute | `--mute-audio` | sound on |
| Disable translate | kernel default off | — |
| Disable save-password | `--disable-save-password` | save-password **on** by default |
| Block notifications | `--block-notifications` | prompt |
| Deny all permissions | `--deny-permission-prompts` | prompt |
| Random all noise | `--fingerprint-random` | per-class flags |
| Persist cookies/passwords | `--user-data-dir=...` | temp profile |

Address-bar search is restored to Google (ungoogled “No Search” / `trk:` prefix removed).

`--proxy-server` does **not** accept user:pass. Use a local unauthenticated SOCKS bridge.

---

## 6. Per-version notes

- 138: all flags above; audio noise is shallower
- 144 / 150: same set; extra `--fingerprint-screen-width` / `-height`
- 150 scores best on FingerprintJS ML (older kernels look like anti-detect browsers)

`--fingerprint-device-scale-factor` works on all three (early builds ignored it).

---

## 7. Recipes

### A. FingerprintJS Pro not detected

No noise, no GPU strings:

```
--fingerprint-platform=windows
--fingerprint-brand=Chrome
--fingerprint-platform-version=10.0.0
--fingerprint-hardware-concurrency=8
--fingerprint-device-memory=8
--fingerprint-screen=1536x864
--fingerprint-device-scale-factor=1.25
--fingerprint-screen-color-depth=24
--fingerprint-battery=1,1.0,0,Infinity
--timezone=<exit-IP-zone>
```

### B. Low traffic

```
--blink-settings=imagesEnabled=false
--max-image-size-kb=300
--autoplay-policy=document-user-activation-required
--mute-audio
--block-notifications
--disable-save-password
--user-data-dir=D:\profiles\acc01
```

### C. Android Pixel 7

```
--fingerprint-platform=android
--fingerprint-screen=412x915
--fingerprint-device-scale-factor=2.625
--fingerprint-gpu-vendor=Qualcomm
--fingerprint-gpu-renderer=ANGLE (Qualcomm, Adreno (TM) 730, OpenGL ES 3.2)
```

### D. iOS iPhone 14 Pro

```
--fingerprint-platform=ios
--fingerprint-screen=393x852
--fingerprint-device-scale-factor=3
--fingerprint-gpu-vendor=Apple Inc.
--fingerprint-gpu-renderer=Apple GPU
```

### E. BrowserScan 100%

```
--user-data-dir=D:\profiles\acc01
--no-first-run --no-default-browser-check
--disable-features=Translate
--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36
--fingerprint-brand=Chrome
--fingerprint-brand-version=150.0.7871.124
--fingerprint-platform=windows
--fingerprint-platform-version=10.0.0
--lang=en-SG
--accept-lang=en-SG,en
--timezone=Asia/Singapore
--fingerprint-hardware-concurrency=12
--fingerprint-device-memory=4
--fingerprint-screen=1536x864
--fingerprint-screen-color-depth=24
--fingerprint-device-scale-factor=1.25
--webrtc-ip-handling-policy=disable_non_proxied_udp
```

Pitfalls: reduced UA; both lang flags; no `q=`; paired screen+DPR; timezone/lang match exit IP; do not duplicate flags.

---

## 8. Notes

1. Noise / GPU strings help uniqueness (CreepJS) but FingerprintJS Pro marks Tampering. Pick one goal.
2. Align `--timezone`, `--lang`, `--accept-lang` with the exit IP. Pass **both** lang flags. Never put `q=` in `--accept-lang`.
3. Custom UA must use `MAJOR.0.0.0`.
4. Platform, UA, UA-CH, GPU strings, and DPR must describe the same device class.
