const { spawn } = require("child_process");
const fs = require("fs");
const path = require("path");

const chrome =
  process.env.OVO_CHROME ||
  "D:\\ovobrowser-150\\chrome.exe";
const profile =
  process.env.OVO_PROFILE || "D:\\ovobrowser-profiles\\node-demo";

const args = [
  `--user-data-dir=${profile}`,
  "--no-first-run",
  "--no-default-browser-check",
  "--disable-quic",
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
  process.env.OVO_URL || "https://demo.fingerprint.com/playground",
];

if (!fs.existsSync(chrome)) {
  console.error("chrome.exe 不存在:", chrome);
  process.exit(1);
}
fs.mkdirSync(profile, { recursive: true });
spawn(chrome, args, { detached: true, stdio: "ignore" }).unref();
console.log("已启动", chrome);
console.log("profile", profile);
