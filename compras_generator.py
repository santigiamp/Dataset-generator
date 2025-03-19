import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_compras(productos_df, num_compras=500):
    """
    Generate a synthetic dataset of inventory purchases with realistic attributes.
    
    Args:
        productos_df: DataFrame containing product information
        num_compras: Number of purchase transactions to generate
        
    Returns:
        DataFrame: A pandas DataFrame containing purchase information
    """
    # Define date range for the simulation (4 years)
    start_date = datetime.strptime('2020-01-01', '%Y-%m-%d')
    end_date = datetime.strptime('2023-12-31', '%Y-%m-%d')
    days_range = (end_date - start_date).days
    
    # Initialize data lists
    data = {
        'ID_Compra': list(range(1, num_compras + 1)),
        'ID_Producto': [],
        'Fecha_Compra': [],
        'Cantidad_Adquirida': [],
        'Costo_Unitario': [],
        'Costo_Total_Compra': []
    }
    
    # Generate data for each purchase
    for _ in range(num_compras):
        # Generate random date within the simulation period
        random_days = np.random.randint(0, days_range)
        fecha_compra = (start_date + timedelta(days=random_days)).strftime('%Y-%m-%d')
        
        # Select random product
        id_producto = np.random.choice(productos_df['ID_Producto'])
        
        # Get product cost and category
        producto_row = productos_df[productos_df['ID_Producto'] == id_producto].iloc[0]
        costo_variable_unitario = producto_row['Costo_Variable_Unitario']
        
        # Generate random quantity based on product cost
        if costo_variable_unitario > 1000:  # Productos caros (electrónica)
            cantidad = np.random.randint(5, 30)
            # Mayor descuento en productos caros
            descuento = np.random.uniform(0.05, 0.15) if cantidad > 15 else np.random.uniform(0.03, 0.08)
        elif costo_variable_unitario > 200:  # Productos de precio medio (hogar)
            cantidad = np.random.randint(15, 80)
            descuento = np.random.uniform(0.04, 0.12) if cantidad > 40 else np.random.uniform(0.02, 0.06)
        else:  # Productos más económicos
            cantidad = np.random.randint(30, 250)
            descuento = np.random.uniform(0.03, 0.10) if cantidad > 100 else np.random.uniform(0.02, 0.05)
        
        # Aplicar descuento al costo unitario
        costo_unitario = costo_variable_unitario * (1 - descuento)
        
        # Calculate total purchase cost
        costo_total = cantidad * costo_unitario
        
        # Add data to lists
        data['ID_Producto'].append(id_producto)
        data['Fecha_Compra'].append(fecha_compra)
        data['Cantidad_Adquirida'].append(cantidad)
        data['Costo_Unitario'].append(round(costo_unitario, 2))
        data['Costo_Total_Compra'].append(round(costo_total, 2))
    
    # Create DataFrame
    df = pd.DataFrame(data)
    
    # Sort by date
    df = df.sort_values('Fecha_Compra')
    
    # Reset index
    df = df.reset_index(drop=True)
    
    # Return the DataFrame with columns in the correct order
    return df[['ID_Compra', 'ID_Producto', 'Fecha_Compra', 
              'Cantidad_Adquirida', 'Costo_Unitario', 'Costo_Total_Compra']]