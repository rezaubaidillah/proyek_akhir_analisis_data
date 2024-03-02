import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set(style="dark")


def create_daily_orders_df(df):
    daily_orders_df = df.resample(rule="D", on="dteday").agg(
        {
            "instant": "nunique",
            "cnt": "sum",
        }
    )
    daily_orders_df = daily_orders_df.reset_index()
    daily_orders_df.rename(
        columns={"instant": "order_count", "cnt": "count"}, inplace=True
    )
    return daily_orders_df


def create_sum_count_hour_df(df):
    sum_count_hour_df = df.groupby("hr").cnt.sum().sort_values(ascending=False).reset_index()
    return sum_count_hour_df


all_df = pd.read_csv("hour.csv")

datetime_columns = ["dteday"]
all_df.sort_values(by="dteday", inplace=True)
all_df.reset_index(inplace=True)

for column in datetime_columns:
    all_df[column] = pd.to_datetime(all_df[column])

min_date = all_df["dteday"].min()
max_date = all_df["dteday"].max()

with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://cdn-icons-png.flaticon.com/256/2972/2972215.png")

    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label="Rentang Waktu", min_value=min_date, max_value=max_date, value=[min_date, max_date]
    )

main_df = all_df[(all_df["dteday"] >= str(start_date)) & (all_df["dteday"] <= str(end_date))]

daily_orders_df = create_daily_orders_df(main_df)
sum_count_hour_df = create_sum_count_hour_df(main_df)

st.header("Rent Bike Dashboard :sparkles:")

st.subheader("Daily Orders")


with st.container():
    total_orders = daily_orders_df.order_count.sum()
    st.metric("Total orders", value=total_orders)


fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(daily_orders_df["dteday"], daily_orders_df["order_count"], marker="o", linewidth=2, color="#90CAF9")
ax.tick_params(axis="y", labelsize=20)
ax.tick_params(axis="x", labelsize=15)
st.pyplot(fig)

st.subheader("High Demand by hour")

fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(35, 15))

# Create the bar plot
sns.barplot(x="hr", y="cnt", data=sum_count_hour_df.head(24), ax=ax)

# Customize the plot
ax.set_ylabel(None)
ax.set_xlabel("Hour", fontsize=30)
ax.set_title("Best Performing Product", loc="center", fontsize=50)
ax.tick_params(axis="y", labelsize=35)
ax.tick_params(axis="x", labelsize=30)

# Display the plot in Streamlit
st.pyplot(fig)

st.caption("Reza Ubaidillah (c)2024")
