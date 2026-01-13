# 📊 Instrukcja Użytkowania Skryptów Benchmarkowych

## 🎯 Przegląd

Projekt zawiera dwa skrypty Python do automatycznego testowania wydajności programu obliczającego liczbę PI:

1. **benchmark_demo.py** - Szybki test demonstracyjny (~2 minuty)
2. **benchmark.py** - Pełny benchmark (~kilka godzin)

## 🚀 Przygotowanie

### 1. Kompilacja programu C++

```bash
g++ -std=c++11 -pthread pi_calculator.cpp -o pi_calculator
```

### 2. Instalacja zależności Python

```bash
pip install matplotlib tqdm numpy
```

## 🧪 Skrypt Demonstracyjny (Szybki Test)

### Parametry:
- **Liczba przedziałów**: 1'000'000, 10'000'000, 50'000'000
- **Zakres wątków**: 1-10
- **Czas wykonania**: ~1-2 minuty
- **Liczba testów**: 30 (3 przedziały × 10 wątków)

### Uruchomienie:

```bash
python3 benchmark_demo.py
```

### Wyjście:
- **Plik**: `wykres_wydajnosci_demo.png`
- **Wykres**: 3 linie pokazujące wydajność dla różnych liczb przedziałów
- **Statystyki**: Najszybsze czasy i przyspieszenie

---

## 🏆 Pełny Benchmark

### Parametry:
- **Liczba przedziałów**: 100'000'000, 1'000'000'000, 3'000'000'000
- **Zakres wątków**: 1-50
- **Czas wykonania**: ⚠️ **KILKA GODZIN** (szacunkowo 3-6 godzin)
- **Liczba testów**: 150 (3 przedziały × 50 wątków)

### Uruchomienie:

```bash
python3 benchmark.py
```

**Zalecenia:**
- Uruchom w `screen` lub `tmux` aby móc odłączyć terminal
- Upewnij się, że komputer ma dostępne zasoby CPU
- Nie uruchamiaj innych wymagających aplikacji

### Przykład użycia z screen:

```bash
# Utwórz nową sesję screen
screen -S pi_benchmark

# Uruchom benchmark
python3 benchmark.py

# Odłącz sesję: Ctrl+A, następnie D
# Wróć do sesji: screen -r pi_benchmark
```

### Wyjście:
- **Plik**: `wykres_wydajnosci.png`
- **Wykres**: Szczegółowa analiza wydajności
- **Statystyki**: Kompleksowa analiza przyspieszenia

---

## 📈 Interpretacja Wyników

### Wykres pokazuje:

**Oś X**: Liczba wątków (1-10 lub 1-50)  
**Oś Y**: Czas wykonania w sekundach  
**Linie**: 3 różne konfiguracje liczby przedziałów

### Typowe obserwacje:

✅ **Idealne przyspieszenie**: Czas maleje proporcjonalnie do liczby wątków  
⚠️ **Overhead wątków**: Przy małych zadaniach więcej wątków może spowolnić  
🔄 **Prawo Amdahla**: Przyspieszenie jest ograniczone przez część sekwencyjną  
💻 **Nasycenie CPU**: Po osiągnięciu liczby rdzeni przyspieszenie maleje

### Przykład interpretacji:

```
1,000,000 przedziałów:
  Najszybszy: 0.0029s (3 wątków)
  Najwolniejszy: 0.0043s (10 wątków)
  Przyspieszenie: 1.46x
```

**Wnioski**: 
- Dla małych zadań overhead tworzenia wątków przewyższa korzyści
- Optymalna liczba wątków to 3
- Więcej wątków = więcej overhead = wolniej

---

## 🛠️ Dostosowywanie Parametrów

### Edycja benchmark_demo.py:

```python
# Zmień wartości przedziałów
INTERVALS = [1_000_000, 10_000_000, 50_000_000]

# Zmień zakres wątków
THREAD_RANGE = range(1, 11)  # Od 1 do 10
```

### Edycja benchmark.py:

```python
# Zmień wartości przedziałów
INTERVALS = [100_000_000, 1_000_000_000, 3_000_000_000]

# Zmień zakres wątków
THREAD_RANGE = range(1, 51)  # Od 1 do 50
```

---

## 📊 Format Wyjścia

### Konsola:

```
============================================================
BENCHMARK PROGRAMU OBLICZAJĄCEGO LICZBĘ PI
============================================================
Przedziały: [100000000, 1000000000, 3000000000]
Zakres wątków: 1 - 50
============================================================

Testowanie dla 100,000,000 przedziałów...
   1 wątków: 0.3245s
   2 wątków: 0.1678s
   ...
```

### Plik PNG:

Profesjonalny wykres z:
- Tytułem i opisami osi
- Legendą (3 linie dla różnych przedziałów)
- Siatką dla łatwiejszego odczytu
- Wysoką rozdzielczością (300 DPI)

---

## ⚡ Wskazówki Optymalizacji

1. **Znalezienie optymalnej liczby wątków**: Uruchom demo i sprawdź przy jakiej liczbie wątków czas jest najkrótszy

2. **System z 4 rdzeniami**: Optymalna liczba wątków to zazwyczaj 4-8

3. **System z 8+ rdzeniami**: Możesz zwiększyć liczbę przedziałów dla lepszej równoległości

4. **Małe zadania**: Unikaj nadmiernej liczby wątków (overhead > korzyści)

5. **Duże zadania**: Wykorzystaj wszystkie dostępne rdzenie

---

## 🐛 Rozwiązywanie Problemów

### Problem: "ModuleNotFoundError: No module named 'matplotlib'"

**Rozwiązanie**:
```bash
pip install matplotlib tqdm numpy
```

### Problem: Wykres się nie wyświetla

**Rozwiązanie**:
- Wykres jest zapisywany jako PNG
- Jeśli używasz SSH bez X11, wykres nie wyświetli się interaktywnie
- Plik PNG zawsze zostanie zapisany i można go otworzyć później

### Problem: Benchmark trwa zbyt długo

**Rozwiązanie**:
- Użyj `benchmark_demo.py` zamiast pełnego benchmarku
- Zmniejsz zakres wątków w skrypcie
- Zmniejsz wartości INTERVALS

### Problem: "Permission denied"

**Rozwiązanie**:
```bash
chmod +x pi_calculator
chmod +x benchmark.py
chmod +x benchmark_demo.py
```

---

## 📝 Dodatkowe Informacje

### Struktura wyników:

```
results = {
    100_000_000: [0.324, 0.167, 0.118, ...],  # Czasy dla 1-50 wątków
    1_000_000_000: [3.245, 1.678, 1.189, ...],
    3_000_000_000: [9.734, 5.034, 3.567, ...]
}
```

### Dokładność obliczeń:

Im więcej przedziałów, tym dokładniejszy wynik, ale dłuższy czas:
- 1M przedziałów: błąd ~10⁻⁶
- 100M przedziałów: błąd ~10⁻⁸
- 1000M przedziałów: błąd ~10⁻¹⁰

---

## 🎓 Cel Edukacyjny

Skrypty benchmarkowe pokazują:

1. **Prawo Amdahla**: Ograniczenia równoległości
2. **Overhead wątków**: Koszty synchronizacji
3. **Skalowalność**: Jak wydajność rośnie z liczbą wątków
4. **Optymalizacja**: Znajdowanie optymalnej konfiguracji

**Eksperymentuj i ucz się!** 🚀
