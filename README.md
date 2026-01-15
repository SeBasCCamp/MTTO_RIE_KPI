## Requisitos
- Python 3.10 o superior

---

## Instalación (Windows)
## Crear y activar entorno virtual:

```bash
python -m venv venv
venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Generacion de KPIs y alertas
jupyter notebook

# Abrir y correr
notebooks/Kpis_mtto.ipynb

/* Los resultados se guardan en: data/procesados/
  Archivos generados:
  kpis_por_equipo.csv
  alerta_dm_bajo.csv
  alerta_confiabilidad_baja.csv
  alerta_paradas_altas.csv
  alerta_preventivos_no_ejecutados.csv */

# Ejecutar dashboard
streamlit run dashboard/app.py

