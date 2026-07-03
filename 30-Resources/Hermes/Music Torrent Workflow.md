---
tags:
  - resource
  - systems
  - bittorrent
  - music
created: 2026-07-02
---

# Music Torrent Workflow

Quartz: http://192.168.1.223:8080/30-Resources/Hermes/Music-Torrent-Workflow

## Overview

Music torrent acquisition via Bitsearch.to → qBittorrent. Used for artist discographies, Billboard compilations, and pop music.

## Source: Bitsearch.to

Bitsearch.to is the primary music source. It's curl-friendly (no auth, plain HTML), returns clean results, and has good coverage for mainstream artists. 1377x is unusable for music (adult-content noise).

**Python search pattern** (from the torrent-media-workflow skill):

```python
import urllib.request, urllib.parse, re
from html import unescape

BASE = 'https://bitsearch.to'

def search(query):
    url = BASE + '/search?q=' + urllib.parse.quote(query)
    data = urllib.request.urlopen(
        urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'}),
        timeout=25).read().decode('utf-8', 'ignore')
    
    results = []
    for m in re.finditer(r'<a[^>]*href="(magnet:\?[^"]+)"', data):
        mag = unescape(m.group(1))
        qsp = urllib.parse.parse_qs(urllib.parse.urlparse(mag).query)
        xt = qsp.get('xt', [''])[0]
        h = xt.rsplit(':', 1)[-1].lower()
        dn = urllib.parse.unquote_plus(
            qsp.get('dn', [''])[0]).replace('[Bitsearch.to] ', '')
        if h and dn:
            results.append((h, dn, mag))
    
    # Dedup by hash — Bitsearch returns same magnet twice
    seen = set()
    return [(h, dn, mag) for h, dn, mag in results if h not in seen and seen.add(h) is None]
```

## Rate Limiting

**Bitsearch returns HTTP 429 after ~6 rapid queries.** Critical patterns:

- Sleep **3+ seconds** between searches
- On 429, back off 5s × attempt number (up to 3 retries)
- Search quality degrades before the 429 — the first ~6 results per batch are the best

## Filtering False Positives

Search results need aggressive filtering. Always:

1. **Verify artist name** is in the result (`swift`/`taylor` or `jackson`/`michael`)
2. **Skip non-music**: `video`, `dvd`, `avi`, `xvid`, `karaoke`, `instrumental`, `documentary`
3. **Skip whisky**: "Michael Jackson" also matches the whisky writer — filter `whisky`, `whiskey`, `malt`
4. **Skip international noise**: `italian` documentaries appear for MJ

## Scoring

Sort by keyword hits on the search query, preferring longer names (more complete):

```python
qwords = [w for w in re.sub(r'[^a-z0-9]+', ' ', query.lower()).split() if len(w) > 2]
scored = []
for h, dn, mag in results:
    n = re.sub(r'[^a-z0-9]+', ' ', dn.lower()).strip()
    hits = sum(1 for w in qwords if w in n)
    scored.append((hits, len(dn), h, dn, mag))
scored.sort(key=lambda x: (x[0], x[1]), reverse=True)
```

## Adding to qBittorrent

Same pattern as audiobooks but with music save path:

```python
# Always explicitly set savepath
op.open(QB_URL + '/api/v2/torrents/add',
    data=urllib.parse.urlencode({
        'urls': magnet,
        'savepath': '/mnt/office-d/Media/Music',
        'category': 'music',
        'paused': 'false'
    }).encode(),
    timeout=20)
```

## Pitfalls

### Magnet failures ("Fails.")

Some torrents consistently fail to add even though they appear in search results. Seen with:
- **Michael Jackson - Dangerous** (individual albums and The Collection 2009): both magnets rejected by qBittorrent
- **Large multi-album compilations**: "The Collection 2009" (Off the Wall + Thriller + Bad + Dangerous + Invincible) — magnet broken

When this happens, try a different search query for the same album. Sometimes a different torrent listing works.

### dn= truncation

Bitsearch truncates the `dn=` parameter in magnets at ~80 chars. The full display name is in the page HTML `<a>` tag text. For identification purposes the truncated `dn` is usually sufficient.

### Whisky false match

"The Essential Michael Jackson" matched a whisky book. Always filter `whisky`/`whiskey`/`malt` when searching for Michael Jackson music.

### Missing albums

Some albums are genuinely absent from Bitsearch:
- **Taylor Swift - Debut (2006)**: No results across multiple query variations
- **Taylor Swift - Speak Now (studio)**: Only the World Tour Live version found, not the studio album
- **Taylor Swift - Midnights**: Required a more specific query ("Taylor Swift Midnights 320") — the first attempt with "Taylor Swift Midnights album" returned nothing

### Query formulation matters

| Query | Result |
|---|---|
| "Michael Jackson Bad album" | No results |
| "Michael Jackson Bad 320kbps mp3" | Found 25th Anniversary Deluxe |
| "Taylor Swift Midnights album" | No results |
| "Taylor Swift Midnights 320" | Found Deluxe Edition |

Adding `320` or `320kbps` often improves results — Bitsearch seems to weight quality tags.

## Session History

### 2026-07-02: Taylor Swift + Michael Jackson discographies

- **16 albums added** (10 TS, 5 MJ + 1 Greatest Hits)
- 3 gaps: TS debut (not on Bitsearch), MJ Dangerous (broken magnet), MJ Got To Be There (not searched)
- 18 searches across 3 batches due to rate limiting
- 429 errors after batch 1 (6 rapid queries) → added 3s delays for batches 2-3

## Related

- [[30-Resources/Hermes/Audiobook Torrent Workflow]]
- [[30-Resources/Hermes/BitTorrent VPN Solution]]