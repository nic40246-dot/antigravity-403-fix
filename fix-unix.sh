#!/usr/bin/env bash
# Antigravity 403 / 503 & Session Reset Helper for macOS and Linux

set -e

echo -e "\033[1;36m==================================================\033[0m"
echo -e "\033[1;36m   Antigravity Fixer for macOS & Linux           \033[0m"
echo -e "\033[1;36m==================================================\033[0m"

# 1. Kill processes
echo -e "\n\033[33m[*] Stopping Antigravity processes...\033[0m"
pkill -9 -f -i antigravity 2>/dev/null || true
echo -e "\033[32m[✓] Antigravity processes stopped.\033[0m"

# 2. Clear cache
echo -e "\n\033[33m[*] Cleaning session cache...\033[0m"
rm -rf ~/.antigravity ~/.gemini ~/.antigravity-ide ~/.config/Antigravity 2>/dev/null || true
if [[ "$OSTYPE" == "darwin"* ]]; then
  security delete-generic-password -s gemini -a antigravity 2>/dev/null || true
fi
echo -e "\033[32m[✓] Cache directories wiped.\033[0m"

# 3. Check for validation_url in logs
LOG_PATHS=(
  "$HOME/.hermes/logs/errors.log"
  "$HOME/.hermes/logs/agent.log"
  "$HOME/Library/Application Support/Antigravity/logs/language_server.log"
  "$HOME/.config/Antigravity/logs/language_server.log"
)

FOUND_URL=""

for log in "${LOG_PATHS[@]}"; do
  if [ -f "$log" ]; then
    URL=$(grep -oE 'https://accounts\.google\.com/signin/continue\?[^"'\'' \t\r\n\\]+' "$log" | tail -n 1 || true)
    if [ -n "$URL" ]; then
      FOUND_URL="$URL"
      break
    fi
  fi
done

if [ -n "$FOUND_URL" ]; then
  echo -e "\n\033[1;33m[!] Found Google Human Verification URL:\033[0m"
  echo -e "\033[36m$FOUND_URL\033[0m"
  echo -e "\n\033[33m[*] Launching in browser...\033[0m"
  if command -v xdg-open >/dev/null 2>&1; then
    xdg-open "$FOUND_URL"
  elif command -v open >/dev/null 2>&1; then
    open "$FOUND_URL"
  else
    echo -e "\033[33m[!] Please copy the URL above and open it in your browser.\033[0m"
  fi
  echo -e "\033[32m[✓] Complete verification in browser, then restart Antigravity.\033[0m"
else
  echo -e "\n\033[32m[✓] No pending validation URLs detected. Session cleaned successfully.\033[0m"
fi
