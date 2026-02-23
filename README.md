# Vienmačio Optimizavimo Metodai

Šiame projekte realizuoti trys klasikiniai vienmačio optimizavimo metodai:

## Įgyvendinti Metodai

### 1. Intervalo Dalijimo Pusiau Metodas (Bisection Method)
- Iteratyviai mažina paieškos intervalą dalijant jį į dalis
- Pradiniame intervale parenkami trys tolygiai pasiskirste bandymo taškai: x_m, x_1 ir x_2
- Algoritmas:
  - x_m = (l + r) / 2, L = r - l
  - x_1 = l + L/4, x_2 = r - L/4
  - Pagal funkcijų reikšmes atmetama dalis intervalo
- Kiekvienos iteracijos metu atmetama pusė intervalo
- Atlikus N funkcijų skaičiavimų, gauto intervalo ilgis sudaro (1/2)^((N-1)/2) pradinio intervalo dalį
- Pati efektyviausia iš visų intervalo dalijimo į lygias dalis metodų
- Nepriklausomas metodas - nereikia išvestinių

### 2. Auksinio Pjūvio Metodas (Golden Section Method)
- Naudoja auksinio pjūvio santykį φ = (1 + √5)/2 ≈ 1.618
- Efektyvesnis nei paprastas dalijimas pusiau
- Optimalus intervalo mažinimo greitis
- Nepriklausomasmetodas - nereikia išvestinių

### 3. Niutono Metodas (Newton's Method)
- Naudoja pirmąją ir antrąją funkcijos išvestines
- Labai greita konvergencija (kvadratinė)
- Reikalauja funkcijos išvestinių skaičiavimo
- Priklauso nuo pradinio taško pasirinkimo

## Failų Struktūra

```
opt1laboras/
├── optimization_methods.py    # Pagrindiniai algoritmai
├── examples.py                # Pavyzdžiai su skirtingomis funkcijomis
└── README.md                  # Dokumentacija
```

## Kaip Naudoti

### Pagrindinė Demonstracija

```bash
python optimization_methods.py
```

Šis scenarijus paleis visus tris metodus su testine funkcija f(x) = (x - 2)² + 1.

### Pavyzdžiai su Skirtingomis Funkcijomis

```bash
python examples.py
```

Šis scenarijus:
- Paleis visus metodus su 4 skirtingomis funkcijomis
- Sukurs grafikus kiekvienam optimizavimo rezultatui
- Išsaugos rezultatus PNG formatu

## Programinio Kodo Naudojimas

### Pavyzdys 1: Intervalo Dalijimo Pusiau Metodas

```python
from optimization_methods import bisection_method

# Apibrėžkite funkciją
def f(x):
    return (x - 2)**2 + 1

# Paleiskite optimizavimą
x_min, f_min, iterations, history = bisection_method(
    f=f,
    l=0,      # Intervalo pradžia (kairysis galas)
    r=5,      # Intervalo pabaiga (dešinysis galas)
    epsilon=1e-6  # Tikslumas
)

print(f"Minimumas: x* = {x_min}, f(x*) = {f_min}")
print(f"Iteracijų skaičius: {iterations}")

# Pavyzdys iš nuotraukos: f(x) = (100 - x)²
def f_example(x):
    return (100 - x)**2

x_min, f_min, iterations, history = bisection_method(
    f=f_example,
    l=60,
    r=150,
    epsilon=1e-6
)

# Pirmoji iteracija:
# l = 60, r = 150, L = 90, x_m = 105
# x_1 = 60 + 90/4 = 82.5
# x_2 = 150 - 90/4 = 127.5
# f(82.5) = 306.25 > f(105) = 25
# f(127.5) = 756.25 > f(105) = 25
# Atmetami [60; 82.5) ir (127.5; 150]
# Naujas intervalas: [82.5; 127.5], ilgis = 45
```

### Pavyzdys 2: Auksinio Pjūvio Metodas

```python
from optimization_methods import golden_section_method

def f(x):
    return x**4 - 4*x**3 + 4*x**2 + 1

x_min, f_min, iterations, history = golden_section_method(
    f=f,
    l=0,
    r=3,
    epsilon=1e-6
)

print(f"Minimumas: x* = {x_min}, f(x*) = {f_min}")
```

### Pavyzdys 3: Niutono Metodas

```python
from optimization_methods import newton_method

# Funkcija ir jos išvestinės
def f(x):
    return (x - 2)**2 + 1

def df(x):  # Pirmoji išvestinė
    return 2 * (x - 2)

def d2f(x):  # Antroji išvestinė
    return 2

x_min, f_min, iterations, history = newton_method(
    f=f,
    df=df,
    d2f=d2f,
    x0=0,     # Pradinis taškas
    epsilon=1e-6
)

print(f"Minimumas: x* = {x_min}, f(x*) = {f_min}")
```

## Parametrai

Visi metodai priima šiuos bendrus parametrus:

- `f`: Tikslo funkcija (reikia minimizuoti)
- `epsilon`: Tikslumo riba (numatytoji: 1e-6)
- `max_iter`: Maksimalus iteracijų skaičius (numatytasis: 1000)

### Intervalo Metodai (Bisection, Golden Section)
- `l`: Intervalo pradžia (kairysis galas)
- `r`: Intervalo pabaiga (dešinysis galas)

### Niutono Metodas
- `df`: Pirmoji funkcijos išvestinė
- `d2f`: Antroji funkcijos išvestinė
- `x0`: Pradinis paieškos taškas

## Grąžinamos Reikšmės

Visi metodai grąžina:
- `x_min`: Rastas minimumo taškas
- `f_min`: Funkcijos reikšmė minimume
- `iterations`: Iteracijų skaičius iki konvergencijos
- `history`: Sąrašas su informacija apie kiekvieną iteraciją

## Reikalavimai

```bash
pip install numpy matplotlib
```

## Metodų Palyginimas

| Metodas | Privalumai | Trūkumai |
|---------|-----------|----------|
| **Dalijimas pusiau** | Paprastas, patikimas | Lėtas konvergavimas |
| **Auksinis pjūvis** | Efektyvus, patikimas | Vidutinis greitis |
| **Niutono metodas** | Labai greitas | Reikia išvestinių, jautrus pradiniam taškui |

## Pavyzdžių Funkcijos

1. **f(x) = (x - 2)² + 1** - Paprasta kvadratinė funkcija
2. **f(x) = x⁴ - 4x³ + 4x² + 1** - Daugianaris
3. **f(x) = x² + sin(5x)** - Funkcija su trigonometrija
4. **f(x) = eˣ - 3x** - Eksponentinė funkcija

## Licencija

Šis kodas sukurtas mokymo tikslais.
