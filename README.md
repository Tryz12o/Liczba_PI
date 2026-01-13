# Liczba PI - Obliczanie metodą całkowania numerycznego

Program oblicza przybliżoną wartość liczby π używając metody całkowania numerycznego z równoległymi obliczeniami.

## Kompilacja

```bash
g++ -std=c++11 -pthread pi_calculator.cpp -o pi_calculator
```

## Uruchomienie

```bash
./pi_calculator
```

Program poprosi o:
- Liczbę przedziałów całkowania (im więcej, tym dokładniejszy wynik)
- Liczbę wątków do równoległych obliczeń

## Przykład użycia

```
Wprowadź liczbę przedziałów całkowania: 100000000
Wprowadź liczbę wątków: 4

=== WYNIKI ===
Przybliżona wartość liczby PI: 3.14159265
Rzeczywista wartość PI:        3.14159265
Błąd bezwzględny:              5.06573e-10
Czas obliczeń:                 0.152 sekund
```

## Opis algorytmu

Program wykorzystuje metodę prostokątów do całkowania numerycznego funkcji:

```
∫[0,1] 4/(1+x²) dx = π
```

Obliczenia są równoleglone przy użyciu biblioteki `std::thread` z C++11.

## Benchmarking

Projekt zawiera skrypty Python do automatycznego testowania wydajności:

### Szybki test (demo)

```bash
python3 benchmark_demo.py
```

Testuje 3 konfiguracje (1M, 10M, 50M przedziałów) z 1-10 wątków.
Czas wykonania: ~1-2 minuty.

### Pełny benchmark

```bash
python3 benchmark.py
```

Testuje 3 konfiguracje (100M, 1000M, 3000M przedziałów) z 1-50 wątków.
⚠️ **Uwaga**: Pełny benchmark może trwać **kilka godzin**!

### Wymagania

```bash
pip install matplotlib tqdm numpy
```

### Wyniki

Skrypty generują:
- Wykres wydajności (3 linie dla różnych liczb przedziałów)
- Oś X: liczba wątków
- Oś Y: czas wykonania (sekundy)
- Statystyki przyspieszenia
- Plik PNG z wykresem