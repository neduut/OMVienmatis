from optimization_methods import int_dalijimo_pusiau_metodas, auksinio_pjuvio_metodas, niutono_metodas
import numpy as np
import matplotlib.pyplot as plt


def get_digits_from_student_number(student_number: str) -> tuple:
    """
    istraukia skaitmenis 'a' ir 'b' ix studento knygelds numerio "2*1**ab" formato    
    parametrai:
        student_number: studento knygeles numeris
    grazina:
        (a, b): istraukti skaitmenys
    """
    # ieškome "2*1**ab" formato, kai visada yra 7 skaitmenys
    if len(student_number) != 7 or not student_number.isdigit():
        raise ValueError("Numeris turi būti tiksliai 7 skaitmenų")

    if student_number[0] != "2" or student_number[2] != "1":
        raise ValueError("Numerio 1 ir 3 skaitmenys turi būti 2 ir 1")

    a = int(student_number[-2])
    b = int(student_number[-1])
    return a, b


def reduce_to_single_digit(number: int) -> int:
    """
    sumuoja skaitmenis tol, kol lieka vienas skaitmuo.
    
    pvz: 123 -> 1+2+3=6 -> 6
         99 -> 9+9=18 -> 1+8=9 -> 9
    """
    while number >= 10:
        number = sum(int(d) for d in str(number))
    return number


def process_student_number(student_number: str) -> tuple:
    """
    apdoroja studento numerį ir grąžina a ir b reikšmes.
    jei b = 0, sumuoja visus skaitmenis iki vienzenklio skaičiaus.
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


# 2. Tikslo funkcijos aprašymas

def create_objective_function(a: float, b: float):
    """
    sukuria tikslo funkciją ir jos išvestines pagal parametrus a ir b.
    
    f(x) = (x² - a)² / b - 1
    f'(x) = 4x(x² - a) / b
    f''(x) = (12x² - 4a) / b
    
    parametrai:
        a, b: parametrai iš studento numerio
    
    grąžina:
        (f, df, d2f): funkcija ir jos išvestinės
    """
    def f(x):
        """tikslo funkcija: f(x) = (x² - a)² / b - 1"""
        return ((x**2 - a)**2) / b - 1
    
    def df(x):
        """pirmoji išvestinė: f'(x) = 4x(x² - a) / b"""
        return (4 * x * (x**2 - a)) / b
    
    def d2f(x):
        """antroji išvestinė: f''(x) = (12x² - 4a) / b"""
        return (12 * x**2 - 4 * a) / b
    
    return f, df, d2f


def main():
  
    print("="*70)
    print("1-ASIS LABORATORINIS DARBAS: VIENMAČIO OPTIMIZAVIMO METODAI")
    print("="*70)
    
    # gauti studento numerį
    while True:
        student_number = input("\nĮveskite studento knygelės numerį (2*1**ab): ").strip()
        if (
            len(student_number) == 7 and
            student_number.isdigit() and
            student_number[0] == "2" and
            student_number[2] == "1"
        ):
            break
        print("Neteisingas numeris. Bandykite dar kartą.")
    
    # apdoroti studento numerį
    a, b = process_student_number(student_number)
    
    # sukurti tikslo funkciją
    print(f"\n{'='*70}")
    print("2. TIKSLO FUNKCIJA")
    print(f"{'='*70}")
    print(f"\nParametrai: a = {a}, b = {b}")
    print(f"\nTikslo funkcija:")
    print(f"  f(x) = (x² - {a})² / {b} - 1")
    print(f"  f'(x) = 4x(x² - {a}) / {b}")
    print(f"  f''(x) = (12x² - 4·{a}) / {b}")
    
    f, df, d2f = create_objective_function(a, b)
    
    # testuojame funkciją keliuose taškuose
    print(f"\nFunkcijos reikšmės keliuose taškuose:")
    test_points = [-2, -1, 0, 1, 2]
    for x in test_points:
        print(f"  f({x:2d}) = {f(x):10.4f},  f'({x:2d}) = {df(x):10.4f},  f''({x:2d}) = {d2f(x):10.4f}")
    
    # 3. minimizavimas trimis metodais
    print(f"\n{'='*70}")
    print("3. FUNKCIJOS MINIMIZAVIMAS")
    print(f"{'='*70}")
    
    # parametrai
    l, r = 0, 10  # intervalas
    x0 = 5  # pradinis taškas niutono metodui
    epsilon = 1e-4  # tikslumas
    
    print(f"\nParametrai:")
    print(f"  Intervalas: [{l}, {r}]")
    print(f"  Tikslumas: ε = {epsilon}")
    print(f"  Pradinis taškas (Newton): x₀ = {x0}")
    
    # 3.1 intervalo dalijimo pusiau metodas
    print(f"\n{'-'*70}")
    print("3.1. INTERVALO DALIJIMO PUSIAU METODAS")
    print(f"{'-'*70}")
    x_min_bis, f_min_bis, iter_bis, f_evals_bis, history_bis = int_dalijimo_pusiau_metodas(f, l, r, epsilon)
    print(f"Rastas minimumas: x* = {x_min_bis:.6f}")
    print(f"Funkcijos reikšmė: f(x*) = {f_min_bis:.6f}")
    print(f"Iteracijų skaičius: {iter_bis}")
    print(f"Funkcijų skaičiavimų skaičius: {f_evals_bis}")
    
    # 3.2 auksinio pjūvio metodas
    print(f"\n{'-'*70}")
    print("3.2. AUKSINIO PJŪVIO METODAS")
    print(f"{'-'*70}")
    x_min_gold, f_min_gold, iter_gold, f_evals_gold, history_gold = auksinio_pjuvio_metodas(f, l, r, epsilon)
    print(f"Rastas minimumas: x* = {x_min_gold:.6f}")
    print(f"Funkcijos reikšmė: f(x*) = {f_min_gold:.6f}")
    print(f"Iteracijų skaičius: {iter_gold}")
    print(f"Funkcijų skaičiavimų skaičius: {f_evals_gold}")
    
    # 3.3 niutono metodas
    print(f"\n{'-'*70}")
    print("3.3. NIUTONO METODAS")
    print(f"{'-'*70}")
    x_min_newton, f_min_newton, iter_newton, f_evals_newton, history_newton = niutono_metodas(
        f, df, d2f, x0, epsilon
    )
    print(f"Rastas minimumas: x* = {x_min_newton:.6f}")
    print(f"Funkcijos reikšmė: f(x*) = {f_min_newton:.6f}")
    print(f"Iteracijų skaičius: {iter_newton}")
    print(f"Funkcijų skaičiavimų skaičius: {f_evals_newton} (f'(x) ir f''(x) + f(x) galutinei reikšmei)")
    if history_newton:
        last_step = history_newton[-1].get('step')
        if last_step is not None:
            print(f"Paskutinio žingsnio ilgis: {last_step:.6e}")
    
    # palyginimas
    print(f"\n{'='*70}")
    print("REZULTATŲ PALYGINIMAS")
    print(f"{'='*70}")
    print(f"{'Metodas':<30} {'x*':<12} {'f(x*)':<12} {'Žingsniai':<12} {'f skaič.':<12}")
    print(f"{'-'*70}")
    print(f"{'Dalijimas pusiau':<30} {x_min_bis:<12.6f} {f_min_bis:<12.6f} {iter_bis:<12} {f_evals_bis:<12}")
    print(f"{'Auksinis pjūvis':<30} {x_min_gold:<12.6f} {f_min_gold:<12.6f} {iter_gold:<12} {f_evals_gold:<12}")
    print(f"{'Niutono metodas':<30} {x_min_newton:<12.6f} {f_min_newton:<12.6f} {iter_newton:<12} {f_evals_newton:<12}")
    
    # 4. vizualizacija
    print(f"\n{'='*70}")
    print("4. VIZUALIZACIJA")
    print(f"{'='*70}")

    # surenkame bandymo taškus
    points_bis = []
    for h in history_bis:
        points_bis.extend([h['l'], h['x_1'], h['x_m'], h['x_2'], h['r']])

    points_gold = []
    for h in history_gold:
        points_gold.extend([h['l'], h['x_1'], h['x_2'], h['r']])

    points_newton = [h['x_i'] for h in history_newton]
    for h in history_newton:
        if 'x_next' in h:
            points_newton.append(h['x_next'])

    # funkcijos grafikas
    xs = np.linspace(l, r, 1000)
    ys = [f(x) for x in xs]

    plt.figure(figsize=(10, 6))
    plt.plot(xs, ys, 'b-', linewidth=2, label='f(x)')

    # bandymo taškai
    plt.scatter(points_bis, [f(x) for x in points_bis], s=15, alpha=0.6, label='Dalijimas pusiau')
    plt.scatter(points_gold, [f(x) for x in points_gold], s=15, alpha=0.6, label='Auksinis pjūvis')
    plt.scatter(points_newton, [f(x) for x in points_newton], s=25, alpha=0.8, label='Niutono metodas')

    # rasti minimumai
    plt.scatter([x_min_bis], [f_min_bis], c='red', s=60, marker='x', label='Minimumas (dalijimas pusiau)')
    plt.scatter([x_min_gold], [f_min_gold], c='green', s=60, marker='x', label='Minimumas (auksinis pjūvis)')
    plt.scatter([x_min_newton], [f_min_newton], c='purple', s=60, marker='x', label='Minimumas (Niutono metodas)')

    plt.title('Tikslo funkcija ir bandymo taškai')
    plt.xlabel('x')
    plt.ylabel('f(x)')
    plt.grid(True, alpha=0.3)
    plt.legend(fontsize=9)
    plt.tight_layout()
    plt.savefig('vizualizacija.png', dpi=150)
    plt.close()

    # priartintas vaizdas aplink minimumą
    min_x = x_min_newton
    zoom_half_width = 0.2  # priartinamas plotis apie minimumą
    zx_min = max(l, min_x - zoom_half_width)
    zx_max = min(r, min_x + zoom_half_width)

    zxs = np.linspace(zx_min, zx_max, 600)
    zys = [f(x) for x in zxs]

    plt.figure(figsize=(10, 6))
    plt.plot(zxs, zys, 'b-', linewidth=2, label='f(x)')
    plt.scatter([x for x in points_bis if zx_min <= x <= zx_max],
                [f(x) for x in points_bis if zx_min <= x <= zx_max],
                s=15, alpha=0.6, label='Dalijimas pusiau')
    plt.scatter([x for x in points_gold if zx_min <= x <= zx_max],
                [f(x) for x in points_gold if zx_min <= x <= zx_max],
                s=15, alpha=0.6, label='Auksinis pjūvis')
    plt.scatter([x for x in points_newton if zx_min <= x <= zx_max],
                [f(x) for x in points_newton if zx_min <= x <= zx_max],
                s=25, alpha=0.8, label='Niutono metodas')

    plt.scatter([x_min_bis], [f_min_bis], c='red', s=60, marker='x', label='Minimumas (dalijimas pusiau)')
    plt.scatter([x_min_gold], [f_min_gold], c='green', s=60, marker='x', label='Minimumas (auksinis pjūvis)')
    plt.scatter([x_min_newton], [f_min_newton], c='purple', s=60, marker='x', label='Minimumas (Niutono metodas)')

    # dinamiškai nustatyti y-ašies ribas - rasti min ir max funkcijos reikšmes priartintame intervale
    zy_values = zys  # funkcijos reikšmės priartintame intervale
    zy_min_val = min(zy_values)
    zy_max_val = max(zy_values)
    zy_margin = (zy_max_val - zy_min_val) * 0.05  # 5% marža
    
    plt.xlim(zx_min, zx_max)
    plt.ylim(zy_min_val - zy_margin, zy_max_val + zy_margin)
    plt.title('Priartintas vaizdas aplink minimumą')
    plt.xlabel('x')
    plt.ylabel('f(x)')
    plt.grid(True, alpha=0.3)
    plt.legend(fontsize=9)
    plt.tight_layout()
    plt.savefig('vizualizacija_arti.png', dpi=150)
    plt.close()

    print("Vizualizacijos išsaugotos failuose: vizualizacija.png, vizualizacija_arti.png")

    print(f"\n{'='*70}")


if __name__ == "__main__":
    main()
