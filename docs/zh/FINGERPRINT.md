# ovobrowser 指纹修改详情

本文汇总三套内核（138 / 144 / 150）相对上游 Chromium / ungoogled-chromium **实际改过的指纹能力**。
开关级用法、取值、默认行为见 [FLAGS.md](FLAGS.md)。英文版：[FINGERPRINT.md](../en/FINGERPRINT.md)。

规则：**不传开关 = 用真机/上游默认**；**传入 = 按你给的值伪装或加噪**。

---

## 1. 产品层（与检测站 UA 解耦）

内核把对外产品名从 `Chromium` 改为 `ovobrowser`，覆盖：

- 任务管理器 / exe 属性 / AppUserModelID
- `chrome://version` 顶部产品名与字标
- 菜单「关于」、设置页文案（200+ 语言翻译 ID 已重配对）
- 默认用户数据目录：`%LOCALAPPDATA%\ovobrowser\User Data`

**故意没改的：**

- `navigator.userAgent` 与 Client Hints 品牌仍是 Chrome / Chromium / GREASE
- 法律与版权行仍归属 The Chromium Authors

改 UA 品牌会立刻被判未知浏览器，指纹伪装归零。

---

## 2. 分类指纹噪声（5 类独立）

实现位置：渲染进程对 Canvas / WebGL / Audio / ClientRects / 字体度量插入可复现噪声。

| 开关 | 改动的 JS / 像素面 | 不传 |
|---|---|---|
| `--fingerprint-canvas[=种子]` | `toDataURL` / `getImageData` / `measureText` | 原生 Canvas |
| `--fingerprint-webgl[=种子]` | WebGL `readPixels` | 原生 WebGL 读回 |
| `--fingerprint-audio[=种子]` | AudioContext 波形 / 采样率统计 | 原生音频 |
| `--fingerprint-rects[=种子]` | `getClientRects` / `getBoundingClientRect` 亚像素 | 原生几何 |
| `--fingerprint-font[=种子]` | 字体度量与可用字体列表 | 原生字体 |

行为：

- 裸开关：本次启动随机种子，**同一次运行跨标签一致**
- `=数字`：固定种子，档案可复现
- `--fingerprint-random`：五类同时打开（各随机种子）
- `--fingerprint=<数字>`：仅作分类开关缺省种子回退，**单独传不再触发噪声**

版本差：

- 138：audio 仅帧数微扰，无采样率噪声；canvas 主线程 vs Worker 未对齐
- 144 / 150：audio 完整；canvas 主线程与 Worker 噪声一致

**FingerprintJS Pro：** 开噪声或 GPU 串伪装 → 易报 Browser Tampering。要全绿就不要开这五类和 `--fingerprint-gpu-*`。

---

## 3. Navigator / UA-CH / 硬件画像

| 开关 | 改什么 |
|---|---|
| `--user-agent=` | `navigator.userAgent` + 请求头 UA。版本位必须 `主版本.0.0.0` |
| `--fingerprint-brand=` | UA-CH `brands` |
| `--fingerprint-brand-version=` | UA-CH **完整补丁号**（`fullVersionList`） |
| `--fingerprint-platform=` | `navigator.platform` + UA-CH platform：`windows` / `macos` / `linux` / `android` / `ios` |
| `--fingerprint-platform-version=` | UA-CH `platformVersion`（Win11 用 ≥ `13.0.0`，UA 里仍写 `Windows NT 10.0`） |
| `--fingerprint-hardware-concurrency=` | `navigator.hardwareConcurrency` |
| `--fingerprint-device-memory=` | `navigator.deviceMemory`（0.25/0.5/1/2/4/8） |
| `--fingerprint-dnt=` | `navigator.doNotTrack` |
| `--fingerprint-battery=` | `getBattery()` 四字段 `c,l,ct,dt` |
| `--fingerprint-disable-speech-voices` | `speechSynthesis.getVoices()` 返回空 |

GREASE 品牌串由内核按主版本用 Chromium 原生算法生成，不必手写。

`platform=ios` 时自动隐藏 `navigator.userAgentData`（对齐真机 Safari）。

---

## 4. 屏幕与 DPR（必须成对）

| 开关 | 改什么 |
|---|---|
| `--fingerprint-screen=宽x高` | `screen.width/height/avail*`，填的是 **CSS 逻辑像素** |
| `--fingerprint-device-scale-factor=` | `devicePixelRatio`、CSS `resolution` 媒体查询、`Sec-CH-DPR` |
| `--fingerprint-screen-color-depth=` | `colorDepth` / `pixelDepth` |
| `--fingerprint-screen-width=` / `-height=` | 144/150 历史分量写法，等价于 screen |

检测站显示的「物理分辨率」= `screen.width × devicePixelRatio`。

只传 screen 不传 DPR → 用宿主机真实缩放去乘，会算出不存在的分辨率，CreepJS 交叉校验必抓。

常见真机搭配见参数手册 3.1 节。macOS 只有 DPR `1` 或 `2`；Windows 常见 `1/1.25/1.5/1.75/2/2.25`，不要编 `1.33`。

---

## 5. GPU / WebGPU / 蓝牙 / WebRTC

| 开关 | 改什么 |
|---|---|
| `--fingerprint-gpu-vendor=` | WebGL `UNMASKED_VENDOR_WEBGL` |
| `--fingerprint-gpu-renderer=` | WebGL `UNMASKED_RENDERER_WEBGL` |
| `--fingerprint-webgpu=disable` | `navigator.gpu = null` |
| `--fingerprint-disable-bluetooth` | `navigator.bluetooth = null` |
| `--webrtc-ip-handling-policy=` | ICE 候选；推荐 `disable_non_proxied_udp`（默认即此，防内网 IP） |

vendor 与 renderer 必须是同一块真实 GPU 的成套字符串，乱配会被判 tampering / 虚拟机。
移动端 UA 配桌面 RTX + D3D11 同理。

---

## 6. 时区 / 语言

| 开关 | 改什么 |
|---|---|
| `--timezone=` | JS `Intl` / `Date` IANA 时区 |
| `--lang=` | UI 语言 + `navigator.language` + `Intl` 默认 locale |
| `--accept-lang=` | 请求头 `Accept-Language` + `navigator.languages`（**不要带 q=**） |

必须与**出口 IP** 对齐，否则 BrowserScan：

- Different time zones −10%
- Language mismatch −10%（只改 accept-lang 不改 lang 时，中文系统会漏 `zh-CN`）

---

## 7. 行为类与其它内核开关

| 开关 | 作用 |
|---|---|
| `--blink-settings=imagesEnabled=false` | 不加载图片 |
| `--max-image-size-kb=` | 按 Content-Length 丢弃大图 |
| `--autoplay-policy=document-user-activation-required` | 禁自动播放 |
| `--mute-audio` | 全局静音 |
| `--disable-save-password` | 关保存密码气泡（默认会保存，已从 ungoogled 的 false 改回 true） |
| `--block-notifications` | 只拒通知 |
| `--deny-permission-prompts` | 拒全部权限弹窗 |
| `--disable-quic` | SOCKS 代理场景必须关，否则 https 易 `ERR_SSL_PROTOCOL_ERROR` |

地址栏默认搜索已从 ungoogled 的「No Search」改回 Google，并去掉 `trk:` 拦截前缀；旧 profile 会随引擎表版本号自动刷新。

---

## 8. 一致性修复（无开关，默认生效）

- getClientRects / getBoundingClientRect 噪声跨调用一致
- 144/150：Canvas 主线程与 Worker 噪声一致
- UA / UA-CH 与真实内核主版本自洽

---

## 9. 调用面

内核只吃 **命令行开关**。任意语言用创建进程即可，见 `examples/`。

Chromium `--proxy-server` **不支持用户名密码**。住宅代理带认证时：

```
浏览器 → 本地无认证 SOCKS5 桥 →（可选）本机梯子 7890 → 上游认证代理
```

时区/语言应在启动前按出口 IP geoip 填好；启动后再改 `--timezone` 无效，只能重启进程。

---

## 10. 检测站实测结论（摘要）

- **FingerprintJS Pro 全绿：** 不开五类噪声、不开 GPU 串伪装；硬件/屏幕/时区语言仍可改。副作用：真机指纹稳定，换 IP 仍可能被 Velocity 串成同一 visitor。
- **BrowserScan 100%：** UA 缩减形式 + brand-version 完整号；screen+DPR 成对；lang+accept-lang+timezone 对齐出口 IP。噪声对 BrowserScan 不一定扣分，但对 FingerprintJS 会扣 Tampering。
- 住宅代理 IP 段可能被标 IP Blocklist，与内核指纹无关。
