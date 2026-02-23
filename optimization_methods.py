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
) -> Tuple[float, float, int, list]:
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
        history: iteraciju istorija
    """
    history = []
    
    for iteration in range(max_iter):
        # intervalo ilgis
        L = r - l
        # intervalo vidurio taskas
        x_m = (l + r) / 2
        # du papildomi bandymo taskai
        x_1 = l + L / 4
        x_2 = r - L / 4
        # funkciju reiksmes
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
        
        # tikrina ar pasiektas tikslumas
        if L < epsilon:
            x_min = x_m
            f_min = f_xm
            return x_min, f_min, iteration + 1, history
        
        # intervalo mazinimas
        if f_x1 < f_xm:
            # 3.1: atmetamas (x_m, r], keiciant r = x_m
            # 3.2: intervalo centru tampa x_1, tad keiciama x_m = x_1
            r = x_m
        elif f_x2 < f_xm:
            # 4.1: atmetamas [l, x_m), keiciant l = x_m
            # 4.2: intervalo centru tampa x_2, tad keiciama x_m = x_2
            l = x_m
        else:
            # 5.1: atmetami intervalai [l, x_1] ir (x_2, r]
            l = x_1
            r = x_2
    
    # jei nepasiektas tikslumas per max_iter iteraciju
    x_min = (l + r) / 2
    f_min = f(x_min)
    return x_min, f_min, max_iter, history


def auksinio_pjuvio_metodas(
    f: Callable[[float], float],
    l: float,
    r: float,
    epsilon: float = 1e-6,
    max_iter: int = 1000
) -> Tuple[float, float, int, list]:
    """
    Auksinio pjuvio metodas optimizavimui.
    
    Algoritmas:
    1. L = r - l, x_1 = r - τL ir x_2 = l + τL, skaiciuojame f(x_1) ir f(x_2)
    2. jei f(x_2) < f(x_1), tai atmetamas [l, x_1), l = x_1, x_1 = x_2
    3. priesingu atveju atmetamas (x_2, r], r = x_2, x_2 = x_1
    4. skaiciuojama viena tikslo funkcijos reiksme iteracijoj
    
    Sustojimo salyga:
    - pagal fiksuota funkcijos bandymu skaiciu (max_iter), arba
    - pagal paieskos intervalo ilgi (L < epsilon)
    
    Tolesnis bandymo taskas gaunamas pagal formules:
    - w = r - τ^N arba w = l + τ^N
    - priklausomai kuris pointervals buvo atmestas ankstesnej iteracijoj
    
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
        history: iteraciju istorija
    """
    # fibonacio skaicius 
    tau = (np.sqrt(5) - 1) / 2  # ≈ 0.618
    
    history = []
    
    # pradinis int ir taskai
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
        
        # tikrina ar pasiektas tikslumas
        if L < epsilon:
            x_min = (l + r) / 2
            f_min = f(x_min)
            return x_min, f_min, iteration + 1, history
        
        # int mazinimas
        if f_x2 < f_x1:
            # 2. atmetamas [l, x_1) atliekant keitima l = x_1, L = r - l
            l = x_1
            L = r - l
            # 2.2 kairiuoju tasku tampa ankstesnis desinysis taskas x_1 = x_2
            x_1 = x_2
            f_x1 = f_x2
            # 2.3 naujasis desinysis taskas x_2 = l + τL, skaiciuojam f(x_2)
            x_2 = l + tau * L
            f_x2 = f(x_2)
        else:
            # 3. atmetamas (x_2, r] atliekant keitima r = x_2, L = r - l
            r = x_2
            L = r - l
            # 3.2 desiniuoju tasku tampa ankstesnis kairysis taskas x_2 = x_1
            x_2 = x_1
            f_x2 = f_x1
            # 3.3 naujasis kairysis taskas x_1 = r - τL, skaiciuojame f(x_1)
            x_1 = r - tau * L
            f_x1 = f(x_1)
    
    # jei nepasiektas tikslumas per max_iter iteraciju
    x_min = (l + r) / 2
    f_min = f(x_min)
    return x_min, f_min, max_iter, history


def niutono_metodas(
    f: Callable[[float], float],
    df: Callable[[float], float],
    d2f: Callable[[float], float],
    x0: float,
    epsilon: float = 1e-6,
    max_iter: int = 1000,
    stop_on_gradient: bool = True
) -> Tuple[float, float, int, list]:
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
        f: tikslo funkcija (naudojama tik galutinei reiksmei)
        df: pirmoji isvestinė f'(x)
        d2f: antroji isvestinė f''(x)
        x0: pradinis taskas
        epsilon: tikslumo riba (|x_{i+1} - x_i| < epsilon; papildomai galima |f'(x)| < epsilon)
        max_iter: maksimalus iteraciju skaicius
        stop_on_gradient: jei True, taikoma papildoma |f'(x)| < epsilon salyga
    
    Grazina:
        x_min: minimumo taskas
        f_min: funkcijos reiksme minimume
        iterations: iteraciju skaicius
        history: iteraciju istorija
    """
    x = x0
    history = []
    
    for iteration in range(max_iter):
        dfx = df(x)
        d2fx = d2f(x)
        
        # patikrinimas, ar antroji isvestine nera nulis
        if abs(d2fx) < 1e-10:
            print(f"Įspėjimas: Antroji išvestinė artima nuliui iteracijoje {iteration + 1}")
            f_min = f(x)
            return x, f_min, iteration + 1, history
        
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

        # patikrinimas, ar pasiektas tikslumas (gradientas artimas nuliui)
        if stop_on_gradient and abs(dfx) < epsilon:
            f_min = f(x)
            return x, f_min, iteration + 1, history
        
        # patikrinimas, ar pasikeitimas pakankamai mazas
        if step < epsilon:
            x = x_new
            f_min = f(x)
            return x, f_min, iteration + 1, history
        
        x = x_new
    
    f_min = f(x)
    return x, f_min, max_iter, history

