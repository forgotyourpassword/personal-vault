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

    # Prose habits — "- **Exercise:** Yes" / "- Exercise: Yes" / "- **Ate well:** Yes"
    # Handles optional bold markers (**), varied labels, plain or bolded format
    if not result["exercise"] and re.search(r"-\s*\**Exercise\**[:\s]+Yes", text, re.IGNORECASE):
        result["exercise"] = True
    if not result["read"] and re.search(r"-\s*\**Read(?:ing)?\**[:\s]+Yes", text, re.IGNORECASE):
        result["read"] = True
    if not result["nourished"] and re.search(
        r"-\s*\**(Nourished|Ate well|Nutrition|Nourishment|Food)\**[:\s]+Yes", text, re.IGNORECASE
    ):
        result["nourished"] = True

    # One sentence — try multiple heading variants
    m = re.search(r"##\s*(?:Today in )?One [Ss]entence.*?\n(.+)", text, re.IGNORECASE)
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


# ── Build the image ───────────────────────────────────────────────────────────
def make_dashboard(days: list[dict]) -> str:
    import math
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    from matplotlib.gridspec import GridSpec, GridSpecFromSubplotSpec
    from matplotlib.patches import FancyBboxPatch
    import numpy as np

    # ── Colour palette ─────────────────────────────────────────────────────────
    BG      = "#0a0c12"        # near-black background
    CARD    = "#13161f"        # primary card
    CARD2   = "#1a1e2e"        # secondary card (slightly lighter)
    CARD3   = "#1f2437"        # tertiary (hover-ish)
    ACCENT  = "#7c6af7"        # purple — reading
    GREEN   = "#22c55e"        # exercise
    YELLOW  = "#f59e0b"        # nourishment
    RED     = "#f43f5e"        # miss
    GREY    = "#2a3050"        # track / inactive
    GRIDFG  = "#252a3d"        # grid lines
    TEXT    = "#f0f4ff"        # primary text
    SUBTEXT = "#7b87a0"        # secondary text
    DIM     = "#454e6a"        # very dim text / decorative
    WHITE   = "#ffffff"

    # Habit config: label, color, key
    HABITS = [
        ("Exercise",    GREEN,  "exercise"),
        ("Reading",     ACCENT, "read"),
        ("Nourishment", YELLOW, "nourished"),
    ]

    today = date.today()

    # ── Data ───────────────────────────────────────────────────────────────────
    week_days  = days[-7:]
    month_days = days

    def pct(items, key):
        total = len(items)
        if total == 0:
            return 0
        done = sum(1 for d in items if d[key] is True)
        return round(100 * done / total)

    w_vals = [pct(week_days,  h[2]) for h in HABITS]
    m_vals = [pct(month_days, h[2]) for h in HABITS]
    streak = _streak(days)["all"]

    # ── Figure ─────────────────────────────────────────────────────────────────
    fig = plt.figure(figsize=(14, 10), facecolor=BG, dpi=160)

    # 3 rows × 4 cols
    gs = GridSpec(
        3, 4, figure=fig,
        hspace=0.55, wspace=0.35,
        left=0.04, right=0.97,
        top=0.91, bottom=0.06,
        height_ratios=[1.1, 1.0, 1.2],
    )

    # ── Header ─────────────────────────────────────────────────────────────────
    week_start = (today - timedelta(days=6)).strftime("%b %d")
    week_end   = today.strftime("%b %d, %Y")

    fig.text(0.5, 0.968, "Michael's Progress Dashboard",
             ha="center", va="top", color=WHITE,
             fontsize=22, fontweight="bold", fontfamily="DejaVu Sans")
    fig.text(0.5, 0.937, f"Week of {week_start} – {week_end}",
             ha="center", va="top", color=SUBTEXT, fontsize=11.5)

    # Thin accent line under header
    fig.add_artist(plt.Line2D([0.04, 0.97], [0.924, 0.924],
                              transform=fig.transFigure,
                              color=GRIDFG, lw=1.0, zorder=0))

    # ── Helper: draw a rounded card background ─────────────────────────────────
    def card_bg(ax, color=CARD, alpha=1.0):
        ax.set_facecolor(color)
        for spine in ax.spines.values():
            spine.set_visible(False)
        ax.set_xticks([])
        ax.set_yticks([])

    # ── Helper: donut gauge ────────────────────────────────────────────────────
    def donut(ax, value, label, color):
        card_bg(ax, CARD)
        ax.set_xlim(-1.15, 1.15)
        ax.set_ylim(-1.15, 1.15)
        ax.set_aspect("equal")

        lw = 18
        r  = 0.65

        # Shadow ring (depth effect)
        shadow = mpatches.Arc((0.03, -0.03), 2*r, 2*r, angle=0,
                              theta1=0, theta2=360,
                              color="#000000", lw=lw+4, zorder=1, alpha=0.25)
        ax.add_patch(shadow)

        # Track ring
        track = mpatches.Arc((0, 0), 2*r, 2*r, angle=0,
                              theta1=0, theta2=360,
                              color=GREY, lw=lw, zorder=2)
        ax.add_patch(track)

        # Glow effect behind progress arc (slightly wider, more transparent)
        if value > 0:
            glow = mpatches.Arc((0, 0), 2*r, 2*r, angle=0,
                                theta1=90 - 360*value/100, theta2=90,
                                color=color, lw=lw+6, zorder=2, alpha=0.18)
            ax.add_patch(glow)

            arc = mpatches.Arc((0, 0), 2*r, 2*r, angle=0,
                               theta1=90 - 360*value/100, theta2=90,
                               color=color, lw=lw, zorder=3)
            ax.add_patch(arc)

            # Dot at start of arc (cap)
            end_angle = math.radians(90 - 360*value/100)
            ex_pt = r * math.cos(end_angle)
            ey_pt = r * math.sin(end_angle)
            ax.plot(ex_pt, ey_pt, "o", color=color, ms=lw*0.22, zorder=4)

        # Center percentage
        ax.text(0,  0.18, f"{value}%",
                ha="center", va="center", color=WHITE,
                fontsize=20, fontweight="bold", zorder=5)
        # Label
        ax.text(0, -0.12, label,
                ha="center", va="center", color=TEXT,
                fontsize=9.5, fontweight="semibold", zorder=5)
        # "This Week" sub-label
        ax.text(0, -0.38, "this week",
                ha="center", va="center", color=SUBTEXT,
                fontsize=8, zorder=5)

        # Thin color accent line at bottom of card
        ax.axhline(-1.08, xmin=0.25, xmax=0.75, color=color, lw=2.5, alpha=0.5, zorder=6)

    # ── Row 0: Donuts ──────────────────────────────────────────────────────────
    for col, (label, color, key) in enumerate(HABITS):
        donut(fig.add_subplot(gs[0, col]), w_vals[col], label, color)

    # Streak card
    ax_streak = fig.add_subplot(gs[0, 3])
    card_bg(ax_streak, CARD2)
    ax_streak.set_xlim(0, 1)
    ax_streak.set_ylim(0, 1)

    # Streak icon — use text symbol instead of emoji (font compatibility)
    streak_icon = "★" if streak > 0 else "○"
    ax_streak.text(0.5, 0.78, streak_icon,
                   ha="center", va="center", fontsize=24,
                   color=YELLOW if streak > 0 else DIM,
                   transform=ax_streak.transAxes)
    ax_streak.text(0.5, 0.52, str(streak),
                   ha="center", va="center",
                   color=YELLOW if streak > 0 else SUBTEXT, fontsize=40, fontweight="bold",
                   transform=ax_streak.transAxes)
    ax_streak.text(0.5, 0.28, "Day Streak",
                   ha="center", va="center",
                   color=TEXT, fontsize=10.5, fontweight="semibold",
                   transform=ax_streak.transAxes)
    ax_streak.text(0.5, 0.13, "all 3 habits",
                   ha="center", va="center",
                   color=SUBTEXT, fontsize=8.5,
                   transform=ax_streak.transAxes)

    # ── Helper: 7-day bar chart ────────────────────────────────────────────────
    def mini_bar(ax, values, dates, color, title):
        card_bg(ax, CARD)
        ax.set_xlim(-0.7, 6.7)
        ax.set_ylim(0, 2.0)

        day_abbrs = []
        for d in dates:
            try:
                dt = datetime.strptime(d, "%Y-%m-%d")
                day_abbrs.append(dt.strftime("%a")[:2])   # Mo Tu We…
            except Exception:
                day_abbrs.append(d[-5:].replace("-", "/"))

        for i, v in enumerate(values):
            if v is True:
                bar_color = color
                sym, sym_color = "✓", color
            elif v is False:
                bar_color = "#1e2235"
                sym, sym_color = "✗", RED
            else:
                bar_color = "#161922"
                sym, sym_color = "–", DIM

            # Bar with slight rounding illusion via extra alpha rect
            ax.bar(i, 1.0, color=bar_color, width=0.72,
                   zorder=2, edgecolor=BG, linewidth=0.8)

            # Color accent top stripe on completed bars
            if v is True:
                ax.bar(i, 0.06, bottom=0.94, color=color,
                       width=0.72, zorder=3, alpha=0.9)

            # Symbol above bar
            ax.text(i, 1.22, sym, ha="center", va="bottom",
                    color=sym_color, fontsize=11, fontweight="bold", zorder=4)

        # Day labels
        ax.set_xticks(range(7))
        ax.set_xticklabels(day_abbrs, color=SUBTEXT, fontsize=8.5)
        ax.tick_params(axis="x", length=0, pad=3)
        ax.set_yticks([])

        # Title with color dot
        ax.set_title(f"● {title}  (7d)", color=color, fontsize=9.5,
                     pad=9, fontweight="semibold", loc="left")

        # Thin bottom border accent
        ax.axhline(0, color=color, lw=1.5, alpha=0.3, zorder=1)

    # ── Row 1: Bar charts ──────────────────────────────────────────────────────
    recent  = days[-7:]
    dates_r = [d["date"] for d in recent]

    for col, (label, color, key) in enumerate(HABITS):
        mini_bar(fig.add_subplot(gs[1, col]),
                 [d[key] for d in recent], dates_r, color, label)

    # ── 30-day stats card (row 1, col 3) ──────────────────────────────────────
    ax_mo = fig.add_subplot(gs[1, 3])
    card_bg(ax_mo, CARD2)
    ax_mo.set_xlim(0, 1)
    ax_mo.set_ylim(0, 1)

    ax_mo.text(0.5, 0.92, "30-Day Avg",
               ha="center", va="top", color=TEXT,
               fontsize=10, fontweight="bold",
               transform=ax_mo.transAxes)

    # Horizontal divider
    ax_mo.axhline(0.82, color=GRIDFG, lw=0.8)

    row_ys = [0.63, 0.42, 0.21]
    for (label, color, key), y, val in zip(HABITS, row_ys, m_vals):
        short = label[:4]
        # Background pill
        ax_mo.barh(y, 0.82, left=0.09, height=0.14,
                   color=CARD3, zorder=1, transform=ax_mo.transAxes)
        # Fill pill
        fill_w = 0.82 * val / 100
        ax_mo.barh(y, fill_w, left=0.09, height=0.14,
                   color=color, alpha=0.25, zorder=2, transform=ax_mo.transAxes)
        ax_mo.text(0.13, y, short, ha="left", va="center",
                   color=color, fontsize=8.5, fontweight="bold",
                   transform=ax_mo.transAxes)
        ax_mo.text(0.87, y, f"{val}%", ha="right", va="center",
                   color=color, fontsize=11, fontweight="bold",
                   transform=ax_mo.transAxes)

    ax_mo.text(0.5, 0.05, f"last {len(month_days)} days",
               ha="center", va="bottom", color=DIM,
               fontsize=7.5, transform=ax_mo.transAxes)

    # ── Row 2: Trend line ──────────────────────────────────────────────────────
    first_entry = next((i for i, d in enumerate(days)
                        if d["exercise"] is not None), 0)
    trend_days = days[first_entry:]

    ax_trend = fig.add_subplot(gs[2, :3])
    ax_trend.set_facecolor(CARD)
    for spine in ax_trend.spines.values():
        spine.set_edgecolor(GRIDFG)
        spine.set_linewidth(0.7)

    ax_trend.set_title("30-Day Habit Trend  ·  7-day rolling avg",
                       color=TEXT, fontsize=10, pad=10,
                       fontweight="semibold", loc="left")
    ax_trend.tick_params(colors=SUBTEXT, labelsize=8)
    ax_trend.grid(True, color=GRIDFG, lw=0.5, linestyle="--", alpha=0.5)
    ax_trend.set_ylim(-8, 118)
    ax_trend.set_yticks([0, 25, 50, 75, 100])
    ax_trend.yaxis.set_tick_params(labelcolor=SUBTEXT, labelsize=8)

    def rolling(vals, w=7):
        out = []
        for i in range(len(vals)):
            sl = [v for v in vals[max(0, i-w+1):i+1] if v is not None]
            out.append(round(100 * sum(sl) / len(sl)) if sl else 0)
        return out

    xs = list(range(len(trend_days)))
    xl = [d["date"][-5:] for d in trend_days]

    for label, color, key in HABITS:
        ys = rolling([d[key] for d in trend_days])
        # Filled area under curve (subtle)
        ax_trend.fill_between(xs, ys, alpha=0.08, color=color, zorder=1)
        # Main line
        ax_trend.plot(xs, ys, color=color, lw=2.5,
                      label=label, zorder=3, solid_capstyle="round")
        # Dot at last point
        ax_trend.plot(xs[-1], ys[-1], "o", color=color,
                      ms=6, zorder=4)

    # 80% reference line
    ax_trend.axhline(80, color=DIM, lw=1.0, ls="--", alpha=0.6, zorder=1)
    ax_trend.text(len(trend_days) - 0.5, 82, "80% target",
                  color=DIM, fontsize=7.5, va="bottom", ha="right")

    # X-axis ticks
    tick_step = max(1, len(trend_days) // 8)
    tick_idx  = list(range(0, len(trend_days), tick_step))
    ax_trend.set_xticks(tick_idx)
    ax_trend.set_xticklabels([xl[i] for i in tick_idx],
                              color=SUBTEXT, fontsize=8, rotation=20, ha="right")
    ax_trend.set_xlim(-0.5, len(trend_days) - 0.5)

    ax_trend.legend(loc="upper left", fontsize=9,
                    facecolor=CARD2, edgecolor=GRIDFG,
                    labelcolor=TEXT, framealpha=0.95,
                    handlelength=1.6, handleheight=0.8)
    ax_trend.set_facecolor(CARD)

    # ── Row 2 col 3: Today's sentence card ────────────────────────────────────
    ax_q = fig.add_subplot(gs[2, 3])
    card_bg(ax_q, CARD2)
    ax_q.set_xlim(0, 1)
    ax_q.set_ylim(0, 1)

    last_entry = next((d for d in reversed(days) if d.get("sentence")), None)
    sentence   = last_entry["sentence"] if last_entry else ""
    entry_date = last_entry["date"] if last_entry else ""

    # Format date nicely
    try:
        dt_label = datetime.strptime(entry_date, "%Y-%m-%d").strftime("%b %d")
    except Exception:
        dt_label = entry_date

    ax_q.text(0.5, 0.93, "Today in One Sentence",
              ha="center", va="top", color=TEXT,
              fontsize=9, fontweight="bold",
              transform=ax_q.transAxes)
    ax_q.axhline(0.85, color=GRIDFG, lw=0.8)

    # Word-wrap sentence
    if sentence:
        words = sentence.split()
        lines_q, line = [], []
        for w in words:
            line.append(w)
            if len(" ".join(line)) > 22:
                lines_q.append(" ".join(line[:-1]))
                line = [w]
        if line:
            lines_q.append(" ".join(line))
        quote_text = "\n".join(lines_q[:5])

        ax_q.text(0.5, 0.62, f'"{quote_text}"',
                  ha="center", va="center", color=TEXT,
                  fontsize=8.5, style="italic",
                  transform=ax_q.transAxes, multialignment="center",
                  linespacing=1.5)
    else:
        ax_q.text(0.5, 0.55, "(no entry yet)",
                  ha="center", va="center", color=DIM,
                  fontsize=9, transform=ax_q.transAxes)

    ax_q.axhline(0.12, color=GRIDFG, lw=0.8)
    ax_q.text(0.5, 0.06, f"— {dt_label}" if dt_label else "",
              ha="center", va="bottom", color=SUBTEXT,
              fontsize=8, transform=ax_q.transAxes)

    # ── Save ───────────────────────────────────────────────────────────────────
    out = tempfile.mktemp(suffix=".png")
    fig.savefig(out, dpi=160, bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    return out


# ── Send to Telegram ───────────────────────────────────────────────────────────
def send_telegram_photo(image_path: str, caption: str):
    token = os.environ.get("TELEGRAM_BOT_TOKEN", "")
    chat  = os.environ.get("TELEGRAM_HOME_CHANNEL", "")
    if not token or not chat:
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
        print(json.dumps(days, indent=2))
        return

    image = make_dashboard(days)

    today_str = date.today().strftime("%A, %B %d")
    # Use same formula as chart: all 7 calendar days as denominator (None = miss)
    week_all = days[-7:]
    w_ex = round(100 * sum(1 for d in week_all if d["exercise"] is True) / 7)
    w_rd = round(100 * sum(1 for d in week_all if d["read"]     is True) / 7)
    w_nu = round(100 * sum(1 for d in week_all if d["nourished"] is True) / 7)
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
