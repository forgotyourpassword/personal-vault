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
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    from matplotlib.gridspec import GridSpec
    import numpy as np

    # Colour palette
    BG       = "#0f1117"
    CARD     = "#1a1d27"
    ACCENT   = "#7c6af7"   # purple
    GREEN    = "#22c55e"
    YELLOW   = "#f59e0b"
    RED      = "#ef4444"
    GREY     = "#374151"
    TEXT     = "#f1f5f9"
    SUBTEXT  = "#94a3b8"

    today = date.today()
    week_days  = [d for d in days if d["exercise"] is not None][-7:]
    month_days = [d for d in days if d["exercise"] is not None]

    def pct(items, key):
        vals = [d[key] for d in items if d[key] is not None]
        return round(100 * sum(vals) / len(vals)) if vals else 0

    w_ex = pct(week_days, "exercise")
    w_rd = pct(week_days, "read")
    w_nu = pct(week_days, "nourished")
    m_ex = pct(month_days, "exercise")
    m_rd = pct(month_days, "read")
    m_nu = pct(month_days, "nourished")
    streak = _streak(days)

    fig = plt.figure(figsize=(12, 9), facecolor=BG)
    gs  = GridSpec(3, 4, figure=fig, hspace=0.55, wspace=0.45,
                   left=0.06, right=0.97, top=0.91, bottom=0.06)

    # ── Title ──────────────────────────────────────────────────────────────────
    fig.text(0.5, 0.96, "Michael's Progress Dashboard",
             ha="center", va="top", color=TEXT, fontsize=18, fontweight="bold")
    fig.text(0.5, 0.925, f"Week of {(today - timedelta(days=6)).strftime('%b %d')} – {today.strftime('%b %d, %Y')}",
             ha="center", va="top", color=SUBTEXT, fontsize=11)

    # ── Helper: donut ──────────────────────────────────────────────────────────
    def donut(ax, value, label, color, sublabel=""):
        ax.set_facecolor(CARD)
        for spine in ax.spines.values():
            spine.set_visible(False)
        ax.set_xticks([]); ax.set_yticks([])
        radius = 0.38
        theta = 2 * 3.14159 * value / 100
        angles = [i * 0.01 for i in range(int(theta / 0.01) + 1)]
        xs = [radius * __import__("math").cos(a - 3.14159/2) for a in angles]
        ys = [radius * __import__("math").sin(a - 3.14159/2) for a in angles]
        track = plt.Circle((0, 0), radius, color=GREY, fill=False, linewidth=10, zorder=2)
        ax.add_patch(track)
        if angles:
            ax.plot([0] + xs, [0] + ys, color=color, linewidth=10,
                    solid_capstyle="round", zorder=3)
        ax.set_xlim(-0.55, 0.55); ax.set_ylim(-0.55, 0.55)
        ax.text(0, 0.07, f"{value}%", ha="center", va="center",
                color=TEXT, fontsize=16, fontweight="bold")
        ax.text(0, -0.12, label, ha="center", va="center",
                color=SUBTEXT, fontsize=8)
        if sublabel:
            ax.text(0, -0.28, sublabel, ha="center", va="center",
                    color=SUBTEXT, fontsize=7)

    # ── Helper: bar ─────────────────────────────────────────────────────────────
    def mini_bar(ax, values, labels, color, title):
        ax.set_facecolor(CARD)
        for spine in ax.spines.values():
            spine.set_visible(False)
        colors = [GREEN if v else RED if v is False else GREY for v in values]
        ax.bar(range(len(values)), [1]*len(values), color=colors, width=0.85, zorder=2)
        ax.set_xticks(range(len(values)))
        ax.set_xticklabels(labels, color=SUBTEXT, fontsize=7)
        ax.set_yticks([])
        ax.set_ylim(0, 1.6)
        ax.set_title(title, color=TEXT, fontsize=9, pad=6)
        # add X / checkmarks
        for i, v in enumerate(values):
            sym = "✓" if v else ("✗" if v is False else "·")
            clr = GREEN if v else (RED if v is False else GREY)
            ax.text(i, 1.15, sym, ha="center", color=clr, fontsize=9, fontweight="bold")

    # Row 0: weekly donuts
    donut(fig.add_subplot(gs[0, 0]), w_ex, "Exercise",   GREEN,  "This Week")
    donut(fig.add_subplot(gs[0, 1]), w_rd, "Reading",    ACCENT, "This Week")
    donut(fig.add_subplot(gs[0, 2]), w_nu, "Nourishment",YELLOW, "This Week")

    # Streak card
    ax_streak = fig.add_subplot(gs[0, 3])
    ax_streak.set_facecolor(CARD)
    for spine in ax_streak.spines.values():
        spine.set_visible(False)
    ax_streak.set_xticks([]); ax_streak.set_yticks([])
    ax_streak.text(0.5, 0.72, str(streak["all"]), ha="center", va="center",
                   color=ACCENT, fontsize=36, fontweight="bold",
                   transform=ax_streak.transAxes)
    ax_streak.text(0.5, 0.42, "Day Streak", ha="center", va="center",
                   color=TEXT, fontsize=10, transform=ax_streak.transAxes)
    ax_streak.text(0.5, 0.22, "(all 3 habits)", ha="center", va="center",
                   color=SUBTEXT, fontsize=8, transform=ax_streak.transAxes)

    # Row 1: mini bars for last 7 days
    recent = days[-7:]
    dlabels = [d["date"][-5:].replace("-", "/") for d in recent]
    ex_vals = [d["exercise"] for d in recent]
    rd_vals = [d["read"] for d in recent]
    nu_vals = [d["nourished"] for d in recent]

    mini_bar(fig.add_subplot(gs[1, 0]), ex_vals, dlabels, GREEN,  "Exercise (7d)")
    mini_bar(fig.add_subplot(gs[1, 1]), rd_vals, dlabels, ACCENT, "Reading (7d)")
    mini_bar(fig.add_subplot(gs[1, 2]), nu_vals, dlabels, YELLOW, "Nourishment (7d)")

    # Monthly summary card
    ax_mo = fig.add_subplot(gs[1, 3])
    ax_mo.set_facecolor(CARD)
    for spine in ax_mo.spines.values():
        spine.set_visible(False)
    ax_mo.set_xticks([]); ax_mo.set_yticks([])
    lines = [
        ("30-Day Avg", TEXT, 10, 0.82),
        (f"Exercise  {m_ex}%",  GREEN,  9, 0.62),
        (f"Reading   {m_rd}%",  ACCENT, 9, 0.47),
        (f"Nutrition {m_nu}%",  YELLOW, 9, 0.32),
    ]
    for txt, clr, sz, y in lines:
        ax_mo.text(0.5, y, txt, ha="center", color=clr, fontsize=sz,
                   transform=ax_mo.transAxes,
                   fontweight="bold" if sz == 10 else "normal")

    # Row 2: 30-day trend line
    ax_trend = fig.add_subplot(gs[2, :3])
    ax_trend.set_facecolor(CARD)
    for spine in ax_trend.spines.values():
        spine.set_edgecolor(GREY)
    ax_trend.set_title("30-Day Habit Trend (7-day rolling avg)", color=TEXT, fontsize=9, pad=6)

    def rolling(vals, w=7):
        out = []
        for i in range(len(vals)):
            sl = [v for v in vals[max(0,i-w+1):i+1] if v is not None]
            out.append(round(100*sum(sl)/len(sl)) if sl else 0)
        return out

    xs = list(range(len(days)))
    xl = [d["date"][-5:] for d in days]
    ax_trend.plot(xs, rolling([d["exercise"]  for d in days]), color=GREEN,  lw=2, label="Exercise")
    ax_trend.plot(xs, rolling([d["read"]      for d in days]), color=ACCENT, lw=2, label="Reading")
    ax_trend.plot(xs, rolling([d["nourished"] for d in days]), color=YELLOW, lw=2, label="Nutrition")
    ax_trend.set_ylim(0, 110)
    ax_trend.set_yticks([0, 50, 100])
    ax_trend.yaxis.set_tick_params(labelcolor=SUBTEXT, labelsize=8)
    tick_idx = list(range(0, len(days), 5))
    ax_trend.set_xticks(tick_idx)
    ax_trend.set_xticklabels([xl[i] for i in tick_idx], color=SUBTEXT, fontsize=7, rotation=30)
    ax_trend.axhline(80, color=GREY, lw=0.8, ls="--")
    ax_trend.legend(loc="lower right", fontsize=8, facecolor=CARD,
                    edgecolor=GREY, labelcolor=TEXT)
    ax_trend.set_facecolor(CARD)

    # Row 2 col 3: motivational quote / latest sentence
    ax_q = fig.add_subplot(gs[2, 3])
    ax_q.set_facecolor(CARD)
    for spine in ax_q.spines.values():
        spine.set_visible(False)
    ax_q.set_xticks([]); ax_q.set_yticks([])
    last_sentence = next((d["sentence"] for d in reversed(days) if d.get("sentence")), "")
    # wrap
    words = last_sentence.split()
    lines_q, line = [], []
    for w in words:
        line.append(w)
        if len(" ".join(line)) > 20:
            lines_q.append(" ".join(line)); line = []
    if line:
        lines_q.append(" ".join(line))
    quote = "\n".join(lines_q[:4])
    ax_q.text(0.5, 0.65, f'"{quote}"', ha="center", va="center",
              color=SUBTEXT, fontsize=8, style="italic",
              transform=ax_q.transAxes, wrap=True, multialignment="center")
    ax_q.text(0.5, 0.20, "— Today's sentence", ha="center",
              color=GREY, fontsize=7, transform=ax_q.transAxes)

    # Save
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
