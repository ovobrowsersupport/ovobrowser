using System.Diagnostics;

var chrome = Environment.GetEnvironmentVariable("OVO_CHROME")
    ?? @"D:\ovobrowser-150\chrome.exe";
var profile = Environment.GetEnvironmentVariable("OVO_PROFILE")
    ?? @"D:\ovobrowser-profiles\csharp-demo";
var url = Environment.GetEnvironmentVariable("OVO_URL")
    ?? "https://demo.fingerprint.com/playground";

if (!File.Exists(chrome))
{
    Console.Error.WriteLine($"chrome.exe 不存在: {chrome}");
    return 1;
}
Directory.CreateDirectory(profile);

var args = string.Join(" ", new[]
{
    $"--user-data-dir=\"{profile}\"",
    "--no-first-run",
    "--no-default-browser-check",
    "--disable-quic",
    "--fingerprint-platform=windows",
    "--fingerprint-brand=Chrome",
    "--fingerprint-brand-version=150.0.7871.124",
    "--fingerprint-platform-version=10.0.0",
    "--user-agent=\"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36\"",
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
});

Process.Start(new ProcessStartInfo
{
    FileName = chrome,
    Arguments = args,
    UseShellExecute = true,
});
Console.WriteLine($"已启动 {chrome}");
return 0;
