import pandas as pd
import plotly.express as px
import streamlit as st

from load_db import get_table

st.set_page_config(page_title="Axmed App", page_icon=":tada:")
st.title("Price evolution by country and year")


df = pd.read_csv("pricing_history.csv")
df["date"] = pd.to_datetime(df["date"], format="%Y-%m-%d")
df["year"] = df["date"].dt.year.astype(str)
df["month"] = df["date"].dt.month.astype(str)
df_medicine = get_table("medicine")
df_medicine.rename(columns={"name": "medicine"}, inplace=True)
df = pd.merge(df, df_medicine, on="medicine", how="left")
df["medicine_id"] = df["medicine_id"].astype(str)
result = (
    df.groupby(["year", "month", "medicine"])
    .agg(avg_month=("pricing_history", "mean"))
    .reset_index()
)
df = pd.merge(df, result, on="medicine", how="left", suffixes=("", "_drop"))
df = df[[col for col in df.columns if not col.endswith("_drop")]]
df["year_month"] = df["year"] + "-" + df["month"]
df.drop_duplicates(["date", "medicine_id", "country"], keep="last", inplace=True)

df.drop(columns=["month"], inplace=True)
print(df.head())

all_countries = ["All"] + list(df["country"].unique())
all_years = ["All"] + list(sorted(df["year"].unique()))

selected_country = st.selectbox(
    "Select Country",
    options=all_countries,
    index=all_countries.index("DZA") if "DZA" in all_countries else "ZWE",
    key="country_filter",
)
selected_year = st.selectbox(
    "Select Year",
    options=all_years,
    index=all_years.index("2024") if "2024" in all_years else "2023",
    key="year_filter",
)


if selected_country == "All":
    filtered_data = df[df["year"] == selected_year]
else:
    filtered_data = df[
        (df["country"] == selected_country) & (df["year"] == selected_year)
    ]

print(filtered_data)
if not filtered_data.empty:
    fig = px.bar(
        filtered_data,
        x="year_month",
        y="avg_month",
        color="medicine_id",
        barmode="group",
        title=f"Medicine Pricing History in {selected_country}",
        labels={
            "avg_month": "Avg price by month",
            "medicine_id": "Medicine id",
            "year_month": "Year-Month",
        },
    )

    st.plotly_chart(fig)


df = pd.read_csv("pricing_history.csv", parse_dates=["date"])
amox_data = df[df["medicine"] == "Amoxicillin Tablet 500mg"]

amox_data["year"] = amox_data["date"].dt.year.astype(str)
amox_data["month"] = amox_data["date"].dt.month.astype(str)


avg_pricing = (
    amox_data.groupby(["year", "month", "country"])
    .agg(avg_month=("pricing_history", "mean"))
    .reset_index()
)

avg_pricing["year_month"] = avg_pricing["year"] + "-" + avg_pricing["month"]

avg_pricing["year_month"] = avg_pricing["year_month"].astype(str)
avg_pricing = avg_pricing.sort_values(by="year_month")


all_countries = ["All"] + list(avg_pricing["country"].unique())
all_years = ["All"] + list(sorted(avg_pricing["year"].unique()))


st.title("Amoxicillin Pricing Trend")

selected_country = st.selectbox(
    "Select Country",
    options=all_countries,
    index=all_countries.index("DZA") if "DZA" in all_countries else "ZWE",
    key="second_country_filter",
)
selected_year = st.selectbox(
    "Select Year",
    options=all_years,
    index=all_years.index("2024") if "2024" in all_years else "2023",
    key="second_year_filter",
)


if selected_country == "All":
    second_filtered_data = avg_pricing[avg_pricing["year"] == selected_year]
else:
    second_filtered_data = avg_pricing[
        (avg_pricing["country"] == selected_country)
        & (avg_pricing["year"] == selected_year)
    ]

print(second_filtered_data)
if not second_filtered_data.empty:
    st.dataframe(second_filtered_data, hide_index=True)
