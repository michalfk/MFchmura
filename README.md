Aplikacja pogodowa napisana w python wraz z zautomatyzowanym potokiem CI/CD zrealizowanym za pomoca GHActions

## 1. Architektura i Konfiguracja Kontenera (Dockerfile)
Aplikacja została skonteneryzowana przy użyciu wieloetapowego budowania.
* **Etap 1 (Builder):** Wykorzystuje obraz `python:3.11-slim`. Instaluje zależności zdefiniowane w `requirements.txt` do katalogu użytkownika (`--user`). Dodatkowo na tym etapie aktualizowane są pakiety systemowe w celu mitygacji podatności.
* **Etap 2 (Final):** Korzysta z czystego obrazu bazowego, do którego kopiowane są wyłącznie zainstalowane biblioteki oraz kod źródłowy aplikacji (`appMod.py`). Zapewnia to minimalny rozmiar obrazu produkcyjnego.

## 2. Opis Kroków Potoku CI/CD
Potok zdefiniowany w pliku `.github/workflows/deploy.yml` uruchamia się automatycznie przy każdym wypchnięciu kodu (`git push`) do gałęzi `main`. Realizuje on następujące wymagania:

* **Budowanie wieloarchitekturowe:** Dzięki integracji z emulatorami `QEMU` oraz narzędziem `Docker Buildx`, potok buduje finalny obraz jednocześnie na dwie architektury procesorowe: `linux/amd64` oraz `linux/arm64`.
* **Zarządzanie pamięcią podręczną:** W celu przyspieszenia działania potoku, konfiguracja wykorzystuje zewnętrzny rejestr Docker Hub do zapisu i odczytu cache w trybie `max` (`mode=max`).
* **Skanowanie bezpieczeństwa CVE:** Przed publikacją obrazu uruchamiany jest skaner `Trivy`. Skanuje on zbudowany obraz i w przypadku wykrycia podatności o krytyczności `HIGH` lub `CRITICAL` celowo przerywa potok. Znalezione podatności w obrazie bazowym zostały przeanalizowane i zabezpieczone przy użyciu pliku `.trivyignore`.

## 3. Schemat Tagowania Obrazów
Zostal zastosowany nastepujacy schemat tagowania:
1. `:latest` - Wskaźnik zawsze wskazujący na najnowszą, bezpieczną i pomyślnie zbudowaną wersję aplikacji.
2. `:${{ github.sha }}` - Tag dynamiczny, wykorzystujący unikalny skrót SHA commitu z Git. Pozwala to na precyzyjne powiązanie konkretnego obrazu kontenera z dokładną wersją kodu źródłowego w historii Git.

## 4. Potwierdzenie Działania
Łańcuch GitHub Actions został pomyślnie uruchomiony w zakładce **Actions**, potwierdzając poprawne przejście wszystkich testów bezpieczeństwa oraz pomyślną publikację wieloplatformowego obrazu w rejestrze **GitHub Container Registry (ghcr.io)**.