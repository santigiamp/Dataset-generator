import pandas as pd
import numpy as np

def generate_cuentas_bancarias(num_cuentas=5):
    """
    Generate a synthetic dataset of bank accounts with realistic attributes.
    
    Args:
        num_cuentas: Number of bank accounts to generate
        
    Returns:
        DataFrame: A pandas DataFrame containing bank account information
    """
    # Define bank names
    bancos = [
        'Banco Nacional', 'Banco Comercial', 'Banco Industrial', 'Banco Internacional',
        'Banco Metropolitano', 'Banco Regional', 'Banco Empresarial', 'Banco Capital'
    ]
    
    # Define account types and their characteristics
    tipos_cuenta = [
        {'nombre': 'Corriente', 'saldo_min': 10000, 'saldo_max': 500000},
        {'nombre': 'Ahorro', 'saldo_min': 5000, 'saldo_max': 200000}
    ]
    
    # Define currencies
    monedas = ['MXN', 'USD', 'EUR']
    moneda_probs = [0.7, 0.2, 0.1]  # 70% MXN, 20% USD, 10% EUR
    
    # Initialize data lists
    data = {
        'ID_Cuenta_Bancaria': list(range(1, num_cuentas + 1)),
        'Banco': [],
        'Tipo_Cuenta': [],
        'Saldo_Inicial': [],
        'Moneda': []
    }
    
    # Generate data for each account
    for i in range(num_cuentas):
        # First account should be Corriente and MXN
        if i == 0:
            tipo_cuenta = tipos_cuenta[0]  # Corriente
            moneda = 'MXN'
        # Second account should be Ahorro (if we have more than one account)
        elif i == 1:
            tipo_cuenta = tipos_cuenta[1]  # Ahorro
            moneda = np.random.choice(monedas, p=moneda_probs)
        else:
            tipo_cuenta = np.random.choice(tipos_cuenta)
            moneda = np.random.choice(monedas, p=moneda_probs)
        
        banco = np.random.choice(bancos)
        saldo_inicial = np.random.uniform(tipo_cuenta['saldo_min'], tipo_cuenta['saldo_max'])
        
        data['Banco'].append(banco)
        data['Tipo_Cuenta'].append(tipo_cuenta['nombre'])
        data['Saldo_Inicial'].append(round(saldo_inicial, 2))
        data['Moneda'].append(moneda)
    
    # Create DataFrame
    df = pd.DataFrame(data)
    
    # Return the DataFrame with columns in the correct order
    return df[['ID_Cuenta_Bancaria', 'Banco', 'Tipo_Cuenta', 'Saldo_Inicial', 'Moneda']]