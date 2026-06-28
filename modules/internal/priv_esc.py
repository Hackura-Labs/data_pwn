import os
import subprocess

class PrivEsc:
    """Privilege escalation checks for Linux and Windows."""

    def __init__(self, output_dir, logger):
        self.output_dir = output_dir
        self.logger = logger

    def linux_checks(self):
        """Common Linux privilege escalation checks."""
        self.logger.scan("Running Linux privilege escalation checks...")
        checks = {
            "suid_binaries": "find / -perm -4000 -type f 2>/dev/null",
            "sgid_binaries": "find / -perm -2000 -type f 2>/dev/null",
            "writable_paths": "echo $PATH | tr ':' '\\n' | xargs -I{} find {} -writable 2>/dev/null",
            "sudo_list": "sudo -l 2>/dev/null",
            "cron_jobs": "cat /etc/crontab 2>/dev/null",
            "kernel_version": "uname -a",
        }
        results = {}
        for name, cmd in checks.items():
            try:
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=10)
                if result.stdout.strip():
                    results[name] = result.stdout.strip()
                    self.logger.found(f"[PrivEsc] {name}: found output")
            except:
                pass

        out_file = f"{self.output_dir}/privesc_linux.txt"
        with open(out_file, "w") as f:
            for name, output in results.items():
                f.write(f"=== {name} ===\n{output}\n\n")
        if results:
            self.logger.success(f"Linux privesc checks saved to {out_file}")
        return results

    def windows_checks(self):
        """Common Windows privilege escalation checks (stub - runs on Windows targets via SSH/shell)."""
        self.logger.info("Windows privesc checks: extend via SSH session or Meterpreter (stub)")

    def check_kernel_vulns(self):
        """Check for common kernel vulnerabilities (stub)."""
        self.logger.info("Kernel vulnerability check: integrate linux-exploit-suggester or similar (stub)")
