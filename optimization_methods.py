t"""
Vienmačio optimizavimo metodai:
1. Intervalo dalijimas pusiau (Bisection)
2. Auksinio pjūvio metodas (Golden Section)
3. Niutono metodas (Newton's Method)
"""

import numpy as np
from typing import Callable, Tuple, Optional


def bisection_method(
    f: Callable[[float], float],
    l: float,
    r: float,
    epsilon: float = 1e-6,
    max_iter: int = 1000
) -> Tuple[float, float, int, list]:
    """
    Intervalo dalijimo pusiau metodas optimizavimui.
    
    Algoritmas:
    1. Pradiniame intervale parenkami trys tolygiai pasiskirste bandymo taškai x_m, x_1 ir x_2
    2. x_m = (l + r)/2, L = r - l
    3. x_1 = l + L/4, x_2 = r - L/4
    4. Jei f(x_1) < f(x_m), tai atmetamas (x_m, r] ir xm = x_1
    5. Jei f(x_2) < f(x_m), tai atmetamas [l, x_m) ir xm = x_2
    6. Priešingu atveju atmetami [l, x_1] ir (x_2, r]
    
    Parametrai:
        f: Tikslo funkcija
        l: Intervalo pradžia (kairysis galas)
        r: Intervalo pabaiga (dešinysis galas)
        epsilon: Tikslumo riba
        max_iter: Maksimalus iteracijų skaičius
    
    Grąžina:
        x_min: Minimumo taškas
        f_min: Funkcijos reikšmė minimume
        iterations: Iteracijų skaičius
        history: Iteracijų istorija
    """
    history = []
    
    for iteration in range(max_iter):
        # Intervalo ilgis
        L = r - l
        
        # Intervalo vidurio taškas
        x_m = (l + r) / 2
        
        # Du papildomi bandymo taškai
        x_1 = l + L / 4
        x_2 = r - L / 4
        
        # Funkcijų reikšmės
        f_xm = f(x_m)
        f_x1 = f(x_1)
        f_x2 = f(x_2)
        
        history.append({
            'iteration': iteration + 1,
            'l': l,
            'r': r,
            'L': L,
            'x_m': x_m,
            'x_1': x_1,
            'x_2': x_2,
            'f(x_m)': f_xm,
            'f(x_1)': f_x1,
            'f(x_2)': f_x2
        })
        
        # Patikrinimas, ar pasiektas tikslumas
        if L < epsilon:
            x_min = x_m
            f_min = f_xm
            return x_min, f_min, iteration + 1, history
        
        # Intervalo mažinimas pagal algoritmo logiką
        if f_x1 < f_xm:
            # 3.1: atmetamas (x_m, r], keičiant r = x_m
            # 3.2: intervalo centru tampa x_1, tad keičiama x_m = x_1
            r = x_m
        elif f_x2 < f_xm:
            # 4.1: atmetamas [l, x_m), keičiant l = x_m
            # 4.2: intervalo centru tampa x_2, tad keičiama x_m = x_2
            l = x_m
        else:
            # 5.1: atmetami intervalai [l, x_1] ir (x_2, r]
            l = x_1
            r = x_2
    
    # Jei nepasiektas tikslumas per max_iter iteracijų
    x_min = (l + r) / 2
    f_min = f(x_min)
    return x_min, f_min, max_iter, history


def golden_section_method(
    f: Callable[[float], float],
    l: float,
    r: float,
    epsilon: float = 1e-6,
    max_iter: int = 1000
) -> Tuple[float, float, int, list]:
    """
    Auksinio pjūvio metodas optimizavimui.
    
    Algoritmas:
    1. L = r - l, x_1 = r - τL ir x_2 = l + τL, skaičiuojame f(x_1) ir f(x_2)
    2. Jei f(x_2) < f(x_1), tai atmetamas [l, x_1), l = x_1, x_1 = x_2
    3. Priešingu atveju atmetamas (x_2, r], r = x_2, x_2 = x_1
    4. Skaičiuojama viena tikslo funkcijos reikšmė iteracijoje
    
    Sustojimo sąlyga:
    - Pagal fiksuotą funkcijos bandymų skaičių (max_iter), arba
    - Pagal paieškos intervalo ilgį (L < epsilon)
    
    Tolesnis bandymo taškas gaunamas pagal formules:
    - w = r - τ^N arba w = l + τ^N
    - Priklausomai kuris pointervals buvo atmestas ankstesnėje iteracijoje
    
    Parametrai:
        f: Tikslo funkcija
        l: Intervalo pradžia (kairysis galas)
        r: Intervalo pabaiga (dešinysis galas)
        epsilon: Tikslumo riba
        max_iter: Maksimalus iteracijų skaičius
    
    Grąžina:
        x_min: Minimumo taškas
        f_min: Funkcijos reikšmė minimume
        iterations: Iteracijų skaičius
        history: Iteracijų istorija
    """
    # Auksinio pjūvio koeficientas (Fibonačio skaičius)
    # τ = (√5 - 1)/2 ≈ 0.618
    # τ² = 1 - τ ≈ 0.382
    tau = (np.sqrt(5) - 1) / 2  # ≈ 0.618
    
    history = []
    
    # Pradinis intervalas ir taškai
    L = r - l
    x_1 = r - tau * L
    x_2 = l + tau * L
    f_x1 = f(x_1)
    f_x2 = f(x_2)
    
    for iteration in range(max_iter):
        history.append({
            'iteration': iteration + 1,
            'l': l,
            'r': r,
            'L': L,
            'x_1': x_1,
            'x_2': x_2,
            'f(x_1)': f_x1,
            'f(x_2)': f_x2
        })
        
        # Patikrinimas, ar pasiektas tikslumas
        if L < epsilon:
            x_min = (l + r) / 2
            f_min = f(x_min)
            return x_min, f_min, iteration + 1, history
        
        # Intervalo mažinimas pagal funkcijos reikšmes
        if f_x2 < f_x1:
            # 2. Atmetamas [l, x_1) atliekant keitimą l = x_1, L = r - l
            l = x_1
            L = r - l
            # 2.2 kairiuoju tašku tampa ankstesnis dešinysis taškas x_1 = x_2
            x_1 = x_2
            f_x1 = f_x2
            # 2.3 naujasis dešinysis taškas x_2 = l + τL, skaičiuojame f(x_2)
            x_2 = l + tau * L
            f_x2 = f(x_2)
        else:
            # 3. Atmetamas (x_2, r] atliekant keitimą r = x_2, L = r - l
            r = x_2
            L = r - l
            # 3.2 dešiniuoju tašku tampa ankstesnis kairysis taškas x_2 = x_1
            x_2 = x_1
            f_x2 = f_x1
            # 3.3 naujasis kairysis taškas x_1 = r - τL, skaičiuojame f(x_1)
            x_1 = r - tau * L
            f_x1 = f(x_1)
    
    # Jei nepasiektas tikslumas per max_iter iteracijų
    x_min = (l + r) / 2
    f_min = f(x_min)
    return x_min, f_min, max_iter, history


def newton_method(
    f: Callable[[float], float],
    df: Callable[[float], float],
    d2f: Callable[[float], float],
    x0: float,
    epsilon: float = 1e-6,
    max_iter: int = 1000
) -> Tuple[float, float, int, list]:
    """
    Niutono metodas optimizavimui.
    
    Algoritmas:
    - Remiamasi būtinosiomis minimumo sąlygomis, galime uždavinį spresti 
      netiesiogiiai, pakeisdami jį lygties f'(x) = 0 sprendimu
    - Naudojama Teiloro eilutė: f'(x) ≈ f'(x_i) + f''(x_i)·(x - x_i)
    - Prilyginę nuliui, gausime iteracinę metodo formulę:
      x_{i+1} = x_i - f'(x_i) / f''(x_i)
    
    Interpretacija:
    - Iteracine formule išreiškiamas tikslo funkcijos f(x) kvadratinės 
      aproksimacijos minimumo taškas
    - Taške x_i tikslo funkcija aproksimuojama Teiloro eilute, įvertinant 
      ne aukštesnės negu antros eilės narius
    - Apskaičiuojamas aproksimuojančiosios kvadratinės funkcijos minimumo 
      taškas x_{i+1} ir juo pakeičiamas x_i
    - Metodas apibrėžtas naudojant pirmąsias ir antrąsias išvestines, 
      bet nenaudojant tikslo funkcijos reikšmių
    - Jei tikslo funkcija būtų kvadratinė, jos minimumas būtų gautas 
      vienu žingsniu
    - Bendru atveju formulė taikoma iteratyviai
    
    Parametrai:
        f: Tikslo funkcija (naudojama tik galutinei reikšmei)
        df: Pirmoji išvestinė f'(x)
        d2f: Antroji išvestinė f''(x)
        x0: Pradinis taškas
        epsilon: Tikslumo riba (|f'(x)| < epsilon arba |x_{i+1} - x_i| < epsilon)
        max_iter: Maksimalus iteracijų skaičius
    
    Grąžina:
        x_min: Minimumo taškas
        f_min: Funkcijos reikšmė minimume
        iterations: Iteracijų skaičius
        history: Iteracijų istorija
    """
    x = x0
    history = []
    
    for iteration in range(max_iter):
        dfx = df(x)
        d2fx = d2f(x)
        
        history.append({
            'iteration': iteration + 1,
            'x_i': x,
            "f'(x_i)": dfx,
            "f''(x_i)": d2fx
        })
        
        # Patikrinimas, ar pasiektas tikslumas (gradientas artimas nuliui)
        if abs(dfx) < epsilon:
            f_min = f(x)
            return x, f_min, iteration + 1, history
        
        # Patikrinimas, ar antroji išvestinė nėra nulis
        if abs(d2fx) < 1e-10:
            print(f"Įspėjimas: Antroji išvestinė artima nuliui iteracijoje {iteration + 1}")
            f_min = f(x)
            return x, f_min, iteration + 1, history
        
        # Niutono formulė: x_{i+1} = x_i - f'(x_i) / f''(x_i)
        x_new = x - dfx / d2fx
        
        # Patikrinimas, ar pasikeitimas pakankamai mažas
        if abs(x_new - x) < epsilon:
            x = x_new
            f_min = f(x)
            return x, f_min, iteration + 1, history
        
        x = x_new
    
    f_min = f(x)
    return x, f_min, max_iter, history

