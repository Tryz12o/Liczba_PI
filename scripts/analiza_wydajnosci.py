#!/usr/bin/env python3
"""
Skrypt do analizy wydajności - sprawdza czy czas maleje wraz ze wzrostem wątków
"""

import subprocess
import re
import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm

INTERVALS = [10_000_000, 50_000_000]  # Mniejsze wartości dla szybkiego testu
THREAD_RANGE = range(1, 9)  # Od 1 do 8 wątków
EXECUTABLE = "./pi_calculator"
NUM_RUNS = 3  # Uruchom każdą konfigurację 3 razy dla średniej

def run_pi_calculator(intervals, threads):
    """
    Uruchamia program pi_calculator z podanymi parametrami
    Zwraca czas wykonania w sekundach
    """
    try:
        input_data = f"{intervals}\n{threads}\n"
        
        result = subprocess.run(
            [EXECUTABLE],
            input=input_data,
            capture_output=True,
            text=True,
            timeout=120
        )
        
        match = re.search(r'Czas obliczeń:\s+([\d.]+)\s+sekund', result.stdout)
        if match:
            return float(match.group(1))
        else:
            return None
            
    except Exception as e:
        print(f"Błąd: {e}")
        return None

def main():
    print("=" * 70)
    print("ANALIZA WYDAJNOŚCI - SPRAWDZENIE SKALOWANIA WĄTKÓW")
    print("=" * 70)
    print(f"Przedziały: {INTERVALS}")
    print(f"Zakres wątków: {min(THREAD_RANGE)} - {max(THREAD_RANGE)}")
    print(f"Liczba przebiegów na konfigurację: {NUM_RUNS}")
    print("=" * 70)
    
    results = {intervals: [] for intervals in INTERVALS}
    all_times = {intervals: [] for intervals in INTERVALS}
    
    total_tests = len(INTERVALS) * len(THREAD_RANGE) * NUM_RUNS
    
    with tqdm(total=total_tests, desc="Wykonywanie testów") as pbar:
        for intervals in INTERVALS:
            print(f"\n\n📊 Testowanie dla {intervals:,} przedziałów ({NUM_RUNS} przebiegów na konfigurację)...")
            
            for threads in THREAD_RANGE:
                times_for_config = []
                
                for run in range(NUM_RUNS):
                    time = run_pi_calculator(intervals, threads)
                    if time is not None:
                        times_for_config.append(time)
                        all_times[intervals].append((threads, time))
                    pbar.update(1)
                
                if times_for_config:
                    avg_time = np.mean(times_for_config)
                    std_dev = np.std(times_for_config)
                    results[intervals].append(avg_time)
                    tqdm.write(f"  {threads:2d} wątków: {avg_time:.4f}s ± {std_dev:.4f}s (min: {min(times_for_config):.4f}s, max: {max(times_for_config):.4f}s)")
                else:
                    results[intervals].append(None)
                    tqdm.write(f"  {threads:2d} wątków: BŁĄD")
    
    # Analiza wyników
    print("\n\n" + "=" * 70)
    print("ANALIZA WYNIKÓW")
    print("=" * 70)
    
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    
    for idx, intervals in enumerate(INTERVALS):
        times = results[intervals]
        valid_threads = [t for t, time in zip(THREAD_RANGE, times) if time is not None]
        valid_times = [time for time in times if time is not None]
        
        print(f"\n📈 {intervals:,} przedziałów:")
        print("   Liczba wątków → Czas (s)")
        for t, time in zip(valid_threads, valid_times):
            print(f"   {t:2d} → {time:.4f}")
        
        # Sprawdzenie trendu
        if len(valid_times) > 1:
            min_time = min(valid_times)
            max_time = max(valid_times)
            min_idx = valid_threads[valid_times.index(min_time)]
            max_idx = valid_threads[valid_times.index(max_time)]
            
            speedup = max_time / min_time
            
            print(f"\n   ✓ Najszybszy: {min_time:.4f}s ({min_idx} wątków)")
            print(f"   ✗ Najwolniejszy: {max_time:.4f}s ({max_idx} wątków)")
            print(f"   📊 Ratio szybkości: {speedup:.2f}x")
            
            # Trend analysis
            if max_idx > min_idx:
                print(f"   ⚠️  OSTRZEŻENIE: Więcej wątków → WOLNIEJ!")
                print(f"       Czas rośnie zamiast maleć!")
            elif min_idx < 2:
                print(f"   ✅ Dobra skalowalność - optymalnie przy {min_idx} wątkach")
            else:
                print(f"   ⚠️  Możliwy problem - czas nie maleje znacznie")
            
            # Oblicz czy jest liniowe przyspieszenie
            if len(valid_threads) >= 2:
                time_1_thread = valid_times[0] if valid_threads[0] == 1 else None
                time_2_threads = None
                for t, time in zip(valid_threads, valid_times):
                    if t == 2:
                        time_2_threads = time
                        break
                
                if time_1_thread and time_2_threads:
                    linear_speedup = time_1_thread / time_2_threads
                    print(f"   Przyspieszenie 1→2 wątki: {linear_speedup:.2f}x (ideał: ~2.0x)")
                    if linear_speedup < 1.3:
                        print(f"   ⚠️  SŁABA SKALOWALNOŚĆ - Overhead wątków zbyt wysoki!")
        
        # Wykres dla tej konfiguracji
        ax = axes[idx]
        ax.plot(valid_threads, valid_times, marker='o', linewidth=2, markersize=8, color='#2E86AB')
        ax.set_xlabel('Liczba wątków', fontsize=12, fontweight='bold')
        ax.set_ylabel('Czas wykonania (s)', fontsize=12, fontweight='bold')
        ax.set_title(f'{intervals:,} przedziałów\n(średnia z {NUM_RUNS} przebiegów)', fontsize=13, fontweight='bold')
        ax.grid(True, alpha=0.3, linestyle='--')
        ax.set_xticks(valid_threads)
        
        # Podświetl najszybszy punkt
        if valid_times:
            min_idx_plot = valid_times.index(min(valid_times))
            ax.plot(valid_threads[min_idx_plot], valid_times[min_idx_plot], 'g*', markersize=20, label='Najszybszy')
            ax.legend(fontsize=10)
    
    plt.tight_layout()
    plt.savefig('analiza_wydajnosci.png', dpi=300, bbox_inches='tight')
    print(f"\n\n✓ Wykres zapisany: analiza_wydajnosci.png")
    plt.show()
    
    # Wnioski
    print("\n\n" + "=" * 70)
    print("WNIOSKI")
    print("=" * 70)
    
    all_speedups = []
    for intervals in INTERVALS:
        times = results[intervals]
        valid_times = [time for time in times if time is not None]
        if valid_times:
            speedup = max(valid_times) / min(valid_times)
            all_speedups.append(speedup)
    
    if all_speedups:
        avg_speedup = np.mean(all_speedups)
        
        print(f"\n📊 Średnia szybkość (max/min): {avg_speedup:.2f}x")
        
        if avg_speedup < 1.1:
            print("\n❌ MOŻLIWY PROBLEM!")
            print("   Czas zmienia się minimalnie lub wciąż rośnie")
            print("   Oznacza to:")
            print("   1. Problem z synchronizacją (mutex)")
            print("   2. Overhead tworzenia wątków")
            print("   3. Algorytm może być sekwencyjny")
            print("\n   Rekomendacje:")
            print("   • Sprawdzić czy mutex nie jest bottleneckiem")
            print("   • Zmniejszyć częstość lock_guard'a")
            print("   • Sprawdzić czy suma jest dobrze obliczana")
            
        elif avg_speedup < 1.5:
            print("\n⚠️  SŁABA SKALOWALNOŚĆ")
            print("   Przyspieszenie jest małe")
            print("   Przyczyną może być:")
            print("   • Częste synchronizowanie dostępu do zmiennej pi")
            print("   • Overhead wątków dominuje nad pracą")
            print("   • Problem z pamięcią/cache'em")
            
        else:
            print("\n✅ DOBRA SKALOWALNOŚĆ")
            print("   Program dobrze wykorzystuje wątki")
            print("   Czas wyraźnie maleje ze wzrostem liczby wątków")
    
    print("\n" + "=" * 70)

if __name__ == "__main__":
    main()
