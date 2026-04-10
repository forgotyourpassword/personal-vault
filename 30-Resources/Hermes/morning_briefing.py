#!/usr/bin/env python3
"""
Morning Briefing Script
Fetches weather, calendar events, news, and a motivational quote,
then formats a daily briefing for delivery via Hermes cron.
"""

import urllib.request
import urllib.parse
import json
import re
import random
from datetime import datetime, date, timezone, timedelta

# ── Config ──────────────────────────────────────────────────────────────────
FAMILY_CAL   = "https://calendar.google.com/calendar/ical/family08964334146044158758%40group.calendar.google.com/private-b0b5dbb3aed56d7672323a4cd01e8fac/basic.ics"
SPORTS_CAL   = "https://calendar.google.com/calendar/ical/nn8c1br511vl1cdiua7fag24og%40group.calendar.google.com/private-240566389f9e3e532390257ff34e6ee7/basic.ics"
QUOTES_FILE  = "/home/mike/vault/10-Areas/Family/Morning Briefing Quotes.md"
WEATHER_ZIP  = "21128"
WEATHER_URL  = f"https://wttr.in/{WEATHER_ZIP}?format=j1"

# ── Helpers ──────────────────────────────────────────────────────────────────

def fetch(url, timeout=10):
    req = urllib.request.Request(url, headers={"User-Agent": "MorningBriefing/1.0"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode("utf-8", errors="replace")


def parse_ical_events(ical_text, target_date, tomorrow_date):
    """Return (today_events, tomorrow_events) as lists of dicts."""
    today_events    = []
    tomorrow_events = []
    current = {}
    lines = ical_text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        # Handle line folding (lines starting with space/tab continue previous)
        while i + 1 < len(lines) and lines[i+1][:1] in (' ', '\t'):
            i += 1
            line = line + lines[i][1:]
        if line == "BEGIN:VEVENT":
            current = {}
        elif line == "END:VEVENT":
            if current:
                ev_date = current.get("date")
                if ev_date == target_date:
                    today_events.append(current)
                elif ev_date == tomorrow_date:
                    tomorrow_events.append(current)
            current = {}
        elif line.startswith("SUMMARY:"):
            current["summary"] = line[8:].strip()
        elif line.startswith("LOCATION:"):
            current["location"] = line[9:].strip().replace("\\,", ",").replace("\\n", " ")
        elif line.startswith("DTSTART"):
            val = line.split(":", 1)[-1].strip().replace("Z", "")
            try:
                if "T" in val:
                    dt = datetime.strptime(val[:15], "%Y%m%dT%H%M%S")
                    current["date"] = dt.date()
                    current["time"] = dt.strftime("%-I:%M %p")
                else:
                    current["date"] = datetime.strptime(val[:8], "%Y%m%d").date()
                    current["time"] = None
            except Exception:
                pass
        i += 1
    return today_events, tomorrow_events


def get_weather():
    try:
        data = json.loads(fetch(WEATHER_URL))
        current = data["current_condition"][0]
        desc    = current["weatherDesc"][0]["value"]
        temp_f  = current["temp_F"]
        feels_f = current["FeelsLikeF"]
        humidity = current["humidity"]

        today_weather = data["weather"][0]
        max_f = today_weather["maxtempF"]
        min_f = today_weather["mintempF"]
        hourly = today_weather.get("hourly", [])
        precip = max((float(h.get("chanceofrain", 0)) for h in hourly), default=0)

        lines = [
            f"Currently {temp_f}°F, feels like {feels_f}°F — {desc}",
            f"High {max_f}°F / Low {min_f}°F | Humidity {humidity}%",
        ]
        if precip >= 30:
            lines.append(f"Rain chance: {int(precip)}% — bring an umbrella")
        return "\n".join(lines)
    except Exception as e:
        return f"Weather unavailable ({e})"


def get_news():
    """Fetch AP and NPR RSS headlines."""
    feeds = {
        "AP Business": "https://feeds.apnews.com/rss/apf-business",
        "AP Top News": "https://feeds.apnews.com/rss/apf-topnews",
        "NPR News":    "https://feeds.npr.org/1001/rss.xml",
    }
    business_headlines = []
    us_headlines       = []

    for source, url in feeds.items():
        try:
            xml = fetch(url, timeout=10)
            titles = re.findall(r"<title><!\[CDATA\[(.*?)\]\]></title>", xml)
            if not titles:
                titles = re.findall(r"<title>(.*?)</title>", xml)
            # Skip feed-level title (first one)
            titles = [t.strip() for t in titles[1:] if t.strip() and "RSS" not in t]
            if "Business" in source:
                business_headlines.extend([(source, t) for t in titles[:5]])
            else:
                us_headlines.extend([(source, t) for t in titles[:5]])
        except Exception:
            pass

    biz_top3 = business_headlines[:3]
    us_top1  = us_headlines[:1]
    return biz_top3, us_top1


def get_quote():
    try:
        with open(QUOTES_FILE, "r") as f:
            content = f.read()
        quotes = re.findall(r'^\d+\.\s+"(.+?)"\s+—\s+(.+)$', content, re.MULTILINE)
        if quotes:
            text, author = random.choice(quotes)
            return f'"{text}" — {author}'
    except Exception:
        pass
    return '"The time is always right to do what is right." — Martin Luther King Jr.'


def is_inperson(event):
    """Filter out reminder-style events without real locations."""
    summary = event.get("summary", "").lower()
    location = event.get("location", "").strip()
    skip_keywords = ["bulk trash", "reminder", "pick up tomorrow", "no school"]
    for kw in skip_keywords:
        if kw in summary:
            return False
    return bool(location)


def format_event(ev):
    summary  = ev.get("summary", "Unknown")
    time_str = ev.get("time")
    location = ev.get("location", "")
    parts = []
    if time_str:
        parts.append(time_str)
    parts.append(summary)
    if location:
        # Trim to first meaningful part of address
        loc_short = location.split(",")[0]
        parts.append(f"@ {loc_short}")
    return " | ".join(parts)


# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    today     = date.today()
    tomorrow  = today + timedelta(days=1)
    day_str   = today.strftime("%A, %B %-d, %Y")

    # Calendars
    family_ical = fetch(FAMILY_CAL)
    sports_ical = fetch(SPORTS_CAL)

    fam_today,  fam_tmrw  = parse_ical_events(family_ical, today, tomorrow)
    spt_today,  spt_tmrw  = parse_ical_events(sports_ical, today, tomorrow)

    all_today  = sorted(fam_today  + spt_today,  key=lambda e: e.get("time") or "")
    tmrw_inperson = [e for e in fam_tmrw + spt_tmrw if is_inperson(e)]

    # Weather
    weather = get_weather()

    # News
    biz_headlines, us_headlines = get_news()

    # Quote
    quote = get_quote()

    # ── Format output ────────────────────────────────────────────────────────
    lines = []
    lines.append(f"Good morning, Michael! ☀️")
    lines.append(f"{day_str}")
    lines.append("")

    lines.append("WEATHER — Perry Hall, MD")
    lines.append(weather)
    lines.append("")

    lines.append("TODAY'S EVENTS")
    if all_today:
        for ev in all_today:
            lines.append(f"  • {format_event(ev)}")
    else:
        lines.append("  No events scheduled today")
    lines.append("")

    if tmrw_inperson:
        lines.append("TOMORROW — IN-PERSON")
        for ev in tmrw_inperson:
            lines.append(f"  • {format_event(ev)}")
        lines.append("")

    lines.append("BUSINESS NEWS")
    if biz_headlines:
        for i, (src, title) in enumerate(biz_headlines, 1):
            lines.append(f"  {i}. {title} [{src}]")
    else:
        lines.append("  Unavailable")
    lines.append("")

    lines.append("TOP US NEWS")
    if us_headlines:
        for src, title in us_headlines:
            lines.append(f"  • {title} [{src}]")
    else:
        lines.append("  Unavailable")
    lines.append("")

    lines.append("QUOTE OF THE DAY")
    lines.append(f"  {quote}")

    print("\n".join(lines))


if __name__ == "__main__":
    main()
