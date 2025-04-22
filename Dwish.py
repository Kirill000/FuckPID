import numpy as np
from sympy import symbols, Poly, solve

def get_polynomial_expr(coeffs, s):
    """Возвращает символьное выражение полинома"""
    return sum(c * s**i for i, c in enumerate(reversed(coeffs)))

def calculate_pid(num, den, desired_poly_coeffs):
    s = symbols('s')
    p2, p1, p0, l2, l1, l0 = symbols('p2 p1 p0 l2 l1 l0')

    # Получаем объектную передаточную функцию
    G_num = get_polynomial_expr(num, s)
    G_den = get_polynomial_expr(den, s)

    # Режим регулятора: kd*s^2 + kp*s + ki
    R_num = Poly(p2*s**2+p1*s+p0, s)
    R_gen = Poly(l2*s**2+l1*s+l0, s)

    # Характеристический полином: A(s)*R(s) + B(s)
    A = Poly(G_den, s)
    B = Poly(G_num, s)
    desired_poly = Poly(get_polynomial_expr(desired_poly_coeffs, s), s)

    char_eq = Poly(A*R_gen + B*R_num, s)
    char_coeffs = char_eq.all_coeffs()
    desired_coeffs = desired_poly.all_coeffs()

    # Дополнение нулями, если степени разные
    max_len = max(len(char_coeffs), len(desired_coeffs))
    char_coeffs = [c.expand() for c in ([0]*(max_len - len(char_coeffs)) + char_coeffs)]
    desired_coeffs = [0]*(max_len - len(desired_coeffs)) + desired_coeffs

    # Формируем уравнения
    equations = [char - des for char, des in zip(char_coeffs, desired_coeffs)]

    # Решаем
    solution = solve(equations, (p2, p1, p0, l2, l1, l0))
    
    l0_default = 0
    solution_substituted = {k: v.subs(l0, l0_default) for k, v in solution.items()}

    return solution_substituted


def main():
    from sympy import symbols
    s = symbols('s')

    print("Введите передаточную функцию объекта управления.")
    print("Формат: числитель и знаменатель через пробел. Пример: 1 3 2 / 1 2 1")
    tf_input = input("TF: ").strip()

    try:
        num_str, den_str = tf_input.split('/')
        num = list(map(float, num_str.strip().split()))
        den = list(map(float, den_str.strip().split()))
    except Exception as e:
        print("Ошибка при вводе передаточной функции:", e)
        return

    print("Введите желаемый характеристический полином (собственный оператор).")
    print("Пример: 2.5 4 2.5 1 (это 2.5s^3 + 4s^2 + 2.5s + 1)")
    try:
        desired_input = input("Желаемый полином: ").strip()
        desired_poly = list(map(float, desired_input.strip().split()))
    except Exception as e:
        print("Ошибка при вводе характеристического полинома:", e)
        return

    result = calculate_pid(num, den, desired_poly)

    print("\n📊 Найденные коэффициенты ПИД-регулятора:")
    print(result)
    p2 = result.get(symbols('p2'), 0)
    p1 = result.get(symbols('p1'), 0)
    p0 = result.get(symbols('p0'), 0)
    l2 = result.get(symbols('l2'), 0)
    l1 = result.get(symbols('l1'), 0)
    l0 = result.get(symbols('l0'), 0)

    print(f"kd = {(p1*l1**2-p1*l1*l2+p0*l2**2)/(l1**3)}")
    print(f"kp = {(p1*l1-p0*l2)/(l1**2)}")
    print(f"ki = {p0/l1}")


if __name__ == "__main__":
    main()

# 4 / 43.94 54.08 16.9 1
# 1 15 90 270 405 243