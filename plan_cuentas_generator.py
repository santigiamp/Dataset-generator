import pandas as pd
import numpy as np

def generate_plan_cuentas():
    """
    Generate a chart of accounts (plan de cuentas) for the accounting system.
    
    Returns:
        DataFrame: A pandas DataFrame containing the chart of accounts
    """
    # Define the structure of the chart of accounts
    data = {
        'ID_Cuenta': [],
        'Nombre_Cuenta': [],
        'Tipo_Cuenta': [],
        'Clasificacion': []
    }
    
    # Asset accounts (Activo)
    # Current assets (Activo Circulante)
    activo_circulante = [
        ('1001', 'Caja', 'Activo', 'Circulante'),
        ('1002', 'Bancos', 'Activo', 'Circulante'),
        ('1003', 'Inversiones Temporales', 'Activo', 'Circulante'),
        ('1004', 'Cuentas por Cobrar', 'Activo', 'Circulante'),
        ('1005', 'Inventario de Mercancías', 'Activo', 'Circulante'),
        ('1006', 'IVA Acreditable', 'Activo', 'Circulante'),
        ('1007', 'Anticipo a Proveedores', 'Activo', 'Circulante')
    ]
    
    # Non-current assets (Activo No Circulante)
    activo_no_circulante = [
        ('1101', 'Terrenos', 'Activo', 'No Circulante'),
        ('1102', 'Edificios', 'Activo', 'No Circulante'),
        ('1103', 'Maquinaria y Equipo', 'Activo', 'No Circulante'),
        ('1104', 'Equipo de Transporte', 'Activo', 'No Circulante'),
        ('1105', 'Equipo de Cómputo', 'Activo', 'No Circulante'),
        ('1106', 'Mobiliario y Equipo de Oficina', 'Activo', 'No Circulante'),
        ('1107', 'Depreciación Acumulada de Edificios', 'Activo', 'No Circulante'),
        ('1108', 'Depreciación Acumulada de Maquinaria y Equipo', 'Activo', 'No Circulante'),
        ('1109', 'Depreciación Acumulada de Equipo de Transporte', 'Activo', 'No Circulante'),
        ('1110', 'Depreciación Acumulada de Equipo de Cómputo', 'Activo', 'No Circulante'),
        ('1111', 'Depreciación Acumulada de Mobiliario y Equipo de Oficina', 'Activo', 'No Circulante')
    ]
    
    # Liability accounts (Pasivo)
    # Current liabilities (Pasivo Circulante)
    pasivo_circulante = [
        ('2001', 'Proveedores', 'Pasivo', 'Circulante'),
        ('2002', 'Acreedores Diversos', 'Pasivo', 'Circulante'),
        ('2003', 'Documentos por Pagar a Corto Plazo', 'Pasivo', 'Circulante'),
        ('2004', 'IVA por Pagar', 'Pasivo', 'Circulante'),
        ('2005', 'ISR por Pagar', 'Pasivo', 'Circulante'),
        ('2006', 'Anticipos de Clientes', 'Pasivo', 'Circulante')
    ]
    
    # Non-current liabilities (Pasivo No Circulante)
    pasivo_no_circulante = [
        ('2101', 'Préstamos Bancarios a Largo Plazo', 'Pasivo', 'No Circulante'),
        ('2102', 'Documentos por Pagar a Largo Plazo', 'Pasivo', 'No Circulante')
    ]
    
    # Equity accounts (Patrimonio)
    patrimonio = [
        ('3001', 'Capital Social', 'Patrimonio', 'Capital'),
        ('3002', 'Reserva Legal', 'Patrimonio', 'Capital'),
        ('3003', 'Utilidades Acumuladas', 'Patrimonio', 'Resultados'),
        ('3004', 'Utilidad del Ejercicio', 'Patrimonio', 'Resultados'),
        ('3005', 'Pérdidas Acumuladas', 'Patrimonio', 'Resultados')
    ]
    
    # Income accounts (Ingresos)
    ingresos = [
        ('4001', 'Ventas', 'Ingresos', 'Operativos'),
        ('4002', 'Devoluciones sobre Ventas', 'Ingresos', 'Operativos'),
        ('4003', 'Descuentos sobre Ventas', 'Ingresos', 'Operativos'),
        ('4004', 'Ingresos Financieros', 'Ingresos', 'No Operativos'),
        ('4005', 'Otros Ingresos', 'Ingresos', 'No Operativos')
    ]
    
    # Expense accounts (Gastos)
    gastos = [
        ('5001', 'Costo de Ventas', 'Gastos', 'Operativos'),
        ('5002', 'Compras', 'Gastos', 'Operativos'),
        ('5003', 'Devoluciones sobre Compras', 'Gastos', 'Operativos'),
        ('5004', 'Descuentos sobre Compras', 'Gastos', 'Operativos'),
        ('5005', 'Gastos de Administración', 'Gastos', 'Operativos'),
        ('5006', 'Gastos de Venta', 'Gastos', 'Operativos'),
        ('5007', 'Gastos Financieros', 'Gastos', 'No Operativos'),
        ('5008', 'Otros Gastos', 'Gastos', 'No Operativos')
    ]
    
    # Combine all accounts
    all_accounts = activo_circulante + activo_no_circulante + pasivo_circulante + \
                  pasivo_no_circulante + patrimonio + ingresos + gastos
    
    # Populate the data dictionary
    for account in all_accounts:
        data['ID_Cuenta'].append(account[0])
        data['Nombre_Cuenta'].append(account[1])
        data['Tipo_Cuenta'].append(account[2])
        data['Clasificacion'].append(account[3])
    
    # Create DataFrame
    df = pd.DataFrame(data)
    
    return df