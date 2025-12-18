import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button

def jacobi_method(A, b, x0, tolerance=1e-6, max_iterations=1000):
    n = len(b)
    x = x0.copy()
    residuals = []
    
    for k in range(max_iterations):
        x_new = np.zeros_like(x)
        
        for i in range(n):
            sigma = 0
            for j in range(n):
                if j != i:
                    sigma += A[i, j] * x[j]
            x_new[i] = (b[i] - sigma) / A[i, i]
        
        residual = np.linalg.norm(A @ x_new - b)
        residuals.append(residual)
        
        if residual < tolerance:
            return x_new, residuals, k + 1
        
        x = x_new
    
    return x_new, residuals, max_iterations

def seidel_method(A, b, x0, tolerance=1e-6, max_iterations=1000):
    n = len(b)
    x = x0.copy()
    residuals = []
    
    for k in range(max_iterations):
        x_new = x.copy()
        
        for i in range(n):
            sigma = 0
            for j in range(n):
                if j != i:
                    sigma += A[i, j] * x_new[j]
            x_new[i] = (b[i] - sigma) / A[i, i]
        
        residual = np.linalg.norm(A @ x_new - b)
        residuals.append(residual)
        
        if residual < tolerance:
            return x_new, residuals, k + 1
        
        x = x_new
    
    return x_new, residuals, max_iterations

class InteractivePlot:
    def __init__(self, results, tolerance):
        self.results = results
        self.tolerance = tolerance
        self.current_view = 'all'
        
        self.fig, self.ax = plt.subplots(figsize=(14, 9))
        plt.subplots_adjust(bottom=0.15)
        
        self.create_buttons()
        self.plot_all()
        
    def create_buttons(self):
        ax_all = plt.axes([0.1, 0.02, 0.15, 0.06])
        ax_jacobi = plt.axes([0.3, 0.02, 0.15, 0.06])
        ax_seidel = plt.axes([0.5, 0.02, 0.15, 0.06])
        ax_zoom = plt.axes([0.7, 0.02, 0.15, 0.06])
        
        self.btn_all = Button(ax_all, 'Все методы')
        self.btn_jacobi = Button(ax_jacobi, 'Только Якоби')
        self.btn_seidel = Button(ax_seidel, 'Только Зейдель')
        self.btn_zoom = Button(ax_zoom, 'Приблизить конец')
        
        self.btn_all.on_clicked(self.show_all)
        self.btn_jacobi.on_clicked(self.show_jacobi)
        self.btn_seidel.on_clicked(self.show_seidel)
        self.btn_zoom.on_clicked(self.zoom_end)
        
    def plot_all(self):
        self.ax.clear()
        colors = ['blue', 'red', 'green']
        markers = ['o', 's', '^']
        
        for i, (x0, jacobi_data, seidel_data) in enumerate(self.results):
            res_jacobi, iter_jacobi = jacobi_data
            res_seidel, iter_seidel = seidel_data
            
            # Метод Якоби
            self.ax.plot(range(len(res_jacobi)), res_jacobi, 
                        color=colors[i], linestyle='-', linewidth=2,
                        marker=markers[i], markersize=4, markevery=max(1, len(res_jacobi)//10),
                        label=f'Якоби (нач.{i+1}: {x0}, итер.: {iter_jacobi})')
            
            # Метод Зейделя
            self.ax.plot(range(len(res_seidel)), res_seidel, 
                        color=colors[i], linestyle='--', linewidth=2,
                        marker=markers[i], markersize=4, markevery=max(1, len(res_seidel)//10),
                        label=f'Зейдель (нач.{i+1}: {x0}, итер.: {iter_seidel})')
        
        self.ax.axhline(self.tolerance, color='black', linestyle=':', 
                       linewidth=2, label=f'Точность {self.tolerance:.1e}')
        
        self.ax.set_xlabel('Номер итерации', fontsize=12)
        self.ax.set_ylabel('Норма невязки', fontsize=12)
        self.ax.set_title('Сравнение методов Якоби и Зейделя', fontsize=14, fontweight='bold')
        self.ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        self.ax.grid(True, alpha=0.3)
        self.ax.set_yscale('log')
        self.ax.set_xlim(0, None)
        
        # Включаем навигацию
        self.fig.canvas.toolbar.zoom()
        self.fig.canvas.toolbar.pan()
        
        plt.draw()
    
    def show_all(self, event):
        self.current_view = 'all'
        self.plot_all()
    
    def show_jacobi(self, event):
        self.ax.clear()
        colors = ['blue', 'red', 'green']
        markers = ['o', 's', '^']
        
        for i, (x0, jacobi_data, seidel_data) in enumerate(self.results):
            res_jacobi, iter_jacobi = jacobi_data
            self.ax.plot(range(len(res_jacobi)), res_jacobi, 
                        color=colors[i], linestyle='-', linewidth=2,
                        marker=markers[i], markersize=6, markevery=max(1, len(res_jacobi)//10),
                        label=f'Якоби (нач.{i+1}: {x0}, итер.: {iter_jacobi})')
        
        self.ax.axhline(self.tolerance, color='black', linestyle=':', linewidth=2)
        self.ax.set_xlabel('Номер итерации')
        self.ax.set_ylabel('Норма невязки')
        self.ax.set_title('Метод Якоби - зависимость невязки от итерации')
        self.ax.legend()
        self.ax.grid(True, alpha=0.3)
        self.ax.set_yscale('log')
        plt.draw()
    
    def show_seidel(self, event):
        self.ax.clear()
        colors = ['blue', 'red', 'green']
        markers = ['o', 's', '^']
        
        for i, (x0, jacobi_data, seidel_data) in enumerate(self.results):
            res_seidel, iter_seidel = seidel_data
            self.ax.plot(range(len(res_seidel)), res_seidel, 
                        color=colors[i], linestyle='--', linewidth=2,
                        marker=markers[i], markersize=6, markevery=max(1, len(res_seidel)//10),
                        label=f'Зейдель (нач.{i+1}: {x0}, итер.: {iter_seidel})')
        
        self.ax.axhline(self.tolerance, color='black', linestyle=':', linewidth=2)
        self.ax.set_xlabel('Номер итерации')
        self.ax.set_ylabel('Норма невязки')
        self.ax.set_title('Метод Зейделя - зависимость невязки от итерации')
        self.ax.legend()
        self.ax.grid(True, alpha=0.3)
        self.ax.set_yscale('log')
        plt.draw()
    
    def zoom_end(self, event):
        if self.current_view == 'all':
            self.plot_all()
        max_iter = 0
        for _, jacobi_data, seidel_data in self.results:
            max_iter = max(max_iter, len(jacobi_data), len(seidel_data))
        
        # Приближаем на последние 20 итераций или 1/4 графика
        zoom_start = max(0, max_iter - min(20, max_iter // 4))
        self.ax.set_xlim(zoom_start, max_iter)
        plt.draw()

def main():
    print("Решение СЛАУ методами Якоби и Зейделя")
    
    n = int(input("Размерность системы (2 или 3): "))
    
    print(f"\nВведите матрицу A {n}x{n} построчно:")
    A = []
    for i in range(n):
        row = list(map(float, input(f"Строка {i+1}: ").split()))
        A.append(row)
    A = np.array(A)
    
    b = list(map(float, input(f"\nВектор b ({n} чисел): ").split()))
    b = np.array(b)
    
    tolerance = float(input("\nТочность (например 0.0001): "))
    
    approximations = [
        np.zeros(n),
        np.ones(n),
        np.array([2.0, -1.0, 0.5][:n])
    ]
    
    exact_solution = np.linalg.solve(A, b)
    print(f"\nТочное решение: {exact_solution}")
    
    print(f"\nРешаем систему:")
    for i in range(n):
        equation = " + ".join([f"{A[i,j]}x{j+1}" for j in range(n)])
        print(f"{equation} = {b[i]}")
    
    # Собираем результаты
    results = []
    for i, x0 in enumerate(approximations):
        print(f"\n--- Начальное приближение {i+1}: {x0} ---")
        
        x_jacobi, res_jacobi, iter_jacobi = jacobi_method(A, b, x0, tolerance)
        print(f"Метод Якоби:   x = {x_jacobi}, итераций: {iter_jacobi}")
        
        x_seidel, res_seidel, iter_seidel = seidel_method(A, b, x0, tolerance)
        print(f"Метод Зейделя: x = {x_seidel}, итераций: {iter_seidel}")
        
        results.append((x0, (res_jacobi, iter_jacobi), (res_seidel, iter_seidel)))
    
    # Создаем интерактивный график
    plot = InteractivePlot(results, tolerance)
    plt.show()

if __name__ == "__main__":
    main()