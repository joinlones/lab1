import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.integrate import quad

# Определение функции для проверки попадания точки в целевую область
def is_in_target(x, y):
    # Левая нижняя четверть круга (R=5, x <= 0, y <= 0)
    quarter_circle = (x <= 0) & (y <= 0) & (x ** 2 + y ** 2 <= 25)

    # Область над параболой y = (x - 1)^2, ограниченная прямоугольником обстрела
    parabola_x_min = 1 - np.sqrt(5)
    parabola_x_max = 1 + np.sqrt(5)
    parabola = (
            (x >= parabola_x_min) &
            (x <= parabola_x_max) &
            (y >= (x - 1) ** 2) &
            (y <= 5)  # Верхняя граница прямоугольника
    )

    return quarter_circle | parabola

# Границы прямоугольника обстрела
x_min, x_max = -5, 5
y_min, y_max = -5, 5

# Функция для проведения одного эксперимента
def run_experiment():
    n = np.random.randint(500, 1000)
    x = np.random.uniform(x_min, x_max, n)
    y = np.random.uniform(y_min, y_max, n)
    hits = is_in_target(x, y)
    nr = np.sum(hits)
    p = nr / n
    return n, nr, p, x, y, hits

# Построение точечной диаграммы
def plot_diagram(x, y, hits):
    plt.figure(figsize=(8, 8))
    plt.scatter(x[hits], y[hits], color='green', label='Попали')
    plt.scatter(x[~hits], y[~hits], color='red', label='Не попали')
    plt.title('Результаты стрельбы')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.legend()
    plt.grid(True)
    plt.show()

# Проведение 20 экспериментов
results = []
for i in range(20):
    n, nr, p, x, y, hits = run_experiment()
    results.append({'i': i, 'n': n, 'nr': nr, 'p': p})
    # Построить диаграмму только для первого эксперимента
    if i == 0:
        plot_diagram(x, y, hits)

# Создание датафрейма
df = pd.DataFrame(results)
print("Датафрейм:")
print(df)

# Сохранение результатов в Excel
df.to_excel('results.xlsx', index=False, engine='openpyxl')

# Расчет средней экспериментальной вероятности
pi_exp = df['p'].mean()
print(f'\nСредняя экспериментальная вероятность: {pi_exp:.6f}')

# Расчет теоретической вероятности
def lower_circle_area():
    return 0.5 * np.pi * 5**2

def upper_parabola_area():
    a = 1 - np.sqrt(5)
    b = 1 + np.sqrt(5)
    def integrand(x):
        return 5 - (x - 1)**2
    area, _ = quad(integrand, a, b)
    return area

S_circle = lower_circle_area()
S_parabola = upper_parabola_area()
S_total = S_circle + S_parabola
S_rectangle = (x_max - x_min) * (y_max - y_min)
P_theor = S_total / S_rectangle
print(f'Теоретическая вероятность: {P_theor:.6f}')

# Сравнение вероятностей
print(f'\nСредняя экспериментальная вероятность: {pi_exp:.6f}')
print(f'Теоретическая вероятность: {P_theor:.6f}')