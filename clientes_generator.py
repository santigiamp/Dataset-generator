import pandas as pd
import numpy as np

def generate_clientes(num_clientes=100):
    """
    Generate a synthetic dataset of clients with realistic attributes.
    
    Args:
        num_clientes: Number of clients to generate
        
    Returns:
        DataFrame: A pandas DataFrame containing client information
    """
    # Define the structure of the clients dataset
    data = {
        'ID_Cliente': list(range(1, num_clientes + 1)),
        'Nombre': [],
        'Categoria': []
    }
    
    # Define client categories and their distribution
    categorias = ['Minorista', 'Mayorista', 'Corporativo']
    categoria_probs = [0.6, 0.3, 0.1]  # 60% Minorista, 30% Mayorista, 10% Corporativo
    
    # Generate categories based on probabilities
    data['Categoria'] = np.random.choice(categorias, size=num_clientes, p=categoria_probs)
    
    # Define sample names for each category
    nombres_minorista = [
        'Juan Pérez', 'María García', 'Carlos López', 'Ana Martínez', 'Pedro Rodríguez',
        'Laura Sánchez', 'Miguel González', 'Carmen Fernández', 'José Ramírez', 'Isabel Torres',
        'Francisco Díaz', 'Sofía Ruiz', 'Antonio Vargas', 'Elena Castro', 'Manuel Ortega',
        'Rosa Jiménez', 'Javier Romero', 'Patricia Moreno', 'David Álvarez', 'Lucía Gutiérrez'
    ]
    
    nombres_mayorista = [
        'Distribuidora González S.A.', 'Comercial López e Hijos', 'Mayorista Fernández',
        'Distribuciones Martínez', 'Comercializadora Rodríguez', 'Mayoreo Sánchez',
        'Abastecedora Torres', 'Distribuidora Nacional', 'Comercial del Centro',
        'Mayorista del Sur'
    ]
    
    nombres_corporativo = [
        'Industrias Globales S.A.', 'Corporación Tecnológica', 'Grupo Empresarial Omega',
        'Conglomerado Industrial', 'Multinacional Sigma', 'Corporación Financiera Alpha',
        'Grupo Hotelero Internacional', 'Consorcio Energético', 'Corporación Alimentaria',
        'Grupo Farmacéutico'
    ]
    
    # Assign realistic names based on category
    nombres = []
    for categoria in data['Categoria']:
        if categoria == 'Minorista':
            nombres.append(np.random.choice(nombres_minorista))
        elif categoria == 'Mayorista':
            nombres.append(np.random.choice(nombres_mayorista))
        else:  # Corporativo
            nombres.append(np.random.choice(nombres_corporativo))
    
    data['Nombre'] = nombres
    
    # Create and return DataFrame
    df = pd.DataFrame(data)
    return df[['ID_Cliente', 'Nombre', 'Categoria']]