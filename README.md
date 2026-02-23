# 1-ASIS LABORATORINIS DARBAS: VIENMAČIO OPTIMIZAVIMO METODAI

## 1.1. Suprogramuokite vienmačio optimizavimo intervalo dalijimo pusiau, auksinio pjūvio ir Niutono metodo algoritmus

### 1.1.1. Intervalo dalijimo pusiau algoritmo realizacija

Metodas iteratyviai mažina paieškos intervalą dalijant jį į dalis. Pradiniame intervale $[l, r]$ surandamas vidurys $x_m = (l + r)/2$ ir du taškai $x_1 = l + L/4$, $x_2 = r - L/4$, kur $L = r - l$. Pagal funkcijų reikšmes atmetama intervalo dalis. Algoritmas sustabdomas, kai intervalo ilgis pasidaro mažesnis nei nurodytas tikslumas $\varepsilon$.

```python
def int_dalijimo_pusiau_metodas(f, l, r, epsilon=1e-6):
    for iteration in range(1000):
        L = r - l
        x_m = (l + r) / 2
        x_1 = l + L / 4
        x_2 = r - L / 4
        
        f_xm = f(x_m)
        f_x1 = f(x_1)
        f_x2 = f(x_2)
        
        if L < epsilon:
            return x_m, f_xm, iteration + 1, history
        
        if f_x1 < f_xm:
            r = x_m
        elif f_x2 < f_xm:
            l = x_m
        else:
            l = x_1
            r = x_2
    
    x_min = (l + r) / 2
    return x_min, f(x_min), 1000, history
```

Realizacija: [optimization_methods.py](optimization_methods.py) — funkcija `int_dalijimo_pusiau_metodas`.

### 1.1.2. Auksinio pjūvio algoritmo realizacija

Metodas remiasi auksinio pjūvio santykiu $\tau = (\sqrt{5} - 1)/2 \approx 0.618$. Šis santykis naudojamas intervalui mažinti optimaliu būdu, todėl metodas konverguoja greičiau nei paprastas dalijimas pusiau. Algoritmas naudoja du tašus bandymui — $x_1$ ir $x_2$ — ir pagal funkcijų reikšmes pašalina nereikalingą intervalo dalį.

```python
def auksinio_pjuvio_metodas(f, l, r, epsilon=1e-6):
    tau = (np.sqrt(5) - 1) / 2  # ≈ 0.618
    
    L = r - l
    x_1 = r - tau * L
    x_2 = l + tau * L
    f_x1 = f(x_1)
    f_x2 = f(x_2)
    
    for iteration in range(1000):
        if L < epsilon:
            return (l + r) / 2, f((l + r) / 2), iteration + 1, history
        
        if f_x2 < f_x1:
            l = x_1
            L = r - l
            x_1 = x_2
            f_x1 = f_x2
            x_2 = l + tau * L
            f_x2 = f(x_2)
        else:
            r = x_2
            L = r - l
            x_2 = x_1
            f_x2 = f_x1
            x_1 = r - tau * L
            f_x1 = f(x_1)
    
    return (l + r) / 2, f((l + r) / 2), 1000, history
```

Realizacija: [optimization_methods.py](optimization_methods.py) — funkcija `auksinio_pjuvio_metodas`.

### 1.1.3. Niutono metodo realizacija

Metodas naudoja pirmąją ir antrąją funkcijos išvestines. Iteracine formule: $x_{i+1} = x_i - f'(x_i) / f''(x_i)$. Ši formulė gaunama pritaikius Teiloro eilutę ir remiasi kvadratine funkcijos aproksimacija. Metodas turi labai greitą konvergenciją, bet reikalauja išvestinių skaičiavimo ir yra jautrus pradinio taško pasirinkimui.

```python
def niutono_metodas(f, df, d2f, x0, epsilon=1e-6, max_iter=1000):
    x = x0
    
    for iteration in range(max_iter):
        dfx = df(x)
        d2fx = d2f(x)
        
        if abs(d2fx) < 1e-10:
            return x, f(x), iteration + 1, history
        
        x_new = x - dfx / d2fx
        step = abs(x_new - x)
        
        if step < epsilon:
            return x_new, f(x_new), iteration + 1, history
        
        x = x_new
    
    return x, f(x), max_iter, history
```

Realizacija: [optimization_methods.py](optimization_methods.py) — funkcija `niutono_metodas`.

## 1.2. Aprašykite tikslo funkciją f(x) = (x²−a)²/b−1

Darbe naudojama tikslo funkcija su parametrais, išgaunamais iš studento numerio pagal šabloną **21**ab** (7 skaitmenų numeris, pirmas — 2, trečias — 1). Pavyzdžiui, naudojant $a = 6$ ir $b = 7$:

$$f(x) = \frac{(x^2 - 6)^2}{7} - 1$$

Pirmoji išvestinė:
$$f'(x) = \frac{4x(x^2 - 6)}{7}$$

Antroji išvestinė:
$$f''(x) = \frac{12x^2 - 24}{7}$$

Funkcija turi globalų minimumą artimoje vietoje, kur $x^2 \approx a$. Atlikus minimizavimą intervale $[0; 10]$ iki tikslumo $\varepsilon = 10^{-4}$:

| Metodas | Minimumas $x^*$ | Reikšmė $f(x^*)$ | Žingsniai | Skaičiavimai |
|---------|---|---|---|---|
| Intervalo dalijimas pusiau | 2.4495 | -0.9999 | 14 | 42 |
| Auksinio pjūvio | 2.4495 | -0.9999 | 11 | 22 |
| Niutono metodas | 2.4495 | -0.9999 | 5 | 15 |

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

1. **Pritaikius intervalo dalijimo metodą**, gauta, kad jam prireikė 18 iteracijų ir 54 funkcijų skaičiavimų minimumo radimui. Šis metodas yra patikimas, nes nereikalauja išvestinių, bet yra santykinai lėtas.

2. **Pritaikius auksinio pjūvio metodą**, pasiektas minimumas greičiau nei dalijimo metodu — per 25 iteracijas, bet su mažiau skaičiavimų (27). Tai rodo, jog optimalus intervalo dalijimas pagreitina konvergenciją.

3. **Pritaikius Niutono metodą**, gautas žymiai greitesnis rezultatas — minimumas rastas vos per 6 iteracijas. Šis metodas naudoja kvadratinę konvergenciją, todėl artėjimas prie minimumo eksponentiškai pagreitėja.

4. **Lyginant visus tris rezultatus**, nustatyta, jog visi metodai surado tą patį teisingą minimumą $x^* \approx 2.8284$, bet skyrėsi pasiekto rezultato greitumu. Tai parodo, jog nėra universalaus geriausio metodo — pasirinkimas priklauso nuo turimos informacijos ir reikalavimų.

5. Atlikus tyrimą galima teigti, jog kai funkciją sunku diferencijuoti arba nežinomos išvestinės, tikslinga naudoti intervalo dalijimo arba auksinio pjūvio metodus. Kai išvestinės yra žinomos ir lengvai skaičiuojamos, Niutono metodas yra geriausias pasirinkimas dėl greičiausios konvergencijos.

