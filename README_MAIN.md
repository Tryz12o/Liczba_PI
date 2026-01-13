# Liczba PI - Całkowanie Numeryczne z Wielowątkowością

**Status**: ✅ Gotowy | **Algorytm**: Poprawny | **Optymalizacja**: +14% | **Dokumentacja**: Pełna

---

## ⚡ Szybki Start (5 min)

```bash
# Kompilacja
cd src
g++ -std=c++11 -O2 -pthread pi_calculator_optimized.cpp -o ../build/pi

# Uruchomienie
../build/pi
# Wpisz: 50000000 i 2

# Test
cd ../scripts
python3 benchmark_demo.py
```

---

## 📁 Projekt

**Cel**: Obliczanie π metodą całkowania numerycznego  
**Technologia**: C++11 + POSIX threads + optymalizacja cache  
**Rezultat**: π ≈ 3.14159265 (błąd: 1.7e-13)

### Struktura
```
Liczba_PI/
├── docs/              → 5 dokumentów (bez powtórzeń)
├── src/               → 2 wersje kodu C++
├── scripts/           → 5 narzędzi do testów
├── results/           → 2 wykresy PNG
└── build/             → 2 executables
```

### Dokumentacja (Czytaj w tej kolejności)

1. **[docs/WYNIKI_ANALIZY.md](docs/WYNIKI_ANALIZY.md)** ⭐ - **NAJPIERW TA!**
   - Werdykt: Algorytm 100% poprawny
   - Wniosek: Problem to sprzęt (2 rdzenie), nie kod

2. **[docs/POROWNANIE_WERSJI.md](docs/POROWNANIE_WERSJI.md)** - Dla programistów
   - v1 vs v2: +14% szybciej
   - Dlaczego: alignas(64) cache-line padding

3. **[docs/RAPORT_DIAGNOSTYKI.md](docs/RAPORT_DIAGNOSTYKI.md)** - Głębokie zagłębienie
   - Analiza wydajności
   - Prawo Amdahla w praktyce

4. **[docs/INSTRUKCJA_BENCHMARK.md](docs/INSTRUKCJA_BENCHMARK.md)** - Jak testować
   - benchmark_demo.py (~2 min)
   - benchmark.py (kilka h)

5. **[docs/MONITORING.md](docs/MONITORING.md)** - Narzędzia systemowe
   - monitor.sh i check_load.sh

---

## 💻 Kod

### [src/pi_calculator.cpp](src/pi_calculator.cpp) - Wersja 1
- Podstawowa: demonstracyjna, bez mutex'ów

### [src/pi_calculator_optimized.cpp](src/pi_calculator_optimized.cpp) ⭐ **ZALECANA**
- Z cache padding: +14% szybsza, produkcyjna

```cpp
struct alignas(64) CachePaddedDouble {
    double value = 0.0;  // Każdy element = pełna cache-line
};
```

---

## 🧪 Testy

| Skrypt | Czas | Opis |
|--------|------|------|
| `benchmark_demo.py` | ~2 min | Szybki test (10M, 50M przedziałów) |
| `benchmark.py` | kilka h | Pełny test (100M-3000M, 1-50 wątków) |
| `analiza_wydajnosci.py` | ~5 min | Analiza z wielokrotnymi przebiegami |
| `monitor.sh` | live | Monitor CPU/RAM (Ctrl+C) |
| `check_load.sh` | instant | Snapshot obciążenia |

```bash
# Szybki start testu
cd scripts
python3 benchmark_demo.py  # ~2 minuty
```

---

## 📊 Wyniki

| Konfiguracja | Czas | Wzrost |
|--|--|--|
| 50M, 1 wątek | 0.187s | 1.0x baseline |
| 50M, 2 wątki | 0.106s | **1.76x** ⭐ |

**Poprawa v2 vs v1**: +14%

Wykresy: [results/](results/) (PNG)

---

## ✅ Podsumowanie

| Aspekt | Status |
|--------|--------|
| Poprawność matematyczna | ✅ 100% |
| Thread-safety | ✅ Bezpieczne |
| Optymalizacja | ✅ +14% |
| Dokumentacja | ✅ Bez powtórzeń |
| Testy | ✅ Automatyczne |
| Produkcja | ✅ Gotowy |

---

## 🎓 Czego Się Nauczysz

✅ C++11 wielowątkowanie  
✅ Lambda expressions z przechwytywaniem  
✅ POSIX threads (std::thread)  
✅ Optymalizacja cache (alignas, padding)  
✅ Benchmarking i profiling  
✅ Prawo Amdahla w praktyce  

---

## ❓ FAQ

**Gdzie zacząć?** → [docs/WYNIKI_ANALIZY.md](docs/WYNIKI_ANALIZY.md)

**Którą wersję?** → `pi_calculator_optimized` (+14%)

**Dlaczego więcej wątków = wolniej?** → Codespace ma 2 rdzenie. Czytaj [docs/RAPORT_DIAGNOSTYKI.md](docs/RAPORT_DIAGNOSTYKI.md)

**Jak szybko testować?** → `python3 scripts/benchmark_demo.py`

---

**🚀 Zacznij: Czytaj dokumenty, uruchom testy, baw się parametrami!**
