$ErrorActionPreference = "Stop"
$chrome = $env:OVO_CHROME
if (-not $chrome) { $chrome = "D:\ovobrowser-150\chrome.exe" }
$profile = $env:OVO_PROFILE
if (-not $profile) { $profile = "D:\ovobrowser-profiles\ps-demo" }
$url = $env:OVO_URL
if (-not $url) { $url = "https://demo.fingerprint.com/playground" }

if (-not (Test-Path $chrome)) { throw "chrome.exe 不存在: $chrome" }
New-Item -ItemType Directory -Force -Path $profile | Out-Null

$args = @(
  "--user-data-dir=$profile",
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
  $url
)
Start-Process -FilePath $chrome -ArgumentList $args
Write-Host "已启动 $chrome"
Write-Host "profile $profile"
