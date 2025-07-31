import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

st.set_page_config(page_title="Batch Health Zone Dashboard", layout="wide")
st.title("📊 Batch Health Zone Dashboard - 4 Graphs")

# Upload all 4 files
st.sidebar.header("📂 Upload All 4 CSV Files")
file_v_below = st.sidebar.file_uploader("1️⃣ Vertical-wise BH < 10%", type="csv")
file_v_above = st.sidebar.file_uploader("2️⃣ Vertical-wise BH > 50%", type="csv")
file_c_below = st.sidebar.file_uploader("3️⃣ Category-wise BH < 10%", type="csv")
file_c_above = st.sidebar.file_uploader("4️⃣ Category-wise BH > 50%", type="csv")

# Color logic
def get_color_below(val, avg):
    return 'red' if val > avg + 5 else 'orange' if avg - 5 <= val <= avg + 5 else 'green'

def get_color_above(val, avg):
    return 'green' if val > avg + 5 else 'orange' if avg - 5 <= val <= avg + 5 else 'red'

# Chart function
def draw_zone_graph(df, label_col, is_below, title):
    df["Last week"] = df["Last week"].astype(str).str.replace("%", "").astype(float)
    df["This week"] = df["This week"].astype(str).str.replace("%", "").astype(float)
    
    labels = df[label_col].tolist()
    last = df["Last week"].tolist()
    this = df["This week"].tolist()
    
    avg = np.mean(this)
    x = np.arange(len(labels))
    width = 0.35
    
    zone_colors = [get_color_below(v, avg) if is_below else get_color_above(v, avg) for v in this]

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.bar(x - width/2, last, width, color='white', edgecolor='black', label='Last Week')
    ax.bar(x + width/2, this, width, color=zone_colors, edgecolor='black', label='This Week')

    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=45, ha='right')
    ax.set_ylabel("Batch %")
    ax.set_title(f"{title} (Avg: {avg:.2f}%)")

    # Legend inside plot
    legend_items = [
        Patch(facecolor='green', edgecolor='black', label='🟩 Healthy'),
        Patch(facecolor='orange', edgecolor='black', label='🟧 Watch Zone'),
        Patch(facecolor='red', edgecolor='black', label='🟥 Risk'),
        Patch(facecolor='white', edgecolor='black', label='⬜ Last Week'),
        Patch(facecolor='black', edgecolor='black', label='⬛ This Week'),
    ]
    ax.legend(handles=legend_items, loc='upper right', bbox_to_anchor=(1, 1))
    st.pyplot(fig)

# Process each file
if file_v_below:
    st.subheader("1️⃣ Vertical-wise BH < 10% (Risk)")
    df = pd.read_csv(file_v_below)
    df.columns = df.columns.str.strip()
    draw_zone_graph(df, label_col="Vertical", is_below=True, title="Vertical-wise BH < 10%")

if file_v_above:
    st.subheader("2️⃣ Vertical-wise BH > 50% (Healthy)")
    df = pd.read_csv(file_v_above)
    df.columns = df.columns.str.strip()
    draw_zone_graph(df, label_col="Vertical", is_below=False, title="Vertical-wise BH > 50%")

if file_c_below:
    st.subheader("3️⃣ Category-wise BH < 10% (Risk)")
    df = pd.read_csv(file_c_below)
    df.columns = df.columns.str.strip()
    draw_zone_graph(df, label_col="Category", is_below=True, title="Category-wise BH < 10%")

if file_c_above:
    st.subheader("4️⃣ Category-wise BH > 50% (Healthy)")
    df = pd.read_csv(file_c_above)
    df.columns = df.columns.str.strip()
    draw_zone_graph(df, label_col="Category", is_below=False, title="Category-wise BH > 50%")

if file_category_above:
    st.subheader("4️⃣ Category-wise BH > 50% (Healthy Zones)")
    df = pd.read_csv(file_category_above)
    df.rename(columns=lambda x: x.strip(), inplace=True)
    plot_chart(df, "Category-wise % of Batches Above BH 50%", "Category", is_below=False)
