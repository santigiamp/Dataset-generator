import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_libro_diario(plan_cuentas_df, ventas_df, compras_df, movimientos_bancarios_df, productos_df):
    """
    Generate a synthetic dataset of accounting journal entries with realistic attributes.
    
    Args:
        plan_cuentas_df: DataFrame containing chart of accounts
        ventas_df: DataFrame containing sales information
        compras_df: DataFrame containing purchase information
        movimientos_bancarios_df: DataFrame containing bank transactions
        productos_df: DataFrame containing product information
        
    Returns:
        DataFrame: A pandas DataFrame containing journal entries
    """
    # Initialize empty list for journal entries
    asientos = []
    asiento_id = 1
    
    # Get account IDs for common accounts
    cuenta_ventas = plan_cuentas_df[plan_cuentas_df['Nombre_Cuenta'] == 'Ventas']['ID_Cuenta'].iloc[0]
    cuenta_costo_ventas = plan_cuentas_df[plan_cuentas_df['Nombre_Cuenta'] == 'Costo de Ventas']['ID_Cuenta'].iloc[0]
    cuenta_inventario = plan_cuentas_df[plan_cuentas_df['Nombre_Cuenta'] == 'Inventario de Mercancías']['ID_Cuenta'].iloc[0]
    cuenta_cuentas_cobrar = plan_cuentas_df[plan_cuentas_df['Nombre_Cuenta'] == 'Cuentas por Cobrar']['ID_Cuenta'].iloc[0]
    cuenta_bancos = plan_cuentas_df[plan_cuentas_df['Nombre_Cuenta'] == 'Bancos']['ID_Cuenta'].iloc[0]
    cuenta_iva_acreditable = plan_cuentas_df[plan_cuentas_df['Nombre_Cuenta'] == 'IVA Acreditable']['ID_Cuenta'].iloc[0]
    cuenta_iva_por_pagar = plan_cuentas_df[plan_cuentas_df['Nombre_Cuenta'] == 'IVA por Pagar']['ID_Cuenta'].iloc[0]
    cuenta_proveedores = plan_cuentas_df[plan_cuentas_df['Nombre_Cuenta'] == 'Proveedores']['ID_Cuenta'].iloc[0]
    cuenta_compras = plan_cuentas_df[plan_cuentas_df['Nombre_Cuenta'] == 'Compras']['ID_Cuenta'].iloc[0]
    
    # Generate journal entries for sales
    for _, venta in ventas_df.iterrows():
        fecha = venta['Fecha']
        total_venta = venta['Total_Venta']
        # Get product cost from productos_df
        producto_row = productos_df[productos_df['ID_Producto'] == venta['ID_Producto']].iloc[0]
        costo_variable_unitario = producto_row['Costo_Variable_Unitario']
        # Apply a 75% reduction to the cost of goods sold (adjusted from 60%)
        # This decreases costs compared to previous implementation
        costo_variable_unitario = costo_variable_unitario * 0.25
        costo_venta = venta['Cantidad_Vendida'] * costo_variable_unitario
        
        # Calculate tax (IVA 16%)
        iva = round(total_venta * 0.16, 2)
        subtotal = round(total_venta - iva, 2)
        
        # 1. Record the sale (debit accounts receivable, credit sales and IVA)
        asientos.append({
            'ID_Asiento': asiento_id,
            'Fecha_Transaccion': fecha,
            'ID_Cuenta': cuenta_cuentas_cobrar,
            'Concepto': f"Venta #{venta['ID_Venta']} - Cliente #{venta['ID_Cliente']}",
            'Debito': total_venta,
            'Credito': 0
        })
        
        # Combined entry for sales and IVA (instead of two separate entries)
        asientos.append({
            'ID_Asiento': asiento_id,
            'Fecha_Transaccion': fecha,
            'ID_Cuenta': cuenta_ventas,
            'Concepto': f"Venta #{venta['ID_Venta']} - Cliente #{venta['ID_Cliente']} (incluye IVA)",
            'Debito': 0,
            'Credito': total_venta
        })
        
        asiento_id += 1
        
        # 2. Record the cost of goods sold - use proper accounting entries
        # Lower threshold to ensure more cost entries are recorded
        if round(costo_venta, 2) > 10:  # Decreased threshold from 20 to 10
            asientos.append({
                'ID_Asiento': asiento_id,
                'Fecha_Transaccion': fecha,
                'ID_Cuenta': cuenta_costo_ventas,
                'Concepto': f"Costo de Venta #{venta['ID_Venta']}",
                'Debito': round(costo_venta, 2),
                'Credito': 0
            })
            
            asientos.append({
                'ID_Asiento': asiento_id,
                'Fecha_Transaccion': fecha,
                'ID_Cuenta': cuenta_inventario,
                'Concepto': f"Costo de Venta #{venta['ID_Venta']} - Ajuste de inventario",
                'Debito': 0,
                'Credito': round(costo_venta, 2)
            })
            
            asiento_id += 1
    
    # Generate additional operating expenses based on sales volume
    # This will create a more realistic EBIT by adding administrative and selling expenses
    
    # Get account IDs for expense accounts
    cuenta_gastos_admin = plan_cuentas_df[plan_cuentas_df['Nombre_Cuenta'] == 'Gastos de Administración']['ID_Cuenta'].iloc[0]
    cuenta_gastos_venta = plan_cuentas_df[plan_cuentas_df['Nombre_Cuenta'] == 'Gastos de Venta']['ID_Cuenta'].iloc[0]
    
    # Group sales by month for expense allocation
    ventas_df['Mes'] = pd.to_datetime(ventas_df['Fecha']).dt.to_period('M')
    ventas_mensuales = ventas_df.groupby('Mes')['Total_Venta'].sum().reset_index()
    
    # Generate monthly operating expenses
    for _, mes_venta in ventas_mensuales.iterrows():
        # Convert period to date string (use the first day of the month)
        fecha = mes_venta['Mes'].to_timestamp().strftime('%Y-%m-%d')
        total_ventas_mes = mes_venta['Total_Venta']
        
        # Calculate administrative expenses (reduced from 15% to 10% of monthly sales)
        gastos_admin = round(total_ventas_mes * 0.10, 2)
        
        # Calculate selling expenses (reduced from 20% to 15% of monthly sales)
        gastos_venta = round(total_ventas_mes * 0.15, 2)
        
        # Record administrative expenses
        asientos.append({
            'ID_Asiento': asiento_id,
            'Fecha_Transaccion': fecha,
            'ID_Cuenta': cuenta_gastos_admin,
            'Concepto': f"Gastos administrativos del mes",
            'Debito': gastos_admin,
            'Credito': 0
        })
        
        asientos.append({
            'ID_Asiento': asiento_id,
            'Fecha_Transaccion': fecha,
            'ID_Cuenta': cuenta_bancos,
            'Concepto': f"Pago de gastos administrativos del mes",
            'Debito': 0,
            'Credito': gastos_admin
        })
        
        asiento_id += 1
        
        # Record selling expenses
        asientos.append({
            'ID_Asiento': asiento_id,
            'Fecha_Transaccion': fecha,
            'ID_Cuenta': cuenta_gastos_venta,
            'Concepto': f"Gastos de venta del mes",
            'Debito': gastos_venta,
            'Credito': 0
        })
        
        asientos.append({
            'ID_Asiento': asiento_id,
            'Fecha_Transaccion': fecha,
            'ID_Cuenta': cuenta_bancos,
            'Concepto': f"Pago de gastos de venta del mes",
            'Debito': 0,
            'Credito': gastos_venta
        })
        
        asiento_id += 1
    
    # Generate journal entries for purchases
    for _, compra in compras_df.iterrows():
        fecha = compra['Fecha_Compra']
        total_compra = compra['Costo_Total_Compra']
        
        # Lower threshold to ensure more purchase entries are recorded
        if total_compra > 100:  # Decreased threshold from 200 to 100
            # Calculate tax (IVA 16%)
            iva = round(total_compra * 0.16, 2)
            subtotal = round(total_compra - iva, 2)
            
            # Record the purchase with proper accounting entries
            asientos.append({
                'ID_Asiento': asiento_id,
                'Fecha_Transaccion': fecha,
                'ID_Cuenta': cuenta_inventario,
                'Concepto': f"Compra #{compra['ID_Compra']} - Producto #{compra['ID_Producto']}",
                'Debito': subtotal,
                'Credito': 0
            })
            
            asientos.append({
                'ID_Asiento': asiento_id,
                'Fecha_Transaccion': fecha,
                'ID_Cuenta': cuenta_iva_acreditable,
                'Concepto': f"IVA por Compra #{compra['ID_Compra']}",
                'Debito': iva,
                'Credito': 0
            })
            
            asientos.append({
                'ID_Asiento': asiento_id,
                'Fecha_Transaccion': fecha,
                'ID_Cuenta': cuenta_proveedores,
                'Concepto': f"Compra #{compra['ID_Compra']} - Producto #{compra['ID_Producto']}",
                'Debito': 0,
                'Credito': total_compra
            })
            
            asiento_id += 1
    
    # Generate journal entries for bank transactions
    for _, movimiento in movimientos_bancarios_df.iterrows():
        fecha = movimiento['Fecha']
        monto = movimiento['Monto']
        concepto = movimiento['Concepto']
        
        if 'Cobro venta' in concepto:
            # Payment received from customer
            asientos.append({
                'ID_Asiento': asiento_id,
                'Fecha_Transaccion': fecha,
                'ID_Cuenta': cuenta_bancos,
                'Concepto': concepto,
                'Debito': monto,
                'Credito': 0
            })
            
            asientos.append({
                'ID_Asiento': asiento_id,
                'Fecha_Transaccion': fecha,
                'ID_Cuenta': cuenta_cuentas_cobrar,
                'Concepto': concepto,
                'Debito': 0,
                'Credito': monto
            })
            
        elif 'Pago compra' in concepto:
            # Payment to supplier
            asientos.append({
                'ID_Asiento': asiento_id,
                'Fecha_Transaccion': fecha,
                'ID_Cuenta': cuenta_proveedores,
                'Concepto': concepto,
                'Debito': monto,
                'Credito': 0
            })
            
            asientos.append({
                'ID_Asiento': asiento_id,
                'Fecha_Transaccion': fecha,
                'ID_Cuenta': cuenta_bancos,
                'Concepto': concepto,
                'Debito': 0,
                'Credito': monto
            })
            
        else:
            # Other bank transactions
            # Determine appropriate accounts based on transaction type
            if movimiento['Tipo'] == 'Ingreso':
                # Income transactions
                if 'Préstamo' in concepto:
                    cuenta_contraparte = plan_cuentas_df[plan_cuentas_df['Nombre_Cuenta'] == 'Préstamos Bancarios a Largo Plazo']['ID_Cuenta'].iloc[0]
                elif 'Devolución impuestos' in concepto:
                    cuenta_contraparte = plan_cuentas_df[plan_cuentas_df['Nombre_Cuenta'] == 'ISR por Pagar']['ID_Cuenta'].iloc[0]
                elif 'Venta de activo' in concepto:
                    cuenta_contraparte = plan_cuentas_df[plan_cuentas_df['Nombre_Cuenta'] == 'Otros Ingresos']['ID_Cuenta'].iloc[0]
                else:
                    cuenta_contraparte = plan_cuentas_df[plan_cuentas_df['Nombre_Cuenta'] == 'Otros Ingresos']['ID_Cuenta'].iloc[0]
                
                asientos.append({
                    'ID_Asiento': asiento_id,
                    'Fecha_Transaccion': fecha,
                    'ID_Cuenta': cuenta_bancos,
                    'Concepto': concepto,
                    'Debito': monto,
                    'Credito': 0
                })
                
                asientos.append({
                    'ID_Asiento': asiento_id,
                    'Fecha_Transaccion': fecha,
                    'ID_Cuenta': cuenta_contraparte,
                    'Concepto': concepto,
                    'Debito': 0,
                    'Credito': monto
                })
                
            else:  # Egreso
                # Expense transactions
                if 'nómina' in concepto.lower():
                    cuenta_contraparte = plan_cuentas_df[plan_cuentas_df['Nombre_Cuenta'] == 'Gastos de Administración']['ID_Cuenta'].iloc[0]
                elif 'Servicios' in concepto:
                    cuenta_contraparte = plan_cuentas_df[plan_cuentas_df['Nombre_Cuenta'] == 'Gastos de Administración']['ID_Cuenta'].iloc[0]
                elif 'Impuestos' in concepto:
                    cuenta_contraparte = plan_cuentas_df[plan_cuentas_df['Nombre_Cuenta'] == 'ISR por Pagar']['ID_Cuenta'].iloc[0]
                elif 'Seguros' in concepto or 'Mantenimiento' in concepto:
                    cuenta_contraparte = plan_cuentas_df[plan_cuentas_df['Nombre_Cuenta'] == 'Gastos de Administración']['ID_Cuenta'].iloc[0]
                elif 'Alquiler' in concepto:
                    cuenta_contraparte = plan_cuentas_df[plan_cuentas_df['Nombre_Cuenta'] == 'Gastos de Administración']['ID_Cuenta'].iloc[0]
                else:
                    cuenta_contraparte = plan_cuentas_df[plan_cuentas_df['Nombre_Cuenta'] == 'Otros Gastos']['ID_Cuenta'].iloc[0]
                
                asientos.append({
                    'ID_Asiento': asiento_id,
                    'Fecha_Transaccion': fecha,
                    'ID_Cuenta': cuenta_contraparte,
                    'Concepto': concepto,
                    'Debito': monto,
                    'Credito': 0
                })
                
                asientos.append({
                    'ID_Asiento': asiento_id,
                    'Fecha_Transaccion': fecha,
                    'ID_Cuenta': cuenta_bancos,
                    'Concepto': concepto,
                    'Debito': 0,
                    'Credito': monto
                })
        
        asiento_id += 1
    
    # Create DataFrame from the list of journal entries
    libro_diario_df = pd.DataFrame(asientos)
    
    # Sort by date and ID
    libro_diario_df = libro_diario_df.sort_values(['Fecha_Transaccion', 'ID_Asiento'])
    
    # Reset index
    libro_diario_df = libro_diario_df.reset_index(drop=True)
    
    # Round monetary values to 2 decimal places
    libro_diario_df['Debito'] = libro_diario_df['Debito'].round(2)
    libro_diario_df['Credito'] = libro_diario_df['Credito'].round(2)
    
    # Return the DataFrame with columns in the correct order
    return libro_diario_df[['ID_Asiento', 'Fecha_Transaccion', 'ID_Cuenta', 'Concepto', 'Debito', 'Credito']]