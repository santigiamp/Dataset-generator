import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_activos(num_activos=30):
    """
    Generate a synthetic dataset of fixed assets with realistic attributes.
    
    Args:
        num_activos: Number of assets to generate
        
    Returns:
        DataFrame: A pandas DataFrame containing asset information
    """
    # Define asset types and their characteristics
    tipos_activos = [
        {'nombre': 'Maquinaria', 'costo_min': 5000, 'costo_max': 50000, 'vida_util': [5, 10], 'valor_residual_pct': [0.05, 0.15]},
        {'nombre': 'Equipo', 'costo_min': 1000, 'costo_max': 10000, 'vida_util': [3, 7], 'valor_residual_pct': [0.03, 0.10]},
        {'nombre': 'Vehículos', 'costo_min': 15000, 'costo_max': 80000, 'vida_util': [5, 8], 'valor_residual_pct': [0.10, 0.20]},
        {'nombre': 'Inmuebles', 'costo_min': 100000, 'costo_max': 500000, 'vida_util': [20, 40], 'valor_residual_pct': [0.20, 0.40]},
        {'nombre': 'Mobiliario', 'costo_min': 500, 'costo_max': 5000, 'vida_util': [5, 10], 'valor_residual_pct': [0.05, 0.10]}
    ]
    
    # Generate start date range (3 years before simulation start to simulation start)
    start_date = datetime.strptime('2017-01-01', '%Y-%m-%d')  # 3 years before simulation
    end_date = datetime.strptime('2020-01-01', '%Y-%m-%d')    # Start of simulation
    days_range = (end_date - start_date).days
    
    # Initialize data lists
    data = {
        'ID_Activo': list(range(1, num_activos + 1)),
        'Nombre_Activo': [],
        'Tipo_Activo': [],
        'Fecha_Compra': [],
        'Costo_Adquisicion': [],
        'Vida_Util_Anios': [],
        'Valor_Residual': [],
        'Depreciacion_Acumulada': [],
        'Valor_Neto_Libros': []
    }
    
    # Generate data for each asset
    for _ in range(num_activos):
        tipo_activo = np.random.choice(tipos_activos)
        costo_adquisicion = np.random.uniform(tipo_activo['costo_min'], tipo_activo['costo_max'])
        vida_util = np.random.randint(tipo_activo['vida_util'][0], tipo_activo['vida_util'][1] + 1)
        valor_residual_pct = np.random.uniform(tipo_activo['valor_residual_pct'][0], tipo_activo['valor_residual_pct'][1])
        valor_residual = costo_adquisicion * valor_residual_pct
        
        # Generate random purchase date
        random_days = np.random.randint(0, days_range)
        fecha_compra = (start_date + timedelta(days=random_days)).strftime('%Y-%m-%d')
        
        # Calculate depreciation based on purchase date
        days_since_purchase = (end_date - (start_date + timedelta(days=random_days))).days
        years_since_purchase = days_since_purchase / 365.25
        depreciation_per_year = (costo_adquisicion - valor_residual) / vida_util
        depreciacion_acumulada = min(depreciation_per_year * years_since_purchase, costo_adquisicion - valor_residual)
        valor_neto_libros = costo_adquisicion - depreciacion_acumulada
        
        data['Tipo_Activo'].append(tipo_activo['nombre'])
        data['Fecha_Compra'].append(fecha_compra)
        data['Costo_Adquisicion'].append(round(costo_adquisicion, 2))
        data['Vida_Util_Anios'].append(vida_util)
        data['Valor_Residual'].append(round(valor_residual, 2))
        data['Depreciacion_Acumulada'].append(round(depreciacion_acumulada, 2))
        data['Valor_Neto_Libros'].append(round(valor_neto_libros, 2))
    
    # Generate asset names based on type
    nombres_activos = []
    for tipo in data['Tipo_Activo']:
        if tipo == 'Maquinaria':
            prefijos = ['Máquina', 'Equipo', 'Sistema', 'Línea', 'Unidad']
            tipos = ['Producción', 'Ensamblaje', 'Empaque', 'Procesamiento', 'Industrial']
            marcas = ['IndusTech', 'MaquiPro', 'TechMach', 'PowerEquip', 'MachSystems']
        elif tipo == 'Equipo':
            prefijos = ['Equipo', 'Sistema', 'Dispositivo', 'Unidad', 'Kit']
            tipos = ['Medición', 'Análisis', 'Control', 'Seguridad', 'Comunicación']
            marcas = ['TechEquip', 'ProSystems', 'EquipTech', 'DevicePro', 'TechTools']
        elif tipo == 'Vehículos':
            prefijos = ['Automóvil', 'Camión', 'Furgoneta', 'Camioneta', 'Vehículo']
            tipos = ['Reparto', 'Ejecutivo', 'Transporte', 'Carga', 'Comercial']
            marcas = ['Toyota', 'Ford', 'Mercedes', 'Volkswagen', 'Nissan']
        elif tipo == 'Inmuebles':
            prefijos = ['Edificio', 'Local', 'Oficina', 'Bodega', 'Terreno']
            tipos = ['Comercial', 'Industrial', 'Corporativo', 'Almacén', 'Administrativo']
            marcas = ['Ubicación', 'Sector', 'Zona', 'Área', 'Región']
        else:  # Mobiliario
            prefijos = ['Escritorio', 'Silla', 'Archivero', 'Mesa', 'Estantería']
            tipos = ['Ejecutivo', 'Ergonómico', 'Modular', 'Funcional', 'Profesional']
            marcas = ['OfficePro', 'ErgoStyle', 'ModuOffice', 'FurniTech', 'ComfortDesign']
        
        prefijo = np.random.choice(prefijos)
        tipo_especifico = np.random.choice(tipos)
        marca = np.random.choice(marcas)
        modelo = f"{chr(65 + np.random.randint(0, 26))}{np.random.randint(100, 1000)}"
        
        nombre = f"{prefijo} {tipo_especifico} {marca} {modelo}"
        nombres_activos.append(nombre)
    
    data['Nombre_Activo'] = nombres_activos
    
    # Create DataFrame
    df = pd.DataFrame(data)
    
    # Return the DataFrame with columns in the correct order
    return df[['ID_Activo', 'Nombre_Activo', 'Tipo_Activo', 'Fecha_Compra', 
               'Costo_Adquisicion', 'Vida_Util_Anios', 'Valor_Residual', 
               'Depreciacion_Acumulada', 'Valor_Neto_Libros']]