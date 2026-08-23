# ovobrowser 指纹内核 · 启动参数说明

英文版：[FLAGS.md](../en/FLAGS.md)

> 本文档说明三套自编译内核（**138 / 144 / 150**）在启动时可以插入哪些参数、
> 每个参数改什么、示例取值、**不传时的默认行为**，并按版本标注差异。
> 三套内核的指纹改动、产品图标、系统版本伪装均保持一致，差异只在个别历史开关与 audio 噪声深度。

---

## 一、三套内核总览

| 内核 | 完整版本号 | 基线 | 便携版 zip |
|---|---|---|---|
| **138** | `138.0.7204.183` | fingerprint-chromium 138（ungoogled）| `ovobrowser-138-138.0.7204.183-win64-portable.zip` |
| **144** | `144.0.7559.132` | CloakBrowser / ungoogled 144 | `ovobrowser-144-144.0.7559.132-win64-portable.zip` |
| **150** | `150.0.7871.124` | CloakBrowser / ungoogled 150 | `ovobrowser-150-150.0.7871.124-win64-portable.zip` |

> 压缩包名已随产品改名从 `CloakBrowser-*` 换成 `ovobrowser-*`；旧包仍留在
> `release` 目录里没删，需要回退对比时可以直接用。

三套都内置：

- **分类指纹噪声开关**（canvas / audio / webgl / rects / font，各自独立）
- 6 大扩展指纹开关（deviceMemory / screen / colorDepth / DNT / battery / speechVoices）
- WebGL vendor/renderer 字符串伪装
- **WebGPU 隐藏**（`--fingerprint-webgpu=disable` → `navigator.gpu=null`）
- **蓝牙隐藏**（`--fingerprint-disable-bluetooth` → `navigator.bluetooth=null`）
- **WebRTC IP 策略**（`--webrtc-ip-handling-policy`，防内网 IP 泄露）
- **浏览器行为类开关**（禁图片 / 图片大小上限 / 禁自动播放 / 静音 / 禁保存密码 / 禁通知 / 随机指纹）
- `navigator.platform` / UA-CH 平台伪装（含移动端 Android / iOS）；iOS 隐藏 `navigator.userAgentData`
- getClientRects / getBoundingClientRect 噪声一致性修复；（144/150）canvas 主线程 vs Worker 一致性修复
- 版本号自洽（UA / UA-CH 与真实内核版本一致，避免 BrowserScan 报版本不符）

### 产品名已改为 ovobrowser（三套内核均已生效，无需任何启动参数）

内核层面把产品名从 `Chromium` 改成了 `ovobrowser`，改完的地方：

| 位置 | 改动前 | 改动后 |
|---|---|---|
| 任务管理器进程名 / exe 右键属性 | Chromium | **ovobrowser** |
| `chrome://version` 顶部产品名 | Chromium 150.0.7871.124 | **ovobrowser** 150.0.7871.124 |
| 菜单「帮助 → 关于」、设置页标题 | 关于 Chromium | **关于 ovobrowser** |
| 设置页里所有提到浏览器名的文案 | …Chromium… | …**ovobrowser**… |
| 任务栏分组用的 AppUserModelID | Chromium | ovobrowser |
| 文件关联显示名 | Chromium HTML Document | ovobrowser HTML Document |
| 默认用户数据目录 | `%LOCALAPPDATA%\Chromium\User Data` | `%LOCALAPPDATA%\ovobrowser\User Data` |
| `chrome://version` 右上角字标图 | 圆标 + chromium | 圆标 + **ovobrowser** |
| 设置「关于」页卡片里的字标 | 圆标 + chromium | 圆标 + **ovobrowser** |

字标是「圆形图标 + 文字」烧在一起的位图（`product_logo*.png`、
`product_logo_name_22*.png`，各有 100% / 200% / 深色 / 浅色四份），改字符串改不到，
已单独重绘：圆形图标原封不动搬过来，只把右侧文字换成 ovobrowser，字号、灰度
(`#5F6368`)、画布尺寸都跟原图一致，所以版本页排版没有任何变化。

**⚠️ 三件必须知道的事**

1. **UA 和 Client Hints 刻意没改**，仍然是 `Chrome/<版本>` 和
   `Chromium / Google Chrome / Not;A=Brand`。这两处在内核里本来就是硬编码的、
   跟产品名解耦，改了会立刻被所有检测站识别成"未知浏览器"，指纹伪装直接归零。
   即改名**完全不影响**已有的指纹参数和 BrowserScan / FingerprintJS 得分。
   实测：改名后 `navigator.userAgent` 仍为
   `…Chrome/150.0.0.0 Safari/537.36`，`--fingerprint-brand` 覆盖照常生效。

2. **默认用户数据目录名跟着变了**。如果之前有窗口是靠"不传 `--user-data-dir`"
   用默认目录跑的，改名后会到新目录去、看起来像"登录状态全丢了"——老数据还在
   `%LOCALAPPDATA%\Chromium\User Data`，把它整个复制到 `ovobrowser` 目录下即可。
   显式传 `--user-data-dir` 的启动方式不受影响。

3. **200+ 种语言的翻译都同步跟上了**。grit 的翻译是按"英文原文指纹"匹配的，
   只改英文原文会让中文/日文界面里几百条设置文案退回英文（既难看，也是个
   指纹不一致点）。这里在改名前后各导出一次消息指纹、按内容配对重算了
   翻译 ID，实测中/日/德三语的"关于 ovobrowser / ovobrowser について /
   Über ovobrowser"都能正确显示。

4. **法律与上游归属文案保留 Chromium**，这是故意的：版权行仍是
   "版权所有 The Chromium Authors"，关于页仍是"ovobrowser 的诞生离不开
   **Chromium** 开放源代码项目"。这里指的是上游开源项目本身，跟着改名会变成
   "ovobrowser 的诞生离不开 ovobrowser 开源项目"这种语义错误，也不符合许可要求。

---

## 二、分类指纹噪声开关

canvas / audio / webgl / rects / font **5 个独立开关**，各自互不影响。规则统一：
**传入该开关 = 该类插入噪声（随机化）；不传 = 该类保持系统原生输出（本地真实值，足够用）**。

| 参数 | 作用（JS 可见影响）| 传入=？ | 不传=？ |
|---|---|---|---|
| `--fingerprint-canvas[=种子]` | Canvas 2D `toDataURL`/`getImageData`/`measureText` 像素与文字度量噪声 | 该类**随机化**（带种子则固定复现）| Canvas 原生输出 |
| `--fingerprint-webgl[=种子]` | WebGL `readPixels` 像素读回噪声 | 该类随机化 | WebGL 原生输出 |
| `--fingerprint-audio[=种子]` | AudioContext 波形/采样率统计噪声 | 该类随机化 | 音频原生输出 |
| `--fingerprint-rects[=种子]` | `getClientRects`/`getBoundingClientRect` 亚像素偏移 | 该类随机化 | 几何原生输出 |
| `--fingerprint-font[=种子]` | 字体度量/可用字体列表噪声 | 该类随机化 | 字体原生输出 |

规则说明：

- **裸开关**（如 `--fingerprint-canvas`，不带值）：浏览器进程生成一个「本次启动随机、全会话一致」
  的种子并下发给所有渲染进程 → 每次启动画布指纹都不同，但同一次运行内跨标签/子帧一致。
- **带种子**（如 `--fingerprint-canvas=8842`）：用固定种子，指纹可复现（同一档案想长期稳定用这个）。
- **不传**：该类完全不加噪声，输出与原生 Chromium 一致（用于 FingerprintJS 全绿场景）。
- 各类互不影响：只开 `--fingerprint-canvas` 时，rects/audio/font 保持原生。
- 三套内核（138 / 144 / 150）均已支持这 5 个分类开关，用法完全一致。
- 一键随机：`--fingerprint-random` 等价于同时打开全部 5 类（各用随机种子），见第五节。

**各版本噪声支持差异**：

| 噪声类 | 138 | 144 | 150 |
|---|---|---|---|
| canvas | 支持 | 支持 | 支持 |
| webgl（readPixels）| 支持 | 支持 | 支持 |
| rects | 支持 | 支持 | 支持 |
| font | 支持 | 支持 | 支持 |
| audio | 仅帧数微扰（无采样率噪声）| 完整（帧数+采样率）| 完整（帧数+采样率）|
| canvas 主线程/Worker 一致性 | 无该修复 | 有 | 有 |

---

## 三、通用指纹参数（138 / 144 / 150 全部支持）

> 规则：**不传 = 用真机 / 默认值**；**传了 = 按你给的值伪装**。

| 参数 | 改什么（JS 可见字段）| 示例值 | 不传的效果 |
|---|---|---|---|
| `--fingerprint-canvas` / `-webgl` / `-audio` / `-rects` / `-font` | **分类噪声开关**（见上一节）| `--fingerprint-canvas=8842` | 该类不加噪声，原生输出 |
| `--fingerprint=<数字种子>` | 分类开关缺省种子的回退来源（旧全局开关，单独传不再触发噪声）| `--fingerprint=20260720` | 分类开关自行取随机/固定种子 |
| `--user-agent=<UA串>` | `navigator.userAgent` + 请求头 `User-Agent` | 见下方 ⚠️ | 用内核自带 UA |
| `--fingerprint-brand=<品牌>` | UA-CH `brands` 品牌名 | `--fingerprint-brand=Chrome` | 默认 Chromium / Google Chrome 品牌 |
| `--fingerprint-brand-version=<完整版本>` | UA-CH 的完整版本号（`fullVersionList` / `sec-ch-ua-full-version-list`）。**这里才放完整补丁号** | `--fingerprint-brand-version=150.0.7871.124` | 用内核自带版本 |
| `--fingerprint-platform=<平台>` | `navigator.platform` + UA-CH platform | `windows` / `macos` / `linux` / `android` / `ios` | 用真实操作系统（Win32）|
| `--fingerprint-platform-version=<版本>` | UA-CH `platformVersion` | `--fingerprint-platform-version=10.0.0` | 用真实系统版本 |
| `--fingerprint-hardware-concurrency=<核数>` | `navigator.hardwareConcurrency` | `--fingerprint-hardware-concurrency=8` | 用真机 CPU 逻辑核数 |
| `--fingerprint-device-memory=<GB>` | `navigator.deviceMemory` | `0.25/0.5/1/2/4/8` | 默认 `8`（Chromium 上限）|
| `--fingerprint-screen=<宽x高>` | `screen.width/height/availWidth/availHeight` | `--fingerprint-screen=1920x1080` | 用真实屏幕分辨率 |
| `--fingerprint-screen-color-depth=<位>` | `screen.colorDepth / pixelDepth` | `--fingerprint-screen-color-depth=24` | 用真实色深（通常 24）|
| `--fingerprint-device-scale-factor=<倍率>` | `window.devicePixelRatio`、CSS `@media (resolution)` / `matchMedia`、请求头 `Sec-CH-DPR`。**必须和 `--fingerprint-screen` 配成真实存在的组合**，见下方 ⚠️ | `--fingerprint-device-scale-factor=1.25` | 用宿主机真实缩放（换台机器就变，会泄露真机并导致分辨率组合不真实）|
| `--fingerprint-dnt=<值>` | `navigator.doNotTrack` | `1` / `0` / `unspecified` | 返回 `null`（未指定）|
| `--fingerprint-battery=<c,l,ct,dt>` | `getBattery()` 四字段 | `--fingerprint-battery=1,1.0,0,Infinity` | 返回真实电量曲线（笔记本会暴露）|
| `--fingerprint-disable-speech-voices` | 让 `speechSynthesis.getVoices()` 返回空 | 传入即生效（无值）| 返回真实语音列表（一条较强指纹）|
| `--fingerprint-gpu-vendor=<串>` | WebGL `UNMASKED_VENDOR_WEBGL` | `--fingerprint-gpu-vendor=Qualcomm` | 用真实 GPU 厂商。⚠️与真机 WebGL 能力不符会被判 tampering |
| `--fingerprint-gpu-renderer=<串>` | WebGL `UNMASKED_RENDERER_WEBGL` | `ANGLE (Qualcomm, Adreno (TM) 730, OpenGL ES 3.2)` | 用真实 GPU 渲染器 |
| `--fingerprint-webgpu=disable` | 隐藏 WebGPU：`navigator.gpu` 返回 `null` | 传入即生效（无值）| `navigator.gpu` 正常存在（暴露 GPU 适配器信息）|
| `--fingerprint-disable-bluetooth` | 隐藏蓝牙：`navigator.bluetooth` 返回 `null` | 传入即生效（无值）| `navigator.bluetooth` 正常存在 |
| `--webrtc-ip-handling-policy=<策略>` | WebRTC ICE 候选的 IP 暴露策略（防内网 IP 泄露）| `disable_non_proxied_udp`（推荐）/ `default_public_interface_only` / `default` | 默认 `disable_non_proxied_udp` |
| `--timezone=<IANA时区>` | JS `Intl` / `Date` 时区 | `--timezone=Asia/Tokyo` | 用系统时区（易与代理 IP 不符）|
| `--lang=<语言>` | **浏览器界面/系统显示语言**，同时决定 JS `navigator.language`（单个主语言值）| `--lang=en-US` | 用系统语言 |
| `--accept-lang=<语言列表>` | **插入网络请求头 `Accept-Language`**（服务器据此返回对应语言页面），同时影响 `navigator.languages`（语言列表）。⚠️**只给逗号分隔的语言标签，绝对不要自己带 `q=` 权重**，权重由内核生成 | `--accept-lang=en-US,en` | 用系统默认请求语言 |

### ⚠️ `--user-agent` 版本号必须写成「缩减形式」

真实 Chrome 自 **UA Reduction** 起，UA 里的版本位**永远只报 `主版本.0.0.0`**，完整补丁号只出现在
Client Hints（`sec-ch-ua-full-version-list`）。所以 UA 里写完整补丁号，等于自报"我改过 UA"。

BrowserScan 会直接扣分并给出原文提示：

> **Different browser version −5%**
> *The browser version set by your browser does not match your actual browser version.
> It looks like you changed the UserAgent*

实测过的五种组合（150 内核 + 已对齐的时区/语言，其余条件相同）：

| UA 里的版本位 | `--fingerprint-brand-version` | BrowserScan 结果 |
|---|---|---|
| `150.0.7871.124`（完整号）| 150.0.7871.124 | ❌ Different browser version −5% |
| `151.0.7922.47`（完整号）| 151.0.7922.47 | ❌ Different browser version −5% |
| `150.0.0.0` | 150.0.7871.124 | ✅ 100%，零扣分 |
| `150.0.0.0` | 150.0.7871.182 | ✅ 100%，零扣分 |
| `151.0.0.0` | 151.0.7922.47 | ✅ 100%，零扣分 |

结论：**只要 UA 写完整补丁号就红，只要写 `主版本.0.0.0` 就绿，与报的是哪个主版本无关。**

正确写法（推荐：主版本用内核真实版本）：

```
--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36
--fingerprint-brand=Chrome
--fingerprint-brand-version=150.0.7871.124
```

想伪装成别的主版本（实测同样满分，把两处主版本一起换）：

```
--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36
--fingerprint-brand=Chrome
--fingerprint-brand-version=151.0.7922.47
```

三条硬性约束：

1. **两处主版本必须一致**。UA 写 151 就要配 `--fingerprint-brand-version=151.x.x.x`，否则 UA 与
   Client Hints 自相矛盾，比不改更容易被抓。
2. **`Windows NT` 后面固定写 `10.0`**，不要写 11。真实 Chrome 在 Win11 上 UA 也是 `Windows NT 10.0`
   （同属 UA Reduction 的一部分），Win11 只体现在 `--fingerprint-platform-version`（13.0.0 及以上）。
3. **建议主版本就用内核真实主版本**。BrowserScan 只校验 UA 格式，所以报别的主版本也满分；但更严格的
   检测站会用 JS 特性支持情况、TLS/HTTP2 指纹反推真实内核版本，这些由二进制本身决定、改不了。

> UA-CH 的 GREASE 品牌（那个 `"Not;A=Brand"` 假品牌）无需手工干预：内核按主版本用 Chromium 原生算法
> 推导，品牌串、版本号、排列顺序都会自动与真实 Chrome 同版本一致。例如报 150 时自动生成
> `"Not;A=Brand";v="8"` 且顺序为 `[GREASE, Chromium, Google Chrome]`，与真机实测完全相同。

### ⚠️ `--fingerprint-device-scale-factor`（DPR）必须和分辨率配套

**它是什么**：`devicePixelRatio`，即"1 个 CSS 像素等于几个物理像素"，对应 Windows 显示设置里的
**缩放比例**——100% = 1.0、125% = 1.25、150% = 1.5、200% = 2.0。

**为什么必须传**：检测站上那行"屏幕分辨率"**不是** `screen.width`，而是

```
物理分辨率 = screen.width × devicePixelRatio
```

反过来说，`--fingerprint-screen` 里填的是 **CSS 逻辑像素**（＝物理分辨率 ÷ 缩放），**不是**物理分辨率。
想报一台「1920×1080 屏 @125% 缩放」的笔记本，这里要填 `1536x864` 而不是 `1920x1080`。

所以只传 `--fingerprint-screen` 不传 DPR，网页看到的分辨率会是「你伪装的宽高 × 宿主机真实缩放」，
既不是你想报的值，也大概率不是任何真实显示器的规格。实测对比（宿主机缩放 225%）：

| 启动参数 | `devicePixelRatio` | `matchMedia('(resolution:1.25dppx)')` | `Sec-CH-DPR` 请求头 | 检测站显示的分辨率 |
|---|---|---|---|---|
| 只传 `--fingerprint-screen=1536x864` | 2.25（真机）| false | 2.25 | ❌ 3456×1944（不存在的规格）|
| 再加 `--fingerprint-device-scale-factor=1.25` | 1.25 | true | 1.25 | ✅ 1920×1080 |

三处（JS 属性、CSS 媒体查询、请求头）会一起改，不会出现"JS 说 1.25、媒体查询说 2.25"这种
自相矛盾——那种矛盾正是 CreepJS 这类做一致性交叉校验的站点最容易抓的。

**不改渲染**：只改网页读到的值，浏览器窗口和界面大小不受影响。这点和 Chromium 原生的
`--force-device-scale-factor` 不同，后者是真的改渲染缩放，UI 会跟着变大变小。

**常见真实搭配**（照抄即可，不要自己乱配）：

| `--fingerprint-screen` | `--fingerprint-device-scale-factor` | 对应真实硬件 |
|---|---|---|
| `1920x1080` | `1` | 1920×1080 显示器 @100% |
| `1536x864` | `1.25` | 1920×1080 笔记本 @125%（最常见）|
| `1280x720` | `1.5` | 1920×1080 @150% |
| `2560x1440` | `1` | 2K 显示器 @100% |
| `2048x1152` | `1.25` | 2560×1440 笔记本 @125% |
| `1366x768` | `1` | 1366×768 老款/办公本 @100% |
| `1707x960` | `2.25` | 4K 屏 @225% |
| `1920x1080` | `2` | 4K 屏 @200% |
| `1280x800` | `2` | MacBook Pro 13" Retina（物理 2560×1600）|
| `1512x982` | `2` | MacBook Pro 14"（物理 3024×1964，默认缩放）|
| `1728x1117` | `2` | MacBook Pro 16"（物理 3456×2234，默认缩放）|

**DPR 要跟 `--fingerprint-platform` 对得上**：macOS 只有 `1`（非 Retina）和 `2`（Retina）两档，
报 `platform=macos` 却给 `1.25` / `1.5` / `2.25` 这种 Windows 特有的缩放值，是一眼可见的矛盾。
反过来 Windows 常见 `1` / `1.25` / `1.5` / `1.75` / `2` / `2.25`，但**不要自己编** `1.1`、`1.33`
这类系统里根本选不出来的倍率。

移动端必须传：iPhone 系列 DPR 是 `3`，Pixel 系列是 `2.625`。UA 报手机而 DPR 是 1.0 或桌面机的
缩放值，一眼就是假的。

#### 成对使用的完整案例

下面每一组都是「分辨率 + DPR」配套的写法，直接照抄换值即可。每组后面注明了检测站会看到的结果。

**案例 1 · 最常见的 1080p 笔记本（1920×1080 屏 @125% 缩放）**

```
chrome.exe ^
  --user-data-dir=D:\profiles\acc01 ^
  --fingerprint-screen=1536x864 ^
  --fingerprint-device-scale-factor=1.25 ^
  --fingerprint-screen-color-depth=24
```

检测站看到：可用宽高 `1536×864`（CSS 像素）、`devicePixelRatio = 1.25`、屏幕分辨率 `1920×1080`。
这是 Windows 笔记本里占比最高的一种组合，最不容易引人注意。

**案例 2 · 外接 1080p 显示器（1920×1080 @100% 缩放）**

```
chrome.exe ^
  --user-data-dir=D:\profiles\acc02 ^
  --fingerprint-screen=1920x1080 ^
  --fingerprint-device-scale-factor=1 ^
  --fingerprint-screen-color-depth=24
```

检测站看到：可用宽高 `1920×1080`、`devicePixelRatio = 1`、屏幕分辨率 `1920×1080`。
DPR 为 1 时两个数字相同，这是台式机 + 外接显示器最典型的样子。

**案例 3 · 2K 显示器（2560×1440 @100% 缩放）**

```
chrome.exe ^
  --user-data-dir=D:\profiles\acc03 ^
  --fingerprint-screen=2560x1440 ^
  --fingerprint-device-scale-factor=1 ^
  --fingerprint-screen-color-depth=24
```

**案例 4 · 4K 屏 @200% 缩放（高端笔记本 / 设计本常见）**

```
chrome.exe ^
  --user-data-dir=D:\profiles\acc04 ^
  --fingerprint-screen=1920x1080 ^
  --fingerprint-device-scale-factor=2 ^
  --fingerprint-screen-color-depth=24
```

注意这组和案例 2 的可用宽高完全一样，都是 `1920×1080`，但因为 DPR 不同，检测站还原出的屏幕
分辨率一个是 1920×1080、一个是 3840×2160。**这正说明只有分辨率、没有 DPR 是描述不清一台机器的。**

**案例 5 · 移动端 Android（Pixel 7）**

```
chrome.exe ^
  --user-data-dir=D:\profiles\phone01 ^
  --fingerprint-platform=android ^
  --fingerprint-screen=412x915 ^
  --fingerprint-device-scale-factor=2.625 ^
  --fingerprint-gpu-vendor=Qualcomm ^
  --fingerprint-gpu-renderer=ANGLE (Qualcomm, Adreno (TM) 730, OpenGL ES 3.2)
```

**案例 6 · 移动端 iOS（iPhone 14 Pro）**

```
chrome.exe ^
  --user-data-dir=D:\profiles\phone02 ^
  --fingerprint-platform=ios ^
  --fingerprint-screen=393x852 ^
  --fingerprint-device-scale-factor=3 ^
  --fingerprint-gpu-vendor=Apple Inc. ^
  --fingerprint-gpu-renderer=Apple GPU
```

**反面案例 · 只传分辨率不传 DPR（不要这么写）**

```
chrome.exe --fingerprint-screen=1536x864
```

在一台缩放 225% 的宿主机上实测的后果：`devicePixelRatio` 仍是真机的 `2.25`，检测站算出的屏幕
分辨率变成 `3456×1944`——世界上没有这个规格的显示器。而且同一份配置换到 100% 缩放的机器上跑，
又会变成 `1536×864`，**同一个"环境"在不同宿主机上指纹不一致**，既不利于养号，也等于把宿主机的
缩放设置泄露了出去。

#### 启动后自检

在 Console 里跑这一段，三处（JS 属性 / 媒体查询 / 还原出的物理分辨率）一次看全：

```js
console.table({
  逻辑分辨率: `${screen.width}x${screen.height}`,
  可用区域:   `${screen.availWidth}x${screen.availHeight}`,
  DPR:        devicePixelRatio,
  物理分辨率: `${screen.width * devicePixelRatio}x${screen.height * devicePixelRatio}`,
  媒体查询一致: matchMedia(`(resolution: ${devicePixelRatio}dppx)`).matches,
});
```

三条都对上才算过：

1. `DPR` 等于你传入的值，不是宿主机的缩放；
2. `物理分辨率` 正好是所伪装机型的真实规格（对着上面的搭配表核）；
3. `媒体查询一致` 为 `true`，说明 CSS 侧没有和 JS 侧打架。

最后再做一次跨机验证：**把同一份参数换到一台显示缩放不同的电脑上再跑一遍，输出必须逐字相同**。
只要有一项跟着宿主机变，就说明 DPR 没传进去。

> 各语言的启动示例都直接传入这个命令行参数，见 [`../../examples/`](../../examples/)。

---

## 四、对标竞品能力（WebRTC / WebGPU / 蓝牙 / 地理位置 / 设备名·MAC）

| 竞品面板项 | 本内核实现 | 参数 / 方式 |
|---|---|---|
| WebRTC（真实/替换/禁用）| ✅ 内置 | `--webrtc-ip-handling-policy=disable_non_proxied_udp`（只走代理，不漏内网 IP）|
| WebGPU（真实/禁用）| ✅ 新增内核开关 | `--fingerprint-webgpu=disable` → `navigator.gpu=null`；不禁用时其适配器 vendor 跟随 `--fingerprint-gpu-vendor` 对齐 WebGL（“基于 WebGL”）|
| 蓝牙（隐私/真实）| ✅ 新增内核开关 | `--fingerprint-disable-bluetooth` → `navigator.bluetooth=null` |
| 地理位置（基于 IP / 自定义 / 禁止）| ✅ 启动器层 | 通过 Playwright / CDP 的 geolocation 与权限参数实现；不属于内核命令行开关 |
| WebGL 自定义（vendor/renderer）| ✅ 已有 | `--fingerprint-gpu-vendor` / `--fingerprint-gpu-renderer` |
| Canvas / Audio / ClientRects / 字体 噪声 | ✅ 已有 | 见第二节 5 个开关 |
| DNT / 电池 / 语音列表 / CPU / 内存 / 分辨率 | ✅ 已有 | 见第三节参数表 |

> **关于「设备名称」「MAC 地址」**：这两项**不经标准 Web JS 暴露**——浏览器沙箱不会把主机名或
> 网卡 MAC 提供给网页（历史上 WebRTC 曾泄露 MAC，早已移除）。竞品面板里这两项是给**本地原生
> 程序 / WebRTC mDNS 主机名**用的，网页检测面（FingerprintJS、BrowserScan、CreepJS）读不到，
> 因此无需内核开关。WebRTC mDNS 混淆默认开启，`.local` 主机名不会外泄。

---

## 五、浏览器行为类启动命令（省流量 / 免打扰 / 隐私）

> 这类不是「指纹」，而是控制浏览器加载/弹窗行为，三套内核（138 / 144 / 150）均支持，
> 直接用 chrome.exe 命令行即可。

| 能力 | 参数 | 类型 | 不传的效果 |
|---|---|---|---|
| 禁止加载图片 | `--blink-settings=imagesEnabled=false` | Chromium 内置 | 正常加载图片 |
| 禁止加载超过 N KB 的图片 | `--max-image-size-kb=300` | **新增内核开关** | 不限制图片大小 |
| 禁止视频自动播放/预加载 | `--autoplay-policy=document-user-activation-required` | Chromium 内置 | 允许自动播放 |
| 禁止网站播放声音 | `--mute-audio` | Chromium 内置 | 正常出声 |
| 禁止谷歌翻译弹窗 | 本内核**默认已关**（pref `translate.enabled=false`）| 内核默认 | 本内核天然不弹翻译气泡 |
| 禁止保存密码弹窗 | `--disable-save-password` | **新增内核开关** | 默认会弹并保存；也可随 profile 设置 |
| 禁止网页弹出消息通知 | `--block-notifications` | **新增内核开关** | 通知权限正常弹窗询问 |
| 禁止**所有**权限弹窗（摄像头/麦克风/定位/通知等）| `--deny-permission-prompts` | Chromium 内置 | 各权限正常弹窗询问 |
| 启动时随机指纹（一键开全部 5 类噪声）| `--fingerprint-random` | **新增内核开关** | 各类噪声按各自开关，默认原生 |
| 同步 / 保留 Cookie | `--user-data-dir=<持久化目录>` | Chromium 内置 | 用临时目录，退出后不留 Cookie |
| 同步 / 保存已保存的账号密码 | `--user-data-dir=<持久化目录>`（**默认即会弹"保存密码"并写入密码库**）| 内核默认已开启 | 默认就保存；只有传 `--disable-save-password` 才不保存 |

说明：

- **`--max-image-size-kb=N`**：内核在图片响应到达时读 `Content-Length`，超过 N KB 直接取消该图片
  加载（省流量、拦大图）。
- **`--fingerprint-random`**：等价于同时传 `--fingerprint-canvas --fingerprint-webgl
  --fingerprint-audio --fingerprint-rects --fingerprint-font`（都用「本次启动随机、全会话一致」的
  种子）。每次启动指纹都不同、同一次运行内跨标签一致。⚠️开噪声会让 FingerprintJS Pro 报
  "Browser Tampering"，与「全绿」目标互斥，按需取舍。
- **`--block-notifications` vs `--deny-permission-prompts`**：前者**只**拒绝通知权限、其它权限
  （定位/摄像头等）仍正常询问；后者拒绝**全部**权限弹窗。按需选一个。
- **Cookie / 密码持久化**：本质是「用固定的 `--user-data-dir` 持久化 profile」。Cookie 自动留存，
  所以重启后登录态不会掉。**密码保存已改为默认开启**：三套内核都把 `credentials_enable_service`
  的注册默认值恢复成上游 Chromium 的 `true`（ungoogled 基线原本改成了 `false`，导致永不弹保存气泡），
  并移除了「检测到 `--enable-automation` 就禁用保存」的分支，所以即便通过 CDP / 自动化连接也照常保存。
  只有显式传 `--disable-save-password` 才关闭。多账号隔离＝多个 `--user-data-dir` 目录。
- **注意区分两件事**：「登录态是否掉线」看 Cookie（由 `--user-data-dir` 决定）；「是否弹保存密码气泡、
  是否自动填账号密码」看密码管理器（由上面这条决定）。两者互不影响。

各语言的参数拼装方式见 [`../../examples/`](../../examples/)。

### 地址栏默认搜索（无需任何参数，三套内核均已恢复）

ungoogled 基线把默认搜索引擎换成了一个叫 **No Search** 的假引擎，它的搜索地址是
`http://{searchTerms}`——所以在地址栏里敲任何一个词都会被当成域名去打开，比如输入「指纹检测」
就跳到 `http://指纹检测` 然后报 `ERR_NAME_NOT_RESOLVED`；同时它还把搜索建议开关的默认值
改成了关，所以输入时也没有下拉候选。

三套内核已改回和正版 Chrome 一致的行为，**开箱即用，不需要传任何启动参数**：

- 默认搜索引擎恢复为 **Google**（关键字 `google.com`，搜索地址与建议地址都是 Chrome 原版的那套）。
- 地址栏输入时**出下拉搜索建议**（`search.suggest_enabled` 默认值改回 `true`）。
- 顺带修掉了 ungoogled 给 Google 基址加的 `trk:` 拦截前缀和替换域名（138 上原本是
  `trk:113:https://www.9oo91e.qjz9zk/`，144 是 `trk:113:https://www.google.com/`）。这个前缀会让
  搜索导航被内部拦截器直接丢弃，表现为「敲回车没有任何反应」，只换引擎不修它是搜不出东西的。
- 内置引擎表的数据版本号已抬高，所以**已经建好的旧 profile 再次启动时也会自动刷新**，不必删配置重建。

想换成 Bing / DuckDuckGo 等，在设置里改或用 `--user-data-dir` 各自持久化即可，引擎表里都有。

> 开了搜索建议之后，地址栏的输入会实时发给搜索引擎的 suggest 接口——这与正版 Chrome 行为一致，
> 且走的是你配置的代理出口。如果某个环境不想要这个请求，在「设置 → 同步和 Google 服务 →
> 自动补全搜索和网址」里关掉即可，只影响下拉建议，不影响回车搜索。

---

## 六、按版本标注的差异

### 138 版本可改
- 支持第二/三/四/五节**全部参数**（含 5 个分类噪声开关、WebGPU / 蓝牙 / WebRTC、全部行为类开关）。
- 差异：`audio` 类噪声在 138 基座上仅微扰帧数、无采样率噪声（见第二节差异表）。

### 144 版本可改
- 支持第二/三/四/五节**全部参数**。
- 额外历史开关（分量式写法，等价于 `--fingerprint-screen`）：
  - `--fingerprint-screen-width=<宽>` / `--fingerprint-screen-height=<高>`

### 150 版本可改
- 与 **144 完全相同**（同一套开关集）。
- 版本号最新，ML 检测友好度最好（旧版内核本身会被 FingerprintJS 的模型判为反检测浏览器，150 通过率最高）。

> **一句话记忆**：三套开关集基本一致（144/150 多两个分量式屏幕历史开关），仅版本号与 audio 噪声深度不同。
> `--fingerprint-device-scale-factor` 三套都已实现并实测生效（早期版本里它只是被透传、不起作用，现已修复）。

---

## 七、推荐启动组合

### A. 桌面「全绿」配置（FingerprintJS Pro Not detected）
关键：**不开噪声种子、不开 GPU 字符串伪装**，只用开关类伪装保持唯一性。
```
chrome.exe ^
  --fingerprint-platform=windows ^
  --fingerprint-brand=Chrome ^
  --fingerprint-platform-version=10.0.0 ^
  --fingerprint-hardware-concurrency=8 ^
  --fingerprint-device-memory=8 ^
  --fingerprint-screen=1536x864 ^
  --fingerprint-device-scale-factor=1.25 ^
  --fingerprint-screen-color-depth=24 ^
  --fingerprint-battery=1,1.0,0,Infinity ^
  --timezone=Asia/Tokyo ^
  --proxy-server=socks5://127.0.0.1:xxxx
```

### B. 省流量 / 免打扰配置（爬取或挂机）
```
chrome.exe ^
  --blink-settings=imagesEnabled=false ^
  --max-image-size-kb=300 ^
  --autoplay-policy=document-user-activation-required ^
  --mute-audio ^
  --block-notifications ^
  --disable-save-password ^
  --user-data-dir=D:\profiles\acc01
```

### C. 移动端 Android（Pixel 7）
```
chrome.exe ^
  --user-data-dir=D:\profiles\phone01 ^
  --fingerprint-platform=android ^
  --fingerprint-screen=412x915 ^
  --fingerprint-device-scale-factor=2.625 ^
  --fingerprint-gpu-vendor=Qualcomm ^
  --fingerprint-gpu-renderer=ANGLE (Qualcomm, Adreno (TM) 730, OpenGL ES 3.2)
```
视口 412×915 配 DPR 2.625 才是 Pixel 7 的真实参数。**DPR 必须和视口一起传**，
只传视口的话 DPR 会是宿主机的桌面缩放值，UA 报着手机、DPR 却是 1.0 或 1.25，一眼假。

### D. 移动端 iOS（iPhone 14 Pro）
```
chrome.exe ^
  --user-data-dir=D:\profiles\phone02 ^
  --fingerprint-platform=ios ^
  --fingerprint-screen=393x852 ^
  --fingerprint-device-scale-factor=3 ^
  --fingerprint-gpu-vendor=Apple Inc. ^
  --fingerprint-gpu-renderer=Apple GPU
```
配合 Safari UA；`userAgentData` 在 `platform=ios` 时会自动隐藏为 `null`（真机 Safari 没有这个 API）。
iPhone 全系 DPR 都是 3，别写别的值。

> **maxTouchPoints=5**：真机移动端为 5。便携版直接命令行启动时该值走内核默认；
> 自动化启动时可通过 CDP 的 `Emulation.setTouchEmulationEnabled` 将
> `maxTouchPoints` 覆写为 5。

### E. BrowserScan 100 分配置（实测零扣分）

下面这套是**实测 `Browser fingerprint authenticity: 100%`、扣分项为空、Bot Detection: No** 的完整参数
（150 内核，出口 IP 与时区/语言已对齐）。三个容易踩坑的位置已用注释标出。

```
chrome.exe ^
  --user-data-dir=D:\profiles\acc01 ^
  --proxy-server=socks5://127.0.0.1:1080 ^
  --no-first-run --no-default-browser-check ^
  --disable-quic ^
  --disable-features=Translate ^
  --user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36 ^
  --fingerprint-brand=Chrome ^
  --fingerprint-brand-version=150.0.7871.124 ^
  --fingerprint-platform=windows ^
  --fingerprint-platform-version=10.0.0 ^
  --lang=en-SG ^
  --accept-lang=en-SG,en ^
  --timezone=Asia/Singapore ^
  --fingerprint-hardware-concurrency=12 ^
  --fingerprint-device-memory=4 ^
  --fingerprint-screen=1536x864 ^
  --fingerprint-screen-color-depth=24 ^
  --fingerprint-device-scale-factor=1.25 ^
  --webrtc-ip-handling-policy=disable_non_proxied_udp
```

四个最容易踩坑的位置：

1. `--user-agent` 的版本位写 `150.0.0.0`（缩减形式），**不要**写完整补丁号 `150.0.7871.124`；
   完整补丁号只放 `--fingerprint-brand-version`。
2. `--lang` 和 `--accept-lang` **两个都要传**，主语言保持一致（`en-SG` / `en-SG,en`）。
3. `--accept-lang` 只给逗号分隔的语言列表，**不要自己带 `q=` 权重**。
4. `--fingerprint-screen` 和 `--fingerprint-device-scale-factor` **成对传**。上例 `1536x864` 配
   `1.25`，检测站还原出的物理分辨率正好是 1920×1080；只传前者的话会用宿主机真实缩放去乘，
   在 225% 缩放的机器上会算出 3456×1944 这种不存在的规格。

其它要点：

- `--timezone` 与 `--lang` / `--accept-lang` 必须匹配**出口 IP 所在地区**。上例是新加坡出口，
  所以时区 `Asia/Singapore`、语言 `en-SG`。IP 与时区不符会扣 **Different time zones −10%**，
  IP 与语言不符会扣 **Language mismatch −10%**。
- 上例未开启五类噪声或 GPU 串伪装；要在 FingerprintJS Pro 保持全绿，也应保持关闭，见第八节第 1 条。
- Chromium 的 `--proxy-server` 不接受用户名密码；认证代理需先经过本地无认证 SOCKS5 桥。
- 拼参数时注意**不要重复追加同一个开关**。Chromium 只取第一次出现的值，重复不会报错但会掩盖拼装逻辑的
  bug（例如同一个 `--fingerprint-canvas` 出现两次）。

---

## 八、注意事项

1. **噪声 vs 隐身权衡**：分类噪声开关（`--fingerprint-canvas` 等）、`--fingerprint-random` 和
   `--fingerprint-gpu-*` 会让指纹更独特（防跨站追踪、利于 CreepJS），但 FingerprintJS Pro 的 ML
   模型会因此报 "Browser Tampering"。想在 FingerprintJS 全绿就别开这些；想抗追踪唯一性就按需开对应类别。
   - **`--fingerprint-gpu-vendor` 与 `--fingerprint-gpu-renderer` 的区别**：`vendor` 是 GPU **厂商**
     （`UNMASKED_VENDOR_WEBGL`，粗粒度，如 `Google Inc. (NVIDIA)`）；`renderer` 是 GPU **具体型号/渲染器**
     （`UNMASKED_RENDERER_WEBGL`，细粒度，如 `ANGLE (NVIDIA, NVIDIA GeForce RTX 3060, ...)`）。
     一个是"哪家厂商"、一个是"具体哪块显卡"，两者要成套匹配同一真实 GPU（含移动端），否则会被判 tampering。
2. **时区 / 语言必须跟代理 IP 对齐**：`--timezone` 与 `--accept-lang` 要匹配出口 IP 的地区，否则
   BrowserScan 会扣分（Different time zones）。请在启动前按实际出口 IP 手动对齐。
   - **`--lang` 与 `--accept-lang` 的区别**：`--lang` 是"浏览器本地显示语言 + 前端单值 `navigator.language`"；
     `--accept-lang` 是"发给服务器的 `Accept-Language` 请求头 + 语言列表 `navigator.languages`"。
     一个偏本地显示、一个偏网络请求，两者要保持一致才不易被识别，例如 `--lang=en-US` 配 `--accept-lang=en-US,en`。
   - **必须两个都传**。只传 `--accept-lang` 不传 `--lang` 时，界面语言仍是系统语言，`Intl` 的默认
     locale（`Intl.DateTimeFormat().resolvedOptions().locale`）会继续暴露系统语言。中文系统上就会出现
     `navigator.language = en-SG` 而 `Intl` locale = `zh-CN`，BrowserScan 直接扣
     **Language mismatch −10%**（原文：*The language of your webpage does not match the language of
     the system*），"Internationalization API"那一行也会标红。
   - ⚠️ **`--accept-lang` 不要自己带 `q=` 权重**。内核收到的是"语言列表"，权重由内核自己生成。
     传 `--accept-lang=en-SG,en;q=0.9,en;q=0.8` 的实测后果：`navigator.languages` 变成
     `['en-SG', 'en;q=0.9', 'en;q=0.8']`（q 值被当成语言标签的一部分塞进数组），
     `Accept-Language` 请求头被**二次加权**成 `en-SG,en;q=0.9,en;q=0.9;q=0.8,en;q=0.8;q=0.7`
     这种非法格式，BrowserScan 上 Languages 与 Accept-Language header 两行都标红。
     正确传 `--accept-lang=en-SG,en` 时：`navigator.languages` = `['en-SG', 'en']`，
     请求头 = `en-SG,en;q=0.9`。
3. **版本号已自洽，但自定义 UA 时要用缩减形式**：三套内核自带的 UA / UA-CH 版本号已同步为各自真实内核
   版本，不会出现「Chrome 144 内核报 150 UA」这类不符。**一旦自己传 `--user-agent`，版本位必须写成
   `主版本.0.0.0`**，完整补丁号只放 `--fingerprint-brand-version`，否则 BrowserScan 会判
   `Different browser version −5%`。详见第三节末尾的「⚠️ `--user-agent` 版本号必须写成缩减形式」。
4. **平台一致性**：改 `--fingerprint-platform` 时，`navigator.platform`、UA、UA-CH platform 会同步改；
   移动端还需配套 GPU 串，否则会因桌面 GPU（如 RTX 3090 / D3D11）暴露被判 tampering / 虚拟机。
