"""拉起 ovobrowser 150（FingerprintJS 全绿配方，无噪声）。"""
import os
import subprocess
import sys

CHROME = os.environ.get(
    "OVO_CHROME",
    r"D:\ovobrowser-150\chrome.exe",
)
PROFILE = os.environ.get("OVO_PROFILE", r"D:\ovobrowser-profiles\python-demo")
START_URL = os.environ.get("OVO_URL", "https://demo.fingerprint.com/playground")


def flags():
    return [
        CHROME,
        f"--user-data-dir={PROFILE}",
        "--no-first-run",
        "--no-default-browser-check",
        "--disable-quic",
        "--disable-features=Translate",
        "--fingerprint-platform=windows",
        "--fingerprint-brand=Chrome",
        "--fingerprint-brand-version=150.0.7871.124",
        "--fingerprint-platform-version=10.0.0",
        "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36",
        "--fingerprint-hardware-concurrency=8",
        "--fingerprint-device-memory=8",
        "--fingerprint-screen=1536x864",
        "--fingerprint-device-scale-factor=1.25",
        "--fingerprint-screen-color-depth=24",
        "--fingerprint-battery=1,1.0,0,Infinity",
        "--webrtc-ip-handling-policy=disable_non_proxied_udp",
        # 按出口 IP 改这两项
        "--timezone=America/New_York",
        "--lang=en-US",
        "--accept-lang=en-US,en",
        START_URL,
    ]


if __name__ == "__main__":
    if not os.path.isfile(CHROME):
        sys.exit(f"chrome.exe 不存在: {CHROME}")
    os.makedirs(PROFILE, exist_ok=True)
    subprocess.Popen(flags())
    print("已启动", CHROME)
    print("profile", PROFILE)
