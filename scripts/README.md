# Narzędzia i Testy

## 📂 Zawartość

```
scripts/
├── benchmark_demo.py ............... Test szybki (~2 min) ⭐
├── benchmark.py ................... Test pełny (kilka h)
├── analiza_wydajnosci.py ......... Analiza (5 min)
├── monitor.sh ..................... Monitor live
├── check_load.sh .................. Snapshot
└── README.md ...................... Ten plik
```

## 🧪 Testy

### benchmark_demo.py - SZYBKI TEST ⭐
```bash
python3 benchmark_demo.py
```
- ⏱️ **Czas**: ~2 minuty
- 📊 **Parametry**: 10M, 50M przedziałów × 1-10 wątków
- 📈 **Wynik**: Wykres `../results/wykres_wydajnosci_demo.png`

### benchmark.py - PEŁNY TEST
```bash
python3 benchmark.py
```
- ⏱️ **Czas**: kilka godzin
- 📊 **Parametry**: 100M, 1000M, 3000M × 1-50 wątków
- 📈 **Wynik**: Szczegółowe dane

### analiza_wydajnosci.py - ANALIZA
```bash
python3 analiza_wydajnosci.py
```
- ⏱️ **Czas**: ~5 minut
- 📊 **Wielokrotne przebiegi**: 3 uruchomienia per konfiguracja
- 📈 **Wynik**: Wykres z trendem `../results/analiza_wydajnosci.png`

## 🔍 Narzędzia Systemowe

### monitor.sh - MONITOR LIVE
```bash
./monitor.sh
```
- 🔄 Auto-refresh co 2 sekundy
- 📊 CPU, RAM, wątki
- ⏹️ Ctrl+C aby zatrzymać

### check_load.sh - SNAPSHOT
```bash
./check_load.sh
```
- 📸 Jednorazowe sprawdzenie
- 📊 Szybka diagnostyka systemu

## 🚀 Rekomendacja

**Zacznij**: `python3 benchmark_demo.py` (~2 min)
