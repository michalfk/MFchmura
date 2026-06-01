#Et1 budowa i instalacja zaleznosci ============
# Używamy oficjalnego, lekkiego obrazu Pythona jako bazy do instalacji bibliotek
FROM python:3.11-slim AS compile-img

#Wyswietlenie danych zgodnie z OCI
LABEL org.opencontainers.image.authors="Michał Fiedorek" 

WORKDIR /app

#skopiowanie pliku requirments.txt zeby po zmianie w kodzie docker nie instalowal bibliotek od nowa
COPY requirements.txt . 


#instalacja wheels zeby zbudowac pakietów binarnych ze skompilowanym kodem - a następnie skopiowanie plików wheels do etapu budowania i zainstalowanie ich tam
RUN pip install --no-cache-dir --user -r requirements.txt 


#Et 2 obraz koncowy
# Rozpoczynamy od świeżego, czystego obrazu slim, aby odrzucić zbędne pliki z etapu budowania
FROM python:3.11-slim AS build-img 

WORKDIR /app

#Skopiowanie bibliotek z poprzedniego etapu -> zmniejsza wage
COPY --from=compile-img /root/.local /root/.local 

# skopiowanie aplikacji python
COPY appMod.py .

# zaktualizowanie PATH zeby biblioteki z etapu budowania byly widoczne
ENV PATH=/root/.local/bin:$PATH 

# Gdzie domyslnie ma dzialac aplikacja
EXPOSE 8501

#Healthcheck -> sprawdzenie co 30 sekund czy aplikacja odpowiada na porcie 8501
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD python3 -c "import urllib.request; urllib.request.urlopen('http://localhost:8501')" || exit 1

#Uruchomienie aplikacji wewnatrz kontenera i zablokowanie otwierania przegladarki wewnatrz dockera
CMD ["streamlit", "run", "appMod.py", "--server.port=8501", "--server.address=0.0.0.0", "--browser.gatherUsageStats=false"]