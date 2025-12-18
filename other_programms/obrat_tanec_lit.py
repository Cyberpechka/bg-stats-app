import numpy as np

def input_matrix():
    while True:
        try:
            n = int(input("Введите размер матрицы n (2-5): "))
            if n < 2 or n > 5:
                print("Размер должен быть от 2 до 5")
                continue
            
            print(f"\nВведите матрицу {n}x{np}:")
            print("Вводите строки через пробелы, например: 1 2 3")
            
            A = []
            for i in range(n):
                while True:
                    try:
                        row_input = input(f"Строка {i+1}: ")
                        row = list(map(float, row_input.split()))
                        if len(row) != n:
                            print(f"Ошибка: нужно ввести {n} чисел")
                            continue
                        A.append(row)
                        break
                    except ValueError:
                        print("Ошибка: вводите только числа через пробелы")
            
            A = np.array(A, dtype=float)
            print("\nВведенная матрица:")
            print_matrix(A)
            return A
        except ValueError:
            print("Ошибка: введите целое число")

def print_matrix(M, decimals=4):
    for row in M:
        print(" ".join([f"{x:.{decimals}f}" for x in row]))

def gauss_inverse(A):
    n = len(A)
    det_A = np.linalg.det(A)
    
    if abs(det_A) < 1e-10:
        return None, det_A
    
    augmented = np.hstack([A, np.eye(n)])
    
    for i in range(n):
        if abs(augmented[i,i]) < 1e-10:
            for k in range(i+1, n):
                if abs(augmented[k,i]) > 1e-10:
                    augmented[[i,k]] = augmented[[k,i]]
                    break
        
        pivot = augmented[i,i]
        if abs(pivot) < 1e-10:
            return None, det_A
        
        augmented[i] = augmented[i] / pivot
        
        for j in range(n):
            if j != i:
                factor = augmented[j,i]
                augmented[j] = augmented[j] - factor * augmented[i]
    
    inverse = augmented[:, n:]
    return inverse, det_A

def main():
    print("=" * 50)
    print("НАХОЖДЕНИЕ ОБРАТНОЙ МАТРИЦЫ МЕТОДОМ ГАУССА")
    print("=" * 50)
    
    A = input_matrix()
    
    inverse, det_A = gauss_inverse(A)
    
    print("\n" + "=" * 50)
    print(f"Определитель матрицы: {det_A:.6f}")
    
    if inverse is None:
        print("Матрица вырожденная (определитель близок к 0)")
        print("Обратной матрицы не существует")
    else:
        print("\nОБРАТНАЯ МАТРИЦА:")
        print_matrix(inverse)
        
        print("\nПРОВЕРКА:")
        print("A * A⁻¹ (должна получиться единичная матрица):")
        I_calculated = np.dot(A, inverse)
        print_matrix(I_calculated)
        
        I_expected = np.eye(len(A))
        error = np.max(np.abs(I_calculated - I_expected))
        print(f"\nМаксимальная ошибка: {error:.2e}")
        
        print("\nA⁻¹ * A (тоже должна получиться единичная матрица):")
        I_calculated2 = np.dot(inverse, A)
        print_matrix(I_calculated2)
        
        error2 = np.max(np.abs(I_calculated2 - I_expected))
        print(f"\nМаксимальная ошибка: {error2:.2e}")
    
    print("\n" + "=" * 50)
    print("Сравнение с numpy.linalg.inv:")
    try:
        inv_numpy = np.linalg.inv(A)
        print("Обратная матрица (numpy):")
        print_matrix(inv_numpy)
        
        if inverse is not None:
            diff = np.max(np.abs(inverse - inv_numpy))
            print(f"\nМаксимальная разность с нашей реализацией: {diff:.2e}")
    except:
        print("Numpy также считает матрицу вырожденной")

if __name__ == "__main__":
    while True:
        main()
        print("\n" + "=" * 50)
        again = input("\nХотите ввести новую матрицу? (да/нет): ")
        if again.lower() not in ['да', 'yes', 'y', 'д']:
            print("Выход из программы")
            break
        print()