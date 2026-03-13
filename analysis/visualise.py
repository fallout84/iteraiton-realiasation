import numpy as np
import matplotlib.pyplot as plt
import os

# 1. Загрузка данных
err1 = np.loadtxt("../result/output_err_cpp.txt", delimiter=",")
time1 = np.loadtxt("../result/output_time_cpp.txt", delimiter=",")
y_internal = np.loadtxt("../result/output_dot_cpp.txt", delimiter=",")
ref = np.arange(len(err1))
a, bx = 0.0, 1.0  # границы x
y0, y1 = 0.0, 0.6312 # граничные условия
n = 20
k = 1
f = 1


# --- Блок аппроксимации ---
half = len(err1) // 2
x_fit = ref[half:]
y_fit = np.log10(err1[half:])

k, b_const = np.polyfit(x_fit, y_fit, 1)
trend_line = 10**(k * ref + b_const)
# --------------------------

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

# График 1: Итерации + Тренд
ax1.semilogy(ref, err1, color='royalblue', linewidth=2, label='Данные', zorder=2)
ax1.semilogy(ref, trend_line, color='crimson', linestyle='--', linewidth=1.5, label='Аппроксимация', zorder=1)

# --- Добавляем текст на график ---
# Выбираем место: x = середина, y = чуть выше линии тренда
text_x = ref[int(len(ref)*0.6)]
text_y = trend_line[int(len(trend_line)*0.6)] * 2  # множитель 2, чтобы текст был над линией

ax1.text(text_x, text_y, f'$y/sim 10^{{{k: .4f} /cdot x}}$',
         fontsize=12, color='crimson', fontweight='bold',
         bbox=dict(facecolor='white', alpha=0.8, edgecolor='none'))
# ---------------------------------

ax1.set_title("Сходимость по итерациям", fontsize=14)
ax1.set_xlabel("Номер шага (Iteration)", fontsize=12)
ax1.set_ylabel("Ошибка (Log Residual)", fontsize=12)
ax1.grid(True, which="both", linestyle='--', alpha=0.7)
# График 2: Время
ax2.semilogy(time1, err1, color='forestgreen', linewidth=2)
ax2.set_title("Сходимость по времени", fontsize=14)
ax2.set_xlabel("Время выполнения (sec)", fontsize=12)
ax2.set_ylabel("Ошибка (Log Residual)", fontsize=12)
ax2.grid(True, which="both", linestyle='--', alpha=0.7)

# --- Параметры задачи (те же, что вводил в консоль) ---
          # точек внутри

# 1. Загрузка решения (внутренние точки)


# 2. Реконструкция полного вектора Y (Граничное 0 + Внутренние + Граничное 1)
y_full = np.concatenate(([y0], y_internal, [y1]))

# 3. Реконструкция координат X
# У нас n внутренних точек + 2 граничные = n + 2 точки всего
x_coords = np.linspace(a, bx, n + 2)

# --- Построение графика решения ---
plt.figure(figsize=(8, 5))
plt.plot(x_coords, y_full, 'o-', color='darkviolet', label='Численное решение')

# Создаем массив x для аналитики (более гладкий для красоты)
x_fine = np.linspace(a, bx, 200)
a, bx = 0.0, 1.0  # границы x
y0, y1 = 0.0, 0.6312 # граничные условия
n = 20
k = 1
f = 1
# Вычисляем аналитическое решение y = 1 - exp(-x)
y_analyt = (f / k) + (y0 - (f / k)) * np.exp(-k * (x_fine - a))
# Рисуем
plt.plot(x_fine, y_analyt, label='Аналитическое решение', linestyle='--', color='red', alpha=0.8)
plt.plot(x_coords, y_full, 'o', label='Твой солвер (C++)', markersize=4, color='blue')

plt.title(f"Решение уравнения $y' + ky = f$ ($n={n}$)", fontsize=14)
plt.xlabel("Координата x", fontsize=12)
plt.ylabel("Значение y(x)", fontsize=12)
plt.grid(True, linestyle=':', alpha=0.6)
plt.legend()
plt.savefig("pics/pic2.png", dpi=300)
plt.show()
# Сохранение
if not os.path.exists('pics'):
    os.makedirs('pics')
fig.savefig("pics/pic1.png", dpi=300, bbox_inches='tight')

