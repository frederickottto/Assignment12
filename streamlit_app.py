import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

def load_data():
    hospital = pd.read_csv("hospital.csv")
    county_level = pd.read_csv("county_level.csv")
    population = pd.read_csv("population.csv")
    revenue = pd.read_csv("revenue.csv")
    return {
        "hospital": hospital,
        "county_level": county_level,
        "population": population,
        "revenue": revenue
    }

dfs = load_data()

st.title("California Healthcare Dashboard")

left_col, right_col = st.columns([2,1])

with left_col:
    st.markdown("### Beds vs Gross Inpatient Revenue")
    fig = px.scatter(
        dfs["hospital"],
        x="AVL_BEDS",
        y="GRIP_TOT",
        hover_name="FAC_NAME",
        labels={"AVL_BEDS": "Available Beds", "GRIP_TOT": "Gross Inpatient Revenue"},
        height=600
    )
    st.plotly_chart(fig, use_container_width=True)

with right_col:
    st.markdown("### Net Revenue vs Operating Expenses")
    fig = px.scatter(
        dfs["hospital"],
        x="TOT_OP_EXP",
        y="NET_TOT",
        hover_name="FAC_NAME",
        labels={"TOT_OP_EXP": "Total Operating Expenses", "NET_TOT": "Net Revenue"},
        height=280
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### County Population Distribution")
    fig = px.histogram(
        dfs["population"],
        x="POPULATION",
        nbins=30,
        title=None,
        height=280
    )
    st.plotly_chart(fig, use_container_width=True)
st.markdown("### Capital Expenditure vs Net Revenue")

cap_col_left, cap_col_center, cap_col_right = st.columns([1, 6, 1])

with cap_col_center:
    st.markdown("#### Filter")
    cap_range = st.slider("Capital Expenditure Range", 0, 10_000_000, (0, 10_000_000), step=100_000, label_visibility="visible")
    log_x = st.checkbox("Log Scale for X-Axis (CAP_EXP)", value=False)

    filtered = dfs["hospital"][(dfs["hospital"]["CAP_EXP"] >= cap_range[0]) & 
                                (dfs["hospital"]["CAP_EXP"] <= cap_range[1])]

    import matplotlib.pyplot as plt
    import seaborn as sns

    fig, ax = plt.subplots(figsize=(9, 5))
    sns.scatterplot(data=filtered, x="CAP_EXP", y="NET_TOT", ax=ax)
    if log_x:
        ax.set_xscale("log")
    ax.set_xlabel("Capital Expenditure (USD)")
    ax.set_ylabel("Net Revenue (USD)")
    ax.set_title("Capital Expenditure vs Net Revenue", loc='center')
    st.pyplot(fig)


col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### Top 10 Counties by Revenue")
    top_rev = dfs["county_level"].sort_values("REVENUE", ascending=False).head(10)
    fig = px.bar(
        top_rev,
        x="REVENUE",
        y="COUNTY_NAME",
        orientation='h',
        height=450
    )
    fig.update_layout(yaxis={'categoryorder':'total ascending'})
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown("### Beds per 1,000 vs Revenue")
    fig = px.scatter(
        dfs["county_level"],
        x="AVL_BEDS_PER_THOUSAND",
        y="REVENUE",
        hover_name="COUNTY_NAME",
        height=450
    )
    st.plotly_chart(fig, use_container_width=True)



