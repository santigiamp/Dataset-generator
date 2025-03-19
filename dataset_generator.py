import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os
import random

# Set random seeds for reproducibility
np.random.seed(42)
random.seed(42)

# Define constants
START_DATE = '2020-01-01'  # Start of 4-year simulation
END_DATE = '2023-12-31'    # End of 4-year simulation
OUTPUT_DIR = 'generated_data'

# Create output directory if it doesn't exist
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

# Helper functions
def generate_dates(start_date, end_date):
    """Generate a list of dates between start_date and end_date"""
    start = datetime.strptime(start_date, '%Y-%m-%d')
    end = datetime.strptime(end_date, '%Y-%m-%d')
    date_list = [start + timedelta(days=x) for x in range((end - start).days + 1)]
    return [date.strftime('%Y-%m-%d') for date in date_list]

def save_to_csv(df, filename):
    """Save DataFrame to CSV with UTF-8 encoding"""
    filepath = os.path.join(OUTPUT_DIR, filename)
    df.to_csv(filepath, index=False, encoding='utf-8')
    print(f"Saved {filename} with {len(df)} records")

# Main function to generate all datasets
def generate_datasets():
    # Generate each dataset
    plan_cuentas_df = generate_plan_cuentas()
    save_to_csv(plan_cuentas_df, 'plan_cuentas.csv')
    
    clientes_df = generate_clientes()
    save_to_csv(clientes_df, 'clientes.csv')
    
    productos_df = generate_productos()
    save_to_csv(productos_df, 'productos.csv')
    
    activos_df = generate_activos()
    save_to_csv(activos_df, 'activos.csv')
    
    cuentas_bancarias_df = generate_cuentas_bancarias()
    save_to_csv(cuentas_bancarias_df, 'cuentas_bancarias.csv')
    
    # Generate time-dependent datasets
    ventas_df = generate_ventas(clientes_df, productos_df)
    save_to_csv(ventas_df, 'ventas.csv')
    
    compras_df = generate_compras(productos_df)
    save_to_csv(compras_df, 'compras.csv')
    
    movimientos_bancarios_df = generate_movimientos_bancarios(cuentas_bancarias_df, ventas_df, compras_df)
    save_to_csv(movimientos_bancarios_df, 'movimientos_bancarios.csv')
    
    libro_diario_df = generate_libro_diario(plan_cuentas_df, ventas_df, compras_df, movimientos_bancarios_df, productos_df)
    save_to_csv(libro_diario_df, 'libro_diario.csv')
    
    libro_mayor_df = generate_libro_mayor(plan_cuentas_df, libro_diario_df)
    save_to_csv(libro_mayor_df, 'libro_mayor.csv')
    
    print("Dataset generation complete!")

# Import individual dataset generation functions
from plan_cuentas_generator import generate_plan_cuentas
from clientes_generator import generate_clientes
from productos_generator import generate_productos
from activos_generator import generate_activos
from cuentas_bancarias_generator import generate_cuentas_bancarias
from ventas_generator import generate_ventas
from compras_generator import generate_compras
from movimientos_bancarios_generator import generate_movimientos_bancarios
from libro_diario_generator import generate_libro_diario
from libro_mayor_generator import generate_libro_mayor

# Run the generator
if __name__ == "__main__":
    generate_datasets()