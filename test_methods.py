"""
Vienmačio optimizavimo metodų testai ir demonstracija
"""

from optimization_methods import bisection_method, golden_section_method, newton_method
import numpy as np


def print_results(method_name: str, x_min: float, f_min: float, iterations: int):
    """Atspausdina optimizavimo rezultatus."""
    print(f"\n{'='*60}")
    print(f"{method_name}")
    print(f"{'='*60}")
    print(f"Rastas minimumas: x* = {x_min:.8f}")
    print(f"Funkcijos reikšmė: f(x*) = {f_min:.8f}")
    print(f"Iteracijų skaičius: {iterations}")
    print(f"{'='*60}")


# ============================================================================
# PAGRINDINIAI TESTAI
# ============================================================================

def test_basic_quadratic():
    """Pagrindinis testas su kvadratine funkcija f(x) = (x - 2)² + 1"""
    print("="*70)
    print("VIENMAČIO OPTIMIZAVIMO METODŲ DEMONSTRACIJA")
    print("Testinė funkcija: f(x) = (x - 2)² + 1")
    print("Tikrasis minimumas: x* = 2, f(x*) = 1")
    print("="*70)
    
    def f(x):
        return (x - 2)**2 + 1
    
    def df(x):
        return 2 * (x - 2)
    
    def d2f(x):
        return 2
    
    # Parametrai
    l, r = 0, 5
    x0 = 0
    epsilon = 1e-6
    
    # 1. Intervalo dalijimo pusiau metodas
    x_min_bis, f_min_bis, iter_bis, history_bis = bisection_method(f, l, r, epsilon)
    print_results("INTERVALO DALIJIMO PUSIAU METODAS", x_min_bis, f_min_bis, iter_bis)
    
    if history_bis:
        print("\nPirmosios iteracijos detali informacija:")
        h = history_bis[0]
        print(f"  l = {h['l']:.2f}; r = {h['r']:.2f}; L = {h['L']:.2f}; x_m = {h['x_m']:.2f}")
        print(f"  x_1 = l + L/4 = {h['l']:.2f} + {h['L']:.2f}/4 = {h['x_1']:.2f}")
        print(f"  x_2 = r - L/4 = {h['r']:.2f} - {h['L']:.2f}/4 = {h['x_2']:.2f}")
        print(f"  f(x_1) = {h['f(x_1)']:.4f}; f(x_m) = {h['f(x_m)']:.4f}; f(x_2) = {h['f(x_2)']:.4f}")
    
    # 2. Auksinio pjūvio metodas
    x_min_gold, f_min_gold, iter_gold, history_gold = golden_section_method(f, l, r, epsilon)
    print_results("AUKSINIO PJŪVIO METODAS", x_min_gold, f_min_gold, iter_gold)
    
    # 3. Niutono metodas
    x_min_newton, f_min_newton, iter_newton, history_newton = newton_method(f, df, d2f, x0, epsilon)
    print_results("NIUTONO METODAS", x_min_newton, f_min_newton, iter_newton)
    
    # Palyginimas
    print(f"\n{'='*60}")
    print("METODŲ PALYGINIMAS")
    print(f"{'='*60}")
    print(f"{'Metodas':<30} {'Iteracijos':<15} {'Tikslumas':<15}")
    print(f"{'-'*60}")
    print(f"{'Dalijimas pusiau':<30} {iter_bis:<15} {abs(x_min_bis - 2):.2e}")
    print(f"{'Auksinis pjūvis':<30} {iter_gold:<15} {abs(x_min_gold - 2):.2e}")
    print(f"{'Niutono metodas':<30} {iter_newton:<15} {abs(x_min_newton - 2):.2e}")
    print(f"{'='*60}")


# ============================================================================
# PAVYZDŽIAI IŠ SKAIDRIŲ
# ============================================================================

def test_bisection_from_slides():
    """Intervalo dalijimo pusiau pavyzdys iš skaidrių: f(x) = (100-x)², x ∈ [60, 150]"""
    print("\n\n" + "="*70)
    print("INTERVALO DALIJIMO PUSIAU - PAVYZDYS IŠ SKAIDRIŲ")
    print("min f(x) = (100-x)², x ∈ [60, 150]")
    print("="*70)
    
    def f(x):
        return (100 - x)**2
    
    x_min, f_min, iterations, history = bisection_method(f, 60, 150, epsilon=1e-6)
    
    print(f"\nRastas minimumas: x* = {x_min:.6f}, f(x*) = {f_min:.6f}")
    print(f"Tikrasis minimumas: x* = 100, f(x*) = 0")
    print(f"Iteracijų skaičius: {iterations}")
    
    print("\nPirmosios kelios iteracijos:")
    for i, h in enumerate(history[:3]):
        print(f"\n{i+1} iteracija:")
        print(f"  l = {h['l']:.2f}; r = {h['r']:.2f}; L = {h['L']:.2f}; x_m = {h['x_m']:.2f}")
        print(f"  x_1 = {h['l']:.2f} + {h['L']:.2f}/4 = {h['x_1']:.2f}")
        print(f"  x_2 = {h['r']:.2f} - {h['L']:.2f}/4 = {h['x_2']:.2f}")
        print(f"  f(x_1) = f({h['x_1']:.2f}) = {h['f(x_1)']:.2f}")
        print(f"  f(x_m) = f({h['x_m']:.2f}) = {h['f(x_m)']:.2f}")
        print(f"  f(x_2) = f({h['x_2']:.2f}) = {h['f(x_2)']:.2f}")
        if i < len(history) - 1:
            next_h = history[i + 1]
            print(f"  Naujas intervalas: [{next_h['l']:.2f}; {next_h['r']:.2f}], ilgis = {next_h['L']:.2f}")


def test_golden_section_from_slides():
    """Auksinio pjūvio pavyzdys iš skaidrių (normalizuotas): f(w) = (40-90w)², w ∈ [0, 1]"""
    print("\n\n" + "="*70)
    print("AUKSINIO PJŪVIO - PAVYZDYS IŠ SKAIDRIŲ")
    print("min f(w) = (40-90w)², w ∈ [0, 1]")
    print("="*70)
    
    def f(w):
        return (40 - 90*w)**2
    
    tau = (np.sqrt(5) - 1) / 2
    print(f"\nAuksinio pjūvio konstanta: τ = (√5 - 1)/2 = {tau:.5f}")
    print(f"τ² = 1 - τ = {1 - tau:.5f}")
    
    x_min, f_min, iterations, history = golden_section_method(f, 0, 1, epsilon=1e-6)
    
    print(f"\nRastas minimumas: w* = {x_min:.8f}")
    print(f"Funkcijos reikšmė: f(w*) = {f_min:.8f}")
    print(f"Tikrasis minimumas: w* = {40/90:.8f}")
    print(f"Iteracijų skaičius: {iterations}")
    
    print("\nPirmosios kelios iteracijos:")
    for i in range(min(3, len(history))):
        h = history[i]
        print(f"\n{i+1} iteracija:")
        print(f"  Intervalas W_{i+1} = [{h['l']:.3f}; {h['r']:.3f}], ilgis L_{i+1} = {h['L']:.3f}")
        
        if i == 0:
            print(f"  w_1 = 1 - τ = τ² = {h['x_1']:.3f}; f(w_1) = {h['f(x_1)']:.1f}")
            print(f"  w_2 = τ = {h['x_2']:.3f}; f(w_2) = {h['f(x_2)']:.1f}")
        else:
            print(f"  Iš ankstesnės iteracijos: w = {h['x_1']:.3f}; f(w) = {h['f(x_1)']:.1f}")
            print(f"  Naujas taškas: w = {h['x_2']:.3f}; f(w) = {h['f(x_2)']:.1f}")
        
        if h['f(x_2)'] < h['f(x_1)']:
            print(f"  f(w_2) < f(w_1), todėl intervalas [{h['l']:.3f}; {h['x_1']:.3f}) atmetamas")
        else:
            print(f"  f(w_1) < f(w_2), todėl intervalas ({h['x_2']:.3f}; {h['r']:.3f}] atmetamas")


# ============================================================================
# VISI TESTAI
# ============================================================================

if __name__ == "__main__":
    # Pagrindinis testas
    test_basic_quadratic()
    
    # Pavyzdžiai iš skaidrių
    test_bisection_from_slides()
    test_golden_section_from_slides()
    
    print("\n\n" + "="*70)
    print("TESTAI BAIGTI!")
    print("="*70)
