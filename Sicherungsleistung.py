print("Welche Sicherungsleistung brauchst du? Gib dafür Netzspannung und Leistung ein")

U = float(input("Netzspannung [V]: "))
P = float(input("Leistung [W]: "))

I = P/U
print(f"Berechneter Strom: {I:.2f} A")

if I < 10:
    print("Empfohlene Sicherung: 10 A")
elif I < 16:
   print("Empfohlene Sicherung: 16 A")
elif I < 20:
   print("Empfohlene Sicherung: 20 A")
elif I < 25:
   print("Empfohlene Sicherung: 25 A")
else:
   print("Empfohlene Sicherung muss größer als 25 A sein.")