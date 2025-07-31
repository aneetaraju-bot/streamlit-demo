import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

st.set_page_config(page_title="Batch Health Zone Dashboard", layout="wide")
st.title("📊 Batch Health Zone Dashboard - 4 Types Analysis")

# Uploaders
st.sidebar.header("📂 Upload Your CSV Files")
file_vertical_below = st.sidebar.file_uploader("1️⃣ Vertical-wise BH < 10%", type="csv")
file_vertical_above = st.sidebar.file_uploader("2️⃣ Vertical-wise BH > 50%", type="csv")
file_category_below = st.sidebar.file_uploader("3️⃣ Category-wise BH < 10%", type="csv")
file_category_above = st.sidebar.file_uploader("4️⃣ Category-wise BH > 50%", type="csv")

# Color logic
def get_zone_color_below(val, avg):
    if val > avg + 5:
        return 'red'
    elif avg - 5 <= val <= avg + 5:
        return 'orange'
    else:
        return 'green'

def get_zone_color_above(val, avg):
    if val >= avg + 5:
        return 'green'
    elif avg - 5 <= val <= avg + 5:
        return 'orange'
    else:
        return 'red'

# Chart drawing
def plot_chart(df, title, label_col, is_below=True):
    df["Last week"] = df["Last week"].astype(str).str.replace("%", "").astype(float)
    df["This week"] = df["This week"].astype(str).str.replace("%", "").astype(float)

    labels = df[label_col].tolist()
    last = df["Last week"].tolist()
    now = df["This week"].tolist()

    x = np.arange(len(labels))
    width = 0.35
    avg = np.mean(now)

    colors = [
        get_zone_color_below(v, avg) if is_below else get_zone_color_above(v, avg)
        for v in now
    ]

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.bar(x - width/2, last, width, color='white', edgecolor='black', label='Last Week')
    ax.bar(x + width/2, now, width, color=colors, edgecolor='black', label='This Week')

    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=45, ha='right')
    ax.set_ylabel("Percentage of Batches")
    ax.set_title(f"{title} (Avg: {avg:.2f}%)")

    legend = [
        Patch(facecolor='green', edgecolor='black', label='🟩 Healthy'),
        Patch(facecolor='orange', edgecolor='black', label='🟧 Watch Zone'),
        Patch(facecolor='red', edgecolor='black', label='🟥 Risk'),
        Patch(facecolor='white', edgecolor='black', label='⬜ Last Week'),
        Patch(facecolor='black', edgecolor='black', label='⬛ This Week')
    ]
    ax.legend(handles=legend, loc='upper right', bbox_to_anchor=(1, 1))
    st.pyplot(fig)

# Load and render charts
if file_vertical_below:
    st.subheader("1️⃣ Vertical-wise BH < 10% (Risk Zones)")
    df = pd.read_csv(file_vertical_below)
    df.rename(columns=lambda x: x.strip(), inplace=True)
    plot_chart(df, "Vertical-wise % of Batches Below BH 10%", "Vertical", is_below=True)

if file_vertical_above:
    st.subheader("2️⃣ Vertical-wise BH > 50% (Healthy Zones)")
    df = pd.read_csv(file_vertical_above)
    df.rename(columns=lambda x: x.strip(), inplace=True)
    plot_chart(df, "Vertical-wise % of Batches Above BH 50%", "Vertical", is_below=False)

if file_category_below:
    st.subheader("3️⃣ Category-wise BH < 10% (Risk by Course)")
    df = pd.read_csv(file_category_below)
    df.rename(columns=lambda x: x.strip(), inplace=True)
    plot_chart(df, "Course-wise % of Batches Below BH 10%", "Course", is_below=True)

if file_category_above:
    st.subheader("4️⃣ Category-wise BH > 50% (Healthy by Course)")
    df = pd.read_csv(file_category_above)
    df.rename(columns=lambda x: x.strip(), inplace=True)
    plot_chart(df, "Course-wise % of Batches Above BH 50%", "Course", is_below=False)
