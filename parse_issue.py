import os
import re
import sys


def extract_field(label, text):
    pattern = rf"###\s+{re.escape(label)}\s*\n+(.+?)(?=\n###|\Z)"
    m = re.search(pattern, text, re.DOTALL)
    if not m:
        print(f"ERROR: could not find field '{label}' in issue body", file=sys.stderr)
        sys.exit(1)
    return m.group(1).strip()


body = os.environ["ISSUE_BODY"]
issue_number = os.environ["ISSUE_NUMBER"]

path = extract_field("Path", body)
url = extract_field("Target URL", body)

# Sanitize path: keep only valid segments, allow 1-5 total
segments = [seg for seg in path.split("/") if re.fullmatch(r'[a-zA-Z0-9_-]+', seg)]
if not (1 <= len(segments) <= 5):
    print(f"ERROR: path must have 1-5 valid segments after sanitization, got {len(segments)}", file=sys.stderr)
    sys.exit(1)
path = "/".join(segments)

# Validate URL
if not re.match(r'https?://', url):
    print(f"ERROR: URL must start with http:// or https://", file=sys.stderr)
    sys.exit(1)

branch = f"add-url/issue-{issue_number}"

with open(os.environ["GITHUB_OUTPUT"], "a") as output_file:
    output_file.write(f"path={path}\n")
    output_file.write(f"url={url}\n")
    output_file.write(f"branch={branch}\n")

print(f"Parsed: path={path!r}  url={url!r}  branch={branch!r}")
