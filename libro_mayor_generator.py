import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_libro_mayor(plan_cuentas_df, libro_diario_df):
    """
    Generate a synthetic dataset of general ledger entries with realistic attributes.
    
    Args:
        plan_cuentas_df: DataFrame containing chart of accounts
        libro_diario_df: DataFrame containing journal entries
        
    Returns:
        DataFrame: A pandas DataFrame containing general ledger information
    """
    # Define date range for the simulation (3 years by months)
    start_date = datetime.strptime('2020-01-01', '%Y-%m-%d')
    end_date = datetime.strptime('2022-12-31', '%Y-%m-%d')
    
    # Generate a list of month-end dates
    month_ends = []
    current_date = start_date
    while current_date <= end_date:
        # Get the last day of the current month
        if current_date.month == 12:
            last_day = datetime(current_date.year, current_date.month, 31)
        else:
            last_day = datetime(current_date.year, current_date.month + 1, 1) - timedelta(days=1)
        
        month_ends.append(last_day.strftime('%Y-%m-%d'))
        
        # Move to the next month
        if current_date.month == 12:
            current_date = datetime(current_date.year + 1, 1, 1)
        else:
            current_date = datetime(current_date.year, current_date.month + 1, 1)
    
    # Initialize empty list for general ledger entries
    libro_mayor_entries = []
    
    # Process each account
    for _, cuenta in plan_cuentas_df.iterrows():
        id_cuenta = cuenta['ID_Cuenta']
        tipo_cuenta = cuenta['Tipo_Cuenta']
        
        # Initialize running balance
        saldo_acumulado = 0
        
        # For asset and expense accounts, debits increase the balance
        # For liability, equity, and income accounts, credits increase the balance
        is_debit_account = tipo_cuenta in ['Activo', 'Gastos']
        
        # Process each month
        for i, fecha in enumerate(month_ends):
            # Get the start date for the period (first day of month or simulation start)
            if i == 0:
                start_period = start_date.strftime('%Y-%m-%d')
            else:
                prev_month_end = datetime.strptime(month_ends[i-1], '%Y-%m-%d')
                start_period = (prev_month_end + timedelta(days=1)).strftime('%Y-%m-%d')
            
            # Get journal entries for this account and period
            period_entries = libro_diario_df[
                (libro_diario_df['ID_Cuenta'] == id_cuenta) & 
                (libro_diario_df['Fecha_Transaccion'] >= start_period) & 
                (libro_diario_df['Fecha_Transaccion'] <= fecha)
            ]
            
            # Calculate total debits and credits for the period
            total_debitos = period_entries['Debito'].sum()
            total_creditos = period_entries['Credito'].sum()
            
            # Calculate the change in balance for the period
            if is_debit_account:
                cambio_saldo = total_debitos - total_creditos
            else:
                cambio_saldo = total_creditos - total_debitos
            
            # Calculate ending balance
            saldo_final = saldo_acumulado + cambio_saldo
            
            # Add entry to the general ledger
            libro_mayor_entries.append({
                'ID_Cuenta': id_cuenta,
                'Fecha': fecha,
                'Saldo_Inicial': round(saldo_acumulado, 2),
                'Debitos': round(total_debitos, 2),
                'Creditos': round(total_creditos, 2),
                'Saldo_Final': round(saldo_final, 2)
            })
            
            # Update running balance for next period
            saldo_acumulado = saldo_final
    
    # Create DataFrame from the list of general ledger entries
    libro_mayor_df = pd.DataFrame(libro_mayor_entries)
    
    # Sort by account and date
    libro_mayor_df = libro_mayor_df.sort_values(['ID_Cuenta', 'Fecha'])
    
    # Reset index
    libro_mayor_df = libro_mayor_df.reset_index(drop=True)
    
    # Return the DataFrame with columns in the correct order
    return libro_mayor_df[['ID_Cuenta', 'Fecha', 'Saldo_Inicial', 'Debitos', 'Creditos', 'Saldo_Final']]