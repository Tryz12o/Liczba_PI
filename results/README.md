# Wyniki Testów

## 📂 Zawartość

```
results/
├── analiza_wydajnosci.png ........ Wykres analizy detali (351K)
├── wykres_wydajnosci_demo.png .... Wykres demo (298K)
└── README.md ..................... Ten plik
```

## 📊 Pliki

### analiza_wydajnosci.png
- **Rozmiar**: 351K
- **Źródło**: `scripts/analiza_wydajnosci.py`
- **Zawartość**: 2 wykresy (średnie z 3 przebiegów)

### wykres_wydajnosci_demo.png
- **Rozmiar**: 298K
- **Źródło**: `scripts/benchmark_demo.py`
- **Zawartość**: 3 linie dla różnych konfiguracji przedziałów

## 🚀 Generowanie

```bash
cd ../scripts

# Szybki test (2 min) → demo wykres
python3 benchmark_demo.py

# Analiza (5 min) → analiza wykres
python3 analiza_wydajnosci.py
```
- 📈 2 wykresy podrzędne
- 📉 Średnie z 3 przebiegów

---

## 🎯 Jak Generować Wykresy

### Szybki Test
```bash
cd ../scripts
python3 benchmark_demo.py
# Generuje: ../results/wykres_wydajnosci_demo.png
```

### Analiza Szczegółowa
```bash
cd ../scripts
python3 analiza_wydajnosci.py
# Generuje: ../results/analiza_wydajnosci.png
```

### Pełny Test (kilka godzin)
```bash
cd ../scripts
python3 benchmark.py
# Generuje: ../results/wykres_wydajnosci.png
```

---

## 📊 Struktura Wyników

```
results/
├── wykres_wydajnosci_demo.png     (298K)
├── analiza_wydajnosci.png         (351K)
└── wykres_wydajnosci.png          (jeśli pełny test)
```

---

## 🔍 Interpretacja Wykresów

### Oś X
Liczba wątków (1, 2, 3, ..., N)

### Oś Y
Czas wykonania w sekundach

### Linie (3 kolory)
- Niebieska: Mała liczba przedziałów (szybkie)
- Magenta: Średnia liczba przedziałów
- Pomarańczowa: Duża liczba przedziałów (wolne)

### Interpretacja Trendu

**Linia idzie w dół** → ✅ Dobre przyspieszenie  
**Linia idzie w górę** → ⚠️ Problem - więcej wątków = wolniej  
**Linia płaska** → ⚠️ Brak przyspieszenia

---

## 📈 Przykładowe Wyniki

### Test Demo (Codespace, 2 rdzenie)

```
10,000,000 przedziałów:
  1 wątek:  0.0127s
  2 wątki:  0.0162s (-27% wolniej!)
  ...

50,000,000 przedziałów:
  1 wątek:  0.0701s
  2 wątki:  0.0723s (-3% wolniej!)
  ...
```

**Przyspieszenie**: 0.78-0.97x (powinno być ~2.0x)

---

## 💾 Rozmiary Plików

| Plik | Rozmiar | Typ |
|------|---------|-----|
| wykres_wydajnosci_demo.png | ~298K | PNG (300 DPI) |
| analiza_wydajnosci.png | ~351K | PNG (300 DPI) |

Wysoka rozdzielczość (300 DPI) = doskonała do prezentacji!

---

## 🎓 Co Możesz Nauczyć Się Z Wyników

1. **Skalowanie wielowątkowe**: Jak wydajność rośnie (lub nie)
2. **Prawo Amdahla**: Teoretyczne vs praktyczne przyspieszenie
3. **Overhead wątków**: Koszt tworzenia i synchronizacji
4. **False sharing**: Problem z cache memory
5. **Sprzęt vs algorytm**: Dlaczego wyniki są takie czy inne

---

## 🚀 Następne Kroki

1. **Uruchom demo**: `python3 ../scripts/benchmark_demo.py`
2. **Obejrzyj wykresy**: Otwórz `.png` w przeglądarce
3. **Czytaj raport**: `docs/WYNIKI_ANALIZY.md`
4. **Przeanalizuj**: `docs/RAPORT_DIAGNOSTYKI.md`

---

**Wszystkie wykresy są generowane automatycznie!** 📊
