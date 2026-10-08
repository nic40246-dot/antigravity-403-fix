#!/usr/bin/env python3
"""
Antigravity 403 / 503 VALIDATION_REQUIRED Auto-Fixer
Universal CLI tool for Windows, macOS, and Linux.

Detects 'PERMISSION_DENIED (VALIDATION_REQUIRED)' in logs,
extracts the hidden Google validation URL, launches the browser,
and provides session reset utilities.
"""

import os
import sys
import re
import json
import webbrowser
import platform
import subprocess
import argparse
from datetime import datetime

VERSION = "1.0.0"

# ANSI color codes
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BOLD = "\033[1m"
DIM = "\033[2m"
RESET = "\033[0m"

def get_possible_log_paths():
    """Returns candidate log file paths based on operating system."""
    home = os.path.expanduser("~")
    paths = []

    # Hermes error logs (cross-platform)
    paths.append(os.path.join(home, ".hermes", "logs", "errors.log"))
    paths.append(os.path.join(home, ".hermes", "logs", "agent.log"))

    # OS-specific paths
    system = platform.system()
    if system == "Windows":
        local_appdata = os.environ.get("LOCALAPPDATA", os.path.join(home, "AppData", "Local"))
        appdata = os.environ.get("APPDATA", os.path.join(home, "AppData", "Roaming"))
        
        paths.append(os.path.join(local_appdata, "hermes", "logs", "errors.log"))
        paths.append(os.path.join(local_appdata, "hermes", "logs", "agent.log"))
        paths.append(os.path.join(appdata, "Antigravity", "logs", "language_server.log"))
        paths.append(os.path.join(appdata, "Antigravity", "logs", "main.log"))
    elif system == "Darwin":  # macOS
        paths.append(os.path.join(home, "Library", "Application Support", "Antigravity", "logs", "main.log"))
        paths.append(os.path.join(home, "Library", "Application Support", "Antigravity", "logs", "language_server.log"))
    else:  # Linux / Termux
        paths.append(os.path.join(home, ".config", "Antigravity", "logs", "main.log"))
        paths.append(os.path.join(home, ".config", "Antigravity", "logs", "language_server.log"))

    # Filter to existing files
    return [p for p in paths if os.path.isfile(p)]

def extract_validation_url(file_path):
    """Scans log file backwards for the most recent validation_url."""
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()
    except Exception as e:
        return None, None

    # Search in reverse (most recent first)
    url_pattern = re.compile(r'https://accounts\.google\.com/signin/continue\?[^\s"\'\\]+')
    
    for i in range(len(lines) - 1, -1, -1):
        line = lines[i]
        if "VALIDATION_REQUIRED" in line or "validation_url" in line or "accounts.google.com/signin/continue" in line:
            match = url_pattern.search(line)
            if match:
                clean_url = match.group(0).rstrip('"\',\\')
                # Attempt to extract timestamp from line
                ts_match = re.search(r'\b\d{4}-\d{2}-\d{2}[ T]\d{2}:\d{2}:\d{2}\b', line)
                ts = ts_match.group(0) if ts_match else "recent"
                return clean_url, ts

    return None, None

def reset_session():
    """Kills Antigravity processes and cleans cache files across OS."""
    system = platform.system()
    home = os.path.expanduser("~")
    print(f"\n{YELLOW}[*] Resetting Antigravity sessions and cache...{RESET}")

    if system == "Windows":
        cmd = 'Stop-Process -Name *antigravity* -Force -EA 0; Remove-Item -Recurse -Force "$HOME\\.antigravity","$HOME\\.gemini" -EA 0'
        try:
            subprocess.run(["powershell", "-NoProfile", "-Command", cmd], check=False)
            print(f"{GREEN}[✓] Windows processes stopped and ~/.antigravity, ~/.gemini cache removed.{RESET}")
        except Exception as e:
            print(f"{RED}[!] Error resetting session: {e}{RESET}")
    elif system == "Darwin":
        cmd = "pkill -9 -f Antigravity 2>/dev/null; rm -rf ~/.antigravity ~/.gemini ~/.antigravity-ide"
        subprocess.run(cmd, shell=True)
        print(f"{GREEN}[✓] macOS processes stopped and cache removed.{RESET}")
    else:  # Linux
        cmd = "pkill -9 -f antigravity 2>/dev/null; rm -rf ~/.antigravity ~/.gemini ~/.config/Antigravity"
        subprocess.run(cmd, shell=True)
        print(f"{GREEN}[✓] Linux processes stopped and cache removed.{RESET}")

def main():
    parser = argparse.ArgumentParser(
        description="Antigravity 403 / 503 VALIDATION_REQUIRED Auto-Fixer"
    )
    parser.add_argument("--no-open", action="store_true", help="Do not automatically open browser")
    parser.add_argument("--reset", action="store_true", help="Force reset session and clear cache")
    parser.add_argument("--log", type=str, help="Specify custom log path to inspect")
    parser.add_argument("--version", action="version", version=f"%(prog)s {VERSION}")

    args = parser.parse_args()

    print(f"\n{BOLD}{CYAN}=================================================={RESET}")
    print(f"{BOLD}{CYAN}   Antigravity 403 / 503 Validation Fixer v{VERSION}{RESET}")
    print(f"{DIM}   Cross-platform Google Human Verification Unblocker{RESET}")
    print(f"{BOLD}{CYAN}=================================================={RESET}\n")

    if args.reset:
        reset_session()

    log_files = [args.log] if args.log else get_possible_log_paths()

    if not log_files:
        print(f"{YELLOW}[!] No log files found in default locations.{RESET}")
        print(f"{DIM}Locations checked: ~/.hermes/logs/, Antigravity/logs/{RESET}")
        return

    found_url = None
    found_source = None
    found_time = None

    for log_path in log_files:
        url, ts = extract_validation_url(log_path)
        if url:
            found_url = url
            found_source = log_path
            found_time = ts
            break

    if found_url:
        print(f"{GREEN}{BOLD}[!] VALIDATION_REQUIRED link detected!{RESET}")
        print(f"{DIM}Source:{RESET} {found_source} ({found_time})\n")
        print(f"{BOLD}Google Verification URL:{RESET}")
        print(f"{CYAN}{found_url}{RESET}\n")

        if not args.no_open:
            print(f"{YELLOW}[*] Opening verification URL in your default browser...{RESET}")
            webbrowser.open(found_url)
            print(f"{GREEN}[✓] Browser opened. Complete captcha/sign-in, then retry your task.{RESET}\n")
        else:
            print(f"{YELLOW}[*] Copy and open the link above in the browser where your account is signed in.{RESET}\n")
    else:
        print(f"{GREEN}[✓] No active VALIDATION_REQUIRED errors found in logs.{RESET}")
        print(f"{DIM}Scanned {len(log_files)} log file(s). If you still encounter 403, run with --reset to clear cache.{RESET}\n")

if __name__ == "__main__":
    main()
