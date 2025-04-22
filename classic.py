import numpy as np
import control as ctrl
import matplotlib.pyplot as plt

def has_sustained_oscillations(system, t_max=1000, min_cycles=10, tolerance=0.1):
    t = np.linspace(0, t_max, 10000)
    t, y = ctrl.step_response(system, t)
    y -= np.mean(y)  # Центрирование сигнала
    
    param1 = True
    param2 = True
    param3 = True

    zero_crossings = np.where(np.diff(np.sign(y)))[0]
    if len(zero_crossings) < 2 * (min_cycles + 1):
        param1 = False

    # Извлекаем времена нулевых переходов (половинки периода)
    crossing_times = t[zero_crossings]
    full_periods = crossing_times[::2]  # каждый второй crossing (полный цикл)
    if len(full_periods) < min_cycles + 1:
        param2 =  False

    # Расчёт последних N периодов
    periods = np.diff(full_periods[-(min_cycles + 1):])
    avg_period = np.mean(periods)
    # max_period_dev = np.max(np.abs(periods - avg_period)) / avg_period

    # Анализ амплитуды пиков
    peaks = []
    for i in range(1, len(zero_crossings) - 1, 2):  # ищем пики между переходами
        seg = y[zero_crossings[i]:zero_crossings[i + 1]]
        if len(seg) == 0:
            continue
        peaks.append(np.max(np.abs(seg)))

    dev = peaks[0]-peaks[-1]
    
    if len(peaks) < min_cycles:
        param3 = False
    # last_peaks = peaks[-min_cycles:]
    # avg_amp = np.mean(last_peaks)
    # max_amp_dev = np.max(np.abs(last_peaks - avg_amp)) / avg_amp

    # Условия устойчивых автоколебаний
    # if max_period_dev < tolerance and max_amp_dev < tolerance:
    param = param1 and param2 and param3
    return dev, avg_period, param
    # return False, None


def find_critical_gain(system, k_low=0.1, k_high=100.0, tolerance=6, max_iter=50):
    print("Поиск критического коэффициента усиления методом бинарного поиска...")

    best_k = None
    best_period = None

    for _ in range(max_iter):
        k_mid = (k_low + k_high) / 2
        closed_loop = ctrl.feedback(k_mid * system, 1)
        dev, period, param = has_sustained_oscillations(closed_loop)
        
        if dev > 0:
            k_low = k_mid  # ищем больший k
        else:
            k_high = k_mid  # ищем меньший k
            
        best_k = k_mid
        best_period = period

        if abs(dev) < 1/(10**tolerance) and param:
            break

    return round(best_k, tolerance), best_period

def calculate_pid(k_critical, period):
    k_p = 0.6 * k_critical
    k_i = 1.2 * k_critical / period
    k_d = 0.075 * k_critical * period
    return k_p, k_i, k_d

def main():
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

    system = ctrl.TransferFunction(num, den)

    k_critical, period = find_critical_gain(system)
    if k_critical is None or period is None:
        print("Не удалось определить границу устойчивости.")
        return

    print(f"\nКритический коэффициент усиления k_кр: {k_critical}")
    print(f"Период автоколебаний T: {period:.4f}")

    k_p, k_i, k_d = calculate_pid(k_critical, period)
    print("\nРассчитанные коэффициенты PID-регулятора:")
    print(f"Kp = {k_p:.4f}")
    print(f"Ki = {k_i:.4f}")
    print(f"Kd = {k_d:.4f}")

if __name__ == "__main__":
    main()
    
# 4 / 43.94 54.08 16.9 1
# 1 15 90 270 405 243