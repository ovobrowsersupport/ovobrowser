use std::env;
use std::fs;
use std::path::Path;
use std::process::Command;

fn env_or(key: &str, default: &str) -> String {
    env::var(key).unwrap_or_else(|_| default.to_string())
}

fn main() {
    let chrome = env_or(
        "OVO_CHROME",
        r"D:\ovobrowser-150\chrome.exe",
    );
    let profile = env_or("OVO_PROFILE", r"D:\ovobrowser-profiles\rust-demo");
    let url = env_or("OVO_URL", "https://demo.fingerprint.com/playground");
    if !Path::new(&chrome).is_file() {
        eprintln!("chrome.exe 不存在: {chrome}");
        std::process::exit(1);
    }
    fs::create_dir_all(&profile).ok();
    Command::new(&chrome)
        .args([
            format!("--user-data-dir={profile}"),
            "--no-first-run".into(),
            "--no-default-browser-check".into(),
            "--disable-quic".into(),
            "--fingerprint-platform=windows".into(),
            "--fingerprint-brand=Chrome".into(),
            "--fingerprint-brand-version=150.0.7871.124".into(),
            "--fingerprint-platform-version=10.0.0".into(),
            "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36".into(),
            "--fingerprint-hardware-concurrency=8".into(),
            "--fingerprint-device-memory=8".into(),
            "--fingerprint-screen=1536x864".into(),
            "--fingerprint-device-scale-factor=1.25".into(),
            "--fingerprint-screen-color-depth=24".into(),
            "--fingerprint-battery=1,1.0,0,Infinity".into(),
            "--webrtc-ip-handling-policy=disable_non_proxied_udp".into(),
            "--timezone=America/New_York".into(),
            "--lang=en-US".into(),
            "--accept-lang=en-US,en".into(),
            url,
        ])
        .spawn()
        .expect("启动失败");
    println!("已启动 {chrome}");
}
