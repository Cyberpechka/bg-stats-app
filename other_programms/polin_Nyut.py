import numpy as np
import matplotlib.pyplot as plt

def divided_differences(x, y):
    n = len(x)
    coef = np.zeros([n, n])
    coef[:,0] = y
    for j in range(1, n):
        for i in range(n - j):
            coef[i,j] = (coef[i+1,j-1] - coef[i,j-1]) / (x[i+j] - x[i])
    return coef[0,:]

def newton_polynomial(coef, x_data, x):
    n = len(coef) - 1
    p = coef[n]
    for k in range(1, n+1):
        p = coef[n-k] + (x - x_data[n-k]) * p
    return p

def solve_interpolation():
    x_data = np.array([0.0, 1.0, 2.0, 3.0, 4.0])
    y_data = np.array([1.0, 2.0, 1.0, 4.0, 3.0])
    
    coef = divided_differences(x_data, y_data)
    
    x_vals = np.linspace(min(x_data)-0.5, max(x_data)+0.5, 400)
    y_vals = [newton_polynomial(coef, x_data, x) for x in x_vals]
    
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(x_vals, y_vals, 'b-', linewidth=2, label='Полином Ньютона')
    ax.plot(x_data, y_data, 'ro', markersize=8, label='Узлы интерполяции')
    
    for i in range(len(x_data)):
        ax.text(x_data[i], y_data[i], f'({x_data[i]}, {y_data[i]})', 
                fontsize=10, ha='right')
    
    ax.set_title('Интерполяционный полином Ньютона')
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.legend()
    ax.grid(True)
    
    plt.show()
    
    print("Узлы интерполяции:")
    for i in range(len(x_data)):
        print(f"x{i} = {x_data[i]:.1f}, y{i} = {y_data[i]:.1f}")
    
    print("\nКоэффициенты полинома Ньютона:")
    for i in range(len(coef)):
        print(f"a{i} = {coef[i]:.6f}")
    
    print("\nПолином в виде:")
    print(f"P(x) = {coef[0]:.3f}", end="")
    for i in range(1, len(coef)):
        term = f" + {coef[i]:.3f}"
        for j in range(i):
            term += f"(x - {x_data[j]:.1f})"
        print(term)
    
    print("\nЗначения в точках:")
    test_points = [0.5, 1.5, 2.5, 3.5]
    for x in test_points:
        y = newton_polynomial(coef, x_data, x)
        print(f"P({x:.1f}) = {y:.4f}")

if __name__ == "__main__":
    solve_interpolation()