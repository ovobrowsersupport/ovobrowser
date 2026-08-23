package main

import (
	"fmt"
	"os"
	"os/exec"
)

func env(k, d string) string {
	if v := os.Getenv(k); v != "" {
		return v
	}
	return d
}

func main() {
	chrome := env("OVO_CHROME", `D:\ovobrowser-150\chrome.exe`)
	profile := env("OVO_PROFILE", `D:\ovobrowser-profiles\go-demo`)
	url := env("OVO_URL", "https://demo.fingerprint.com/playground")
	if _, err := os.Stat(chrome); err != nil {
		fmt.Fprintln(os.Stderr, "chrome.exe 不存在:", chrome)
		os.Exit(1)
	}
	_ = os.MkdirAll(profile, 0o755)
	args := []string{
		"--user-data-dir=" + profile,
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
		url,
	}
	cmd := exec.Command(chrome, args...)
	if err := cmd.Start(); err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
	fmt.Println("已启动", chrome, "pid", cmd.Process.Pid)
}
