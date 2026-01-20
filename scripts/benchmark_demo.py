#!/usr/bin/env python3
"""
Skrypt demonstracyjny - szybki test z mniejszymi wartościami
"""

import subprocess
import re
import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm

# Konfiguracja testów - mniejsze wartości dla szybkiego testu
INTERVALS = [1_000_000, 10_000_000, 50_000_000]  # Mniejsze wartości
THREAD_RANGE = range(1, 11)  # Od 1 do 10 wątków
EXECUTABLE = "../build/pi_calculator"

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
            timeout=60
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
    print("=" * 60)
    print("DEMO - BENCHMARK PROGRAMU OBLICZAJĄCEGO LICZBĘ PI")
    print("=" * 60)
    print(f"Przedziały: {INTERVALS}")
    print(f"Zakres wątków: {min(THREAD_RANGE)} - {max(THREAD_RANGE)}")
    print("=" * 60)
    
    results = {intervals: [] for intervals in INTERVALS}
    
    total_tests = len(INTERVALS) * len(THREAD_RANGE)
    
    with tqdm(total=total_tests, desc="Wykonywanie testów") as pbar:
        for intervals in INTERVALS:
            print(f"\n\nTestowanie dla {intervals:,} przedziałów...")
            
            for threads in THREAD_RANGE:
                time = run_pi_calculator(intervals, threads)
                results[intervals].append(time)
                
                if time is not None:
                    tqdm.write(f"  {threads:2d} wątków: {time:.4f}s")
                else:
                    tqdm.write(f"  {threads:2d} wątków: BŁĄD")
                
                pbar.update(1)
    
    print("\n\nGenerowanie wykresu...")
    
    plt.figure(figsize=(14, 8))
    
    colors = ['#2E86AB', '#A23B72', '#F18F01']
    markers = ['o', 's', '^']
    
    for i, intervals in enumerate(INTERVALS):
        times = results[intervals]
        valid_threads = [t for t, time in zip(THREAD_RANGE, times) if time is not None]
        valid_times = [time for time in times if time is not None]
        
        if valid_times:
            plt.plot(valid_threads, valid_times, 
                    marker=markers[i], 
                    linewidth=2, 
                    markersize=6,
                    color=colors[i],
                    label=f'{intervals:,} przedziałów',
                    alpha=0.8)
    
    plt.xlabel('Liczba wątków', fontsize=14, fontweight='bold')
    plt.ylabel('Czas wykonania (sekundy)', fontsize=14, fontweight='bold')
    plt.title('DEMO: Wydajność obliczania liczby PI - zależność od liczby wątków', 
              fontsize=16, fontweight='bold', pad=20)
    plt.legend(fontsize=12, loc='best', framealpha=0.9)
    plt.grid(True, alpha=0.3, linestyle='--')
    plt.tight_layout()
    
    output_file = 'wykres_wydajnosci_demo.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"\nWykres zapisany jako: {output_file}")
    
    plt.show()
    
    print("\n" + "=" * 60)
    print("STATYSTYKI")
    print("=" * 60)
    
    for intervals in INTERVALS:
        times = [t for t in results[intervals] if t is not None]
        if times:
            min_time = min(times)
            max_time = max(times)
            min_idx = times.index(min_time)
            max_idx = times.index(max_time)
            speedup = max_time / min_time
            
            print(f"\n{intervals:,} przedziałów:")
            print(f"  Najszybszy: {min_time:.4f}s ({min_idx + 1} wątków)")
            print(f"  Najwolniejszy: {max_time:.4f}s ({max_idx + 1} wątków)")
            print(f"  Przyspieszenie: {speedup:.2f}x")
    
    print("\n" + "=" * 60)
    print("Benchmark zakończony pomyślnie!")
    print("=" * 60)

if __name__ == "__main__":
    main()
