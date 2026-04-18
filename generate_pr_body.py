import io
import os

import qrcode

entry_path = os.environ["ENTRY_PATH"]
entry_url = os.environ["ENTRY_URL"]
issue_number = os.environ["ISSUE_NUMBER"]
final_url = f"https://go.scout.ch/{entry_path}"

qr = qrcode.QRCode(border=1)
qr.add_data(final_url)
qr.make(fit=True)

buffer = io.StringIO()
qr.print_ascii(out=buffer)
ascii_qr = buffer.getvalue()

print(f"""\
Adds redirect:

- **Path**: `{entry_path}`
- **Target**: {entry_url}
- **Short URL**: {final_url}

```
{ascii_qr}```

Closes #{issue_number}
""")
