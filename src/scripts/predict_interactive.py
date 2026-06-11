#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
predict_interactive.py — Script interactivo de predicción para modelos de severidad de COVID-19.

Este script permite al usuario ingresar datos clínicos de un paciente a través de un
cuestionario en terminal o cargar un payload JSON, para luego realizar predicciones de
severidad clínica utilizando los modelos entrenados (Decision Tree, Random Forest y XGBoost).

Uso:
    python src/scripts/predict_interactive.py
    python src/scripts/predict_interactive.py --input data/paciente.json
    python src/scripts/predict_interactive.py --output data/paciente.json
"""

import sys
import argparse
import json
import urllib.request
from pathlib import Path
import pandas as pd
import numpy as np
import joblib

# Añadir la raíz del proyecto al sys.path para poder importar módulos de src
project_root = Path(__file__).resolve().parents[2]
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))

from src.utils.constants import MODELS_PATH, SEVERIDAD_MAP, COLS_COMORBILIDADES

# Nombres de archivos de modelos
MODEL_FILENAMES = [
    "decision_tree.joblib",
    "random_forest.joblib",
    "xgboost_model.joblib",
    "features.joblib",
    "preprocessor.joblib"
]

def asegurar_modelos():
    """Valida la existencia de los archivos de modelos y los descarga si faltan."""
    MODELS_PATH.mkdir(parents=True, exist_ok=True)
    url_file = MODELS_PATH / "url.txt"
    
    if not url_file.exists():
        # Fallback si no existe el archivo url.txt
        base_url = "https://huggingface.co/datasets/toporaku/covid19-mx-models/resolve/main/"
        print(f"\033[33mAdvertencia: {url_file} no existe. Usando URL base por defecto.\033[0m")
    else:
        with open(url_file, "r") as f:
            base_url = f.read().strip()
            if not base_url.endswith("/"):
                base_url += "/"

    print("\033[34m[1/3] Verificando archivos de modelos...\033[0m")
    for filename in MODEL_FILENAMES:
        file_path = MODELS_PATH / filename
        if not file_path.exists():
            download_url = f"{base_url}{filename}"
            print(f"  -> Descargando {filename} desde Hugging Face...")
            try:
                urllib.request.urlretrieve(download_url, file_path)
                print(f"  \033[32m✓ Descargado con éxito: {file_path.name}\033[0m")
            except Exception as e:
                print(f"  \033[31m✗ Error al descargar {filename}: {e}\033[0m")
                sys.exit(1)
        else:
            print(f"  \033[32m✓ Encontrado: {filename}\033[0m")

def cargar_modelos():
    """Carga los modelos y el preprocesador serializados."""
    print("\033[34m[2/3] Cargando modelos en memoria...\033[0m")
    try:
        modelo_dt = joblib.load(MODELS_PATH / "decision_tree.joblib")
        modelo_rf = joblib.load(MODELS_PATH / "random_forest.joblib")
        modelo_xgb = joblib.load(MODELS_PATH / "xgboost_model.joblib")
        features = joblib.load(MODELS_PATH / "features.joblib")
        preprocessor = joblib.load(MODELS_PATH / "preprocessor.joblib")
        print("\033[32m✓ Todos los modelos y features se cargaron correctamente.\033[0m")
        return {
            "Decision Tree": modelo_dt,
            "Random Forest": modelo_rf,
            "XGBoost": modelo_xgb,
            "features": features,
            "preprocessor": preprocessor
        }
    except Exception as e:
        print(f"\033[31m✗ Error al cargar los modelos: {e}\033[0m")
        sys.exit(1)

def solicitar_input_consola():
    """Muestra un cuestionario interactivo en español para el ingreso de datos del paciente."""
    print("\n" + "="*60)
    print("      CUESTIONARIO INTERACTIVO DE PACIENTE COVID-19/FLU      ")
    print("="*60)
    print("Ingrese los datos solicitados. Presione Enter para aceptar el valor por defecto [entre corchetes].")
    
    paciente_raw = {}
    
    # 1. EDAD
    while True:
        edad_str = input("\n👉 Edad del paciente (0-120) [45]: ").strip()
        if not edad_str:
            paciente_raw["EDAD"] = 45
            break
        try:
            edad = int(edad_str)
            if 0 <= edad <= 120:
                paciente_raw["EDAD"] = edad
                break
            print("\033[31mPor favor, ingrese una edad válida entre 0 y 120.\033[0m")
        except ValueError:
            print("\033[31mPor favor, ingrese un número entero.\033[0m")

    # 2. SEXO
    while True:
        sexo_str = input("👉 Sexo (1 = Mujer, 2 = Hombre) [2]: ").strip()
        if not sexo_str:
            paciente_raw["SEXO"] = 2
            break
        if sexo_str in ["1", "2"]:
            paciente_raw["SEXO"] = int(sexo_str)
            break
        print("\033[31mPor favor, ingrese 1 (Mujer) o 2 (Hombre).\033[0m")

    # 3. NEUMONIA
    while True:
        neumonia_str = input("👉 ¿Tiene neumonía? (1 = Sí, 2 = No) [2]: ").strip()
        if not neumonia_str:
            paciente_raw["NEUMONIA"] = 2
            break
        if neumonia_str in ["1", "2"]:
            paciente_raw["NEUMONIA"] = int(neumonia_str)
            break
        print("\033[31mPor favor, ingrese 1 o 2.\033[0m")

    # 4. Comorbilidades
    print("\n--- Comorbilidades (1 = Sí, 2 = No) ---")
    for com in COLS_COMORBILIDADES:
        while True:
            val_str = input(f"👉 ¿Tiene {com.replace('_', ' ').title()}? (1=Sí, 2=No) [2]: ").strip()
            if not val_str:
                paciente_raw[com] = 2
                break
            if val_str in ["1", "2"]:
                paciente_raw[com] = int(val_str)
                break
            print("\033[31mPor favor, ingrese 1 o 2.\033[0m")

    # 5. Datos adicionales y diagnósticos con defaults
    print("\n--- Detalles Diagnósticos y Administrativos (Valores por Defecto Recomendados) ---")
    
    # COVID confirmado por defecto
    covid_str = input("👉 Clasificación COVID (1-3: Confirmado, 5: Negativo, 6: Sospechoso) [3]: ").strip()
    paciente_raw["CLASIFICACION_FINAL_COVID"] = int(covid_str) if covid_str else 3
    
    # Flu negativo por defecto
    flu_str = input("👉 Clasificación Influenza (1-3: Confirmado, 5: Negativo) [5]: ").strip()
    paciente_raw["CLASIFICACION_FINAL_FLU"] = int(flu_str) if flu_str else 5

    # PCR positivo por defecto si COVID confirmado
    pcr_str = input("👉 Resultado PCR (1: Positivo, 2: Negativo, 97: No aplica) [1]: ").strip()
    paciente_raw["RESULTADO_PCR"] = int(pcr_str) if pcr_str else 1
    
    # Resto de campos con defaults automáticos
    paciente_raw["RESULTADO_PCR_COINFECCION"] = 0
    paciente_raw["TOMA_MUESTRA_LAB"] = 1
    paciente_raw["TOMA_MUESTRA_ANTIGENO"] = 0
    paciente_raw["OTRO_CASO"] = 1  # Sí tuvo contacto
    paciente_raw["MIGRANTE"] = 2   # No
    paciente_raw["NACIONALIDAD"] = 1 # Mexicano
    paciente_raw["SECTOR"] = 4     # IMSS
    paciente_raw["ENTIDAD_UM"] = 9 # CDMX
    paciente_raw["ENTIDAD_NAC"] = 9
    paciente_raw["ENTIDAD_RES"] = 9
    paciente_raw["MUNICIPIO_RES"] = 2
    paciente_raw["HABLA_LENGUA_INDIG"] = 2
    paciente_raw["INDIGENA"] = 2
    
    # EMBARAZO por defecto 2 (No)
    if paciente_raw["SEXO"] == 1:
        emb_str = input("👉 ¿Está embarazada? (1 = Sí, 2 = No) [2]: ").strip()
        paciente_raw["EMBARAZO"] = int(emb_str) if emb_str else 2
    else:
        paciente_raw["EMBARAZO"] = 2  # No aplica / No
        
    return paciente_raw

def preprocesar_paciente(paciente_raw, preprocessor, features):
    """Aplica los mapeos y el escalador a los datos crudos del paciente."""
    df_raw = pd.DataFrame([paciente_raw])
    
    # 1. Copiar df para transformaciones
    df_mapped = df_raw.copy()
    
    # 2. Codificar comorbilidades + variables clínicas (1=Sí->1, 2=No->0)
    binary_si_no = COLS_COMORBILIDADES + [
        "NEUMONIA", "TOMA_MUESTRA_LAB", "EMBARAZO", "HABLA_LENGUA_INDIG", 
        "INDIGENA", "MIGRANTE", "OTRO_CASO", "NACIONALIDAD",
    ]
    for col in binary_si_no:
        if col in df_mapped.columns:
            df_mapped[col] = df_mapped[col].map({1: 1, 2: 0})
            
    # 3. SEXO: 1=Mujer->0, 2=Hombre->1
    if "SEXO" in df_mapped.columns:
        df_mapped["SEXO"] = df_mapped["SEXO"].map({1: 0, 2: 1})
        
    # 4. TOMA_MUESTRA_ANTIGENO (binaria)
    if "TOMA_MUESTRA_ANTIGENO" in df_mapped.columns:
        df_mapped["TOMA_MUESTRA_ANTIGENO"] = df_mapped["TOMA_MUESTRA_ANTIGENO"].map({1: 1, 2: 0})
        
    # 5. Escalar EDAD
    scaler = preprocessor._edad_scaler
    df_mapped["EDAD_SCALED"] = scaler.transform(df_mapped[["EDAD"]]).flatten()
    
    # 6. Seleccionar y ordenar las columnas del modelo
    df_demo = df_mapped[features]
    return df_demo

def dibujar_barra(probabilidad, ancho=20):
    """Genera una barra visual de carga para las probabilidades."""
    bloques = int(round(probabilidad * ancho))
    return "[" + "█" * bloques + "░" * (ancho - bloques) + f"] {probabilidad:.2%}"

def mostrar_predicciones(df_paciente, modelos, paciente_raw):
    """Ejecuta las inferencias y dibuja los resultados de severidad."""
    print("\n" + "="*80)
    print("                    RESULTADOS DE PREDICCIÓN CLÍNICA                    ")
    print("="*80)
    print(f"Paciente: Edad {paciente_raw['EDAD']} años | Sexo: {'Hombre' if paciente_raw['SEXO'] == 2 else 'Mujer'}")
    print(f"Síntomas principales: Neumonía: {'Sí' if paciente_raw['NEUMONIA'] == 1 else 'No'}")
    comorbilidades_activas = [c.replace('_', ' ').title() for c in COLS_COMORBILIDADES if paciente_raw[c] == 1]
    print(f"Comorbilidades: {', '.join(comorbilidades_activas) if comorbilidades_activas else 'Ninguna'}")
    print("-"*80)
    
    color_map = {
        0: "\033[32m", # Leve - Verde
        1: "\033[33m", # Grave - Amarillo
        2: "\033[35m", # Crítico - Magenta/Naranja
        3: "\033[31m"  # Fallecido - Rojo
    }
    reset = "\033[0m"

    for name in ["Decision Tree", "Random Forest", "XGBoost"]:
        model = modelos[name]
        pred = model.predict(df_paciente)[0]
        probs = model.predict_proba(df_paciente)[0]
        
        nivel = int(pred)
        etiqueta = SEVERIDAD_MAP[nivel]
        color = color_map.get(nivel, "")
        
        print(f"🤖 \033[1mModelo: {name:<15}\033[0m -> Predicción: {color}\033[1m{nivel} ({etiqueta}){reset}")
        print("   Probabilidades por clase:")
        for clase_id, clase_label in SEVERIDAD_MAP.items():
            prob = probs[clase_id]
            color_clase = color_map[clase_id]
            barra = dibujar_barra(prob)
            print(f"     {color_clase}{clase_label:<22}{reset} : {barra}")
        print("-"*80)

def main():
    parser = argparse.ArgumentParser(description="Script interactivo de inferencia COVID-19/Flu.")
    parser.add_argument("--input", type=str, help="Ruta de un archivo JSON con datos del paciente para inferencia directa.")
    parser.add_argument("--output", type=str, help="Ruta para guardar los datos ingresados como un payload JSON.")
    args = parser.parse_args()

    # Asegurar y cargar modelos
    asegurar_modelos()
    modelos = cargar_modelos()
    
    # Obtener datos del paciente
    if args.input:
        input_path = Path(args.input)
        if not input_path.exists():
            print(f"\033[31mError: El archivo de entrada '{input_path}' no existe.\033[0m")
            sys.exit(1)
        print(f"\n\033[34m[3/3] Cargando datos desde {input_path}...\033[0m")
        with open(input_path, "r", encoding="utf-8") as f:
            paciente_raw = json.load(f)
    else:
        paciente_raw = solicitar_input_consola()
        
    # Guardar payload si se solicita
    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(paciente_raw, f, indent=4, ensure_ascii=False)
        print(f"\n\033[32m✓ Payload JSON del paciente guardado en: {output_path}\033[0m")

    # Preprocesar
    df_paciente = preprocesar_paciente(paciente_raw, modelos["preprocessor"], modelos["features"])
    
    # Hacer predicciones
    mostrar_predicciones(df_paciente, modelos, paciente_raw)

if __name__ == "__main__":
    main()
