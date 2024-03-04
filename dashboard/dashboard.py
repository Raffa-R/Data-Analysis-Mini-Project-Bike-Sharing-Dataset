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
day_df = pd.read_csv("D:/Bike-sharing-dataset/day.csv")
hour_df = pd.read_csv("D:/Bike-sharing-dataset/hour.csv")


# Helper function yang dibutuhkan untuk menyiapkan berbagai dataframe
def create_year_df(year2021_df, year2022_df):
    day_df1 = day_df.iloc[:365]
    year2021_df = pd.DataFrame(day_df1.groupby("mnth").cnt.sum().reset_index())
    year2021_df['mnth'] = year2021_df['mnth'].replace({1: 'January', 
                                                   2: 'February', 
                                                   3: 'March',
                                                   4: 'April',
                                                   5: 'May',
                                                   6: 'June',
                                                   7: 'July',
                                                   8: 'August',
                                                   9: 'September',
                                                   10: 'October',
                                                   11: 'November',
                                                   12: 'December'})
    day_df2 = day_df.iloc[365:]
    year2022_df = pd.DataFrame(day_df2.groupby("mnth").cnt.sum().reset_index())
    year2022_df['mnth'] = year2021_df['mnth'].replace({1: 'January', 
                                                   2: 'February', 
                                                   3: 'March',
                                                   4: 'April',
                                                   5: 'May',
                                                   6: 'June',
                                                   7: 'July',
                                                   8: 'August',
                                                   9: 'September',
                                                   10: 'October',
                                                   11: 'November',
                                                   12: 'December'})
    return year2021_df, year2022_df

def create_hours1_df(main2_df):
    hours1_df = hour_df.groupby("hr").cnt.sum().sort_values(ascending=False).reset_index()
    hours1_df["hr"] = hours1_df['hr'].astype('str')
    return hours1_df

def create_day_season(main1_df):
    day_season = pd.DataFrame(day_df.groupby(by="season").cnt.sum().sort_values(ascending=False).reset_index())
    day_season["season"] = day_season["season"].replace({1: 'Summer', 
                                             2: 'Springer', 
                                             3: 'Fall',
                                             4: 'Winter'})
    return day_season

st.header('Bike Sharing Dataset Dashboard :sparkles:')

# Performa penyewaan sepeda oleh perusahan dari 2021-2022
st.subheader("Performa Penyewaan Sepeda")
day_df1 = day_df.iloc[:365]
year2021_df = pd.DataFrame(day_df1.groupby("mnth").cnt.sum().reset_index())
year2021_df['mnth'] = year2021_df['mnth'].replace({1: 'January', 
                                               2: 'February', 
                                               3: 'March',
                                               4: 'April',
                                               5: 'May',
                                               6: 'June',
                                               7: 'July',
                                               8: 'August',
                                               9: 'September',
                                               10: 'October',
                                               11: 'November',
                                               12: 'December'})
day_df2 = day_df.iloc[365:]
year2022_df = pd.DataFrame(day_df2.groupby("mnth").cnt.sum().reset_index())
year2022_df['mnth'] = year2021_df['mnth'].replace({1: 'January', 
                                               2: 'February', 
                                               3: 'March',
                                               4: 'April',
                                               5: 'May',
                                               6: 'June',
                                               7: 'July',
                                               8: 'August',
                                               9: 'September',
                                               10: 'October',
                                               11: 'November',
                                               12: 'December'})
fig0 = plt.figure(figsize=(22, 8))
plt.plot(year2021_df['mnth'], year2021_df['cnt'], label='2021', marker = 'o', color='red')
plt.plot(year2022_df['mnth'], year2022_df['cnt'], label='2022', marker = 'o', color='blue')
plt.title('Performa Penyewaan Sepeda', size=20)

st.pyplot(fig0)
with st.expander("See explanation"):
    st.write(
        """Berdasarkan gambar di atas, dapat diambil kesimpulan bahwa terdapat 
        kenaikan yang signifikan dari bisnis penyewaan sepeda dari tahun 2011 ke tahun 2012, 
        dan bisa dilihat juga dari kedua tahun tersebut terdapat kesamaan yaitu penyewaan sepeda mengalami 
        kenaikan pada 4 bulan pertama dan mengalami penurunan pada 4 bulan terakhir. 
        Hal ini bisa dipengaruhi oleh beberapa faktor, salah satunya adalah faktor perubahan 
        musim yang mana musim selalu berganti setiap triwulan sekali.
        """
    )
# Jumlah penyewaan sepeda per jam nya
st.subheader("Jumlah Penyewaan Sepeda (per jam)")

hours1_df = hour_df.groupby("hr").cnt.sum().sort_values(ascending=False).reset_index()
hours1_df["hr"] = hours1_df['hr'].astype('str')

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(23, 9))

colors = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

sns.barplot(x="cnt", y="hr", data=hours1_df.head(12), orient='h', palette=colors, ax=ax[0])
ax[0].set_ylabel("Jam")
ax[0].set_xlabel("Jumlah Sepeda")
ax[0].set_title("Jumlah Penyewaan sepeda Terbesar", loc="center", fontsize=18)
ax[0].tick_params(axis ='y', labelsize=15)

sns.barplot(x="cnt", y="hr", data=hours1_df.sort_values(by="cnt",ascending=True).head(12), orient='h', palette=colors, ax=ax[1])
ax[1].set_ylabel("Jam")
ax[1].set_xlabel("Jumlah Sepeda")
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_title("Jumlah Penyewaan Sepeda terkecil", loc="center", fontsize=18)
ax[1].tick_params(axis='y', labelsize=15)


st.pyplot(fig)

with st.expander("See explanation"):
    st.write(
        """Berdasarkan gambar di atas, dapat 
        diambil kesimpulan bahwa jumlah sepeda yang disewa paling banyak oleh 
        pelanggan adalah pada pukul 17.00 (5 sore), sedangkan penyewaan sepeda 
        paling sedikit oleh pelanggan adalah pada pukul 4 pagi.
        """
    )

#Jumlah penyewaan sepeda per musim nya
st.subheader("Jumlah Penyewaan Sepeda Berdasarkan Musim (dalam Juta)")

day_season = pd.DataFrame(day_df.groupby(by="season").cnt.sum().sort_values(ascending=False).reset_index())
day_season["season"] = day_season["season"].replace({1: 'Summer', 
                                                     2: 'Springer', 
                                                     3: 'Fall',
                                                     4: 'Winter'})

fig2 = plt.figure(figsize=(20, 8))
colors_ = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
sns.barplot(
    x="cnt",
    y="season",
    data= day_season,
    palette=colors_,
    orient='h',
    errorbar=None
)
#plt.title("Jumlah Penyewaan Sepeda Berdasarkan Musim (dalam Juta)", loc="center", fontsize=15)
plt.ylabel("Musim")
plt.xlabel("Jumlah sepeda (dalam Juta)")
plt.tick_params(axis='y', labelsize=12)

st.pyplot(fig2)

with st.expander("See explanation"):
    st.write(
        """ Berdasarkan gambar di atas, diketahui 
        bahwa kebanyakan pelanggan paling banyak suka menyewa sepeda ketika musim 
        gugur (fall) dan jumlah paling sedikit sepeda yang disewa ketika musim 
        panas (summer).
        """
    )