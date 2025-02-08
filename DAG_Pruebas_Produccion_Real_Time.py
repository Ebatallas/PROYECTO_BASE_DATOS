from airflow import DAG
from airflow.operators.python import PythonOperator
import pandas as pd
import numpy as np
import random
import requests
import json
from datetime import datetime, timedelta

# Configuración del DAG
default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2024, 2, 7),
    "catchup": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=1),
}

dag = DAG(
    "pruebas_real_time",
    default_args=default_args,
    description="Genera datos sintéticos de pruebas de producción cada minuto y los envía a Elasticsearch",
    schedule_interval="* * * * *",  # Ejecutar cada minuto
)

# Ruta del archivo CSV (Asegúrate de mapear esta ruta en Docker)
file_path = "/opt/airflow/dags/Historico_de_Pruebas_de_Produccion.csv"

# URL de Elasticsearch
ELASTICSEARCH_URL = "http://elasticsearch:9200/pruebas_produccion/_doc"


def generar_datos_y_enviar():
    try:
        # Cargar datos históricos asegurando conversión correcta de la fecha
        df = pd.read_csv(file_path, dtype=str)  # Forzar lectura como string para limpieza
        df.rename(columns=lambda x: x.strip(), inplace=True)  # Eliminar espacios en columnas

        # Convertir la columna de fecha
        df["Date"] = pd.to_datetime(df["Date"], format="%d/%m/%Y", errors="coerce")  # Asegurar datetime

        # Verificar si hay fechas válidas
        if df["Date"].isnull().all():
            raise ValueError("Error: No se encontraron fechas válidas en el dataset.")

        # Filtrar pozos activos en los últimos 2 meses
        ultimo_mes = df["Date"].max()
        dos_meses_atras = ultimo_mes - pd.DateOffset(months=2)
        pozos_activos = df[df["Date"] >= dos_meses_atras]["Wellbore"].unique()

        # Generar datos sintéticos
        nuevos_datos = []
        for _ in range(10):  # Generar 10 pruebas cada minuto
            pozo = random.choice(pozos_activos)
            campo = df[df["Wellbore"] == pozo]["Field"].iloc[0]
            valores_base = df[df["Wellbore"] == pozo].iloc[-1]  # Últimos valores registrados

            data_entry = {
                "Date": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
                "Wellbore": pozo,
                "Field": campo,
                "BFPD": round(np.random.uniform(0.9, 1.1) * float(valores_base["BFPD"]), 2),
                "BOPD": round(np.random.uniform(0.9, 1.1) * float(valores_base["BOPD"]), 2),
                "BWPD": round(np.random.uniform(0.9, 1.1) * float(valores_base["BWPD"]), 2),
                "MSCF": round(np.random.uniform(0.9, 1.1) * float(valores_base["MSCF"]), 2),
                "BSW": round(np.random.uniform(0.9, 1.1) * float(valores_base["BSW"]), 2),
                "GOR": round(np.random.uniform(0.9, 1.1) * float(valores_base["GOR"]), 2),
                "API": round(np.random.uniform(0.9, 1.1) * float(valores_base["API"]), 2),
                "WHP": round(np.random.uniform(0.9, 1.1) * float(valores_base["WHP"]), 2),
                "PIP": round(np.random.uniform(0.9, 1.1) * float(valores_base["PIP"]), 2),
                "SALIN.": round(np.random.uniform(0.9, 1.1) * float(valores_base["SALIN."]), 2),
            }

            # Enviar datos a Elasticsearch
            headers = {"Content-Type": "application/json"}
            response = requests.post(ELASTICSEARCH_URL, json=data_entry, headers=headers)

            if response.status_code not in [200, 201]:
                raise Exception(f"Error al enviar datos a Elasticsearch: {response.text}")

            nuevos_datos.append(data_entry)

        # Mostrar los datos en logs de Airflow
        print(f"📅 {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} - 10 pruebas enviadas a Elasticsearch:")
        print(pd.DataFrame(nuevos_datos).to_string(index=False))  # Mostrar datos en logs

    except Exception as e:
        print(f"❌ Error en la generación o envío de datos: {str(e)}")
        raise e  # Lanza el error para que Airflow lo registre


# Tarea en Airflow para generar y enviar datos sintéticos cada minuto
generar_pruebas = PythonOperator(
    task_id="generar_y_enviar_datos",
    python_callable=generar_datos_y_enviar,
    dag=dag,
)

generar_pruebas

