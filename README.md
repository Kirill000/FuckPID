# PID Tuning Methods (Python CLI)

This repository contains Python console applications for tuning PID controllers using three different engineering methods:

1. **Classical Method**
2. **Wished Denominator Method**
3. **Cut-off Frequency Method**

---

## 📦 Installation

Clone the repository:

```bash
git clone https://github.com/Kirill000/PID4U.git
cd PID4U
```

Install required packages (if needed):

```bash
pip install numpy
pip install sympy
```

---

## 🧪 1. Classical Method

This is the most basic method using standard forms of second-order system response and time-domain performance specifications.

### ▶️ Run:

```bash
python classic.py
```

### 📥 Input:
- Desired settling time
- Overshoot or damping ratio
- Plant transfer function (numerator and denominator)

---

## 🧮 2. Wished Denominator Method

This method allows you to define a desired characteristic polynomial (closed-loop poles) and compute PID gains to match it.

### ▶️ Run:

```bash
python Dwish.py
```

### 📥 Input format:
```plaintext
Введите передаточную функцию объекта управления.
Формат: числитель и знаменатель через пробел. Пример: 1 3 2 / 1 2 1
```

### 🔍 Features:
- Computes PID gains based on the comparison of desired and actual characteristic polynomials.
- Uses symbolic pole placement strategy.

---

## 🔊 3. Cut-off Frequency Method

This frequency-domain based method computes PID parameters using the desired cut-off frequency (ωc) and phase margin.

### ▶️ Run:

```bash
python cut_frequency.py
```

### 📥 Input format:
```plaintext
TF: 3 / 1 5 6 0   # equivalent to 3 / (s*(s+2)*(s+3))
ε (epsilon):      # Desired steady-state error
Δφ (phase margin):# Desired phase margin in degrees
```

### 🧠 Principle:
- Calculates the gain and phase at the desired ωc
- Matches required magnitude and phase with PID compensator
- Derives Kp, Ki, Kd from trigonometric identities

---

## 📈 Future Plans

- Add support for Ziegler-Nichols and Cohen-Coon tuning
- GUI version with Bode/Root-Locus plots
- Auto-validation using `scipy.signal` simulation

---

## 🤝 Contributing

Feel free to fork and submit pull requests. Issues and suggestions are always welcome.

---

## 📜 License

This project is licensed under the MIT License.
