import numpy as np
import matplotlib.pyplot as plt

def f(x):
    return x**3 - 3*x**2 + 2*x - 5

def bisection_method(f, a, b, eps=1e-6, max_iter=100):
    if f(a) * f(b) > 0:
        return None, []
    iter_count = 0
    history = []
    while (b - a) > eps and iter_count < max_iter:
        c = (a + b) / 2
        history.append(c)
        if abs(f(c)) < eps:
            break
        if f(a) * f(c) < 0:
            b = c
        else:
            a = c
        iter_count += 1
    return (a + b) / 2, history

def secant_method(f, x0, x1, eps=1e-6, max_iter=100):
    history = [x0, x1]
    for i in range(max_iter):
        if abs(f(x1)) < eps:
            break
        if abs(x1 - x0) < eps:
            break
        f0, f1 = f(x0), f(x1)
        if abs(f1 - f0) < eps:
            break
        x_new = x1 - f1 * (x1 - x0) / (f1 - f0)
        history.append(x_new)
        x0, x1 = x1, x_new
    return x1, history

def solve_and_plot():
    a, b = -2, 5
    x_vals = np.linspace(a, b, 1000)
    y_vals = f(x_vals)
    
    root_bisect, hist_bisect = bisection_method(f, a, b)
    root_secant, hist_secant = secant_method(f, 0, 4)
    
    fig, axes = plt.subplots(1, 3, figsize=(15, 4))
    
    axes[0].plot(x_vals, y_vals, 'b-', linewidth=2)
    axes[0].axhline(y=0, color='k', linestyle='-', alpha=0.3)
    axes[0].plot(root_bisect, f(root_bisect), 'ro', markersize=8, label=f'Корень: {root_bisect:.6f}')
    axes[0].set_title('График функции f(x) = x³ - 3x² + 2x - 5')
    axes[0].set_xlabel('x')
    axes[0].set_ylabel('f(x)')
    axes[0].legend()
    axes[0].grid(True)
    
    axes[1].plot(range(1, len(hist_bisect)+1), hist_bisect, 'bo-', markersize=4)
    axes[1].axhline(y=root_bisect, color='r', linestyle='--', alpha=0.5)
    axes[1].set_title('Метод бисекции (половинного деления)')
    axes[1].set_xlabel('Номер итерации')
    axes[1].set_ylabel('Приближение корня')
    axes[1].grid(True)
    
    axes[2].plot(range(1, len(hist_secant)+1), hist_secant, 'go-', markersize=4)
    axes[2].axhline(y=root_secant, color='r', linestyle='--', alpha=0.5)
    axes[2].set_title('Метод секущих')
    axes[2].set_xlabel('Номер итерации')
    axes[2].set_ylabel('Приближение корня')
    axes[2].grid(True)
    
    plt.tight_layout()
    plt.show()
    
    print("=" * 60)
    print("Метод бисекции (половинного деления):")
    print(f"Корень: {root_bisect:.8f}")
    print(f"Значение функции в корне: {f(root_bisect):.2e}")
    print(f"Количество итераций: {len(hist_bisect)}")
    print()
    print("Метод секущих:")
    print(f"Корень: {root_secant:.8f}")
    print(f"Значение функции в корне: {f(root_secant):.2e}")
    print(f"Количество итераций: {len(hist_secant)-2}")
    
    errors_bisect = [abs(x - root_bisect) for x in hist_bisect]
    errors_secant = [abs(x - root_secant) for x in hist_secant[2:]]
    
    fig2, ax2 = plt.subplots(figsize=(8, 5))
    ax2.plot(range(1, len(errors_bisect)+1), errors_bisect, 'bo-', markersize=4, label='Бисекция')
    ax2.plot(range(1, len(errors_secant)+1), errors_secant, 'go-', markersize=4, label='Секущие')
    ax2.set_xlabel('Номер итерации')
    ax2.set_ylabel('Абсолютная ошибка')
    ax2.set_title('Сравнение скорости сходимости методов')
    ax2.set_yscale('log')
    ax2.legend()
    ax2.grid(True)
    plt.show()

if __name__ == "__main__":
    solve_and_plot()