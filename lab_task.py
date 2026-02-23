"""
1-ojo laboratorinio darbo užduotis: Vienmačio optimizavimo metodai
"""

from optimization_methods import bisection_method, golden_section_method, newton_method
import numpy as np


def get_digits_from_student_number(student_number: str) -> tuple:
    """
    Ištraukia skaitmenis 'a' ir 'b' iš studento knygelės numerio "2*1**ab" formato.
    
    Parametrai:
        student_number: Studento knygelės numeris
    
    Grąžina:
        (a, b): Ištraukti skaitmenys
    """
    # Ieškome "2*1**ab" formato - tai yra 2, tada 1, tada du skaitmenys
    digits = [int(d) for d in student_number if d.isdigit()]
    
    # Randame poziciją kur yra "21"
    for i in range(len(digits) - 3):
        if digits[i] == 2 and digits[i+1] == 1:
            a = digits[i+2]
            b = digits[i+3]
            return a, b
    
    # Jei nerandame formato, naudojame paskutinius du skaitmenis
    if len(digits) >= 2:
        a = digits[-2]
        b = digits[-1]
        return a, b
    
    raise ValueError("Nepavyko ištraukti skaitmenų iš studento numerio")


def reduce_to_single_digit(number: int) -> int:
    """
    Sumuoja skaitmenis tol, kol lieka vienas skaitmuo.
    
    Pvz: 123 -> 1+2+3=6 -> 6
         99 -> 9+9=18 -> 1+8=9 -> 9
    """
    while number >= 10:
        number = sum(int(d) for d in str(number))
    return number


def process_student_number(student_number: str) -> tuple:
    """
    Apdoroja studento numerį ir grąžina a ir b reikšmes.
    Jei b = 0, sumuoja visus skaitmenis iki vienzenklio skaičiaus.
    """
    a, b = get_digits_from_student_number(student_number)
    
    print(f"\nIštraukti skaitmenys iš numerio {student_number}:")
    print(f"  a = {a}")
    print(f"  b = {b}")
    
    if b == 0:
        print(f"\nb = 0, todėl sumuojame visus numerio skaitmenis:")
        all_digits = sum(int(d) for d in student_number if d.isdigit())
        print(f"  Skaitmenų suma: {all_digits}")
        b = reduce_to_single_digit(all_digits)
        print(f"  Sumažinta iki vienženklio: b = {b}")
    
    return a, b


# ===========================================================================
# 2. Tikslo funkcijos aprašymas
# ===========================================================================

def create_objective_function(a: float, b: float):
    """
    Sukuria tikslo funkciją ir jos išvestines pagal parametrus a ir b.
    
    f(x) = (x² - a)² / b - 1
    f'(x) = 4x(x² - a) / b
    f''(x) = (12x² - 4a) / b
    
    Parametrai:
        a, b: Parametrai iš studento numerio
    
    Grąžina:
        (f, df, d2f): Funkcija ir jos išvestinės
    """
    def f(x):
        """Tikslo funkcija: f(x) = (x² - a)² / b - 1"""
        return ((x**2 - a)**2) / b - 1
    
    def df(x):
        """Pirmoji išvestinė: f'(x) = 4x(x² - a) / b"""
        return (4 * x * (x**2 - a)) / b
    
    def d2f(x):
        """Antroji išvestinė: f''(x) = (12x² - 4a) / b"""
        return (12 * x**2 - 4 * a) / b
    
    return f, df, d2f


def main():
    """Pagrindinis programos blokas"""
    
    print("="*70)
    print("1-ASIS LABORATORINIS DARBAS: VIENMAČIO OPTIMIZAVIMO METODAI")
    print("="*70)
    
    # Gauti studento numerį
    student_number = input("\nĮveskite studento knygelės numerį: ").strip()
    
    # Apdoroti studento numerį
    a, b = process_student_number(student_number)
    
    # Sukurti tikslo funkciją
    print(f"\n{'='*70}")
    print("2. TIKSLO FUNKCIJA")
    print(f"{'='*70}")
    print(f"\nParametrai: a = {a}, b = {b}")
    print(f"\nTikslo funkcija:")
    print(f"  f(x) = (x² - {a})² / {b} - 1")
    print(f"  f'(x) = 4x(x² - {a}) / {b}")
    print(f"  f''(x) = (12x² - 4·{a}) / {b}")
    
    f, df, d2f = create_objective_function(a, b)
    
    # Testuojame funkciją keliuose taškuose
    print(f"\nFunkcijos reikšmės keliuose taškuose:")
    test_points = [-2, -1, 0, 1, 2]
    for x in test_points:
        print(f"  f({x:2d}) = {f(x):10.4f},  f'({x:2d}) = {df(x):10.4f},  f''({x:2d}) = {d2f(x):10.4f}")
    
    # 3. Minimizavimas trimis metodais
    print(f"\n{'='*70}")
    print("3. FUNKCIJOS MINIMIZAVIMAS")
    print(f"{'='*70}")
    
    # Parametrai
    l, r = 0, 10  # Intervalas
    x0 = 5  # Pradinis taškas Niutono metodui
    epsilon = 1e-4  # Tikslumas
    
    print(f"\nParametrai:")
    print(f"  Intervalas: [{l}, {r}]")
    print(f"  Tikslumas: ε = {epsilon}")
    print(f"  Pradinis taškas (Newton): x₀ = {x0}")
    
    # 3.1 Intervalo dalijimo pusiau metodas
    print(f"\n{'-'*70}")
    print("3.1. INTERVALO DALIJIMO PUSIAU METODAS")
    print(f"{'-'*70}")
    x_min_bis, f_min_bis, iter_bis, history_bis = bisection_method(f, l, r, epsilon)
    print(f"Rastas minimumas: x* = {x_min_bis:.6f}")
    print(f"Funkcijos reikšmė: f(x*) = {f_min_bis:.6f}")
    print(f"Iteracijų skaičius: {iter_bis}")
    print(f"Galutinio intervalo ilgis: {history_bis[-1]['L']:.6e}")
    
    # 3.2 Auksinio pjūvio metodas
    print(f"\n{'-'*70}")
    print("3.2. AUKSINIO PJŪVIO METODAS")
    print(f"{'-'*70}")
    x_min_gold, f_min_gold, iter_gold, history_gold = golden_section_method(f, l, r, epsilon)
    print(f"Rastas minimumas: x* = {x_min_gold:.6f}")
    print(f"Funkcijos reikšmė: f(x*) = {f_min_gold:.6f}")
    print(f"Iteracijų skaičius: {iter_gold}")
    print(f"Galutinio intervalo ilgis: {history_gold[-1]['L']:.6e}")
    
    # 3.3 Niutono metodas
    print(f"\n{'-'*70}")
    print("3.3. NIUTONO METODAS")
    print(f"{'-'*70}")
    x_min_newton, f_min_newton, iter_newton, history_newton = newton_method(f, df, d2f, x0, epsilon)
    print(f"Rastas minimumas: x* = {x_min_newton:.6f}")
    print(f"Funkcijos reikšmė: f(x*) = {f_min_newton:.6f}")
    print(f"Iteracijų skaičius: {iter_newton}")
    if len(history_newton) >= 2:
        last_step = abs(history_newton[-1]['x_i'] - history_newton[-2]['x_i'])
        print(f"Paskutinio žingsnio ilgis: {last_step:.6e}")
    
    # Palyginimas
    print(f"\n{'='*70}")
    print("REZULTATŲ PALYGINIMAS")
    print(f"{'='*70}")
    print(f"{'Metodas':<30} {'x*':<12} {'f(x*)':<12} {'Iteracijos':<12}")
    print(f"{'-'*70}")
    print(f"{'Dalijimas pusiau':<30} {x_min_bis:<12.6f} {f_min_bis:<12.6f} {iter_bis:<12}")
    print(f"{'Auksinis pjūvis':<30} {x_min_gold:<12.6f} {f_min_gold:<12.6f} {iter_gold:<12}")
    print(f"{'Niutono metodas':<30} {x_min_newton:<12.6f} {f_min_newton:<12.6f} {iter_newton:<12}")
    
    print(f"\n{'='*70}")


if __name__ == "__main__":
    main()
