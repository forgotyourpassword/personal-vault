#!/usr/bin/env python3
"""
Journal KPI Dashboard — parses daily Obsidian journals and generates
a weekly/monthly habit progress image, then sends it via Telegram.

Usage:
  python3 journal_kpi.py           # generates image, sends to Telegram
  python3 journal_kpi.py --stdout  # just print parsed data (for cron context)
"""

import os
import re
import sys
import json
import requests
import tempfile
from pathlib import Path
from datetime import date, timedelta, datetime

# ── Config ────────────────────────────────────────────────────────────────────
VAULT = Path(os.environ.get("OBSIDIAN_VAULT_PATH", "/home/mike/vault"))
JOURNAL_DIR = VAULT / "Journal" / "Daily"
BOT_TOKEN = None  # loaded from env at runtime
CHAT_ID = None

# ── Parse one journal file ────────────────────────────────────────────────────
def parse_journal(path: Path) -> dict:
    text = path.read_text(errors="ignore")
    result = {"date": path.stem, "exercise": False, "read": False, "nourished": False,
               "led_well": "", "sentence": ""}

    # Checkbox habits — [x] = done
    if re.search(r"-\s*\[x\]\s*Exercised", text, re.IGNORECASE):
        result["exercise"] = True
    if re.search(r"-\s*\[x\]\s*Read", text, re.IGNORECASE):
        result["read"] = True
    if re.search(r"-\s*\[x\]\s*Nourished", text, re.IGNORECASE):
        result["nourished"] = True

    # Prose habits — "- **Exercise:** Yes" / "- **Ate well:** Yes" format
    # Bold markers may wrap label+colon: **Exercise:** or just Exercise:
    if not result["exercise"] and re.search(r"-\s*\**Exercise[:\*]+\s*Yes", text, re.IGNORECASE):
        result["exercise"] = True
    if not result["read"] and re.search(r"-\s*\**Read[:\*]+\s*Yes", text, re.IGNORECASE):
        result["read"] = True
    if not result["nourished"] and re.search(
        r"-\s*\**(Nourished|Ate well|Nutrition|Nourishment)[:\*]+\s*Yes", text, re.IGNORECASE
    ):
        result["nourished"] = True

    # One sentence
    m = re.search(r"##\s*One sentence on today\s*\n(.+)", text, re.IGNORECASE)
    if m:
        result["sentence"] = m.group(1).strip()

    # Led well
    m = re.search(r"One thing I led well today:\s*(.+)", text, re.IGNORECASE)
    if m:
        result["led_well"] = m.group(1).strip()[:80]

    return result


# ── Gather date range ─────────────────────────────────────────────────────────
def load_days(days_back: int = 30) -> list[dict]:
    today = date.today()
    results = []
    for i in range(days_back - 1, -1, -1):
        d = today - timedelta(days=i)
        path = JOURNAL_DIR / f"{d}.md"
        if path.exists():
            results.append(parse_journal(path))
        else:
            results.append({"date": str(d), "exercise": None, "read": None,
                            "nourished": None, "sentence": "", "led_well": ""})
    return results


# ── Build the image ───────────────────────────────────────────────────────────
def make_dashboard(days: list[dict]) -> str:
    import math
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    from matplotlib.gridspec import GridSpec
    import numpy as np

    # ── Colour palette ─────────────────────────────────────────────────────────
    BG      = "#0d0f14"
    CARD    = "#161922"
    CARD2   = "#1e2130"   # slightly lighter card for contrast
    ACCENT  = "#7c6af7"   # purple
    GREEN   = "#22c55e"
    YELLOW  = "#f59e0b"
    RED     = "#ef4444"
    GREY    = "#2d3548"
    GRIDFG  = "#2a2f42"
    TEXT    = "#f1f5f9"
    SUBTEXT = "#8b95aa"

    today = date.today()

    # ── Data: use ALL days in range as denominator (not just journaled ones) ───
    week_days  = days[-7:]    # last 7 calendar days
    month_days = days         # all 30 calendar days

    def pct(items, key):
        """Count True/False/None; None = no entry = counts as miss."""
        total = len(items)
        if total == 0:
            return 0
        done = sum(1 for d in items if d[key] is True)
        return round(100 * done / total)

    w_ex = pct(week_days,  "exercise")
    w_rd = pct(week_days,  "read")
    w_nu = pct(week_days,  "nourished")
    m_ex = pct(month_days, "exercise")
    m_rd = pct(month_days, "read")
    m_nu = pct(month_days, "nourished")
    streak = _streak(days)

    # ── Figure & grid ──────────────────────────────────────────────────────────
    fig = plt.figure(figsize=(13, 9), facecolor=BG)
    gs  = GridSpec(3, 4, figure=fig, hspace=0.60, wspace=0.40,
                   left=0.05, right=0.97, top=0.92, bottom=0.07)

    # ── Title ──────────────────────────────────────────────────────────────────
    fig.text(0.5, 0.965, "Michael's Progress Dashboard",
             ha="center", va="top", color=TEXT, fontsize=20, fontweight="bold",
             fontfamily="DejaVu Sans")
    fig.text(0.5, 0.932, f"Week of {(today - timedelta(days=6)).strftime('%b %d')} – {today.strftime('%b %d, %Y')}",
             ha="center", va="top", color=SUBTEXT, fontsize=11)

    # ── Helper: proper donut using Arc patches ─────────────────────────────────
    def donut(ax, value, label, color, week_label="This Week"):
        ax.set_facecolor(CARD)
        for spine in ax.spines.values():
            spine.set_visible(False)
        ax.set_xticks([]); ax.set_yticks([])
        ax.set_xlim(-1, 1); ax.set_ylim(-1, 1)
        ax.set_aspect("equal")

        lw = 14
        r  = 0.62

        # Track (background ring)
        track = mpatches.Arc((0, 0), 2*r, 2*r, angle=0,
                              theta1=0, theta2=360,
                              color=GREY, lw=lw, zorder=2)
        ax.add_patch(track)

        # Progress arc (clockwise from top = start at 90, sweep negative)
        if value > 0:
            arc = mpatches.Arc((0, 0), 2*r, 2*r, angle=0,
                               theta1=90 - 360*value/100, theta2=90,
                               color=color, lw=lw, zorder=3)
            ax.add_patch(arc)

        # Center text
        ax.text(0,  0.14, f"{value}%", ha="center", va="center",
                color=TEXT, fontsize=17, fontweight="bold", zorder=4)
        ax.text(0, -0.14, label, ha="center", va="center",
                color=TEXT, fontsize=9, zorder=4)
        ax.text(0, -0.36, week_label, ha="center", va="center",
                color=SUBTEXT, fontsize=8, zorder=4)

    # ── Helper: daily bar chart ────────────────────────────────────────────────
    def mini_bar(ax, values, labels, color, title):
        ax.set_facecolor(CARD)
        for spine in ax.spines.values():
            spine.set_visible(False)
        bar_colors = [GREEN if v is True else (RED if v is False else GREY) for v in values]
        bars = ax.bar(range(len(values)), [1]*len(values), color=bar_colors,
                      width=0.72, zorder=2, edgecolor=BG, linewidth=0.5)
        ax.set_xticks(range(len(values)))
        ax.set_xticklabels(labels, color=SUBTEXT, fontsize=7.5, rotation=0)
        ax.set_yticks([])
        ax.set_ylim(0, 1.75)
        ax.set_xlim(-0.6, len(values) - 0.4)
        ax.set_title(title, color=TEXT, fontsize=9.5, pad=8, fontweight="semibold")
        for i, v in enumerate(values):
            sym = "✓" if v is True else ("✗" if v is False else "–")
            clr = GREEN if v is True else (RED if v is False else SUBTEXT)
            ax.text(i, 1.2, sym, ha="center", color=clr, fontsize=10, fontweight="bold", zorder=3)

    # ── Row 0: weekly donuts ───────────────────────────────────────────────────
    donut(fig.add_subplot(gs[0, 0]), w_ex, "Exercise",    GREEN)
    donut(fig.add_subplot(gs[0, 1]), w_rd, "Reading",     ACCENT)
    donut(fig.add_subplot(gs[0, 2]), w_nu, "Nourishment", YELLOW)

    # Streak card
    ax_streak = fig.add_subplot(gs[0, 3])
    ax_streak.set_facecolor(CARD2)
    for spine in ax_streak.spines.values():
        spine.set_visible(False)
    ax_streak.set_xticks([]); ax_streak.set_yticks([])
    ax_streak.text(0.5, 0.62, str(streak["all"]), ha="center", va="center",
                   color=ACCENT, fontsize=44, fontweight="bold",
                   transform=ax_streak.transAxes)
    ax_streak.text(0.5, 0.28, "Day Streak", ha="center", va="center",
                   color=TEXT, fontsize=10, transform=ax_streak.transAxes)
    ax_streak.text(0.5, 0.13, "all 3 habits", ha="center", va="center",
                   color=SUBTEXT, fontsize=8, transform=ax_streak.transAxes)

    # ── Row 1: mini bars for last 7 days ──────────────────────────────────────
    recent  = days[-7:]
    dlabels = [d["date"][-5:].replace("-", "/") for d in recent]

    mini_bar(fig.add_subplot(gs[1, 0]), [d["exercise"]  for d in recent], dlabels, GREEN,  "Exercise (7d)")
    mini_bar(fig.add_subplot(gs[1, 1]), [d["read"]      for d in recent], dlabels, ACCENT, "Reading (7d)")
    mini_bar(fig.add_subplot(gs[1, 2]), [d["nourished"] for d in recent], dlabels, YELLOW, "Nourishment (7d)")

    # 30-day stats card
    ax_mo = fig.add_subplot(gs[1, 3])
    ax_mo.set_facecolor(CARD2)
    for spine in ax_mo.spines.values():
        spine.set_visible(False)
    ax_mo.set_xticks([]); ax_mo.set_yticks([])
    ax_mo.text(0.5, 0.88, "30-Day Average", ha="center", color=TEXT,
               fontsize=9.5, fontweight="bold", transform=ax_mo.transAxes)
    # Draw coloured stat rows
    stats = [
        ("Exe",  f"{m_ex}%", GREEN,  0.68),
        ("Read", f"{m_rd}%", ACCENT, 0.50),
        ("Nour", f"{m_nu}%", YELLOW, 0.32),
    ]
    for icon, val, clr, y in stats:
        ax_mo.text(0.22, y, icon, ha="center", color=clr, fontsize=9,
                   transform=ax_mo.transAxes)
        ax_mo.text(0.72, y, val, ha="center", color=clr, fontsize=13,
                   fontweight="bold", transform=ax_mo.transAxes)
    ax_mo.text(0.5, 0.12, f"based on {len(month_days)} days", ha="center",
               color=SUBTEXT, fontsize=7.5, transform=ax_mo.transAxes)

    # ── Row 2: trend line (trim leading all-None days) ────────────────────────
    first_entry = next((i for i, d in enumerate(days)
                        if d["exercise"] is not None), 0)
    trend_days = days[first_entry:]

    ax_trend = fig.add_subplot(gs[2, :3])
    ax_trend.set_facecolor(CARD)
    for spine in ax_trend.spines.values():
        spine.set_edgecolor(GRIDFG)
    ax_trend.set_title("Habit Trend — 7-day rolling avg  (solid days only)",
                       color=TEXT, fontsize=9, pad=8)
    ax_trend.tick_params(colors=SUBTEXT)
    ax_trend.grid(True, color=GRIDFG, lw=0.5, linestyle="--", alpha=0.6)

    def rolling(vals, w=7):
        out = []
        for i in range(len(vals)):
            sl = [v for v in vals[max(0,i-w+1):i+1] if v is not None]
            out.append(round(100*sum(sl)/len(sl)) if sl else 0)
        return out

    xs = list(range(len(trend_days)))
    xl = [d["date"][-5:] for d in trend_days]
    ax_trend.plot(xs, rolling([d["exercise"]  for d in trend_days]),
                  color=GREEN,  lw=2.2, label="Exercise", zorder=3)
    ax_trend.plot(xs, rolling([d["read"]      for d in trend_days]),
                  color=ACCENT, lw=2.2, label="Reading", zorder=3)
    ax_trend.plot(xs, rolling([d["nourished"] for d in trend_days]),
                  color=YELLOW, lw=2.2, label="Nourishment", zorder=3)
    ax_trend.set_ylim(-5, 115)
    ax_trend.set_yticks([0, 25, 50, 75, 100])
    ax_trend.yaxis.set_tick_params(labelcolor=SUBTEXT, labelsize=8)
    ax_trend.axhline(80, color=GREY, lw=1.0, ls="--", alpha=0.7, zorder=1)
    ax_trend.text(len(trend_days) - 0.5, 82, "80%", color=SUBTEXT, fontsize=7, va="bottom", ha="right")
    tick_step = max(1, len(trend_days) // 8)
    tick_idx  = list(range(0, len(trend_days), tick_step))
    ax_trend.set_xticks(tick_idx)
    ax_trend.set_xticklabels([xl[i] for i in tick_idx],
                              color=SUBTEXT, fontsize=8, rotation=20, ha="right")
    ax_trend.legend(loc="upper left", fontsize=8.5, facecolor=CARD2,
                    edgecolor=GRIDFG, labelcolor=TEXT, framealpha=0.9)
    ax_trend.set_facecolor(CARD)

    # ── Row 2 col 3: today's sentence ─────────────────────────────────────────
    ax_q = fig.add_subplot(gs[2, 3])
    ax_q.set_facecolor(CARD2)
    for spine in ax_q.spines.values():
        spine.set_visible(False)
    ax_q.set_xticks([]); ax_q.set_yticks([])

    last_sentence = next((d["sentence"] for d in reversed(days) if d.get("sentence")), "")
    # word-wrap at ~18 chars per line, max 5 lines
    words = last_sentence.split()
    lines_q, line = [], []
    for w in words:
        line.append(w)
        if len(" ".join(line)) > 18:
            lines_q.append(" ".join(line[:-1]))
            line = [w]
    if line:
        lines_q.append(" ".join(line))
    quote_text = "\n".join(lines_q[:5])

    ax_q.text(0.5, 0.88, "Today", ha="center", color=TEXT,
              fontsize=9.5, fontweight="bold", transform=ax_q.transAxes)
    ax_q.text(0.5, 0.58, f'"{quote_text}"' if quote_text else "(no entry yet)",
              ha="center", va="center", color=TEXT, fontsize=8.5,
              style="italic" if quote_text else "normal",
              transform=ax_q.transAxes, multialignment="center")
    ax_q.text(0.5, 0.10, f"— {today.strftime('%b %d')}", ha="center",
              color=SUBTEXT, fontsize=8, transform=ax_q.transAxes)

    # ── Save ───────────────────────────────────────────────────────────────────
    out = tempfile.mktemp(suffix=".png")
    fig.savefig(out, dpi=160, bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    return out


# ── Streak calculation ─────────────────────────────────────────────────────────
def _streak(days):
    streak_all = 0
    for d in reversed(days):
        if d["exercise"] and d["read"] and d["nourished"]:
            streak_all += 1
        elif d["exercise"] is None:
            continue
        else:
            break
    return {"all": streak_all}


# ── Send to Telegram ───────────────────────────────────────────────────────────
def send_telegram_photo(image_path: str, caption: str):
    token = os.environ.get("TELEGRAM_BOT_TOKEN", "")
    chat  = os.environ.get("TELEGRAM_HOME_CHANNEL", "")
    if not token or not chat:
        # load from .env file
        env_file = Path.home() / ".hermes" / ".env"
        if env_file.exists():
            for line in env_file.read_text().splitlines():
                if line.startswith("TELEGRAM_BOT_TOKEN=") and not token:
                    token = line.split("=", 1)[1].strip()
                if line.startswith("TELEGRAM_HOME_CHANNEL=") and not chat:
                    chat = line.split("=", 1)[1].strip()
    if not token or not chat:
        print("ERROR: TELEGRAM_BOT_TOKEN or TELEGRAM_HOME_CHANNEL not set", file=sys.stderr)
        sys.exit(1)

    url = f"https://api.telegram.org/bot{token}/sendPhoto"
    with open(image_path, "rb") as f:
        resp = requests.post(url, data={"chat_id": chat, "caption": caption,
                                        "parse_mode": "HTML"}, files={"photo": f})
    if resp.status_code == 200:
        print("Sent to Telegram OK")
    else:
        print(f"Telegram error: {resp.status_code} {resp.text}", file=sys.stderr)
        sys.exit(1)


# ── Main ───────────────────────────────────────────────────────────────────────
def main():
    days = load_days(30)

    if "--stdout" in sys.argv:
        # Just print parsed JSON for cron context injection
        print(json.dumps(days, indent=2))
        return

    image = make_dashboard(days)

    today_str = date.today().strftime("%A, %B %d")
    week_days = [d for d in days[-7:] if d["exercise"] is not None]
    w_ex = round(100 * sum(d["exercise"] for d in week_days if d["exercise"]) / max(len(week_days),1))
    w_rd = round(100 * sum(d["read"] for d in week_days if d["read"]) / max(len(week_days),1))
    w_nu = round(100 * sum(d["nourished"] for d in week_days if d["nourished"]) / max(len(week_days),1))
    streak = _streak(days)["all"]

    caption = (
        f"<b>Weekly KPI Dashboard — {today_str}</b>\n\n"
        f"This week:\n"
        f"  💪 Exercise:    {w_ex}%\n"
        f"  📚 Reading:     {w_rd}%\n"
        f"  🥗 Nutrition:   {w_nu}%\n\n"
        f"🔥 All-habits streak: <b>{streak} day{'s' if streak != 1 else ''}</b>"
    )

    send_telegram_photo(image, caption)
    os.unlink(image)


if __name__ == "__main__":
    main()
