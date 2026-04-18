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

# Validate path: 2 or 3 slash-separated segments, safe characters only
segments = path.split("/")
if not (2 <= len(segments) <= 3):
    print(f"ERROR: path must have 2 or 3 segments, got {len(segments)}: {path!r}", file=sys.stderr)
    sys.exit(1)
for seg in segments:
    if not re.fullmatch(r'[a-zA-Z0-9_-]+', seg):
        print(f"ERROR: invalid segment {seg!r} — only alphanumerics, hyphens, underscores allowed", file=sys.stderr)
        sys.exit(1)

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
