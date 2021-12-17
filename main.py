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
from fileHandler import csvHandler,jsonHandler

#################DATA###################
#DATA JSON
data_kodenegara = jsonHandler('kode_negara_lengkap.json')
data_json = data_kodenegara.dataFrame
#List negara
negara_li = data_json['name'].tolist()
#DATA CSV
data_negara = csvHandler('produksi_minyak_mentah.csv')
data_csv = data_negara.dataFrame
#################DATA###################

################TITLE#################
st.title('Statistik Produksi Minyak')
st.markdown('Arivah Oktaviani - 12220018')
st.markdown('UAS PROKOM ')
st.markdown('17 Desember 2021 ')
################TITLE#################

##############SIDEBAR################
st.sidebar.title("Pengaturan")
#NEGARA
left_col, mid_col, right_col = st.columns(3)
negara = st.sidebar.selectbox('Negara : ',negara_li)
kode = data_json[data_json['name']==negara]['alpha-3'].tolist()[0]
st.sidebar.write('Kode negara : ',kode)
#TAHUN
st.sidebar.header('Pengaturan Negara')
tahun = st.sidebar.slider("Tahun Produksi :", min_value=1971, max_value=2015)
n_tampil = st.sidebar.number_input("Banyak Negara", min_value=1, max_value=249)
##############SIDEBAR################

####################  BAGIAN A #######################
#Tabel Representasi Data
left_col.subheader("Tabel representasi data")
dfA = pd.DataFrame(data_csv,columns= ['kode_negara','tahun','produksi'])
dfA = dfA.loc[dfA['kode_negara']==kode]
dfA['produksi'] = pd.to_numeric(dfA['produksi'])
left_col.write(dfA)
#Grafik Negara dengan Produksi Sesuai dengan Pilihan
right_col.subheader("Total Produksi Pertahun")
fig, ax = plt.subplots()
ax.plot(dfA['tahun'], dfA['produksi'],color="green")
ax.set_xlabel("Tahun", color="black", fontsize = 14)
ax.set_ylabel("Jumlah Produksi", color="black", fontsize = 14)
ax.legend(fontsize = 14)
right_col.pyplot(fig)
####################  BAGIAN A #######################


####################  BAGIAN B #######################
st.subheader("Grafik Negara dengan Produksi Terbesar Sesuai Banyak Negara dan Tahun Inputan User")
list_kodenegara = []
for i in list(data_csv['kode_negara']) :
    if i not in list(data_json['alpha-3']) :
        list_kodenegara.append(i)
for i in list_kodenegara :
    data_csv = data_csv[data_csv.kode_negara != i]  
dfb = data_csv.loc[data_csv['tahun'] == tahun]
dfb = dfb.sort_values(by='produksi',ascending = False)
df3 = dfb[:n_tampil]
df3.plot.bar(x='kode_negara', y='produksi',width=0.3,align="center",color="green")
plt.show()
st.pyplot(plt)
####################  BAGIAN B #######################



####################  BAGIAN C #######################
st.subheader('Grafik Negara dengan Produksi Terbesar Sesuai Banyak Negara Inputan User')
data1 = []
total = []
for i in list (data_csv['kode_negara']) :
    if i not in data1:
        data1.append(i)       
for i in data1 :
    a=data_csv.loc[data_csv['kode_negara'] ==i,'produksi'].sum()
    total.append(a)    
dk = pd.DataFrame(list(zip(data1,total)), columns = ['kode_negara','kumulatif'])
dk = dk.sort_values(by=['kumulatif'], ascending = False)
dk = dk[:n_tampil]
dk.plot.bar(x='kode_negara', y='kumulatif',width=0.3, align="center",color="green") 
plt.show()
st.pyplot(plt)
####################  BAGIAN C #######################

####################  BAGIAN D #######################
st.header("Summary")
#Negara dengan Produksi Besar Setiap Tahun
jumlah_produksi = dfb[:1].iloc[0]['produksi']
kode_negara = dfb[:1].iloc[0]['kode_negara']
nama_negara = ""
region_negara = ""
subregion_negara = ""

for i in range(len(data_json)):
    if list(data_json['alpha-3'])[i]==kode_negara:
        nama_negara = list(data_json['name'])[i]
        region_negara = list(data_json['region'])[i]
        subregion_negara = list(data_json['sub-region'])[i]

st.subheader('Negara dengan Produksi Terbesar')
st.markdown(f"Negara : {nama_negara}")
st.markdown(f"Kode Negara : {kode_negara}")
st.markdown(f"Region : {region_negara}")
st.markdown(f"SubRegion :{subregion_negara}")
st.markdown(f"Jumlah Produksi :  {jumlah_produksi}")

#Negara dengan Produksi  Besar di Keseluruan Tahun
jumlah_produksi = dk[:1].iloc[0]['kumulatif']
kode_negara = dk[:1].iloc[0]['kode_negara']
nama_negara = ""
region_negara = ""
subregion_negara = ""

for i in range(len(data_json)):
    if list(data_json['alpha-3'])[i]==kode_negara:
        nama_negara = list(data_json['name'])[i]
        region_negara = list(data_json['region'])[i]
        subregion_negara = list(data_json['sub-region'])[i]

st.subheader('Negara dengan Produksi Terbesar di Kesuluruhan Tahun')
st.markdown(f"Negara : {nama_negara}")
st.markdown(f"Kode Negara : {kode_negara}")
st.markdown(f"Region : {region_negara}")
st.markdown(f"SubRegion :{subregion_negara}")
st.markdown(f"Jumlah Produksi :  {jumlah_produksi}")

#Negara dengan Produksi  Terkecil setiap Tahun(tidaknol)
dfterkecil = dfb[dfb.produksi !=0]
dfterkecil = dfterkecil.sort_values(by=['produksi'],ascending=True)
jumlah_produksi = dfterkecil[:1].iloc[0]['produksi']
kode_negara = dfterkecil[:1].iloc[0]['kode_negara']
nama_negara = ""
region_negara = ""
subregion_negara = ""
                                    
for i in range(len(data_json)):
    if list(data_json['alpha-3'])[i]==kode_negara:
        nama_negara = list(data_json['name'])[i]
        region_negara = list(data_json['region'])[i]
        subregion_negara = list(data_json['sub-region'])[i]
                                    
st.subheader('Negara dengan Produksi Terkecil')
st.markdown(f"Negara : {nama_negara}")
st.markdown(f"Kode Negara : {kode_negara}")
st.markdown(f"Region : {region_negara}")
st.markdown(f"SubRegion :{subregion_negara}")
st.markdown(f"Jumlah Produksi :  {jumlah_produksi}")


#Negara dengan Produksi  Terkecil di Keseluruan Tahun (tidaknol)                                  
dfakumulatifmin=dk[dk.kumulatif !=0]
dfakumulatifmin = dfakumulatifmin[:1].sort_values(by=['kumulatif'], ascending = True)
jumlah_produksi = dfakumulatifmin[:1].iloc[0]['kumulatif']
kode_negara = dfakumulatifmin[:1].iloc[0]['kode_negara']
nama_negara = ""
region_negara = ""
subregion_negara = ""
                                                
for i in range(len(data_json)):
    if list(data_json['alpha-3'])[i]==kode_negara:
        nama_negara = list(data_json['name'])[i]
        region_negara = list(data_json['region'])[i]
        subregion_negara = list(data_json['sub-region'])[i]
                                                
st.subheader('Negara dengan Produksi Terkecil di Keseluruhan Tahun')
st.markdown(f"Negara : {nama_negara}")
st.markdown(f"Kode Negara : {kode_negara}")
st.markdown(f"Region : {region_negara}")
st.markdown(f"SubRegion :{subregion_negara}")
st.markdown(f"Jumlah Produksi :  {jumlah_produksi}")


#Negara dengan Produksi Nol di Setiap Tahun
dfproduksinol = dfb[dfb.produksi == 0]
listnegaranol = []
listregionol = []
listsubregionol = []

for i in range(len(dfproduksinol)):
    for j in range(len(data_json)):
        if list (dfproduksinol['kode_negara'])[i] == list(data_json['alpha-3'])[j]:
            listnegaranol.append(list(data_json['name'])[j])
            listregionol.append(list(data_json['region'])[j])
            listsubregionol.append(list(data_json['sub-region'])[j])
st.subheader('Negara dengan Jumlah Produksi Minyak 0 (nol)')
dfproduksinol['negara'] = listnegaranol
dfproduksinol['region'] = listregionol
dfproduksinol['sub-region'] = listsubregionol
 
#Negara dengan Produksi Nok di Keseluruan Tahun                                                        
dfproduksikumulatifnol = dfb[dfb.produksi == 0]
listnegarakumulatifnol = []
listregionkumulatifnol = []
listsubregionkumulatifnol = []

for i in range(len(dfproduksikumulatifnol)):
    for j in range(len(data_json)):
        if list (dfproduksikumulatifnol['kode_negara'])[i] == list(data_json['alpha-3'])[j]:
            listnegarakumulatifnol.append(list(data_json['name'])[j])
            listregionkumulatifnol.append(list(data_json['region'])[j])
            listsubregionkumulatifnol.append(list(data_json['sub-region'])[j])

dfproduksikumulatifnol['negara'] = listnegarakumulatifnol
dfproduksikumulatifnol['region'] = listregionkumulatifnol
dfproduksikumulatifnol['sub-region'] = listsubregionkumulatifnol     
                                                        
st.write(dfproduksinol)
st.subheader('Negara dengan Jumlah Produksi Minyak 0 (nol) di Keseluruhan Tahun')
st.write(dfproduksikumulatifnol)
