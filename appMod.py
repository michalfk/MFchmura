# -*- coding: utf-8 -*-
"""
Created on Tue May  5 19:50:26 2026

@author: Admin
"""

import streamlit as st #Do interfejsu graficznego
import datetime as dt #Do pobrania daty
import logging #Do zostawiania logow
import sys
import requests


#ustawienie poziomu na INFO -> w konsoli powoduje wyswietlenie logu INFO: ... oraz stdout na wyjscie w konsoli
logging.basicConfig(level=logging.INFO, handlers=[logging.StreamHandler(sys.stdout)])

#zapisanie danych do zmiennych
autor = "autor: Michał Fiedorek"
x = "Uruchomiono: " + dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
port = "Port: " + str(st.get_option("server.port"))

#komunikaty
logging.info(autor)
logging.info(x)
logging.info(port)

#info na stronie
st.text(autor)
st.text(x)
st.text(port)


#Wybor miasta
miasto = st.selectbox("Wybierz miasto: ", ['Polska (Warsaw)', 'Polska (Lublin)', 'Niemcy (Berlin)', 'Niemcy (Frankfurt)'])
#Wyciagniecie samego miasta ze stringa, bedzie potrzebne do sprawdzenia pogody
miasto_split = miasto.split()[1].replace("(", "").replace(")", "")

st.text("Wybrane miasto: " + miasto)

if st.button("Sprawdz pogode"):
    #wyciagniecie wspolrzednych dla wybranych miast
    url_wspolrzedne = "https://geocoding-api.open-meteo.com/v1/search?name=" + miasto_split
    response = requests.get(url_wspolrzedne)
    data = response.json()
    szerokosc = data['results'][0]['latitude']
    wysokosc = data['results'][0]['longitude']

    #wyciagniecie pogody (temperatury i predkosci wiatru)
    url_pogoda = "https://api.open-meteo.com/v1/forecast?latitude=x&longitude=y&current_weather=true"
    url_pogoda = url_pogoda.replace("x", str(szerokosc)).replace("y", str(wysokosc))
    response_aktPogoda = requests.get(url_pogoda)
    data2 = response_aktPogoda.json()
    akt_temp = str(data2['current_weather']['temperature'])
    akt_wiatr = str(data2['current_weather']['windspeed'])
    
    #wyswietlenie pogody
    st.text("Aktualna temperatura: " + akt_temp + " stopni C")
    st.text("Aktualna predkosc wiatru: " + akt_wiatr + " km\H")
    
