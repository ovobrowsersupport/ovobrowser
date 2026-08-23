# 推荐配方

英文版：[RECIPES.md](../en/RECIPES.md)

把 `chrome.exe` 换成你的 ovobrowser 路径。Windows 换行用 `^`，其它环境写成参数数组（见 examples）。

## A. FingerprintJS Pro 全绿（不开噪声）

```
--no-first-run --no-default-browser-check --disable-quic
--fingerprint-platform=windows
--fingerprint-brand=Chrome
--fingerprint-brand-version=150.0.7871.124
--fingerprint-platform-version=10.0.0
--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36
--fingerprint-hardware-concurrency=8
--fingerprint-device-memory=8
--fingerprint-screen=1536x864
--fingerprint-device-scale-factor=1.25
--fingerprint-screen-color-depth=24
--fingerprint-battery=1,1.0,0,Infinity
--webrtc-ip-handling-policy=disable_non_proxied_udp
--timezone=<出口IANA时区>
--lang=<出口语言>
--accept-lang=<出口语言>,en
--user-data-dir=<独立目录>
```

## B. BrowserScan 100 分骨架

与 A 相同，额外确认：

1. UA 里是 `Chrome/150.0.0.0` 不是完整补丁号
2. `--lang` 和 `--accept-lang` 都在，且无 `q=`
3. 时区/语言跟出口 IP 同一地区
4. 不要重复传同一个开关（Chromium 只取第一次）

## C. 要换 visitor（会增加 Tampering 风险）

在 A 基础上按档案加固定种子，例如：

```
--fingerprint-canvas=8842
--fingerprint-webgl=8842
--fingerprint-audio=8842
--fingerprint-rects=8842
--fingerprint-font=8842
```

每个账号一套种子 + 独立 `--user-data-dir`。

## D. Android（Pixel 7 画像）

```
--fingerprint-platform=android
--fingerprint-screen=412x915
--fingerprint-device-scale-factor=2.625
--fingerprint-gpu-vendor=Qualcomm
--fingerprint-gpu-renderer=ANGLE (Qualcomm, Adreno (TM) 730, OpenGL ES 3.2)
```

命令行启动时 `maxTouchPoints` 走内核默认；用 CDP 自动化时可再设为 5。

## E. iOS（iPhone 14 Pro 画像）

```
--fingerprint-platform=ios
--fingerprint-screen=393x852
--fingerprint-device-scale-factor=3
--fingerprint-gpu-vendor=Apple Inc.
--fingerprint-gpu-renderer=Apple GPU
```

配 Safari UA；`userAgentData` 会自动变为 `null`。
