# print("=== RC-Glied ===")

# R = float(input("Widerstand [Ohm]: "))
# C = float(input("Kapazität [F]: "))

# tau = R * C

# print()
# print(f"Zeitkonstante: {tau:.3f} s")

print("=== Ohmsches Gesetz ===")

U = float(input("Spannung [V]: "))
R = float(input("Widerstand [Ω]: "))

# U = float(220)
# R = float(54)

I = U/R
P = U*I

print(f"Der Strom beträgt {I:.2f} Ampere")
print(f"die Leistung ist {P:.3f} Watt")
print("Der Strom beträgt", I, "Ampere")