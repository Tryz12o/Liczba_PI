# 🔍 Jak Monitorować Obciążenie Podczas Testów

## 📋 Metody Monitorowania

### ⭐ **METODA 1: Dwa Terminale (ZALECANA)**

Najlepsze rozwiązanie - jeden terminal dla benchmarku, drugi dla monitorowania:

#### Terminal 1 - Uruchom benchmark:
```bash
python3 benchmark_demo.py
# lub
python3 benchmark.py
```

#### Terminal 2 - Uruchom monitor:
```bash
# Opcja A: Interaktywny monitor z auto-odświeżaniem
./monitor.sh

# Opcja B: Jednorazowe sprawdzenie
./check_load.sh

# Opcja C: htop (najlepszy interfejs)
htop
```

**W htop naciśnij `1` aby zobaczyć wszystkie rdzenie CPU osobno!**

---

### 🎯 **METODA 2: watch + polecenie**

Automatyczne odświeżanie co N sekund:

```bash
# Odświeżanie co 2 sekundy
watch -n 2 './check_load.sh'

# Lub bezpośrednio sprawdzanie procesów
watch -n 1 'ps aux | grep pi_calculator | grep -v grep'

# Lub CPU i pamięć
watch -n 1 'top -bn1 | head -20'
```

---

### 💻 **METODA 3: Szybkie Jednorazowe Sprawdzenie**

#### Podstawowe info:
```bash
# Szybki snapshot
./check_load.sh
```

#### CPU:
```bash
# Aktualne użycie CPU
top -bn1 | grep "Cpu(s)"

# Load average (1min, 5min, 15min)
uptime

# Per-CPU statistics
mpstat -P ALL 1 1
```

#### Pamięć:
```bash
# Przegląd pamięci
free -h

# Szczegółowe info
cat /proc/meminfo | head -20
```

#### Procesy:
```bash
# Znajdź procesy pi_calculator
ps aux | grep pi_calculator

# Pokaż drzewo procesów
pstree -p | grep pi_calculator

# Liczba wątków
ps -eLf | grep pi_calculator | wc -l
```

---

### 🚀 **METODA 4: Logi do Pliku**

Zapisz monitoring do pliku, analizuj później:

```bash
# Uruchom benchmark w tle i monitoruj
python3 benchmark.py > benchmark_output.txt 2>&1 &

# W pętli zapisuj statystyki
while pgrep python3 > /dev/null; do
    echo "=== $(date) ===" >> system_load.log
    ./check_load.sh >> system_load.log
    sleep 5
done
```

---

## 📊 Rozumienie Wyników

### Load Average
```
load average: 0.50, 1.20, 2.00
              ^^^^  ^^^^  ^^^^
              1min  5min  15min
```

**Interpretacja** (dla systemu 4-rdzeniowego):
- `< 4.0` - System OK
- `4.0-8.0` - Wysokie obciążenie
- `> 8.0` - Przeciążenie

### CPU Usage
```
%Cpu(s): 75.5 us, 10.2 sy, 0.0 ni, 14.3 id
         ^^^^^    ^^^^^           ^^^^^
         user     system          idle
```

- **us (user)**: Procesy użytkownika (twój program)
- **sy (system)**: Kernel
- **id (idle)**: Bezczynność (im wyżej, tym więcej wolnego CPU)

### Pamięć
```
Mem:  7.8Gi total, 2.3Gi used, 5.5Gi free
```

Sprawdź czy `used` nie zbliża się do `total` (ryzyko OOM).

---

## 🎛️ Komendy według Scenariusza

### Sprawdzenie ile rdzeni CPU masz:
```bash
nproc
# lub
lscpu | grep "^CPU(s):"
```

### Sprawdzenie ile wątków używa program:
```bash
# Gdy program działa:
ps -eLf | grep pi_calculator | wc -l

# Lub bardziej szczegółowo:
ps -eLf | grep pi_calculator | grep -v grep
```

### Sprawdzenie czy wszystkie rdzenie są wykorzystane:
```bash
# Uruchom htop i naciśnij '1'
htop

# Lub w top naciśnij '1'
top
```

### Monitoring w czasie rzeczywistym tylko CPU:
```bash
mpstat 1
```

### Monitoring z historią (graficzny):
```bash
# Jeśli dostępny
vmstat 2
```

---

## 💡 Praktyczne Przykłady

### Przykład 1: Benchmark + Monitoring w Dwóch Terminalach

**Terminal 1:**
```bash
cd /workspaces/Liczba_PI
python3 benchmark_demo.py
```

**Terminal 2:**
```bash
cd /workspaces/Liczba_PI
htop
# lub
./monitor.sh
```

### Przykład 2: Benchmark z Automatycznym Logowaniem

```bash
# Stwórz skrypt
cat > run_with_monitoring.sh << 'EOF'
#!/bin/bash
echo "Rozpoczynam benchmark z monitoringiem..."

# Uruchom benchmark
python3 benchmark_demo.py &
BENCHMARK_PID=$!

# Monitoruj w pętli
while kill -0 $BENCHMARK_PID 2>/dev/null; do
    ./check_load.sh >> monitoring_$(date +%Y%m%d_%H%M%S).log
    sleep 5
done

echo "Benchmark zakończony!"
EOF

chmod +x run_with_monitoring.sh
./run_with_monitoring.sh
```

### Przykład 3: Sprawdzanie Wydajności Per Rdzeń

```bash
# Uruchom w osobnym terminalu podczas benchmarku
watch -n 1 'mpstat -P ALL 1 1 | grep -E "CPU|all|[0-9]"'
```

---

## 🎨 Porównanie Narzędzi

| Narzędzie | Zalety | Kiedy używać |
|-----------|---------|--------------|
| **htop** | ✅ Kolorowy, interaktywny, intuicyjny | Ogólny monitoring |
| **top** | ✅ Wszędzie dostępny | Gdy brak htop |
| **monitor.sh** | ✅ Customowy, czytelny | Specyficzny monitoring |
| **check_load.sh** | ✅ Szybki snapshot | Jednorazowe sprawdzenie |
| **mpstat** | ✅ Per-CPU stats | Analiza per-core |
| **vmstat** | ✅ Historia w czasie | Analiza trendów |

---

## ⚠️ Ostrzeżenia

1. **Nie uruchamiaj ciężkiego monitoringu podczas benchmarku** - może wpłynąć na wyniki
2. **Używaj `watch` z sensownym interwałem** - 1-2 sekundy to minimum
3. **W środowiskach współdzielonych** (jak Codespaces) pamiętaj o limitach zasobów

---

## 🎓 Wskazówki Pro

### Sprawdź ile rdzeni ma twój Codespace:
```bash
nproc
```

### Optymalny benchmark - użyj tyle wątków ile masz rdzeni:
```bash
# Automatyczne ustawienie
CORES=$(nproc)
echo -e "10000000\n$CORES" | ./pi_calculator
```

### Znajdź bottleneck:
```bash
# Jeśli CPU nie jest na 100%, problem może być w:
# - Synchronizacji (mutex)
# - I/O
# - Cache misses

# Sprawdź kontekst switches:
vmstat 1 10
# Wysoka wartość "cs" = dużo przełączeń kontekstu
```

---

**Powodzenia w testowaniu! 🚀**
