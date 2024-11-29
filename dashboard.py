import streamlit as st
import pandas as pd
import plotly.express as px
from recursos.get_experience_table_char import get_experience_table
import datetime as dt
import re


st.set_page_config(layout="wide")


char_name = st.text_input("Char name", "Kin Freezetime")
df = get_experience_table(char_name)

# Processing data
# quero a quantidade de experiencia por dia
df["Date"] = pd.to_datetime(df["Date"])
df = df.sort_values("Date")

df["Month"] = df["Date"].apply(lambda x: str(x.year) + "-" + str(x.month))
month = st.sidebar.selectbox("Mes", df["Month"].unique())

# Creating the lvl gain/loss column
df["LvlChange"] = df['Lvl'].str.extract(r"\(([-+]?\d+)\)").astype(float)
# replacing nan for 0
df["LvlChange"] = df["LvlChange"].fillna(0)

# filling nan whit 0
df["Avg exp per hour"] = df["Avg exp per hour"].str.replace("/h", "")
df["Avg exp per hour"] = df["Avg exp per hour"].replace(",", "", regex=True)
df["Avg exp per hour"] = df["Avg exp per hour"].fillna(0)

df_filtred = df.loc[df["Month"] == month]

# aqui serve para criar caixas imaginarias
# aqui primeiro será dividida em duas caoxas
col1, col2 = st.columns(2)
# aqui primeiro será dividida em tres
col3, col4, col5 = st.columns(3)

fig_daily_exp = px.bar(df_filtred, x="Date", y="Exp change", range_y=[-8000000, 30000000], color="Time on-line", title="Exp per day")
col1.plotly_chart(fig_daily_exp)

fig_daily_lvl = px.bar(df_filtred, x="Date", y="LvlChange", color="Time on-line", title="Lvl per day")
col2.plotly_chart(fig_daily_lvl)

fig_daily_exphour = px.bar(df_filtred, x="Date", y="Avg exp per hour", range_y=[500000, 3000000], title="Avg exp hour per day")
col3.plotly_chart(fig_daily_exphour)

