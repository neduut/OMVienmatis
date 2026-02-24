# 1-ASIS LABORATORINIS DARBAS: VIENMAČIO OPTIMIZAVIMO METODAI

## 1.1. Suprogramuokite vienmačio optimizavimo intervalo dalijimo pusiau, auksinio pjūvio ir Niutono metodo algoritmus

### 1.1.1. Intervalo dalijimo pusiau algoritmo realizacija

Metodas iteratyviai mažina paieškos intervalą dalijant jį į dalis. Pradiniame intervale $[l, r]$ surandamas vidurys $x_m = (l + r)/2$ ir du taškai $x_1 = l + L/4$, $x_2 = r - L/4$, kur $L = r - l$. Pagal funkcijų reikšmes atmetama intervalo dalis. Algoritmas sustabdomas, kai intervalo ilgis pasidaro mažesnis nei nurodytas tikslumas $\varepsilon$.

Intervalų atmetimo metodams reikalingas **unimodalumas** (vienas minimumas intervale). Mūsų tikslo funkcija $f(x) = \frac{(x^2 - a)^2}{b} - 1$ turi du simetriškus minimumus ties $x = \pm\sqrt{a}$. Pasirinkus intervalą $[0; 10]$, lieka tik vienas minimumas ties $x = +\sqrt{a} \approx 2.449$, o funkcija intervale yra unimodali - tai garantuoja algoritmų konvergenciją.

```python
def int_dalijimo_pusiau_metodas(f, l, r, epsilon=1e-6):
    func_calls = 0
    history = []
    
    for iteration in range(1000):
        L = r - l
        
        # tikrina ar pasiektas tikslumas PRIEŠ skaičiuojant
        if L < epsilon:
            x_min = (l + r) / 2
            f_min = f(x_min)
            func_calls += 1
            return x_min, f_min, iteration, func_calls, history
        
        # tik tada skaičiuojame
        x_m = (l + r) / 2
        x_1 = l + L / 4
        x_2 = r - L / 4
        
        f_xm = f(x_m)
        f_x1 = f(x_1)
        f_x2 = f(x_2)
        func_calls += 3
        
        history.append({...})
        
        if f_x1 < f_xm:
            r = x_m
        elif f_x2 < f_xm:
            l = x_m
        else:
            l = x_1
            r = x_2
    
    x_min = (l + r) / 2
    f_min = f(x_min)
    func_calls += 1
    return x_min, f_min, 1000, func_calls, history
```

**Grąžina**: `(x_min, f_min, iterations, func_calls, history)`

### 1.1.2. Auksinio pjūvio algoritmo realizacija

Metodas remiasi auksinio pjūvio santykiu $\tau = (\sqrt{5} - 1)/2 \approx 0.618$. Šis santykis naudojamas intervalui mažinti optimaliu būdu, todėl metodas konverguoja greičiau nei paprastas dalijimas pusiau. Algoritmas naudoja du tašus bandymui — $x_1$ ir $x_2$ — ir pagal funkcijų reikšmes pašalina nereikalingą intervalo dalį. Iteracija laikomas vienas intervalo siaurinimo žingsnis.

```python
def auksinio_pjuvio_metodas(f, l, r, epsilon=1e-6):
    tau = (np.sqrt(5) - 1) / 2  # ≈ 0.618
    func_calls = 0
    iterations = 0
    history = []
    
    # Pradinė inicializacija
    L = r - l
    x_1 = r - tau * L
    x_2 = l + tau * L
    f_1 = f(x_1)
    f_2 = f(x_2)
    func_calls += 2
    
    # while ciklas - sustojimas pagal L > epsilon
    while L > epsilon and iterations < 1000:
        iterations += 1
        
        history.append({...})
        
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
```

**Grąžina**: `(x_min, f_min, iterations, func_calls, history)`

**Pastaba**: Auksinio pjūvio metodas naudoja `while L > epsilon` ciklą ir efektyviai skaičiuoja tik **po 1 naujo f() per iteraciją**.

### 1.1.3. Niutono metodo realizacija

Metodas naudoja pirmąją ir antrąją funkcijos išvestines. Iteracine formule: $x_{i+1} = x_i - f'(x_i) / f''(x_i)$. Ši formulė gaunama pritaikius Teiloro eilutę ir remiasi kvadratine funkcijos aproksimacija. Metodas turi labai greitą konvergenciją, bet reikalauja išvestinių skaičiavimo ir yra jautrus pradinio taško pasirinkimui.

```python
def niutono_metodas(f, df, d2f, x0, epsilon=1e-6, max_iter=1000):
    x = x0
    func_calls = 0
    history = []
    
    for iteration in range(max_iter):
        dfx = df(x)
        func_calls += 1
        d2fx = d2f(x)
        func_calls += 1
        
        if abs(d2fx) < 1e-10:
            raise ValueError("Antroji išvestinė artima nuliui")
        
        # Niutono formulė: x_{i+1} = x_i - f'(x_i) / f''(x_i)
        x_new = x - dfx / d2fx
        step = abs(x_new - x)
        
        history.append({...})
        
        if step < epsilon:
            x = x_new
            f_min = f(x)
            func_calls += 1
            return x, f_min, iteration + 1, func_calls, history
        
        x = x_new
    
    f_min = f(x)
    func_calls += 1
    return x, f_min, max_iter, func_calls, history
```

**Grąžina**: `(x_min, f_min, iterations, func_calls, history)`

**Pastaba**: Niutono metode funkcijų skaičiavimams priskiriami $f'(x)$ ir $f''(x)$ įverčiai, nes pats metodas sprendžia $f'(x)=0$. Funkcija $f(x)$ skaičiuojama tik galutinei minimumo reikšmei.

Realizacija: [optimization_methods.py](optimization_methods.py) — funkcija `niutono_metodas`.

## 1.2. Aprašykite tikslo funkciją f(x) = (x²−a)²/b−1

Darbe naudojama tikslo funkcija su parametrais, išgaunamais iš studento numerio pagal šabloną 2*1**ab (7 skaitmenų numeris, antrasis — *, trečias — 1). Pavyzdžiui, naudojant $a = 6$ ir $b = 7$:

$$f(x) = \frac{(x^2 - 6)^2}{7} - 1$$

Pirmoji išvestinė:
$$f'(x) = \frac{4x(x^2 - 6)}{7}$$

Antroji išvestinė:
$$f''(x) = \frac{12x^2 - 24}{7}$$

Funkcija turi globalų minimumą artimoje vietoje, kur $x^2 \approx a$. Atlikus minimizavimą intervale $[0; 10]$ iki tikslumo $\varepsilon = 10^{-4}$:

| Metodas | Minimumas $x^*$ | Reikšmė $f(x^*)$ | Žingsniai | Skaičiavimai |
|---------|---|---|---|---|
| Intervalo dalijimas pusiau | 2.449493 | -1.000000 | 17 | 52 |
| Auksinio pjūvio | 2.449462 | -1.000000 | 24 | 27 |
| Niutono metodas | 2.449490 | -1.000000 | 6 | 13 |

**Pastaba**: Jei skaičius $b = 0$, susumuojami visi numerio skaitmenys, tada gautos sumos skaitmenys, kol lieka vienženklis skaičius — jis ir imamas kaip $b$.

## 1.3. Vizualizacija

Paleidus programą [lab_task.py](lab_task.py), generuojami du grafikai:

- **vizualizacija.png** — tikslo funkcijos grafikas intervale $[0; 10]$ su visais trijų metodų bandymo taškais
- **vizualizacija_arti.png** — priartintas vaizdas aplink rastą minimumą

Grafikuose skirtingos spalvos ($\circ$ raudona, $\square$ žalia, $\triangle$ mėlyna) žymi skirtingus metodus, o kryžiai ($\times$ juodi) rodo rastus minimumus.

## 1.4. Palyginimas ir rezultatų interpretacija

Palyginimas atliekamas pagal šiuos kriterijus:

- **Rastas minimumas** $x^*$ — taško, kuriame funkcija įgyja minimumą, abscisė
- **Minimumo reikšmė** $f(x^*)$ — funkcijos reikšmė tame taške
- **Žingsnių skaičius** — iteracijų, kurios atliktos iki konvergencijos, kiekis
- **Funkcijų skaičiavimų skaičius** — bendras funkcijos ir išvestinių skaičiavimų kiekis

Šios duomenys rodo, jog labiausiai efektyvus yra Niutono metodas — jis naudoja mažiausiai žingsnių ir skaičiavimų. Tačiau jis reikalauja, kad būtų žinomos funkcijos išvestinės. Intervalo dalijimo ir auksinio pjūvio metodai yra patikimesni, nes nepriklauso nuo išvestinių žinojimo.

## Išvados

1. **Pritaikius intervalo dalijimo metodą**, gauta, kad jam prireikė **17 iteracijų ir 52 funkcijų skaičiavimų** minimumo radimui. Šis metodas yra patikimas, nes nereikalauja išvestinių, bet yra santykinai lėtas. Kiekvienoje iteracijoje skaičiuojamos trys funkcijos reikšmės, todėl funkcijų skaičiavimų skaičius auga proporcingai iteracijų skaičiui.

2. **Pritaikius auksinio pjūvio metodą**, pasiektas minimumas su **24 iteracijomis, bet tik 27 funkcijų skaičiavimais**. Tai rodo, jog auksinio pjūvio santykis ($\tau \approx 0.618$) efektyviai sumažina reikalingą iteracijų skaičių. Metodas per iteraciją skaičiuoja tik vieną naują funkcijos reikšmę, todėl yra ekonomiškas.

3. **Pritaikius Niutono metodą**, gautas žymiai greitesnis rezultatas — minimumas rastas vos per **6 iteracijas su 13 skaičiavimų** (2 išvestinės per iteraciją + 1 galutiniam f(x)). Šis metodas naudoja kvadratinę konvergenciją, todėl artėjimas prie minimumo eksponentiškai pagreitėja. 

4. **Lyginant visus tris rezultatus**, nustatyta, jog visi metodai surado tą patį teisingą minimumą $x^* \approx 2.449$, su f(x*) = -1.0. Tai patvirtina, jog visos implementacijos teisingos. 
   - **Pagal iteracijų skaičių** (mažiau = greičiau): Niuton (6) > Dalijimas (17) > Auksinis (24)
   - **Pagal funkcijų skaičiavimų kiekį** (mažiau = ekonomiškiau): Niuton (13) > Auksinis (27) > Dalijimas (52)

5. **Atlikus tyrimą galima teigti**, jog:
   - Kai funkciją sunku diferencijuoti arba nežinomos išvestinės, tikslinga naudoti **auksinio pjūvio metodą** (geriausias iš intervalų atmetimo metodų, efektyvus 27 skaičiavimai su 24 iteracijomis).
   - Kai išvestinės yra žinomos ir lengvai skaičiuojamos, **Niutono metodas** yra geriausias pasirinkimas dėl greičiausios konvergencijos (vos 6 iteracijos).
   - **Intervalo dalijimo metodas** yra universalus ir patikimas, bet lėtesnis, tinkamas, kai reikalingas paprastas ir stabilus metodas be išvestinių naudojimo.

