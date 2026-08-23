import java.io.File;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;

public class Launch {
    static String env(String k, String d) {
        String v = System.getenv(k);
        return (v == null || v.isEmpty()) ? d : v;
    }

    public static void main(String[] args) throws Exception {
        String chrome = env("OVO_CHROME", "D:\\ovobrowser-150\\chrome.exe");
        String profile = env("OVO_PROFILE", "D:\\ovobrowser-profiles\\java-demo");
        String url = env("OVO_URL", "https://demo.fingerprint.com/playground");
        if (!new File(chrome).isFile()) {
            System.err.println("chrome.exe 不存在: " + chrome);
            System.exit(1);
        }
        Files.createDirectories(Path.of(profile));
        List<String> cmd = new ArrayList<>();
        cmd.add(chrome);
        cmd.add("--user-data-dir=" + profile);
        cmd.add("--no-first-run");
        cmd.add("--no-default-browser-check");
        cmd.add("--disable-quic");
        cmd.add("--fingerprint-platform=windows");
        cmd.add("--fingerprint-brand=Chrome");
        cmd.add("--fingerprint-brand-version=150.0.7871.124");
        cmd.add("--fingerprint-platform-version=10.0.0");
        cmd.add("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36");
        cmd.add("--fingerprint-hardware-concurrency=8");
        cmd.add("--fingerprint-device-memory=8");
        cmd.add("--fingerprint-screen=1536x864");
        cmd.add("--fingerprint-device-scale-factor=1.25");
        cmd.add("--fingerprint-screen-color-depth=24");
        cmd.add("--fingerprint-battery=1,1.0,0,Infinity");
        cmd.add("--webrtc-ip-handling-policy=disable_non_proxied_udp");
        cmd.add("--timezone=America/New_York");
        cmd.add("--lang=en-US");
        cmd.add("--accept-lang=en-US,en");
        cmd.add(url);
        new ProcessBuilder(cmd).start();
        System.out.println("已启动 " + chrome);
    }
}
