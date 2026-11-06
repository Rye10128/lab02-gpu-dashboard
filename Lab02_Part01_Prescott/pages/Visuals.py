# This creates the page for displaying data visualizations.

import streamlit as st
import pandas as pd
import json
import plotly.express as px

# PAGE CONFIGURATION
st.set_page_config(
    page_title="Visuals",
    page_icon="📈",
)

# PAGE TITLE
st.title("Data Visualizations 📈")


# PART 1: GRAPHS FROM data.json
with open("data.json") as f:
    data = json.load(f)
df = pd.DataFrame(data["data_points"])
st.subheader("Raw Data")
st.dataframe(df)

sorted_df = df.sort_values("price")
st.subheader("GPU Launch Price by Model")
fig = px.bar(
    sorted_df,
    x = "name",
    y = "price",
    color = "brand",
    title = "GPU Launch Price by Model",
    labels = {"name": "GPU Name", "price": "GPU Price (USD)", "brand": "GPU Brand"},
)
st.plotly_chart(fig)


#Dynamic
st.subheader("GPU Price vs Cores")
if "brands" not in st.session_state:
    st.session_state.brands = list(df["brand"].unique())
st.multiselect("Choose brands to compare!", options = df["brand"].unique(), key = "brands")

filtered_df = df[df["brand"].isin(st.session_state.brands)]

if filtered_df.empty:
    st.warning("No brands selected")
else:
    fig2 = px.scatter(
        filtered_df,
        x = "price",
        y = "cores",
        color = "brand",
        hover_name = "name",
        title = "GPU Price vs Cores",
        labels = {"name": "GPU Name", "price": "GPU Price (USD)", "brand": "GPU Brand", "cores": "GPU Cores"},
    )
    st.plotly_chart(fig2)

# PART 2: GRAPHS FROM data.csv
st.subheader("GPU Brands Among Survey Responders")
csv_df = pd.read_csv("data.csv")
if csv_df.empty:
    st.info("No data found")
else:
    fig3 = px.pie(
        csv_df,
        names=  "brand",
        labels = {"brand": "GPU Brand"},
        title = "Popular Brands Among Survey Responders",
    )
    st.plotly_chart(fig3)

    max_budget = int(csv_df["budget"].max())
    if "budget_cap" not in st.session_state:
        st.session_state.budget_cap = max_budget
    if st.session_state.budget_cap > max_budget:
        st.session_state.budget_cap = max_budget

    st.subheader("Budget vs Responders")
    st.slider("Budget Cap", min_value = 0, max_value = max_budget, key = "budget_cap")

    capped_df = csv_df[csv_df["budget"] <= st.session_state.budget_cap]
    if capped_df.empty:
        st.warning("No responses at or below this budget")
    else:
        fig4 = px.histogram(
            capped_df,
            x = "budget",
            color = "brand",
            title = "Responders vs Price Ranges",
            labels = {"budget": "Budget (USD)", "count": "Number of Responders"},
        )
        st.plotly_chart(fig4)