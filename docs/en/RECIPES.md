# Recipes

Chinese: [RECIPES.md](../zh/RECIPES.md)

Replace `chrome.exe` with your ovobrowser path. On Windows use `^` line continuations; elsewhere pass an argv array (see `examples/`).

## A. FingerprintJS Pro green (no noise)

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
--timezone=<exit-IP-IANA-zone>
--lang=<exit-locale>
--accept-lang=<exit-locale>,en
--user-data-dir=<isolated-profile>
```

## B. BrowserScan 100% skeleton

Same as A, plus:

1. UA uses `Chrome/150.0.0.0`, never the full patch
2. Both `--lang` and `--accept-lang`, no `q=`
3. Timezone/language match the exit IP region
4. Do not repeat the same flag (Chromium keeps the first)

## C. Rotate visitor identity (raises Tampering risk)

Add per-profile seeds on top of A:

```
--fingerprint-canvas=8842
--fingerprint-webgl=8842
--fingerprint-audio=8842
--fingerprint-rects=8842
--fingerprint-font=8842
```

One seed set + one `--user-data-dir` per account.

## D. Android (Pixel 7)

```
--fingerprint-platform=android
--fingerprint-screen=412x915
--fingerprint-device-scale-factor=2.625
--fingerprint-gpu-vendor=Qualcomm
--fingerprint-gpu-renderer=ANGLE (Qualcomm, Adreno (TM) 730, OpenGL ES 3.2)
```

CLI uses the kernel default for `maxTouchPoints`; CDP automation can set it to 5.

## E. iOS (iPhone 14 Pro)

```
--fingerprint-platform=ios
--fingerprint-screen=393x852
--fingerprint-device-scale-factor=3
--fingerprint-gpu-vendor=Apple Inc.
--fingerprint-gpu-renderer=Apple GPU
```

Use a Safari UA; `userAgentData` becomes `null`.
