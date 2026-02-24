t"""
Vienmacio optimizavimo metodai:
1. Intervalo dalijimas pusiau (Bisection)
2. Auksinio pjuvio metodas (Golden Section)
3. Niutono metodas (Newton's Method)
"""

import numpy as np
from typing import Callable, Tuple, Optional


def int_dalijimo_pusiau_metodas(
    f: Callable[[float], float],
    l: float,
    r: float,
    epsilon: float = 1e-6,
    max_iter: int = 1000
) -> Tuple[float, float, int, int, list]:
    """
    Intervalo dalijimo pusiau metodas optimizavimui.
    
    Algoritmas:
    1. pradiniame intervale parenkami trys tolygiai pasiskirste bandymo taškai x_m, x_1 ir x_2
    2. x_m = (l + r)/2, L = r - l
    3. x_1 = l + L/4, x_2 = r - L/4
    4. jei f(x_1) < f(x_m), tai atmetamas (x_m, r] ir xm = x_1
    5. jei f(x_2) < f(x_m), tai atmetamas [l, x_m) ir xm = x_2
    6. priesingu atveju atmetami [l, x_1] ir (x_2, r]
    
    Parametrai:
        f: tikslo funkcija
        l: intervalo pradzia (kairysis galas)
        r: intervalo pabaiga (desinysis galas)
        epsilon: tikslumo riba
        max_iter: maksimalus iteraciju skaicius
    
    Grazina:
        x_min: minimumo taskas
        f_min: funkcijos reiksme minimume
        iterations: iteraciju skaicius
        func_calls: bendras funkcijos skaiciavimo skaicius
        history: iteraciju istorija
    """
    history = []
    func_calls = 0
    
    for iteration in range(max_iter):
        # intervalo ilgis
        L = r - l
        
        # tikrina ar pasiektas tikslumas PRIEŠ skaičiuojant
        if L < epsilon:
            x_min = (l + r) / 2
            f_min = f(x_min)
            func_calls += 1
            return x_min, f_min, iteration, func_calls, history
        
        # intervalo vidurio taskas
        x_m = (l + r) / 2
        # du papildomi bandymo taskai
        x_1 = l + L / 4
        x_2 = r - L / 4
        # funkciju reiksmes
        f_xm = f(x_m)
        f_x1 = f(x_1)
        f_x2 = f(x_2)
        func_calls += 3
        
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
        
        # intervalo mazinimas
        if f_x1 < f_xm:
            # atmetamas (x_m, r], keiciant r = x_m
            r = x_m
        elif f_x2 < f_xm:
            # atmetamas [l, x_m), keiciant l = x_m
            l = x_m
        else:
            # atmetami intervalai [l, x_1] ir (x_2, r]
            l = x_1
            r = x_2
    
    # jei nepasiektas tikslumas per max_iter iteraciju
    x_min = (l + r) / 2
    f_min = f(x_min)
    func_calls += 1
    return x_min, f_min, max_iter, func_calls, history


def auksinio_pjuvio_metodas(
    f: Callable[[float], float],
    l: float,
    r: float,
    epsilon: float = 1e-6,
    max_iter: int = 1000
) -> Tuple[float, float, int, int, list]:
    """
    Auksinio pjuvio metodas optimizavimui - pagal skaidres.
    
    Algoritmas:
    1. L = r - l, x_1 = r - τL ir x_2 = l + τL, skaiciuojame f(x_1) ir f(x_2)
    2. while L > epsilon:
       - jei f(x_2) < f(x_1): atmetamas [l, x_1), l = x_1, x_1 = x_2, f(x_1) = f(x_2)
       - priesingu atveju: atmetamas (x_2, r], r = x_2, x_2 = x_1, f(x_2) = f(x_1)
       - atnaujinti L ir naujus bandymo taskus
    
    Sustojimo salyga: L <= epsilon
    
    Parametrai:
        f: tikslo funkcija
        l: intervalo pradžia (kairysis galas)
        r: intervalo pabaiga (dešinysis galas)
        epsilon: tikslumo riba
        max_iter: maksimalus iteraciju skaicius
    
    Grazina:
        x_min: minimumo taskas
        f_min: funkcijos reiksme minimume
        iterations: iteraciju skaicius
        func_calls: bendras funkcijos skaiciavimo skaicius
        history: iteraciju istorija
    """
    tau = (np.sqrt(5) - 1) / 2  # ≈ 0.618
    func_calls = 0
    iterations = 0
    history = []
    
    L = r - l
    x_1 = r - tau * L
    x_2 = l + tau * L
    f_1 = f(x_1)
    f_2 = f(x_2)
    func_calls += 2
    
    while L > epsilon and iterations < max_iter:
        iterations += 1
        
        history.append({
            'iteration': iterations,
            'l': l,
            'r': r,
            'L': L,
            'x_1': x_1,
            'x_2': x_2,
            'f(x_1)': f_1,
            'f(x_2)': f_2,
            'func_calls': func_calls
        })
        
        if f_2 < f_1:
            l = x_1
            x_1 = x_2
            f_1 = f_2
            L = r - l
            x_2 = l + tau * L
            f_2 = f(x_2)
            func_calls += 1
        else:
            r = x_2
            x_2 = x_1
            f_2 = f_1
            L = r - l
            x_1 = r - tau * L
            f_1 = f(x_1)
            func_calls += 1
    
    x_min = (l + r) / 2
    f_min = f(x_min)
    func_calls += 1
    
    return x_min, f_min, iterations, func_calls, history


def niutono_metodas(
    f: Callable[[float], float],
    df: Callable[[float], float],
    d2f: Callable[[float], float],
    x0: float,
    epsilon: float = 1e-6,
    max_iter: int = 1000
) -> Tuple[float, float, int, int, list]:
    """
    Niutono metodas optimizavimui.
    
    Algoritmas:
    - remiantis butinosiomis minimumo sąlygomis, galima uzdavini spresti 
      netiesiogiiai, pakeiciant ji lygties f'(x) = 0 sprendimu
    - naudojama Teiloro eilute: f'(x) ≈ f'(x_i) + f''(x_i)·(x - x_i)
    - prilyginus nuliui, gaunama iteracine metodo formule:
      x_{i+1} = x_i - f'(x_i) / f''(x_i)
    
    Interpretacija:
    - iteracine formule isreiskiamas tikslo funkcijos f(x) kvadratines
      aproksimacijos minimumo taskas
    - taske x_i tikslo funkcija aproksimuojama Teiloro eilute, ivertinant 
      ne aukstesnes negu antros eiles narius
    - apskaiciuojamas aproksimuojanciosios kvadratines funkcijos minimumo 
      taskas x_{i+1} ir juo pakeiciamas x_i
    - metodas apibreztas naudojant pirmasias ir antrasias isvestines, 
      bet nenaudojant tikslo funkcijos reiksmiu
    - jei tikslo funkcija butu kvadratine, jos minimumas butu gautas 
      vienu zingsniu
    - bendru atveju formule taikoma iteratyviai
    
    Parametrai:
        f: tikslo funkcija
        df: pirmoji isvestinė f'(x)
        d2f: antroji isvestinė f''(x)
        x0: pradinis taskas
        epsilon: tikslumo riba - algoritmas sustabdomas kai |x_{i+1} - x_i| < epsilon
        max_iter: maksimalus iteraciju skaicius
    
    Grazina:
        x_min: minimumo taskas
        f_min: funkcijos reiksme minimume
        iterations: iteraciju skaicius
        func_calls: bendras funkcijos (isvestiniu) skaiciavimo skaicius
        history: iteraciju istorija
    
    Pastaba:
    Funkcijų skaičiavimams priskiriami f'(x) ir f''(x) įverčiai, nes pats metodas 
    sprendžia f'(x)=0. Funkcija f(x) skaičiuojama tik galutinei minimumo reikšmei.
    """
    x = x0
    history = []
    func_calls = 0
    
    for iteration in range(max_iter):
        dfx = df(x)
        func_calls += 1
        d2fx = d2f(x)
        func_calls += 1
        
        # patikrinimas, ar antroji isvestine nera nulis
        if abs(d2fx) < 1e-10:
            raise ValueError("Antroji išvestinė artima nuliui iteracijoje {}".format(iteration + 1))
        
        # Niutono formule: x_{i+1} = x_i - f'(x_i) / f''(x_i)
        x_new = x - dfx / d2fx
        step = abs(x_new - x)

        history.append({
            'iteration': iteration + 1,
            'x_i': x,
            'x_next': x_new,
            'step': step,
            "f'(x_i)": dfx,
            "f''(x_i)": d2fx
        })

        # patikrinimas, ar pasikeitimas pakankamai mazas
        if step < epsilon:
            x = x_new
            f_min = f(x)
            func_calls += 1
            return x, f_min, iteration + 1, func_calls, history
        
        x = x_new
    
    f_min = f(x)
    func_calls += 1
    return x, f_min, max_iter, func_calls, history

