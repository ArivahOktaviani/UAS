"""
Aplikasi Streamlit untuk menggambarkan data produksi minyak mentah dari berbagai daerah di seluruh dunia.
Referensi API Streamlit: https://docs.streamlit.io/library/api-reference
Nama : Arivah Oktaviani 
NIM : 12220018
"""
import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
from matplotlib import cm 
import matplotlib.colors as colors
from fileHandler import csvHandler,jsonHandler
import json

#################DATA###################
#DATA JSON
with open("kode_negara_lengkap.json") as f:
    data_json = json.load(f)
json = pd.DataFrame(data_json)
#DATA CSV
data_csv = pd.read_csv("produksi_minyak_mentah.csv")
csv = pd.DataFrame(data_csv)
print(csv)
#################DATA###################


################TITLE#################
st.title('Statistik Produksi Minyak')
st.markdown('Arivah Oktaviani - 12220018')
st.markdown('UAS PROKOM ')
st.markdown('17 Desember 2021 ')
negara_li = json['name'].tolist()

#MENGATUR LETAK OUTPUT
st.sidebar.title("Pengaturan")
st.sidebar.header('Pengaturan Jumlah Produksi Per Bulan')
left_col, mid_col, right_col = st.columns(3)
negara = st.sidebar.selectbox('Pilih negara : ',negara_li) 

kode = json[json['name']==negara]['alpha-3'].tolist()[0]

st.sidebar.write('Kode negara : ',kode, color = "green")
st.sidebar.write('Negara : ',negara, color = "red")

# MENGUBAH STRING MENJADI FLOAT
csv['produksi'] = csv['produksi'].astype(str).str.replace(".", "", regex=True).astype(float)
csv['produksi'] = csv['produksi'].astype(str).str.replace(",", "", regex=True).astype(float)
csv['produksi'] = pd.to_numeric(csv['produksi'], errors='coerce')

#OUTPUT TABEL A
df2 = pd.DataFrame(csv,columns= ['kode_negara','tahun','produksi'])
df2=df2.loc[df2['kode_negara']==kode]
df2['produksi'] = pd.to_numeric(df2['produksi'], errors='coerce')

left_col.write(df2)

#OUTPUT GRAFIK A
fig, ax = plt.subplots()
colors = ['yellowgreen', 'gold', 'lightskyblue', 'lightcoral']
ax.plot(df2['tahun'], df2['produksi'], label = df2['tahun'])
ax.set_title("Jumlah Produksi Per Tahun di Negara Pilihan")
ax.set_xlabel("Tahun", color="red", fontsize = 20)
ax.set_ylabel("Jumlah Produksi", color="yellow", fontsize = 20)
ax.legend(fontsize = 20)
plt.scatter("Tahun", "Jumlah Produksi", color="yellow", marker='x', label='item 1')
plt.show()
right_col.pyplot(fig)

#b
list_kodekumpulannegara = []
for i in list(csv['kode_negara']) :
    if i not in list(json['alpha-3']) :
        list_kodekumpulannegara.append(i)

for i in list_kodekumpulannegara :
    csv = csv[csv.kode_negara != i]
print(csv)
   
st.sidebar.header('Pengaturan Negara dengan Produksi Terbesar')
tahun = st.sidebar.number_input("Pilih Tahun produksi", min_value=1971, max_value=2015)
n = st.sidebar.number_input("Pilih Banyak Negara", min_value=1, max_value=None)


dfb = csv.loc[csv['tahun'] == tahun]
dfb = dfb.sort_values(by='produksi', ascending = False)
df3 = dfb[:n]
print(df3)
df3.plot.bar(x='kode_negara', y='produksi')
plt.show()
st.pyplot(plt)

#c
st.write('Grafik Negara dengan Produksi Kumulatif Terbesar')
list_a = []
kumulatif = []

for i in list (csv['kode_negara']) :
    if i not in list_a:
        list_a.append(i)
        
for i in list_a :
    a=csv.loc[csv['kode_negara'] ==i,'produksi'].sum()
    kumulatif.append(a)
    
dk = pd.DataFrame(list(zip(list_a,kumulatif)), columns = ['kode_negara','kumulatif'])
dk = dk.sort_values(by=['kumulatif'], ascending = False)
dk = dk[:n]

dk.plot.bar(x='kode_negara', y='kumulatif') 
plt.show()
st.pyplot(plt)

dfterkecil = dfb[dfb.produksi !=0]
dfterkecil = dfterkecil.sort_values(by=['produksi'],ascending=True)
jumlah_produksi = dfterkecil[:1].iloc[0]['produksi']
kode_negara = dfterkecil[:1].iloc[0]['kode_negara']
nama_negara = ""
region_negara = ""
subregion_negara = ""
                                    
for i in range(len(json)):
    if list(json['alpha-3'])[i]==kode_negara:
        nama_negara = list(df_info['name'])[i]
        region_negara = list(df_info['region'])[i]
        subregion_negara = list(df_info['sub-region'])[i]
                                    
st.write('Negara dengan Produksi Terkecil')
st.write(jumlah_produksi)
st.write(kode_negara)
st.write(nama_negara)
st.write(region_negara)
st.write(subregion_negara)
                                    
dfakumulatifmin=dk[dk.kumulatif !=0]
dfakumulatifmin = dfakumulatifmin[:1].sort_values(by=['kumulatif'], ascending = True)
jumlah_produksi = dfakumulatifmin[:1].iloc[0]['kumulatif']
kode_negara = dfakumulatifmin[:1].iloc[0]['kode_negara']
nama_negara = ""
region_negara = ""
subregion_negara = ""
                                                
for i in range(len(json)):
    if list(json['alpha-3'])[i]==kode_negara:
        nama_negara = list(json['name'])[i]
        region_negara = list(json['region'])[i]
        subregion_negara = list(json['sub-region'])[i]
                                                
st.write('Negara dengan Produksi Terkecil Pada Keseluruhan Tahun')
st.write(jumlah_produksi)
st.write(kode_negara)
st.write(nama_negara)
st.write(region_negara)
st.write(subregion_negara)

#d
dfproduksinol = dfb[dfb.produksi == 0]
listnegaranol = []
listregionol = []
listsubregionol = []

for i in range(len(dfproduksinol)):
    for j in range(len(json)):
        if list (dfproduksinol['kode_negara'])[i] == list(json['alpha-3'])[j]:
            listnegaranol.append(list(json['name'])[j])
            listregionol.append(list(json['region'])[j])
            listsubregionol.append(list(json['sub-region'])[j])

dfproduksinol['negara'] = listnegaranol
dfproduksinol['region'] = listregionol
dfproduksinol['sub-region'] = listsubregionol
 
                                                        
dfproduksikumulatifnol = dfb[dfb.produksi == 0]
listnegarakumulatifnol = []
listregionkumulatifnol = []
listsubregionkumulatifnol = []

for i in range(len(dfproduksikumulatifnol)):
    for j in range(len(json)):
        if list (dfproduksikumulatifnol['kode_negara'])[i] == list(json['alpha-3'])[j]:
            listnegarakumulatifnol.append(list(json['name'])[j])
            listregionkumulatifnol.append(list(json['region'])[j])
            listsubregionkumulatifnol.append(list(json['sub-region'])[j])

dfproduksikumulatifnol['negara'] = listnegarakumulatifnol
dfproduksikumulatifnol['region'] = listregionkumulatifnol
dfproduksikumulatifnol['sub-region'] = listsubregionkumulatifnol     
                                                        
st.write(dfproduksinol)
st.write(dfproduksikumulatifnol)
