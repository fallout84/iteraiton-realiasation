import numpy as np
import time as tm
'# константа, определяющая мелкость шага'
k1 = 60000
A = np.loadtxt('../data/A_7_1.txt')
b = np.loadtxt('../data/b_7_1.txt')
if b.ndim == 1:
    b = b.reshape(-1, 1)
rows_A, cols_A = A.shape
rows_b, cols_b = b.shape
if rows_A != rows_b:
    raise ValueError(f"Несовпадение высот! У матрицы A {rows_A} строк, а у вектора b {rows_b}.")
if rows_A != cols_A:
    raise ValueError(f"Код решает СЛАУ для квадратнх матриц! У матрицы A {rows_A} строк, но {cols_A} cтолбцов.")
print("размерность сошлась")
n = rows_A
'# n - базовая размерность, которую ми используем'
x = np.zeros((n, 1))
'#r - невязка, array - массиви, которие надо для графиков'
r = 0
err = []
time = []
start_time = tm.perf_counter()
tau = A[0][0]/k1
for i in range(0, 100000):
    r = b - A@x
    err.append(np.linalg.norm(r))
    time.append(tm.perf_counter() - start_time)
    x = x + tau * r
    if err[i-1] < 0.01:
        print(f"процесс завершен на {i} шаге из 1000")
        break
print(x)
with open("../result/output_err_3_py.txt", "w") as f:
    # Записываем ошибки (через запятую)
    f.write(", ".join([f"{e: .18e}" for e in err]) + "\n")
with open("../result/output_time_3_py.txt", "w") as f:
    # Записываем время (через запятую)
    f.write(", ".join([f"{t: .18e}" for t in time]) + "\n")
