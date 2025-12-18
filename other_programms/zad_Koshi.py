import numpy as np
import matplotlib.pyplot as plt

def euler_method(f, x0, y0, h, n):
    x = np.zeros(n+1)
    y = np.zeros(n+1)
    x[0] = x0
    y[0] = y0
    for i in range(n):
        y[i+1] = y[i] + h * f(x[i], y[i])
        x[i+1] = x[i] + h
    return x, y

def runge_kutta_2(f, x0, y0, h, n):
    x = np.zeros(n+1)
    y = np.zeros(n+1)
    x[0] = x0
    y[0] = y0
    for i in range(n):
        k1 = f(x[i], y[i])
        k2 = f(x[i] + h, y[i] + h * k1)
        y[i+1] = y[i] + h * (k1 + k2) / 2
        x[i+1] = x[i] + h
    return x, y

def solve_and_plot():
    x0 = 0.0
    y0 = 1.0
    x_end = 1.0
    
    def f(x, y):
        return y
    
    def exact_solution(x):
        return np.exp(x)
    
    steps = [0.2, 0.1, 0.05, 0.025]
    
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    fig.suptitle('Численные методы решения задачи Коши: y\' = y, y(0) = 1', fontsize=14)
    
    x_exact = np.linspace(x0, x_end, 1000)
    y_exact = exact_solution(x_exact)
    
    ax_euler = axes[0, 0]
    ax_euler.set_title('Метод Эйлера с разными шагами')
    ax_euler.plot(x_exact, y_exact, 'k-', linewidth=2, label='Точное решение')
    for h in steps:
        n = int((x_end - x0) / h)
        x_num, y_num = euler_method(f, x0, y0, h, n)
        ax_euler.plot(x_num, y_num, 'o-', markersize=4, label=f'h = {h}')
    ax_euler.set_xlabel('x')
    ax_euler.set_ylabel('y')
    ax_euler.legend()
    ax_euler.grid(True)
    
    ax_rk2 = axes[0, 1]
    ax_rk2.set_title('Метод Рунге-Кутты 2-го порядка')
    ax_rk2.plot(x_exact, y_exact, 'k-', linewidth=2, label='Точное решение')
    for h in steps:
        n = int((x_end - x0) / h)
        x_num, y_num = runge_kutta_2(f, x0, y0, h, n)
        ax_rk2.plot(x_num, y_num, 'o-', markersize=4, label=f'h = {h}')
    ax_rk2.set_xlabel('x')
    ax_rk2.set_ylabel('y')
    ax_rk2.legend()
    ax_rk2.grid(True)
    
    ax_comparison = axes[0, 2]
    h = 0.1
    n = int((x_end - x0) / h)
    x_euler, y_euler = euler_method(f, x0, y0, h, n)
    x_rk2, y_rk2 = runge_kutta_2(f, x0, y0, h, n)
    ax_comparison.set_title(f'Сравнение методов (h = {h})')
    ax_comparison.plot(x_exact, y_exact, 'k-', linewidth=2, label='Точное решение')
    ax_comparison.plot(x_euler, y_euler, 'ro-', markersize=5, label='Метод Эйлера')
    ax_comparison.plot(x_rk2, y_rk2, 'bo-', markersize=5, label='Рунге-Кутта 2-го порядка')
    ax_comparison.set_xlabel('x')
    ax_comparison.set_ylabel('y')
    ax_comparison.legend()
    ax_comparison.grid(True)
    
    errors_euler = []
    for h in steps:
        n = int((x_end - x0) / h)
        x_num, y_num = euler_method(f, x0, y0, h, n)
        error = np.abs(y_num[-1] - exact_solution(x_end))
        errors_euler.append(error)
    ax_error_euler = axes[1, 0]
    ax_error_euler.plot(steps, errors_euler, 'ro-', linewidth=2)
    ax_error_euler.set_xlabel('Шаг h')
    ax_error_euler.set_ylabel('Погрешность в точке x=1')
    ax_error_euler.set_title('Зависимость ошибки от шага (Эйлер)')
    ax_error_euler.grid(True)
    ax_error_euler.set_xscale('log')
    ax_error_euler.set_yscale('log')
    
    errors_rk2 = []
    for h in steps:
        n = int((x_end - x0) / h)
        x_num, y_num = runge_kutta_2(f, x0, y0, h, n)
        error = np.abs(y_num[-1] - exact_solution(x_end))
        errors_rk2.append(error)
    ax_error_rk2 = axes[1, 1]
    ax_error_rk2.plot(steps, errors_rk2, 'bo-', linewidth=2)
    ax_error_rk2.set_xlabel('Шаг h')
    ax_error_rk2.set_ylabel('Погрешность в точке x=1')
    ax_error_rk2.set_title('Зависимость ошибки от шага (Рунге-Кутта 2)')
    ax_error_rk2.grid(True)
    ax_error_rk2.set_xscale('log')
    ax_error_rk2.set_yscale('log')
    
    ax_error_comparison = axes[1, 2]
    ax_error_comparison.plot(steps, errors_euler, 'ro-', linewidth=2, label='Метод Эйлера')
    ax_error_comparison.plot(steps, errors_rk2, 'bo-', linewidth=2, label='Рунге-Кутта 2')
    ax_error_comparison.set_xlabel('Шаг h')
    ax_error_comparison.set_ylabel('Погрешность в точке x=1')
    ax_error_comparison.set_title('Сравнение погрешностей методов')
    ax_error_comparison.legend()
    ax_error_comparison.grid(True)
    ax_error_comparison.set_xscale('log')
    ax_error_comparison.set_yscale('log')
    
    plt.tight_layout()
    plt.show()
    
    print("=" * 60)
    print("Сравнение результатов при h = 0.1:")
    print("=" * 60)
    h = 0.1
    n = int((x_end - x0) / h)
    x_euler, y_euler = euler_method(f, x0, y0, h, n)
    x_rk2, y_rk2 = runge_kutta_2(f, x0, y0, h, n)
    print(f"{'x':<10} {'Точное':<10} {'Эйлер':<10} {'Рунге-Кутта 2':<15}")
    print("-" * 50)
    for i in range(len(x_euler)):
        exact = exact_solution(x_euler[i])
        print(f"{x_euler[i]:<10.3f} {exact:<10.4f} {y_euler[i]:<10.4f} {y_rk2[i]:<15.4f}")
    print("\nПогрешности в конечной точке x = 1:")
    print(f"Метод Эйлера: {abs(y_euler[-1] - exact_solution(1)):.6f}")
    print(f"Метод Рунге-Кутты 2: {abs(y_rk2[-1] - exact_solution(1)):.6f}")

if __name__ == "__main__":
    solve_and_plot()