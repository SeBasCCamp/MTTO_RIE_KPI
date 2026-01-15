import pandas as pd
import streamlit as st
import plotly.express as px
from pathlib import Path

st.set_page_config(
    page_title="Dashboard de Mantenimiento",
    layout="wide"
)

ROOT = Path(__file__).resolve().parent.parent   # mtto_rie/
DATA_PROCESADOS = ROOT / "data" / "procesados"

base = pd.read_csv(DATA_PROCESADOS / "base_kpis_turno.csv", parse_dates=["FECHA"])
kpis_equipo = pd.read_csv(DATA_PROCESADOS / "kpis_por_equipo.csv")
alerta_dm = pd.read_csv(DATA_PROCESADOS / "alerta_dm_bajo.csv")
alerta_rt = pd.read_csv(DATA_PROCESADOS / "alerta_confiabilidad_baja.csv")
alerta_paradas = pd.read_csv(DATA_PROCESADOS / "alerta_paradas_altas.csv")
alerta_prev = pd.read_csv(DATA_PROCESADOS / "alerta_preventivos_no_ejecutados.csv")

st.title("Dashboard de Mantenimiento")

st.sidebar.header("Filtros")
equipos = sorted(base["COD EQ INC"].dropna().unique().tolist())
equipo_sel = st.sidebar.multiselect("Equipo (COD EQ INC)", equipos, default=equipos[:5])

fecha_min = base["FECHA"].min()
fecha_max = base["FECHA"].max()
rango_fechas = st.sidebar.date_input("Rango de fechas", value=(fecha_min, fecha_max))

df = base.copy()
if equipo_sel:
    df = df[df["COD EQ INC"].isin(equipo_sel)]

if isinstance(rango_fechas, tuple) and len(rango_fechas) == 2:
    ini, fin = pd.to_datetime(rango_fechas[0]), pd.to_datetime(rango_fechas[1])
    df = df[(df["FECHA"] >= ini) & (df["FECHA"] <= fin)]

col1, col2, col3, col4, col5 = st.columns(5)
dm = df["DM"].mean() if "DM" in df else 0
ut = df["UT"].mean() if "UT" in df else 0
mtbf = df["MTBF"].mean() if "MTBF" in df else 0
mttr = df["MTTR"].mean() if "MTTR" in df else 0
rt = df["R_t"].mean() if "R_t" in df else 0

col1.metric("DM (prom)", f"{dm:.2%}")
col2.metric("UT (prom)", f"{ut:.2%}")
col3.metric("MTBF (prom)", f"{mtbf:.2f}")
col4.metric("MTTR (prom)", f"{mttr:.2f}")
col5.metric("R(t) (prom)", f"{rt:.2%}")

st.divider()

def semaforo_dm(x):
    if x <= 0.80: return "🔴 Malo"
    if x <= 0.85: return "🟡 Medio"
    return "🟢 Bueno"

def semaforo_rt(x):
    if x <= 0.50: return "🔴 Malo"
    if x <= 0.71: return "🟡 Medio"
    return "🟢 Bueno"

c1, c2 = st.columns(2)
c1.write(f"**Estado DM:** {semaforo_dm(dm)}")
c2.write(f"**Estado R(t):** {semaforo_rt(rt)}")

st.divider()

st.subheader("Tendencias históricas")

dm_diario = df.groupby("FECHA", as_index=False).agg(DM=("DM", "mean"), UT=("UT", "mean"))
fig1 = px.line(dm_diario, x="FECHA", y="DM", title="DM promedio por día")
st.plotly_chart(fig1, use_container_width=True)

fig2 = px.line(dm_diario, x="FECHA", y="UT", title="UT promedio por día")
st.plotly_chart(fig2, use_container_width=True)

st.divider()

st.subheader("KPIs por equipo (filtrado)")

ranking = (
    df.groupby("COD EQ INC", as_index=False)
    .agg(
        DM=("DM", "mean"),
        UT=("UT", "mean"),
        MTBF=("MTBF", "mean"),
        MTTR=("MTTR", "mean"),
        R_t=("R_t", "mean"),
        PARADAS=("PARADA", "sum"),
        HRS_TRAB=("HRS_TRAB", "sum")
    )
    .sort_values("DM")
)

st.dataframe(ranking, use_container_width=True)

st.divider()

st.subheader("Alertas")
umbral_dm = 0.85
umbral_rt = 0.50

alert_dm = ranking[ranking["DM"] < umbral_dm].sort_values("DM")
alert_rt = ranking[ranking["R_t"] < umbral_rt].sort_values("R_t")
alert_par = ranking[ranking["PARADAS"] >= 100].sort_values("PARADAS", ascending=False)

a1, a2, a3 = st.columns(3)
a1.write("**DM < 0.85**")
a1.dataframe(alert_dm, use_container_width=True)

a2.write("**R(t) < 0.50**")
a2.dataframe(alert_rt, use_container_width=True)

a3.write("**PARADAS >= 100**")
a3.dataframe(alert_par, use_container_width=True)

