
"""
Streamlit-App: Altwagen / Offroad-Rennen Manager (einfach)
- Erlaubt Hinzufügen von Fahrern/Teams/Fahrzeugen
- Definieren von PS-Klassen
- Automatische Klassenzuordnung
- Eintragen der gefahrenen Runden
- Automatische Auswertung (Rangliste pro Rennen+Klasse)

Starten: streamlit run app.py
"""
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Altwagen Rennen Manager", layout="wide")

@st.cache_data
def init_data():
    fahrer = pd.DataFrame(columns=["Team","Fahrer","Fahrzeug","PS","Rennen","PS-Klasse","Gefahrene Runden"])
    klassen = pd.DataFrame({"PS min":[0,100,150,200],"PS max":[99,149,199,999],"Klasse":["A","B","C","D"]})
    return fahrer, klassen

if "fahrer" not in st.session_state:
    st.session_state.fahrer, st.session_state.klassen = init_data()

st.title("Altwagen / Offroad-Rennen Manager (einfach)")

col1, col2 = st.columns([2,1])

with col1:
    st.header("Fahrer & Fahrzeuge")
    with st.form("add_fahrer"):
        team = st.text_input("Team")
        fahrer_name = st.text_input("Fahrer")
        fahrzeug = st.text_input("Fahrzeug")
        ps = st.number_input("PS", min_value=0, step=1, value=100)
        rennen = st.text_input("Rennen (Name)")
        gerundet = st.number_input("Gefahrene Runden", min_value=0, step=1, value=0)
        submitted = st.form_submit_button("Eintragen")
        if submitted:
            new = {"Team": team, "Fahrer": fahrer_name, "Fahrzeug": fahrzeug, "PS": ps, "Rennen": rennen, "PS-Klasse": "", "Gefahrene Runden": gerundet}
            st.session_state.fahrer = pd.concat([st.session_state.fahrer, pd.DataFrame([new])], ignore_index=True)
            st.success("Fahrer eingetragen.")

    st.markdown("**Aktuelle Fahrerliste (kann inline editiert werden)**")
    edited = st.data_editor(st.session_state.fahrer, num_rows="dynamic")
    # Save back edits
    st.session_state.fahrer = edited

with col2:
    st.header("PS-Klassen")
    st.markdown("Definiere hier Bereiche -> Klasse")
    kl = st.session_state.klassen
    edited_k = st.data_editor(kl, num_rows="dynamic")
    st.session_state.klassen = edited_k

st.markdown("---")
st.header("Aktionen")
colA, colB, colC = st.columns(3)

with colA:
    if st.button("PS-Klassen automatisch zuordnen"):
        def assign_class(ps, kl_df):
            for _, row in kl_df.iterrows():
                if ps >= row["PS min"] and ps <= row["PS max"]:
                    return row["Klasse"]
            return ""
        st.session_state.fahrer["PS-Klasse"] = st.session_state.fahrer["PS"].apply(lambda x: assign_class(x, st.session_state.klassen))
        st.success("PS-Klassen zugeordnet.")

with colB:
    if st.button("Auswertung erstellen"):
        df = st.session_state.fahrer.copy()
        df["Gefahrene Runden"] = pd.to_numeric(df["Gefahrene Runden"], errors="coerce").fillna(0).astype(int)
        # nur Einträge mit Rennen und Klasse
        df = df[df["Rennen"].str.len() > 0]
        df = df[df["PS-Klasse"].str.len() > 0]
        groups = df.groupby(["Rennen","PS-Klasse"])
        result = []
        for (rennen, klasse), g in groups:
            g_sorted = g.sort_values(by="Gefahrene Runden", ascending=False).reset_index(drop=True)
            for i, r in g_sorted.iterrows():
                result.append({"Rennen": rennen, "Klasse": klasse, "Platz": i+1, "Fahrer": r["Fahrer"], "Team": r["Team"], "Fahrzeug": r["Fahrzeug"], "Runden": int(r["Gefahrene Runden"])})
        res_df = pd.DataFrame(result)
        st.session_state.auswertung = res_df
        st.success("Auswertung erstellt und im Arbeitsbereich verfügbar.")

with colC:
    if st.button("Auswertung zurücksetzen"):
        if "auswertung" in st.session_state:
            del st.session_state["auswertung"]
        st.info("Auswertung entfernt.")

st.markdown("---")
st.header("Auswertung / Rangliste")
if "auswertung" in st.session_state and not st.session_state.auswertung.empty:
    st.dataframe(st.session_state.auswertung)
    st.download_button("Auswertung als CSV herunterladen", st.session_state.auswertung.to_csv(index=False).encode("utf-8"), file_name="auswertung.csv", mime="text/csv")
else:
    st.info("Keine Auswertung vorhanden. Erstelle zuerst eine Auswertung (Button oben).")

st.markdown("---")
st.header("Daten exportieren / importieren")
colx, coly = st.columns(2)
with colx:
    if st.button("Export: Fahrer als CSV"):
        st.download_button("Download Fahrer CSV", st.session_state.fahrer.to_csv(index=False).encode("utf-8"), file_name="fahrer.csv", mime="text/csv")
with coly:
    uploaded = st.file_uploader("Import: Fahrer CSV (ersetzt aktuelle Liste)", type=["csv"])
    if uploaded is not None:
        df_up = pd.read_csv(uploaded)
        st.session_state.fahrer = df_up
        st.success("Fahrerliste importiert.")
