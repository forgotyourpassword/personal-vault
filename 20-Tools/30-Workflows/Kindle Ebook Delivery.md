# Kindle Ebook Delivery via Anna's Archive / LibGen

Quartz: http://192.168.1.223:8080/20-Tools/30-Workflows/Kindle-Ebook-Delivery

## Status

- **Kindle email:** michaelmolloy89@kindle.com
- **Sender:** michaelmolloy89@gmail.com (via Himalaya SMTP)
- **Ebook source:** [Anna's Archive](https://annas-archive.gl) / [Library Genesis](https://libgen.li)
- **Preferred format:** EPUB only (Amazon deprecated MOBI for Send to Kindle)

## Workflow

### 1. Search for the book

Search Anna's Archive: `https://annas-archive.gl/search?q=[book+title]+[author]`

Or LibGen directly: `https://libgen.li/index.php?req=[book+title]+[author]`

### 2. Select the right format

- **EPUB** — Amazon's supported format, auto-converts on delivery
- **MOBI** ❌ — deprecated by Amazon, won't deliver
- **AZW3** — Kindle-native but not explicitly supported via Send to Kindle
- Avoid PDF for Kindle reading unless no other option

If only MOBI is available, convert to EPUB using Python:

```bash
python3 -m venv /tmp/ebook-venv
source /tmp/ebook-venv/bin/activate
pip install mobi ebooklib
python3 << 'PYEOF'
from ebooklib import epub
import mobi, os

result = mobi.extract("/path/to/book.mobi")
html_path = result[1]

with open(html_path, 'r', encoding='utf-8', errors='replace') as f:
    html = f.read()

book = epub.EpubBook()
book.set_identifier('book-id')
book.set_title('Book Title')
book.add_author('Author Name')
chapter = epub.EpubHtml(title='Content', file_name='book.xhtml', lang='en')
chapter.content = f'<html xmlns="http://www.w3.org/1999/xhtml"><body><div>{html}</div></body></html>'
book.add_item(chapter)
book.toc = [epub.Link('book.xhtml', 'Content', 'book')]
book.add_item(epub.EpubNcx())
book.add_item(epub.EpubNav())
book.spine = ['nav', chapter]
epub.write_epub("/path/to/output.epub", book, {})
PYEOF
```

### 3. Download from LibGen

LibGen download flow:
1. Click the title to go to `ads.php?md5=...`
2. Click **GET** to get the download link (redirects through Cloudflare CDN)
3. Sometimes there's a 30-second wait before the download link appears
4. If one CDN fails (502/500 error), try a different book version
5. The direct URL pattern is: `https://cdn[2-5].booksdl.lc/get.php?md5=[MD5]&key=[KEY]`

**Known working approach:** Use `curl` with full browser headers and the key extracted from the `ads.php` GET link:

```
key=$(grep -oP 'key=[A-Za-z0-9]+' page.html | head -1)
curl -L -A "Mozilla/5.0 ..." -o "book.mobi" \
  "https://cdn2.booksdl.lc/get.php?md5=[MD5]&key=$key"
```

### 4. Send to Kindle

Use Himalaya with the MML template. **Important:** file paths must NOT contain spaces or the MML parser fails. Copy to `/tmp/` first if needed.

```bash
cp "/path/to/The Coaching Habit.epub" /tmp/coaching_habit.epub

cat << 'MAILEOF' | himalaya template send
From: michaelmolloy89@gmail.com
To: michaelmolloy89@kindle.com
Subject: Book Title

<#multipart type=mixed>
<#part type=text/plain>
Here's the book.

<#part filename=/tmp/coaching_habit.epub><#/part>
<#/multipart>
MAILEOF
```

## AgentMail (alternate sender)

Inbox: `forgotellen@agentmail.to`  
API key: `AGENTMAIL_API_KEY` in `~/.hermes/scripts/.env`  
⚠️ Inbox-scoped key (`am_us_inbox_...`) has read-only access — cannot send. Would need a full API key for sending.

## Send-to-Kindle Tips

- **Supported formats:** EPUB, PDF, DOCX, HTML, TXT, RTF, PNG, BMP, JPEG, GIF
- **MOBI is NOT supported** — Amazon deprecated it
- **Max attachment size:** 50 MB per file
- **Whitelisted senders:** Only approved email addresses can send (michaelmolloy89@gmail.com is whitelisted)

## Books Already Sent

| Book | Format | Date | Status |
|---|---|---|---|
| *The Coaching Habit* — Michael Bungay Stanier | EPUB | 2026-07-01 | ✅ Sent to Kindle |
| *A Confederacy of Dunces* — John Kennedy Toole | EPUB | 2026-07-01 | ✅ Sent to Kindle |
| *Lonesome Dove* — Larry McMurtry | EPUB | 2026-07-01 | ✅ Sent to Kindle |
| *King Sorrow* — Joe Hill | EPUB | 2026-07-01 | ✅ Sent to Kindle |
