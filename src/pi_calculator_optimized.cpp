#include <iostream>
#include <thread>
#include <vector>
#include <chrono>
#include <cmath>

// Struktura z paddingiem, aby uniknąć false sharing
// Cache line = zazwyczaj 64 bajty
struct alignas(64) CachePaddedDouble {
    double value = 0.0;
    // Padding wystarczy do 64 bajtów
};

int main() {
    int n;  // Liczba przedziałów
    int num_threads;  // Liczba wątków
    
    std::cout << "Wprowadź liczbę przedziałów całkowania: ";
    std::cin >> n;
    
    std::cout << "Wprowadź liczbę wątków: ";
    std::cin >> num_threads;
    
    double h = 1.0 / n;  // Szerokość przedziału
    
    // Wektor z paddingiem - każdy element w osobnym cache line
    std::vector<CachePaddedDouble> thread_results(num_threads);
    
    std::vector<std::thread> threads;
    
    auto start = std::chrono::high_resolution_clock::now();
    
    // Lambda do obliczania części całki
    auto calculate_pi = [&thread_results, n, h, num_threads](int thread_id) {
        double local_sum = 0.0;
        
        // Każdy wątek oblicza co num_threads-ty przedział
        for (int i = thread_id; i < n; i += num_threads) {
            double x = (i + 0.5) * h;  // Środek przedziału
            local_sum += 4.0 / (1.0 + x * x);
        }
        
        // Każdy wątek zapisuje w SWOIM cache line - bez false sharing
        thread_results[thread_id].value = local_sum * h;
    };
    
    // Tworzenie i uruchamianie wątków
    for (int i = 0; i < num_threads; ++i) {
        threads.emplace_back(calculate_pi, i);
    }
    
    // Oczekiwanie na zakończenie wszystkich wątków
    for (auto& t : threads) {
        t.join();
    }
    
    // Sumowanie wyników wszystkich wątków
    double pi = 0.0;
    for (const auto& result : thread_results) {
        pi += result.value;
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
