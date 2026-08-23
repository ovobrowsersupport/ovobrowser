"""用 Playwright 驱动已经带指纹参数的 ovobrowser（persistent context）。
pip install playwright
"""
import os
from playwright.sync_api import sync_playwright

CHROME = os.environ.get(
    "OVO_CHROME",
    r"D:\ovobrowser-150\chrome.exe",
)
PROFILE = os.environ.get("OVO_PROFILE", r"D:\ovobrowser-profiles\pw-demo")

ARGS = [
    "--no-first-run",
    "--no-default-browser-check",
    "--disable-quic",
    "--fingerprint-platform=windows",
    "--fingerprint-brand=Chrome",
    "--fingerprint-brand-version=150.0.7871.124",
    "--fingerprint-platform-version=10.0.0",
    "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36",
    "--fingerprint-screen=1536x864",
    "--fingerprint-device-scale-factor=1.25",
    "--fingerprint-screen-color-depth=24",
    "--fingerprint-hardware-concurrency=8",
    "--fingerprint-device-memory=8",
    "--timezone=America/New_York",
    "--lang=en-US",
    "--accept-lang=en-US,en",
    "--webrtc-ip-handling-policy=disable_non_proxied_udp",
]


def main():
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
        page.goto("https://demo.fingerprint.com/playground", timeout=60000)
        input("检查完毕后回车关闭…")
        ctx.close()


if __name__ == "__main__":
    main()
