
Altwagen / Offroad-Rennen - Dateien (erstellt)

Enthalten im Ordner: /mnt/data/altwagen_tool

1) altwagen_rennen_template.xlsx
   - Excel-Vorlage mit den Sheets:
     * Fahrer (Team, Fahrer, Fahrzeug, PS, Rennen, PS-Klasse, Gefahrene Runden)
     * Klassen (PS min, PS max, Klasse)
     * Auswertung (wird von Makro befüllt)
   - Hinweis: Diese .xlsx enthält **kein** eingebettetes Makro. Bitte öffne das nächste File und füge den VBA-Code in Excel (Alt+F11) in ein Modul ein. Danach als .xlsm speichern.

2) vba_macro_code.txt
   - VBA-Makrocode (Sub AuswertungErstellen), kopieren & in Excel einfügen (Modul).
   - Danach: Speichern als .xlsm, Makros aktivieren. Mit dem Makro werden PS-Klassen zugeordnet und die Auswertung automatisch erstellt.

3) app.py (Streamlit)
   - Einfaches Web-Interface zum Verwalten (lokal oder remote).
   - Starten: `streamlit run app.py` im Ordner mit dieser Datei.
   - Features: Hinzufügen/ bearbeiten von Fahrern, PS-Klassen definieren, automatische Klassenzuordnung, Runden eintragen, Auswertung erstellen und CSV-Export.

4) requirements.txt
   - Benötigte Python-Pakete: streamlit, pandas, openpyxl

Tipps:
- Wenn du die Excel-Lösung bevorzugst und eine fertige .xlsm brauchst, kann ich das für dich erzeugen (brauche dann Bescheid, ob ich Makros automatisch einbetten soll). Momentan ist aus Sicherheits- und Kompatibilitätsgründen der VBA-Code separat, damit du ihn prüfen kannst.
- Die Streamlit-App läuft lokal; um sie remote verfügbar zu machen, kannst du sie auf einem Server (oder Streamlit Cloud) deployen.

Dateien gespeichert unter: /mnt/data/altwagen_tool

