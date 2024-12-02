# -*- coding: utf-8 -*-
"""
Created on Sun Mar  3 19:19:32 2024

@author: ANDRI
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
#from babel.numbers import format_currency

sns.set(style='dark')

# Load cleaned data
#day_df = pd.read_csv('./data/day.csv')
#hour_df = pd.read_csv('./data/hour.csv')


# Helper function yang dibutuhkan untuk menyiapkan berbagai dataframe
def create_daily_rent_df(df):
    daily_rent_df = df.resample(rule='D', on='dteday').agg({
        "weekday": "nunique",
        "cnt": "sum"
    })
    daily_rent_df = daily_rent_df.reset_index()
    daily_rent_df.rename(columns={
        "weekday": "rent_count"
    }, inplace=True)
    
    return daily_rent_df

#def create_year_df(year2021_df, year2022_df):
#    day_df1 = day_df.iloc[:365]
#    year2021_df = pd.DataFrame(day_df1.groupby("mnth").cnt.sum().reset_index())
#    year2021_df['mnth'] = year2021_df['mnth'].replace({1: 'January', 
#                                                   2: 'February', 
#                                                   3: 'March',
#                                                   4: 'April',
#                                                   5: 'May',
#                                                   6: 'June',
#                                                   7: 'July',
#                                                   8: 'August',
#                                                   9: 'September',
#                                                   10: 'October',
#                                                   11: 'November',
#                                                   12: 'December'})
#    day_df2 = day_df.iloc[365:]
#    year2022_df = pd.DataFrame(day_df2.groupby("mnth").cnt.sum().reset_index())
#    year2022_df['mnth'] = year2021_df['mnth'].replace({1: 'January', 
#                                                   2: 'February', 
#                                                   3: 'March',
#                                                   4: 'April',
#                                                   5: 'May',
#                                                   6: 'June',
#                                                   7: 'July',
#                                                   8: 'August',
#                                                   9: 'September',
#                                                   10: 'October',
#                                                   11: 'November',
#                                                   12: 'December'})
#    return year2021_df, year2022_df

#def create_hours1_df(main2_df):
#    hours1_df = hour_df.groupby("hr").cnt.sum().sort_values(ascending=False).reset_index()
#    hours1_df["hr"] = hours1_df['hr'].astype('str')
#    return hours1_df

def create_day_season(df):
#    day_season = pd.DataFrame(day_df.groupby(by="season").cnt.sum().sort_values(ascending=False).reset_index())
#    day_season["season"] = day_season["season"].replace({1: 'Summer', 
#                                             2: 'Springer', 
#                                             3: 'Fall',
#                                             4: 'Winter'})
#    return day_season
    day_season1 = pd.DataFrame(df.groupby(by="season").cnt.mean().round().astype(int).reset_index())
    day_season1["season"] = day_season1["season"].replace({1: 'Winter',
                                                           2: 'Spring',
                                                           3: 'Summer',
                                                           4: 'Fall'})
    return day_season1

def create_day_weekday(df):
    day1_df = df.groupby("weekday").cnt.sum().reset_index()
    day1_df["weekday"] = day1_df["weekday"].replace({0: 'Sunday',
                                             1: 'Monday',
                                             2: 'Tuesday',
                                             3: 'Wednesday',
                                             4: 'Thursday',
                                             5: 'Friday',
                                             6: 'Saturday'})
    day1_df["weekday"] = day1_df['weekday'].astype('str')
    return day1_df

def create_day_weathersit(df):
    day_weatsit1 = pd.DataFrame(df.groupby(by="weathersit").cnt.mean().round().astype(int).reset_index())
    day_weatsit1["weathersit"] = day_weatsit1["weathersit"].replace({1: 'Weather 1',
                                             2: 'Weather 2',
                                             3: 'Weather 3'})
    return day_weatsit1

# Load cleaned data
day_df = pd.read_csv('./data/day.csv')

datetime_columns = "dteday"
#all_df.sort_values(by="order_date", inplace=True)
#all_df.reset_index(inplace=True)

day_df[datetime_columns] = pd.to_datetime(day_df[datetime_columns])

# Filter data
min_date = day_df["dteday"].min()
max_date = day_df["dteday"].max()

with st.sidebar:
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

bike_df = day_df[(day_df["dteday"] >= str(start_date)) & 
                (day_df["dteday"] <= str(end_date))]

# # Menyiapkan berbagai dataframe
daily_rent_df = create_daily_rent_df(bike_df)
day_season1 = create_day_season(bike_df)
day1_df = create_day_weekday(bike_df)
day_weatsit1 = create_day_weathersit(bike_df)

st.header('Bike Sharing Dataset Dashboard :sparkles:')

# Performa penyewaan sepeda oleh perusahan dari 2011-2012
st.subheader("Daily Bikes Rent")
col1, col2 = st.columns(2)

with col1:
    total_rents = daily_rent_df.cnt.sum()
    st.metric("Total rent", value=total_rents)

fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    daily_rent_df["dteday"],
    daily_rent_df["cnt"],
    marker='o', 
    linewidth=2,
    color="#90CAF9"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)

st.pyplot(fig)
#day_df1 = day_df.iloc[:365]
#year2021_df = pd.DataFrame(day_df1.groupby("mnth").cnt.sum().reset_index())
#year2021_df['mnth'] = year2021_df['mnth'].replace({1: 'January', 
#                                               2: 'February', 
#                                               3: 'March',
#                                               4: 'April',
#                                               5: 'May',
#                                               6: 'June',
#                                               7: 'July',
#                                               8: 'August',
#                                               9: 'September',
#                                               10: 'October',
#                                               11: 'November',
#                                               12: 'December'})
#day_df2 = day_df.iloc[365:]
#year2022_df = pd.DataFrame(day_df2.groupby("mnth").cnt.sum().reset_index())
#year2022_df['mnth'] = year2021_df['mnth'].replace({1: 'January', 
#                                               2: 'February', 
#                                               3: 'March',
#                                               4: 'April',
#                                               5: 'May',
#                                               6: 'June',
#                                               7: 'July',
#                                               8: 'August',
#                                               9: 'September',
#                                               10: 'October',
#                                               11: 'November',
#                                               12: 'December'})
#fig0 = plt.figure(figsize=(22, 8))
#plt.plot(year2021_df['mnth'], year2021_df['cnt'], label='2021', marker = 'o', color='red')
#plt.plot(year2022_df['mnth'], year2022_df['cnt'], label='2022', marker = 'o', color='blue')
#plt.title('Performa Penyewaan Sepeda', size=20)

#st.pyplot(fig0)
#with st.expander("See explanation"):
#    st.write(
#        """Berdasarkan gambar di atas, dapat diambil kesimpulan bahwa terdapat 
#        kenaikan yang signifikan dari bisnis penyewaan sepeda dari tahun 2011 ke tahun 2012, 
#        dan bisa dilihat juga dari kedua tahun tersebut terdapat kesamaan yaitu penyewaan sepeda mengalami 
#        kenaikan pada 4 bulan pertama dan mengalami penurunan pada 4 bulan terakhir. 
#        Hal ini bisa dipengaruhi oleh beberapa faktor, salah satunya adalah faktor perubahan 
#        musim yang mana musim selalu berganti setiap triwulan sekali.
#        """
#    )
# Jumlah penyewaan sepeda per jam nya
st.subheader("Jumlah Penyewaan Sepeda (per hari)")

#hours1_df = hour_df.groupby("hr").cnt.sum().sort_values(ascending=False).reset_index()
#hours1_df["hr"] = hours1_df['hr'].astype('str')

#fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(23, 9))

#colors = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

#sns.barplot(x="cnt", y="hr", data=hours1_df.head(12), orient='h', palette=colors, ax=ax[0])
#ax[0].set_ylabel("Jam")
#ax[0].set_xlabel("Jumlah Sepeda")
#ax[0].set_title("Jumlah Penyewaan sepeda Terbesar", loc="center", fontsize=18)
#ax[0].tick_params(axis ='y', labelsize=15)

#sns.barplot(x="cnt", y="hr", data=hours1_df.sort_values(by="cnt",ascending=True).head(12), orient='h', palette=colors, ax=ax[1])
#ax[1].set_ylabel("Jam")
#ax[1].set_xlabel("Jumlah Sepeda")
#ax[1].invert_xaxis()
#ax[1].yaxis.set_label_position("right")
#ax[1].yaxis.tick_right()
#ax[1].set_title("Jumlah Penyewaan Sepeda terkecil", loc="center", fontsize=18)
#ax[1].tick_params(axis='y', labelsize=15)


#st.pyplot(fig)

#with st.expander("See explanation"):
#    st.write(
#        """Berdasarkan gambar di atas, dapat 
#        diambil kesimpulan bahwa jumlah sepeda yang disewa paling banyak oleh 
#        pelanggan adalah pada pukul 17.00 (5 sore), sedangkan penyewaan sepeda 
#        paling sedikit oleh pelanggan adalah pada pukul 4 pagi.
#        """
#   )
# Define a function to create a color palette
def create_palette(df, column, highlight_high, highlight_low, neutral_color):
    palette = [neutral_color] * len(day1_df)
    max_index = day1_df[column].idxmax()
    min_index = day1_df[column].idxmin()
    palette[max_index] = highlight_high
    palette[min_index] = highlight_low
    return palette

fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(12, 8))

# Plot 1: Largest bike rentals
colors = create_palette(day1_df, "cnt","#72d48a","#d48a72", "#D3D3D3")
sns.barplot(x="weekday", y="cnt", data=day1_df, orient='v', palette=colors, ax=ax)
ax.set_ylabel("Hari")
ax.set_xlabel("Jumlah Sepeda")
#ax.set_title("Jumlah Penyewaan Sepeda per Hari", loc="center", fontsize=18)
ax.tick_params(axis='y', labelsize=15)

# Annotate the bars with their values
for i, v in enumerate(day1_df["cnt"]):
    ax.text(i-0.2, v + 30, f"{v}", color='black', va='center', fontsize=10)  # Adjust +2 for spacing

#plt.show()
st.pyplot(fig)

#Jumlah penyewaan sepeda per musim nya
st.subheader("Rata-Rata Penyewaan Sepeda Berdasarkan Musim")
#with st.expander("See explanation"):
#    st.write(
#        """ Berdasarkan gambar di atas, diketahui 
#        bahwa kebanyakan pelanggan paling banyak suka menyewa sepeda ketika musim 
#        gugur (fall) dan jumlah paling sedikit sepeda yang disewa ketika musim 
#        panas (summer).
#        """
#    )
#text = st.text_area('Silahkan berikan Feedback atas hasil analisis data di atas. Terima Kasih')
#st.write('Feedback: ', text)
fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(12, 8))  # Adjust figsize for vertical plot

# Define a function to create a color palette
def create_palette(df, column, highlight_high, highlight_low, neutral_color):
    palette = [neutral_color] * len(day_season1)
    max_index = day_season1[column].idxmax()
    min_index = day_season1[column].idxmin()
    palette[max_index] = highlight_high
    palette[min_index] = highlight_low
    return palette

# Plot 1: Largest bike rentals (Vertical bar plot)
colors_ = create_palette(day_season1, "cnt","#72d48a","#d48a72", "#D3D3D3")
sns.barplot(x="season", y="cnt", data=day_season1, orient='v', palette=colors_, ax=ax)
ax.set_xlabel("Musim", fontsize=14)
ax.set_ylabel("Rata-rata penyewaan sepeda", fontsize=14)
#ax.set_title("Rata-Rata Penyewaan Sepeda Berdasarkan Musim", loc="center", fontsize=18)
ax.tick_params(axis='x', labelsize=12)

# Annotate the bars with their values
for i, v in enumerate(day_season1["cnt"]):
    ax.text(i, v + 30, f"{v}", color='black', ha='center', fontsize=14)  # Adjust +2 for spacing above bars

st.pyplot(fig)

#Rata-rata penyewaan sepeda berdasarkan kondisi cuaca

st.subheader("Rata-Rata Penyewaan Sepeda Berdasarkan Kondisi Cuaca)")
fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(12, 8))  # Adjust figsize for vertical plot

# Define a function to create a color palette
def create_palette(df, column, highlight_high, highlight_low, neutral_color):
    palette = [neutral_color] * len(day_weatsit1)
    max_index = day_weatsit1[column].idxmax()
    min_index = day_weatsit1[column].idxmin()
    palette[max_index] = highlight_high
    palette[min_index] = highlight_low
    return palette

# Plot 1: Largest bike rentals (Vertical bar plot)
colors_1 = create_palette(day_weatsit1, "cnt","#72d48a","#d48a72", "#D3D3D3")
sns.barplot(x="weathersit", y="cnt", data=day_weatsit1, orient='v', palette=colors_1, ax=ax)
ax.set_xlabel("Kondisi Cuaca", fontsize=14)
ax.set_ylabel("Rata-rata penyewaan sepeda", fontsize=14)
#ax.set_title("Rata-Rata Penyewaan Sepeda Berdasarkan Kondisi Cuaca", loc="center", fontsize=18)
ax.tick_params(axis='x', labelsize=12)

# Annotate the bars with their values
for i, v in enumerate(day_weatsit1["cnt"]):
    ax.text(i, v + 30, f"{v}", color='black', ha='center', fontsize=14)  # Adjust +2 for spacing above bars

st.pyplot(fig)