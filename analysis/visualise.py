import numpy as np
import matplotlib.pyplot as plt
import os

# 1. Загрузка данных
err1 = np.loadtxt("../result/output_err_1_py.txt", delimiter=",")
time1 = np.loadtxt("../result/output_time_1_py.txt", delimiter=",")
ref = np.arange(len(err1))

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

ax1.text(text_x, text_y, f'$y \sim 10^{{{k: .4f} \cdot x}}$',
         fontsize=12, color='crimson', fontweight='bold',
         bbox=dict(facecolor='white', alpha=0.8, edgecolor='none'))
# ---------------------------------

ax1.set_title("Сходимость по итерациям", fontsize=14)
ax1.set_xlabel("Номер шага (Iteration)", fontsize=12)
ax1.set_ylabel("Ошибка (Log Residual)", fontsize=12)
ax1.grid(True, which="both", linestyle='--', alpha=0.7)
ax1.legend()

# График 2: Время
ax2.semilogy(time1, err1, color='forestgreen', linewidth=2)
ax2.set_title("Сходимость по времени", fontsize=14)
ax2.set_xlabel("Время выполнения (sec)", fontsize=12)
ax2.set_ylabel("Ошибка (Log Residual)", fontsize=12)
ax2.grid(True, which="both", linestyle='--', alpha=0.7)

# Сохранение
if not os.path.exists('pics'):
    os.makedirs('pics')
fig.savefig("pics/pic1.png", dpi=300, bbox_inches='tight')

print(f"Готово! Наклон k={k: .4f} выведен на график.")
