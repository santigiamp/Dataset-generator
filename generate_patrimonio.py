import pandas as pd
import numpy as np
from ctgan import CTGAN
import datetime

# Configuración de semilla para reproducibilidad
np.random.seed(42)

def generate_activos_base():
    """Genera una tabla base de activos para referencia"""
    n_activos = 100
    tipos_activo = ['Maquinaria', 'Vehiculos', 'Equipos_Informaticos', 'Mobiliario']
    
    # Fechas de adquisición distribuidas en los últimos 3 años
    start_date = datetime.datetime(2022, 1, 1)
    end_date = datetime.datetime(2024, 12, 31)
    days_range = (end_date - start_date).days
    
    activos = pd.DataFrame({
        'id_activo': range(1, n_activos + 1),
        'tipo_activo': np.random.choice(tipos_activo, n_activos),
        'fecha_adquisicion': [
            start_date + datetime.timedelta(days=np.random.randint(0, days_range))
            for _ in range(n_activos)
        ]
    })
    
    # Asignar vida útil según tipo de activo
    vida_util_map = {
        'Maquinaria': 10,
        'Vehiculos': 5,
        'Equipos_Informaticos': 3,
        'Mobiliario': 7
    }
    activos['vida_util_anos'] = activos['tipo_activo'].map(vida_util_map)
    
    return activos

def calculate_depreciation(valor_inicial, fecha_adquisicion, fecha_actual, vida_util_anos):
    """Calcula la depreciación acumulada hasta una fecha específica"""
    anos_transcurridos = (fecha_actual - fecha_adquisicion).days / 365.0
    anos_deprec = min(max(0, anos_transcurridos), vida_util_anos)
    deprec_anual = valor_inicial / vida_util_anos
    return round(deprec_anual * anos_deprec, 2)

def generate_patrimonio_data(activos_df):
    """Genera datos sintéticos para la tabla Patrimonio"""
    registros = []
    
    # Rangos de valores iniciales según tipo de activo (en moneda local)
    rangos_valor = {
        'Maquinaria': (50000, 200000),
        'Vehiculos': (25000, 80000),
        'Equipos_Informaticos': (1000, 5000),
        'Mobiliario': (500, 3000)
    }
    
    anos_fiscales = [2022, 2023, 2024]
    
    for _, activo in activos_df.iterrows():
        # Generar valor inicial realista según tipo de activo
        valor_inicial = round(np.random.uniform(*rangos_valor[activo['tipo_activo']]), 2)
        
        for ano in anos_fiscales:
            fecha_corte = datetime.datetime(ano, 12, 31)
            
            # Solo incluir el activo si ya fue adquirido
            if activo['fecha_adquisicion'] <= fecha_corte:
                deprec_acumulada = calculate_depreciation(
                    valor_inicial,
                    activo['fecha_adquisicion'],
                    fecha_corte,
                    activo['vida_util_anos']
                )
                
                # Asegurar que el valor neto es exactamente valor_inicial - deprec_acumulada
                valor_neto = round(valor_inicial - deprec_acumulada, 2)
                
                registros.append({
                    'id_activo': activo['id_activo'],
                    'ano_fiscal': ano,
                    'valor_inicial': valor_inicial,
                    'depreciacion_acumulada': deprec_acumulada,
                    'valor_neto': valor_neto
                })
    
    return pd.DataFrame(registros)

def validate_patrimonio_data(df):
    """Realiza validaciones sobre los datos generados"""
    validations = {
        'Valores no negativos': (df[['valor_inicial', 'depreciacion_acumulada', 'valor_neto']] >= -0.01).all().all(),
        'Valor neto correcto': (abs(df['valor_inicial'] - df['depreciacion_acumulada'] - df['valor_neto']) < 0.01).all(),
        'Depreciación no mayor al valor inicial': (df['depreciacion_acumulada'] <= df['valor_inicial'] + 0.01).all(),
        'IDs únicos por año': df.groupby('ano_fiscal')['id_activo'].nunique().eq(df.groupby('ano_fiscal')['id_activo'].count()).all(),
        'Depreciación consistente': df.groupby('id_activo')['depreciacion_acumulada'].is_monotonic_increasing.all()
    }
    
    return validations

def print_dataset_summary(df):
    """Imprime un resumen del dataset generado"""
    print("\nResumen del Dataset:")
    print(f"Total de registros: {len(df)}")
    print(f"Años fiscales incluidos: {sorted(df['ano_fiscal'].unique())}")
    print("\nEstadísticas por año fiscal:")
    
    for ano in sorted(df['ano_fiscal'].unique()):
        df_ano = df[df['ano_fiscal'] == ano]
        print(f"\nAño {ano}:")
        print(f"Cantidad de activos: {len(df_ano)}")
        print(f"Valor total inicial: {df_ano['valor_inicial'].sum():,.2f}")
        print(f"Depreciación total: {df_ano['depreciacion_acumulada'].sum():,.2f}")
        print(f"Valor neto total: {df_ano['valor_neto'].sum():,.2f}")
        
        # Mostrar distribución por tipo de activo
        activos_df = activos[activos['id_activo'].isin(df_ano['id_activo'])]
        print("\nDistribución por tipo de activo:")
        print(activos_df['tipo_activo'].value_counts())

def main():
    global activos  # Para poder acceder en print_dataset_summary
    # Generar datos base de activos
    activos = generate_activos_base()
    
    # Generar datos de patrimonio
    patrimonio = generate_patrimonio_data(activos)
    
    # Validar datos
    validations = validate_patrimonio_data(patrimonio)
    print("\nValidaciones:")
    for validation, result in validations.items():
        print(f"{validation}: {'✓' if result else '✗'}")
    
    # Mostrar resumen del dataset
    print_dataset_summary(patrimonio)
    
    # Guardar datos
    patrimonio.to_csv('patrimonio_dataset.csv', index=False, encoding='utf-8')
    print("\nDataset generado y guardado en 'patrimonio_dataset.csv'")

if __name__ == "__main__":
    main()
