from collections import namedtuple
import altair as alt
import math
import sqlite3
import datetime
import pandas as pd

##FONKSİYONLAR
def baglan(vt):
  global conn
  conn=sqlite3.connect(vt)
  global c
  c=conn.cursor()
  return conn,c


def tabloYap(tabloisim,sutunlar):
  komut="CREATE TABLE IF NOT EXISTS "+tabloisim+"("+sutunlar+")"
  c.execute(komut)
  conn.commit()

def veriEkle(tabloisim,*veriler):
  komut="INSERT INTO "+tabloisim+" VALUES"+str(veriler)
  c.execute(komut)
  conn.commit()



def uyeEkle(tabloisim, uye_isim, abonelik, yumurta, gun, telefon, saat):
  komut = "INSERT INTO "+tabloisim+" VALUES (?, ?, ?, ?, ?, ?)".format(tabloisim)
  veriler = (uye_isim, abonelik, yumurta, gun, telefon, saat.strftime("%H:%M"))
  c.execute(komut, veriler)
  conn.commit()



def veriGetir(tabloisim):
  komut="SELECT * FROM "+tabloisim
  c.execute(komut)
  sonuc=c.fetchall()
  return sonuc

def uyeisimleri():
  c.execute("SELECT uye_isim FROM GezenYumurta")
  uyeler=c.fetchall()
  sonuc=[]
  for x in uyeler:
    sonuc.append(x[0])
  return sonuc

def uyeSil(tabloisim,uye_isim):
    c.execute("DELETE FROM "+tabloisim+" WHERE uye_isim=?",(uye_isim,))
    conn.commit()

def yumurtaisimleri():
  c.execute("SELECT yumurta_isimleri FROM Yumurtalar")
  yumurtalar=c.fetchall()
  sonuc=[]
  for x in yumurtalar:
    sonuc.append(x[0])
  return sonuc

def yumurtaSil(tabloisim, yumurta_isimleri):
  c.execute("DELETE FROM " + tabloisim + " WHERE yumurta_isimleri=?", (yumurta_isimleri,))
  conn.commit()

def fiyatGuncelle(tabloisim, yumurta_isimleri, fiyat):
  fiyat_str = "{:.2f} ₺".format(fiyat)
  c.execute("UPDATE " + tabloisim + " SET Fiyat=? WHERE `yumurta_isimleri`=?", (fiyat_str, yumurta_isimleri))
  conn.commit()
  
  #ANASAYFA
  
import pandas as pd
import sqlite3
from fonksiyon import *
import streamlit as st

baglan("Yumurta.db")

st.header("Seçilen Günlerdeki Siparişler")

uyeler = veriGetir("GezenYumurta")
uyeler_tablo = pd.DataFrame(uyeler)
uyeler_tablo.columns = ["İsim", "Abonelik", "Yumurta", "Teslimat Günü", "Telefon", "Teslimat Saati"]

gunler = ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar"]
gun = st.selectbox("Teslimat Gününü Giriniz", gunler)

df_gun = uyeler_tablo[uyeler_tablo["Teslimat Günü"] == gun]

if not df_gun.empty:
    st.table(df_gun[["İsim", "Yumurta"]])
else:
    st.write("Belirtilen güne ait sipariş bulunamadı.")


st.header("Toplam Üye Sayısı")

uyeler = veriGetir("GezenYumurta")
uyeler_tablo = pd.DataFrame(uyeler)
uyeler_tablo.columns = ["İsim", "Abonelik", "Yumurta", "Teslimat Günü", "Telefon", "Teslimat Saati"]

uye_sayisi = len(uyeler_tablo)
st.markdown(f"Toplam Üye Sayısı: **{uye_sayisi}**")

st.header("Kazanç")




yumurta_fiyatlari = {
    "Organik": 15.0,
    "Selenyumlu": 8.0,
    "Bıldırcın": 5.0,
    "Kaz": 9.0,
    "Ördek": 11.0}




gunler = ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar"]



toplam_kazanc = 0.0

for gun in gunler:
    siparisler = uyeler_tablo[uyeler_tablo["Teslimat Günü"] == gun].copy()
    siparisler["Adet"] = 1
    siparisler["Yumurta Fiyatı"] = siparisler["Yumurta"].map(yumurta_fiyatlari)
    if siparisler["Abonelik"].iloc[0] == "Haftalık":
        siparisler["Adet"] *= 4
    siparisler["Toplam Fiyat"] = siparisler["Adet"] * siparisler["Yumurta Fiyatı"]
    gunluk_kazanc = siparisler["Toplam Fiyat"].sum()
    toplam_kazanc += gunluk_kazanc


    st.write(gun, "Günü Kazancı:", gunluk_kazanc)


st.write("Toplam Kazanç:", toplam_kazanc)

#YUMURTAekle

import streamlit as st
from fonksiyon import *
import pandas as pd

st.header("Yumurta Ekle")
baglan("Yumurta.db")
tabloYap("Yumurtalar",
         "isim TEXT,fiyat REAL")

with st.form("yumurta_ekle",clear_on_submit=True):
    yumurta_isim=st.selectbox("Yumurta İsmini Giriniz", ["Organik", "Selenyumlu", "Bıldırcın", "Kaz", "Ördek"])
    fiyat=st.number_input("Fiyat Giriniz")
    fiyat=str(fiyat)
    ekle=st.form_submit_button("Yumurta Fiyatını Ekle")
    if ekle:
        fiyat_text = f"{fiyat} ₺"
        veriEkle("Yumurtalar",yumurta_isim,fiyat_text)
        st.success("Yumurta Ve Fiyatı Başarılı Bir Şekilde Eklendi")
       
 #YUMURTALAR
import streamlit as st
from fonksiyon import *
import pandas as pd

st.header("Yumurtalar")
baglan("Yumurta.db")

yumurta_getir=veriGetir("Yumurtalar")
yumurta_tablo=pd.DataFrame(yumurta_getir)
yumurta_tablo.columns=["Yumurta İsmi","Fiyat"]
st.table(yumurta_tablo)

#YumurtaSilDüzenle

import streamlit as st
from fonksiyon import *


conn, c = baglan("Yumurta.db")
st.header("Yumurta Sil")
with st.form("yumurtaSil", clear_on_submit=True):
    yumurta_isim = st.selectbox("Silinecek Yumurtanın İsmini Giriniz", yumurtaisimleri())
    sil = st.form_submit_button("Yumurtayı Sil")

    if sil:
        yumurtaSil("Yumurtalar",yumurta_isim)
        st.success("Yumurta başarılı bir şekilde silindi")


st.header("Yumurta Fiyatlarını Güncelleme")

with st.form("fiyatGuncelle", clear_on_submit=True):
    secilen_yumurta = st.selectbox("Yumurta İsmi", yumurtaisimleri())
    fiyat = st.number_input("Yeni Fiyat", step=0.1, value=0.0, format="%.2f")
    guncelle = st.form_submit_button("Güncelle")

    if guncelle:
        fiyatGuncelle("Yumurtalar", secilen_yumurta, fiyat)
        st.success(secilen_yumurta + " yumurtasının fiyatı " + "{:.2f} ₺".format(fiyat) + " olarak güncellendi.")
#Uyeler
import streamlit as st
from fonksiyon import *
import pandas as pd

st.header("Üyeler")
baglan("Yumurta.db")


uyeler = veriGetir("GezenYumurta")
uyeler_tablo=pd.DataFrame(uyeler)
uyeler_tablo.columns=["İsim","Abonelik","Yumurta","Teslimat Günü","Telefon","Teslimat Saati"]
st.table(uyeler_tablo)

#UyelikEkle
import streamlit as st
from fonksiyon import *

st.header("Üyelik Ekle")
baglan("Yumurta.db")
tabloYap("GezenYumurta",
         "uye_isim TEXT,abonelik TEXT,yumurta TEXT,gun TEXT,telefon TEXT,saat TEXT")

with st.form("üyeEkle",clear_on_submit=True):
    uye_isim=st.text_input("Üye İsmi Giriniz")
    abonelik=st.selectbox("Aboneli Türü Giriniz",["Aylık","Haftalık"])
    yumurta=st.selectbox("Yumurta Türü Giriniz",["Organik", "Selenyumlu", "Bıldırcın", "Kaz", "Ördek"])
    gun=st.selectbox("Teslimat Günü",["Pazartesi","Salı","Çarşamba","Perşembe","Cuma","Cumartesi","Pazar"])
    telefon=st.text_input("Telefon Numarası Giriniz")
    saat = st.time_input("Lütfen Teslimat Saatini Seçiniz", value=datetime.time(8,0))

    ekle = st.form_submit_button("Kayıt Ekle")
    if ekle:
        uyeEkle("GezenYumurta",uye_isim,abonelik,yumurta,gun,telefon,saat)
        st.success("Kayıt Başarılı Bir Şekilde Eklendi")



#UyeSilDüzenle
import streamlit as st
from fonksiyon import *







conn, c = baglan("Yumurta.db")
st.header("Üye Sil")
with st.form("uyeSil", clear_on_submit=True):
    uye_isim = st.selectbox("Silinecek Üyenin İsmini Giriniz", uyeisimleri())
    sil = st.form_submit_button("Üyeyi Sil")

    if sil:
        uyeSil("GezenYumurta", uye_isim)
        st.success("üye başarılı bir şekilde silindi")

st.header("Üye Düzenle")
uyeler = veriGetir("GezenYumurta")
if uyeler:
    uye_isimleri = [uye[0] for uye in uyeler]
    uye_secimi = st.selectbox("Üye seçiniz:", uye_isimleri)

    if uye_secimi:
        uye = [uye for uye in uyeler if uye[0] == uye_secimi][0]
        abonelik_yeni = st.selectbox("Abonelik durumu:", ["Aylık", "Haftalık"], index=0 )
        yumurta_yeni = st.selectbox("Yumurta türü:", ["Organik", "Selenyumlu", "Bıldırcın", "Kaz", "Ördek"], index=0)
        gun_yeni = st.selectbox("Teslimat günü:",["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar"],
                                index=["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar"].index(uye[3]))
        telefon_yeni = st.text_input("Telefon numarası:", value=uye[4])
        saat_yeni = st.time_input("Teslimat saati:", value=datetime.datetime.strptime(uye[5], "%H:%M").time().replace(second=0))

        if st.button("Değişiklikleri kaydet"):
            try:
                veri = [abonelik_yeni, yumurta_yeni, gun_yeni, telefon_yeni, saat_yeni.strftime("%H:%M"), uye_secimi]
                komut = f"UPDATE GezenYumurta SET abonelik_turu=?, yumurta_turu=?, teslimat_gunu=?, telefon_numarası=?, saat=? WHERE uye_isim=?"

                c.execute(komut, veri)
                conn.commit()
                st.success(f"{uye_secimi} isimli üyenin bilgileri başarılı bir şekilde güncellendi")
            except Exception as e:
                print("Bir hata oluştu:", e)
                st.exception(e)

else:
    st.warning("Henüz hiç üye kaydedilmemiş.")

