import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_ventas(clientes_df, productos_df, num_ventas=1000):
    """
    Generate a synthetic dataset of sales transactions with realistic attributes.
    
    Args:
        clientes_df: DataFrame containing client information
        productos_df: DataFrame containing product information
        num_ventas: Number of sales transactions to generate
        
    Returns:
        DataFrame: A pandas DataFrame containing sales information
    """
    # Define date range for the simulation (4 years)
    start_date = datetime.strptime('2020-01-01', '%Y-%m-%d')
    end_date = datetime.strptime('2023-12-31', '%Y-%m-%d')
    days_range = (end_date - start_date).days
    
    # Initialize data lists
    data = {
        'ID_Venta': list(range(1, num_ventas + 1)),
        'Fecha': [],
        'ID_Cliente': [],
        'ID_Producto': [],
        'Cantidad_Vendida': [],
        'Precio_Unitario': [],
        'Total_Venta': []
    }
    
    # Generate data for each sale
    for _ in range(num_ventas):
        # Generate random date within the simulation period
        random_days = np.random.randint(0, days_range)
        fecha = (start_date + timedelta(days=random_days)).strftime('%Y-%m-%d')
        
        # Select random client and product
        id_cliente = np.random.choice(clientes_df['ID_Cliente'])
        id_producto = np.random.choice(productos_df['ID_Producto'])
        
        # Get product price
        producto_row = productos_df[productos_df['ID_Producto'] == id_producto].iloc[0]
        precio_unitario = producto_row['Precio_Venta_Unitario']
        
        # Generate random quantity based on client category
        cliente_categoria = clientes_df[clientes_df['ID_Cliente'] == id_cliente]['Categoria'].iloc[0]
        if cliente_categoria == 'Minorista':
            cantidad = np.random.randint(1, 10)
        elif cliente_categoria == 'Mayorista':
            cantidad = np.random.randint(10, 50)
        else:  # Corporativo
            cantidad = np.random.randint(50, 200)
        
        # Calculate total sale amount
        total_venta = cantidad * precio_unitario
        
        # Add data to lists
        data['Fecha'].append(fecha)
        data['ID_Cliente'].append(id_cliente)
        data['ID_Producto'].append(id_producto)
        data['Cantidad_Vendida'].append(cantidad)
        data['Precio_Unitario'].append(precio_unitario)
        data['Total_Venta'].append(round(total_venta, 2))
    
    # Create DataFrame
    df = pd.DataFrame(data)
    
    # Sort by date
    df = df.sort_values('Fecha')
    
    # Reset index
    df = df.reset_index(drop=True)
    
    # Return the DataFrame with columns in the correct order
    return df[['ID_Venta', 'Fecha', 'ID_Cliente', 'ID_Producto', 
              'Cantidad_Vendida', 'Precio_Unitario', 'Total_Venta']]