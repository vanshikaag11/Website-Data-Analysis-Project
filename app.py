import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="Website Performance Dashboard",
    layout="wide"
)

# -----------------------------
# TITLE
# -----------------------------
st.title("📊 Website Performance Analysis Dashboard")

st.write(
    "Interactive dashboard for analyzing website traffic, sessions, and engagement."
)

# -----------------------------
# LOAD DATA
# -----------------------------
try:
    df = pd.read_csv("data-export (1).csv", skiprows=1)

    # Rename columns
    df.columns = [
        "Channel group",
        "DateHour",
        "Users",
        "Sessions",
        "Engaged Sessions",
        "Average engagement time per session",
        "Engaged sessions per user",
        "Events per session",
        "Engagement rate",
        "Event count"
    ]

except Exception as e:
    st.error(f"Error loading CSV file: {e}")
    st.stop()

# -----------------------------
# DATA CLEANING
# -----------------------------
try:

    # Convert Date
    df["DateHour"] = pd.to_datetime(
        df["DateHour"],
        format="%Y%m%d%H",
        errors="coerce"
    )

    # Numeric columns
    numeric_cols = [
        "Users",
        "Sessions",
        "Engaged Sessions",
        "Average engagement time per session",
        "Engaged sessions per user",
        "Events per session",
        "Engagement rate",
        "Event count"
    ]

    df[numeric_cols] = df[numeric_cols].apply(
        pd.to_numeric,
        errors="coerce"
    )

    # Hour column
    df["Hour"] = df["DateHour"].dt.hour

except Exception as e:
    st.error(f"Error during data cleaning: {e}")
    st.stop()

# -----------------------------
# SIDEBAR FILTER
# -----------------------------
st.sidebar.header("🔍 Filters")

channels = df["Channel group"].dropna().unique()

selected_channel = st.sidebar.selectbox(
    "Select Channel",
    channels
)

filtered_df = df[df["Channel group"] == selected_channel]

# -----------------------------
# DATA PREVIEW
# -----------------------------
st.subheader("📁 Dataset Preview")

st.dataframe(filtered_df.head())

# -----------------------------
# KPI METRICS
# -----------------------------
st.subheader("📌 Key Metrics")

col1, col2, col3 = st.columns(3)

col1.metric(
    "Total Users",
    int(filtered_df["Users"].sum())
)

col2.metric(
    "Total Sessions",
    int(filtered_df["Sessions"].sum())
)

col3.metric(
    "Average Engagement Rate",
    round(filtered_df["Engagement rate"].mean(), 2)
)

# -----------------------------
# SESSIONS & USERS OVER TIME
# -----------------------------
st.subheader("📈 Sessions and Users Over Time")

try:
    fig1, ax1 = plt.subplots(figsize=(10, 5))

    filtered_df.groupby("DateHour")[["Sessions", "Users"]].sum().plot(ax=ax1)

    ax1.set_title("Sessions and Users Over Time")
    ax1.set_xlabel("DateHour")
    ax1.set_ylabel("Count")

    st.pyplot(fig1)

except Exception as e:
    st.error(f"Error in graph 1: {e}")

# -----------------------------
# TOTAL USERS BY CHANNEL
# -----------------------------
st.subheader("👥 Total Users by Channel")

try:
    fig2, ax2 = plt.subplots(figsize=(8, 5))

    sns.barplot(
        data=df,
        x="Channel group",
        y="Users",
        estimator=np.sum,
        ax=ax2
    )

    plt.xticks(rotation=45)

    st.pyplot(fig2)

except Exception as e:
    st.error(f"Error in graph 2: {e}")

# -----------------------------
# AVG ENGAGEMENT TIME
# -----------------------------
st.subheader("⏱ Average Engagement Time by Channel")

try:
    fig3, ax3 = plt.subplots(figsize=(8, 5))

    sns.barplot(
        data=df,
        x="Channel group",
        y="Average engagement time per session",
        estimator=np.mean,
        ax=ax3
    )

    plt.xticks(rotation=45)

    st.pyplot(fig3)

except Exception as e:
    st.error(f"Error in graph 3: {e}")

# -----------------------------
# ENGAGEMENT RATE DISTRIBUTION
# -----------------------------
st.subheader("📦 Engagement Rate Distribution")

try:
    fig4, ax4 = plt.subplots(figsize=(8, 5))

    sns.boxplot(
        data=df,
        x="Channel group",
        y="Engagement rate",
        ax=ax4
    )

    plt.xticks(rotation=45)

    st.pyplot(fig4)

except Exception as e:
    st.error(f"Error in graph 4: {e}")

# -----------------------------
# ENGAGED VS NON-ENGAGED
# -----------------------------
st.subheader("⚖ Engaged vs Non-Engaged Sessions")

try:
    session_df = df.groupby("Channel group")[
        ["Sessions", "Engaged Sessions"]
    ].sum().reset_index()

    session_df["Non-Engaged"] = (
        session_df["Sessions"] -
        session_df["Engaged Sessions"]
    )

    session_df_melted = session_df.melt(
        id_vars="Channel group",
        value_vars=["Engaged Sessions", "Non-Engaged"]
    )

    fig5, ax5 = plt.subplots(figsize=(8, 5))

    sns.barplot(
        data=session_df_melted,
        x="Channel group",
        y="value",
        hue="variable",
        ax=ax5
    )

    plt.xticks(rotation=45)

    st.pyplot(fig5)

except Exception as e:
    st.error(f"Error in graph 5: {e}")

# -----------------------------
# HEATMAP
# -----------------------------
st.subheader("🔥 Traffic by Hour and Channel")

try:
    heatmap_data = df.groupby(
        ["Hour", "Channel group"]
    )["Sessions"].sum().unstack().fillna(0)

    fig6, ax6 = plt.subplots(figsize=(12, 6))

    sns.heatmap(
        heatmap_data,
        annot=True,
        fmt=".0f",
        linewidths=.5,
        ax=ax6
    )

    st.pyplot(fig6)

except Exception as e:
    st.error(f"Error in graph 6: {e}")

# -----------------------------
# ENGAGEMENT RATE VS SESSIONS
# -----------------------------
st.subheader("📊 Engagement Rate vs Sessions Over Time")

try:
    df_plot = df.groupby("DateHour")[
        ["Engagement rate", "Sessions"]
    ].mean().reset_index()

    fig7, ax7 = plt.subplots(figsize=(10, 5))

    ax7.plot(
        df_plot["DateHour"],
        df_plot["Engagement rate"],
        label="Engagement Rate"
    )

    ax7.plot(
        df_plot["DateHour"],
        df_plot["Sessions"],
        label="Sessions"
    )

    ax7.legend()

    st.pyplot(fig7)

except Exception as e:
    st.error(f"Error in graph 7: {e}")

# -----------------------------
# FOOTER
# -----------------------------
st.write("✅ Dashboard Loaded Successfully")