# Kod Źródłowy

## 📂 Zawartość

```
src/
├── pi_calculator.cpp ................. v1: podstawowa
├── pi_calculator_optimized.cpp ....... v2: +14% szybciej ⭐
└── README.md ......................... Ten plik
```

## 🎯 Porównanie

| Aspekt | v1 | v2 |
|--------|----|----|
| Cache padding | ❌ | ✅ alignas(64) |
| Szybkość | baseline | **+14%** |
| Produkcja | ⚠️ | ✅ |

## 🔨 Kompilacja

```bash
# Wersja zalecaną (v2)
g++ -std=c++11 -O2 -pthread pi_calculator_optimized.cpp -o ../build/pi

# Lub wersję 1 do porównania
g++ -std=c++11 -O2 -pthread pi_calculator.cpp -o ../build/pi_v1
```

## 🚀 Uruchomienie

```bash
../build/pi
# Wpisz: 50000000 i 2
```

## 📝 Szczegóły

**v1**: Demonstracyjna, baza do zrozumienia  
**v2**: Cache-line optimization, +14% szybsza (REKOMENDOWANA)

Oba zawierają:
- Lambda z przechwytywaniem `[&...]`
- std::thread z wielowątkowością
- Całkowanie numeryczne do obliczeń π

Szczegóły: [../docs/POROWNANIE_WERSJI.md](../docs/POROWNANIE_WERSJI.md)

### Wersja Zoptymalizowana (ZALECANA)
```bash
g++ -std=c++11 -O2 -pthread pi_calculator_optimized.cpp -o ../build/pi_calculator_opt
```

### Z Debuggingiem
```bash
g++ -std=c++11 -g -O2 -pthread pi_calculator_optimized.cpp -o ../build/pi_calculator_debug
```

---

## 🚀 Uruchomienie

```bash
../build/pi_calculator_opt
Wprowadź liczbę przedziałów całkowania: 50000000
Wprowadź liczbę wątków: 2

=== WYNIKI ===
Przybliżona wartość liczby PI: 3.14159
Rzeczywista wartość PI:        3.14159
Błąd bezwzględny:              1.72307e-13
Czas obliczeń:                 0.0683035 sekund
```

---

## 📊 Porównanie Wersji

| Aspekt | Podstawowa | Zoptymalizowana |
|--------|-----------|-----------------|
| Rozmiar | 2.2K | 2.3K |
| Wydajność | 0.0796s | 0.0683s ✅ |
| Przyspieszenie | baseline | +14% |
| False Sharing | ⚠️ Możliwe | ✅ Brak |
| Cache Padding | Nie | ✅ Tak |
| Produkcja | Nie | ✅ Tak |

---

## 🎓 Kluczowe Elementy

### 1. Lambda z Przechwytywaniem
```cpp
auto calculate_pi = [&thread_results, n, h, num_threads](int thread_id) {
    // Przechwytywanie przez referencję &
    // Parametr: thread_id
};
```

### 2. POSIX Threads
```cpp
std::vector<std::thread> threads;
for (int i = 0; i < num_threads; ++i) {
    threads.emplace_back(calculate_pi, i);  // Tworzy wątek
}

for (auto& t : threads) {
    t.join();  // Czeka na koniec
}
```

### 3. Synchronizacja
```cpp
// ❌ ZŁE (mutex bottleneck):
std::lock_guard<std::mutex> lock(pi_mutex);
pi += local_sum;

// ✅ DOBRE (każdy wątek pisze do siebie):
thread_results[thread_id] = local_sum * h;
```

### 4. Cache Optimization
```cpp
struct alignas(64) CachePaddedDouble {
    double value = 0.0;
    // Automatycznie padded do 64 bajtów
    // = rozmiar cache line
};
```

---

## 📖 Dokumentacja Kodu

### Funkcja main()

1. **Wejście**: liczba przedziałów, liczba wątków
2. **Inicjalizacja**: przygotowanie danych
3. **Pomiar czasu**: std::chrono
4. **Tworzenie wątków**: emplace_back
5. **Synchronizacja**: join()
6. **Sumowanie wyników**: agregacja wyników
7. **Wynik**: PI oraz czas

---

## 🔍 Co Się Nauczysz

- ✅ Wyrażenia lambda w C++
- ✅ std::thread i wielowątkowość
- ✅ Przechwytywanie zmiennych
- ✅ Cache line awareness
- ✅ False sharing i padding
- ✅ alignas() dla wyrównania

---

## 💡 Wskazówki

1. **Zwykła wersja**: Do nauki i zrozumienia
2. **Zoptymalizowana**: Do produkcji i benchmarków
3. **Oba pliki**: Świetne do porównania optymalizacji

---

Wybierz zoptymalizowaną wersję dla ostatecznego użytku! ⭐
