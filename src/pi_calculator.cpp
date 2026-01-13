#include <iostream>
#include <thread>
#include <vector>
#include <chrono>
#include <cmath>
#include <atomic>

int main() {
    int n;  // Liczba przedziałów
    int num_threads;  // Liczba wątków
    
    std::cout << "Wprowadź liczbę przedziałów całkowania: ";
    std::cin >> n;
    
    std::cout << "Wprowadź liczbę wątków: ";
    std::cin >> num_threads;
    
    double h = 1.0 / n;  // Szerokość przedziału
    
    // Wektor do przechowywania wyników z każdego wątku (bez synchronizacji)
    std::vector<double> thread_results(num_threads, 0.0);
    
    std::vector<std::thread> threads;
    
    auto start = std::chrono::high_resolution_clock::now();
    
    // Lambda do obliczania części całki
    // KLUCZOWE: każdy wątek pisze do innego indeksu - BRAK RYWALIZACJI
    auto calculate_pi = [&thread_results, n, h, num_threads](int thread_id) {
        double local_sum = 0.0;
        
        // Każdy wątek oblicza co num_threads-ty przedział
        for (int i = thread_id; i < n; i += num_threads) {
            double x = (i + 0.5) * h;  // Środek przedziału
            local_sum += 4.0 / (1.0 + x * x);
        }
        
        // Każdy wątek zapisuje swój wynik w WŁASNYM indeksie - bez konfliktu!
        thread_results[thread_id] = local_sum * h;
    };
    
    // Tworzenie i uruchamianie wątków
    for (int i = 0; i < num_threads; ++i) {
        threads.emplace_back(calculate_pi, i);
    }
    
    // Oczekiwanie na zakończenie wszystkich wątków
    for (auto& t : threads) {
        t.join();
    }
    
    // Sumowanie wyników wszystkich wątków (po zakończeniu wszystkich)
    double pi = 0.0;
    for (double result : thread_results) {
        pi += result;
    }
    
    auto end = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double> duration = end - start;
    
    std::cout << "\n=== WYNIKI ===" << std::endl;
    std::cout << "Przybliżona wartość liczby PI: " << pi << std::endl;
    std::cout << "Rzeczywista wartość PI:        " << M_PI << std::endl;
    std::cout << "Błąd bezwzględny:              " << std::abs(pi - M_PI) << std::endl;
    std::cout << "Czas obliczeń:                 " << duration.count() << " sekund" << std::endl;
    
    return 0;
}
