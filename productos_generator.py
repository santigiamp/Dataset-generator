import pandas as pd
import numpy as np

def generate_productos(num_productos=50):
    """
    Generate a synthetic dataset of products with realistic pricing and cost attributes.
    
    Args:
        num_productos: Number of products to generate
        
    Returns:
        DataFrame: A pandas DataFrame containing product information
    """
    # Define product categories and their characteristics with standardized margins for accounting coherence
    categorias = [
        {'nombre': 'Electrónica', 'precio_min': 450, 'precio_max': 7000, 'margen_min': 0.35, 'margen_max': 0.45},
        {'nombre': 'Ropa', 'precio_min': 40, 'precio_max': 600, 'margen_min': 0.40, 'margen_max': 0.50},
        {'nombre': 'Alimentos', 'precio_min': 15, 'precio_max': 150, 'margen_min': 0.25, 'margen_max': 0.35},
        {'nombre': 'Hogar', 'precio_min': 80, 'precio_max': 1500, 'margen_min': 0.30, 'margen_max': 0.40},
        {'nombre': 'Juguetes', 'precio_min': 25, 'precio_max': 400, 'margen_min': 0.35, 'margen_max': 0.45}
    ]
    
    # Initialize data lists
    data = {
        'ID_Producto': list(range(1, num_productos + 1)),
        'Nombre_Producto': [],
        'Categoria': [],
        'Precio_Venta_Unitario': [],
        'Costo_Variable_Unitario': []
    }
    
    # Generate data for each product
    for _ in range(num_productos):
        categoria = np.random.choice(categorias)
        precio_venta = np.random.uniform(categoria['precio_min'], categoria['precio_max'])
        margen = np.random.uniform(categoria['margen_min'], categoria['margen_max'])
        costo_variable = precio_venta * (1 - margen)  # El costo es menor debido al margen más alto
        
        data['Categoria'].append(categoria['nombre'])
        data['Precio_Venta_Unitario'].append(round(precio_venta, 2))
        data['Costo_Variable_Unitario'].append(round(costo_variable, 2))
    
    # Generate product names based on category
    nombres_productos = []
    for categoria in data['Categoria']:
        if categoria == 'Electrónica':
            prefijos = ['Smartphone', 'Laptop', 'Tablet', 'TV', 'Auriculares', 'Altavoz', 'Cámara']
            marcas = ['TechPro', 'Innovatech', 'DigiMax', 'ElectraSmart', 'FutureTech']
        elif categoria == 'Ropa':
            prefijos = ['Camisa', 'Pantalón', 'Vestido', 'Chaqueta', 'Falda', 'Suéter', 'Abrigo']
            marcas = ['FashionStyle', 'TrendyWear', 'ElegantLine', 'UrbanChic', 'ClassicMode']
        elif categoria == 'Alimentos':
            prefijos = ['Cereal', 'Pasta', 'Conserva', 'Snack', 'Bebida', 'Lácteo', 'Condimento']
            marcas = ['NutriFood', 'DeliciaGourmet', 'SaborNatural', 'FrescoPack', 'SaludVital']
        elif categoria == 'Hogar':
            prefijos = ['Sillón', 'Mesa', 'Lámpara', 'Alfombra', 'Cortina', 'Estantería', 'Decoración']
            marcas = ['HomeStyle', 'ComfortDesign', 'ElegantHome', 'ModernSpace', 'CozyLiving']
        else:  # Juguetes
            prefijos = ['Muñeco', 'Juego', 'Puzzle', 'Peluche', 'Construcción', 'Educativo', 'Vehículo']
            marcas = ['FunToys', 'KidJoy', 'PlayWorld', 'ImagineThat', 'LearnPlay']
        
        prefijo = np.random.choice(prefijos)
        marca = np.random.choice(marcas)
        modelo = f"{chr(65 + np.random.randint(0, 26))}{np.random.randint(100, 1000)}"
        
        nombre = f"{marca} {prefijo} {modelo}"
        nombres_productos.append(nombre)
    
    data['Nombre_Producto'] = nombres_productos
    
    # Create DataFrame
    df = pd.DataFrame(data)
    
    # Return only the required columns in the correct order
    return df[['ID_Producto', 'Nombre_Producto', 'Precio_Venta_Unitario', 'Costo_Variable_Unitario']]