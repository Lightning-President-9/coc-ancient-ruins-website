import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import io
import os
from datetime import datetime
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
)
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfgen.canvas import Canvas
from constants import CLAN_MONTHLY_PERFORMANCE_RANGE

# === CONFIG ===
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_URL = f"https://raw.githubusercontent.com/Lightning-President-9/ClanDataRepo/refs/heads/main/Clan%20Members/Clan%20Monthly%20Performance%20JSON/clan_monthly_performance_{CLAN_MONTHLY_PERFORMANCE_RANGE}.json"
CLAN_LOGO = os.path.join(BASE_DIR, "static", "clan-badge_17.png")
WEBSITE_LINK = "https://coc-ancient-ruins-website.onrender.com/"

# Load data
df = pd.read_json(JSON_URL)

METRICS = {
    "War Attacks": "warattack_",
    "Clan Capital": "clancapital_",
    "Clan Games": "clangames_",
    "Clan Games Maxed": "clangamesmaxed_",
    "Clan Score": "clanscore_"
}

plt.style.use('seaborn-v0_8')

# ----------------------------------------
# 🔥 MONTH MAPPING
# ----------------------------------------
MONTH_MAP = {
    "JAN": 1, "FEB": 2, "MAR": 3, "APR": 4,
    "MAY": 5, "JUN": 6, "JUL": 7, "AUG": 8,
    "SEP": 9, "OCT": 10, "NOV": 11, "DEC": 12
}

def extract_all_periods(df):
    """Extract all period names from JSON key prefixes dynamically."""
    periods = set()
    for col in df.columns:
        if "_" in col and any(col.startswith(prefix) for prefix in METRICS.values()):
            period = col.split("_", 1)[1]  # take part after prefix
            periods.add(period)
    return list(periods)

def period_sort_key(period):
    """
    Sort periods like:
    NOV-DEC_2024 → DEC-JAN_2025 → JAN-FEB_2025

    by anchoring to the START month and correcting DEC-JAN year.
    """
    try:
        part, year = period.split("_")
        start_m, end_m = part.split("-")

        year = int(year)

        # 🔥 Critical fix: DEC-JAN belongs to previous year
        if start_m == "DEC" and end_m == "JAN":
            year -= 1

        return datetime(year, MONTH_MAP[start_m], 1)

    except Exception:
        return datetime(9999, 12, 31)

# Footer
def add_footer(canvas: Canvas, doc):
    canvas.saveState()
    footer_text = f"Your Stats, Brought To You By: https://coc-ancient-ruins-website.onrender.com/player-report | Generated on {datetime.now().strftime('%d %B %Y')}"
    canvas.setFont('Helvetica', 8)
    canvas.setFillColor(colors.grey)
    canvas.drawCentredString(A4[0] / 2, 20, footer_text)
    canvas.restoreState()

def get_players():
    return df['name'].tolist()

def generate_player_report(player_name):

    player_data = df[df['name'] == player_name].to_dict(orient='records')[0]

    # ----------------------------------------
    # 🔥 DYNAMIC PERIOD EXTRACTION & SORTING
    # ----------------------------------------
    periods = extract_all_periods(df)
    periods.sort(key=period_sort_key)

    # ----------------------------------------
    # Metric Data Extraction
    # ----------------------------------------
    metric_values = {}
    for metric, prefix in METRICS.items():
        vals = []
        for period in periods:
            val = player_data.get(f"{prefix}{period}", 0)
            if val is None or pd.isna(val) or val < 0:
                val = 0
            vals.append(val)
        metric_values[metric] = vals

    # Peak Performance Table
    peak_data = [["Metric", "Peak Value", "Peak Period"]]
    for metric, vals in metric_values.items():
        peak_idx = vals.index(max(vals)) if max(vals) > 0 else 0
        peak_data.append([metric, max(vals), periods[peak_idx]])

    # === Generate Charts ===
    img_buffers = []

    def create_metric_chart(values, title, color):
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.plot(periods, values, marker='o', color=color, linewidth=2)
        avg = sum(values) / len(values) if values else 0
        ax.axhline(avg, linestyle='--', color='gray', alpha=0.7, label=f"Avg: {avg:.1f}")
        ax.set_title(title, fontsize=14, fontweight='bold', color=color)
        ax.set_xlabel("Period")
        ax.set_ylabel(title)
        ax.grid(True, linestyle='--', alpha=0.6)
        plt.xticks(rotation=45)
        for i, val in enumerate(values):
            ax.text(i, val + (max(values) * 0.05), str(val), ha='center', fontsize=8)
        ax.legend()
        plt.tight_layout()
        buf = io.BytesIO()
        plt.savefig(buf, format='PNG')
        buf.seek(0)
        img_buffers.append(buf)
        plt.close()

    color_palette = ["#1f77b4", "#2ca02c", "#ff7f0e", "#d62728", "#9467bd"]

    for (metric, vals), color in zip(metric_values.items(), color_palette):
        create_metric_chart(vals, metric, color)

    # Combined Line Chart
    fig, ax = plt.subplots(figsize=(8, 4))
    for (metric, vals), color in zip(metric_values.items(), color_palette):
        ax.plot(periods, vals, marker='o', linewidth=2, label=metric, color=color)
    ax.set_title("All Metrics Combined", fontsize=14, fontweight='bold')
    ax.set_xlabel("Period")
    ax.set_ylabel("Value")
    ax.grid(True, linestyle='--', alpha=0.6)
    plt.xticks(rotation=45)
    ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout(rect=[0, 0, 0.8, 1])
    buf = io.BytesIO()
    plt.savefig(buf, format='PNG')
    buf.seek(0)
    img_buffers.append(buf)
    plt.close()

    # Stacked Bar Chart
    fig, ax = plt.subplots(figsize=(8, 4))
    bottom_vals = [0] * len(periods)
    for (metric, vals), color in zip(metric_values.items(), color_palette):
        ax.bar(periods, vals, bottom=bottom_vals, label=metric, color=color)
        bottom_vals = [b + v for b, v in zip(bottom_vals, vals)]
    ax.set_title("Monthly Contribution Breakdown", fontsize=14, fontweight='bold')
    ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.xticks(rotation=45)
    plt.tight_layout(rect=[0, 0, 0.8, 1])
    buf = io.BytesIO()
    plt.savefig(buf, format='PNG')
    buf.seek(0)
    img_buffers.append(buf)
    plt.close()

    # Pie Chart
    totals = [sum(vals) for vals in metric_values.values()]
    fig, ax = plt.subplots(figsize=(6, 6))
    if sum(totals) > 0:
        ax.pie(totals, labels=list(metric_values.keys()), autopct='%1.1f%%',
               colors=color_palette, startangle=140)
        ax.set_title("Overall Contribution Share", fontsize=14, fontweight='bold')
    else:
        ax.text(0.5, 0.5, "No Data Available", ha='center', va='center',
                fontsize=14, color='gray')
        ax.set_title("Overall Contribution Share", fontsize=14, fontweight='bold')
        ax.axis('off')
    buf = io.BytesIO()
    plt.savefig(buf, format='PNG')
    buf.seek(0)
    img_buffers.append(buf)
    plt.close()

    # Heatmap
    heatmap_data = pd.DataFrame(metric_values, index=periods).T
    fig, ax = plt.subplots(figsize=(8, 4))
    sns.heatmap(heatmap_data, annot=True, fmt="g", cmap="YlGnBu", ax=ax)
    ax.set_title("Activity Intensity Heatmap", fontsize=14, fontweight='bold')
    plt.xticks(rotation=45)
    plt.yticks(rotation=0)
    plt.tight_layout()
    buf = io.BytesIO()
    plt.savefig(buf, format='PNG')
    buf.seek(0)
    img_buffers.append(buf)
    plt.close()

    # === PDF BUILD ===
    pdf_buf = io.BytesIO()
    doc = SimpleDocTemplate(
        pdf_buf,
        pagesize=A4,
        title=f"{player_name} Performance Report",
        author="coc-ancient-ruins-website"
    )
    styles = getSampleStyleSheet()
    elements = []

    # Cover Page
    if os.path.exists(CLAN_LOGO):
        elements.append(Image(CLAN_LOGO, width=120, height=120))
    elements.append(Spacer(1, 20))
    elements.append(Paragraph(f"<font size=24 color='#003366'><b>{player_name}</b></font>", styles['Title']))
    elements.append(Spacer(1, 20))
    elements.append(Paragraph("<font size=14 color='#666666'>Performance Report</font>", styles['Normal']))
    elements.append(Spacer(1, 12))
    elements.append(Paragraph(f"<a href='{WEBSITE_LINK}'>{WEBSITE_LINK}</a>", styles['Normal']))
    elements.append(Spacer(1, 12))
    elements.append(Paragraph(
        "This report provides a detailed analysis of the player's performance across "
        "different Clash of Clans activities, including War Attacks, Clan Capital, "
        "Clan Games, and more.",
        styles['Normal']
    ))
    elements.append(Spacer(1, 30))
    elements.append(Paragraph(f"<font size=10 color='#999999'>Generated on {datetime.now().strftime('%d %B %Y')}</font>", styles['Normal']))
    elements.append(Spacer(1, 20))

    # Summary Table
    summary_data = [["Metric", "Total"]] + [[m, sum(v)] for m, v in metric_values.items()]
    summary_table = Table(summary_data, colWidths=[200, 100])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#444444")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black)
    ]))
    elements.append(Paragraph("<b>Summary</b>", styles['Heading2']))
    elements.append(summary_table)
    elements.append(Spacer(1, 12))

    # Peak Performance
    peak_table = Table(peak_data, colWidths=[150, 100, 120])
    peak_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#003366")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black)
    ]))
    elements.append(Paragraph("<b>Peak Performance</b>", styles['Heading2']))
    elements.append(peak_table)
    elements.append(Spacer(1, 20))

    # Charts
    elements.append(Paragraph("<b>Visual Insights</b>", styles['Heading2']))
    for img in img_buffers:
        elements.append(Image(img, width=400, height=250))
        elements.append(Spacer(1, 12))

    doc.build(elements, onFirstPage=add_footer, onLaterPages=add_footer)
    pdf_buf.seek(0)
    return pdf_buf