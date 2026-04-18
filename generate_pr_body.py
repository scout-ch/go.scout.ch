import os

entry_path = os.environ["ENTRY_PATH"]
entry_url = os.environ["ENTRY_URL"]
issue_number = os.environ["ISSUE_NUMBER"]
final_url = f"https://go.scout.ch/{entry_path}"
qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=200x200&data={final_url}"

print(f"""\
Adds redirect:

- **Path**: `{entry_path}`
- **Target**: {entry_url}
- **Short URL**: {final_url}

![QR Code]({qr_url})

Closes #{issue_number}
""")
