import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_movimientos_bancarios(cuentas_bancarias_df, ventas_df, compras_df, num_movimientos_extra=200):
    """
    Generate a synthetic dataset of bank transactions with realistic attributes.
    
    Args:
        cuentas_bancarias_df: DataFrame containing bank account information
        ventas_df: DataFrame containing sales information
        compras_df: DataFrame containing purchase information
        num_movimientos_extra: Number of additional transactions to generate
        
    Returns:
        DataFrame: A pandas DataFrame containing bank transaction information
    """
    # Define date range for the simulation (4 years)
    start_date = datetime.strptime('2020-01-01', '%Y-%m-%d')
    end_date = datetime.strptime('2023-12-31', '%Y-%m-%d')
    days_range = (end_date - start_date).days
    
    # Create transactions based on sales (ingresos)
    movimientos_ventas = []
    for idx, venta in ventas_df.iterrows():
        # Randomly select a bank account (preferring accounts in the same currency)
        cuenta = np.random.choice(cuentas_bancarias_df['ID_Cuenta_Bancaria'])
        
        # Add a small delay for payment (0-15 days)
        fecha_venta = datetime.strptime(venta['Fecha'], '%Y-%m-%d')
        delay_days = np.random.randint(0, 15)
        fecha_pago = (fecha_venta + timedelta(days=delay_days))
        
        # Ensure date is within simulation period
        if fecha_pago > end_date:
            fecha_pago = end_date
        
        movimientos_ventas.append({
            'ID_Movimiento': idx + 1,
            'ID_Cuenta_Bancaria': cuenta,
            'Fecha': fecha_pago.strftime('%Y-%m-%d'),
            'Tipo': 'Ingreso',
            'Monto': venta['Total_Venta'],
            'Concepto': f"Cobro venta #{venta['ID_Venta']}"
        })
    
    # Create transactions based on purchases (egresos)
    movimientos_compras = []
    for idx, compra in compras_df.iterrows():
        # Randomly select a bank account
        cuenta = np.random.choice(cuentas_bancarias_df['ID_Cuenta_Bancaria'])
        
        # Add a small delay for payment (0-30 days)
        fecha_compra = datetime.strptime(compra['Fecha_Compra'], '%Y-%m-%d')
        delay_days = np.random.randint(0, 30)
        fecha_pago = (fecha_compra + timedelta(days=delay_days))
        
        # Ensure date is within simulation period
        if fecha_pago > end_date:
            fecha_pago = end_date
        
        movimientos_compras.append({
            'ID_Movimiento': len(movimientos_ventas) + idx + 1,
            'ID_Cuenta_Bancaria': cuenta,
            'Fecha': fecha_pago.strftime('%Y-%m-%d'),
            'Tipo': 'Egreso',
            'Monto': compra['Costo_Total_Compra'],
            'Concepto': f"Pago compra #{compra['ID_Compra']}"
        })
    
    # Combine sales and purchase transactions
    movimientos_df = pd.DataFrame(movimientos_ventas + movimientos_compras)
    
    # Generate additional transactions
    movimientos_extra = []
    start_id = len(movimientos_df) + 1
    
    for i in range(num_movimientos_extra):
        # Generate random date within the simulation period
        random_days = np.random.randint(0, days_range)
        fecha = (start_date + timedelta(days=random_days)).strftime('%Y-%m-%d')
        
        # Select random bank account
        cuenta = np.random.choice(cuentas_bancarias_df['ID_Cuenta_Bancaria'])
        
        # Determine transaction type
        tipo = np.random.choice(['Ingreso', 'Egreso'], p=[0.4, 0.6])  # More expenses than income
        
        # Generate transaction amount based on type
        if tipo == 'Ingreso':
            monto = np.random.uniform(1000, 50000)
            conceptos = ['Préstamo recibido', 'Devolución impuestos', 'Venta de activo', 'Inversión', 'Otros ingresos']
        else:  # Egreso
            monto = np.random.uniform(500, 30000)
            conceptos = ['Pago nómina', 'Servicios', 'Impuestos', 'Seguros', 'Mantenimiento', 'Alquiler', 'Otros gastos']
        
        concepto = np.random.choice(conceptos)
        
        movimientos_extra.append({
            'ID_Movimiento': start_id + i,
            'ID_Cuenta_Bancaria': cuenta,
            'Fecha': fecha,
            'Tipo': tipo,
            'Monto': round(monto, 2),
            'Concepto': concepto
        })
    
    # Combine all transactions
    all_movimientos = pd.concat([movimientos_df, pd.DataFrame(movimientos_extra)], ignore_index=True)
    
    # Sort by date
    all_movimientos = all_movimientos.sort_values('Fecha')
    
    # Reset index and ensure unique IDs
    all_movimientos = all_movimientos.reset_index(drop=True)
    all_movimientos['ID_Movimiento'] = range(1, len(all_movimientos) + 1)
    
    # Return the DataFrame with columns in the correct order
    return all_movimientos[['ID_Movimiento', 'ID_Cuenta_Bancaria', 'Fecha', 'Tipo', 'Monto', 'Concepto']]