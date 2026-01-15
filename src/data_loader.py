import pandas as pd
from src.config import DATA_RAW

def load_rie():
    return pd.read_excel(
        DATA_RAW / "1. RIE OC1.xlsx",
        sheet_name="RIE"
    )

def load_horometros():
    return pd.read_excel(
        DATA_RAW / "1. RIE OC1.xlsx",
        sheet_name="HOROMETROS"
    )

def load_concreto():
    return pd.read_excel(
        DATA_RAW / "CASO ESTUDIO 1_Minera La Poderosa_2.xlsx"
    )
