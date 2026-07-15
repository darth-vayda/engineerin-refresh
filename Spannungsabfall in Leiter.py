RHO = float(0.0178)

L = float(input("Leitungslänge [m]: "))
A = float(input("Querschnitt [mm^2]: "))
I = float(input("Strom [A]: "))
Unetz = float(230)

R = RHO * L/A
U = R*I
UProzent = U/Unetz * 100

print(f"Der Leitungswiderstand beträgt {R:.2f} Ohm")
print(f"Der Spannungsabfall ist {U:.2f} V")

if U<3:
    print("Das ist im sehr guten Bereich")
elif U<5:
    print("Das ist noch akzeptabel")
else:
    print("Leitung zu lang oder Querschnitt zu klein")

print(f"Das sind {UProzent:.4f} % der Netzspannung")