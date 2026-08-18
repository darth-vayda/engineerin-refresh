# Vibration Monitoring
- data recording is done with my samsung galaxy s20+ via phybox
- 
def import_data
    Erzeuge leeres Dictionary
    Für jede ZIP-Datei:
        Öffne das Archiv
        Öffne die CSV
        Lies sie als DataFrame
        Speichere sie im Dictionary
    Gib das Dictionary zurück


def plot_data
Reihenfolge:
    Messung auswählen  
    Zeitbereich plotten  
    Abtastrate aus Zeitdifferenzen bestimmen  
    FFT bzw. Leistungsspektrum berechnen  
    Frequenzbereich plotten  
    Frequenzspitzen je Lüfterstufe vergleichen


Als Nächstes:
    Wähle aus jeder Messung einen stabilen Zeitabschnitt ohne Start/Stop.
    Entferne den Gleichanteil jeder Achse, also den Mittelwert. Sonst erscheint bei der FFT künstlich viel Energie bei 0 Hz.
    Bestimme aus der Zeitspalte die Abtastrate.
    Berechne und plotte das Frequenzspektrum zuerst für eine Achse.
    Vergleiche die dominanten Frequenzspitzen zwischen den Lüfterstufen.