import numpy as np
from math import atan2, pi, cos, sin, degrees
from sympy import symbols

def main():
    print("Введите передаточную функцию объекта в формате:")
    print("Пример: 3 / 1 5 6 0 (эквивалентно 3 / (s*(s+2)*(s+3)))")
    tf_input = input("TF: ").strip()

    try:
        num_str, den_str = tf_input.split('/')
        num = list(map(float, num_str.strip().split()))
        den = list(map(float, den_str.strip().split()))
    except Exception as e:
        print("Ошибка при вводе передаточной функции:", e)
        return

    try:
        sigma = float(input("Введите значение σ: "))
        k_s = float(input("Введите значение K(σ): "))
        delta_phi_deg = float(input("Введите фазовый запас Δφ (в градусах): "))
        t_reg = float(input("Введите время регулирования (в секундах): "))
    except Exception as e:
        print("Ошибка при вводе параметров:", e)
        return

    wc =  k_s*pi/t_reg
    print(f"\n🔍 Частота среза ωc: {wc:.4f} рад/с")
    
    w = symbols('w')

    jw = complex(0, wc)
    W_jw = np.polyval(num, jw) / np.polyval(den, jw)

    mod_W = abs(W_jw)
    arg_W = atan2(W_jw.imag, W_jw.real)
    arg_W_deg = degrees(arg_W)

    print(f"|W(jωc)| = {mod_W:.4f}")
    print(f"arg(W(jωc)) = {arg_W_deg:.2f}°")

    beta_deg = -180 + delta_phi_deg + arg_W_deg   # у меня фаза отрицательная я поставил сразу +
    beta_rad = beta_deg * pi / 180

    print(f"\n📐 Требуемая фаза K(jωc): {beta_deg:.2f}°")
    
    kf = 0.3          # Kи = 0.1...0.3Kд

    Kp = cos(beta_rad)/mod_W
    Kd = (sin(beta_rad)/mod_W)/(wc - (kf / wc))  
    Ki = kf*Kd

    print("\n📊 Найденные коэффициенты ПИД-регулятора:")
    print(f"Kp = {Kp:.4f}")
    print(f"Ki = {Ki:.4f}")
    print(f"Kd = {Kd:.4f}")

if __name__ == "__main__":
    main()

#4 / 1 6 11 6
# 20
# 2.2
# 50
# 5

# 4 / 43.94 54.08 16.9 1
# 25
# 2.5
# 40
# 0.65