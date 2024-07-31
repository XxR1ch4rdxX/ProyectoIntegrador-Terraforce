# Creating a diet plan in Spanish with ingredients easily found in Santiago de Querétaro
diet_plan_es_local = {
    'Día': ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo'],
    'Desayuno': [
        '1 porción de avena con 1 plátano y un puñado de almendras',
        '2 huevos revueltos con 1 tortilla de maíz y una manzana',
        '1 porción de avena con 1 plátano y un puñado de almendras',
        '2 huevos revueltos con 1 tortilla de maíz y una manzana',
        '1 porción de avena con 1 plátano y un puñado de almendras',
        '2 huevos revueltos con 1 tortilla de maíz y una manzana',
        '1 porción de avena con 1 plátano y un puñado de almendras'
    ],
    'Almuerzo': [
        '100g de pechuga de pollo a la parrilla, 1 taza de nopales, 1/2 taza de frijoles',
        '100g de filete de pescado a la parrilla, 1 taza de ensalada (lechuga, tomate, pepino), 1/2 taza de arroz integral',
        '100g de pechuga de pollo a la parrilla, 1 taza de nopales, 1/2 taza de frijoles',
        '100g de filete de pescado a la parrilla, 1 taza de ensalada (lechuga, tomate, pepino), 1/2 taza de arroz integral',
        '100g de pechuga de pollo a la parrilla, 1 taza de nopales, 1/2 taza de frijoles',
        '100g de filete de pescado a la parrilla, 1 taza de ensalada (lechuga, tomate, pepino), 1/2 taza de arroz integral',
        '100g de pechuga de pollo a la parrilla, 1 taza de nopales, 1/2 taza de frijoles'
    ],
    'Cena': [
        '1 porción de sopa de verduras (zanahoria, calabacita, papa), 1 huevo cocido',
        '1 porción de sopa de verduras (zanahoria, calabacita, papa), 1 huevo cocido',
        '1 porción de sopa de verduras (zanahoria, calabacita, papa), 1 huevo cocido',
        '1 porción de sopa de verduras (zanahoria, calabacita, papa), 1 huevo cocido',
        '1 porción de sopa de verduras (zanahoria, calabacita, papa), 1 huevo cocido',
        '1 porción de sopa de verduras (zanahoria, calabacita, papa), 1 huevo cocido',
        '1 porción de sopa de verduras (zanahoria, calabacita, papa), 1 huevo cocido'
    ],
    'Snacks': [
        '1 manzana, 1 puñado de cacahuates',
        '1 manzana, 1 puñado de cacahuates',
        '1 manzana, 1 puñado de cacahuates',
        '1 manzana, 1 puñado de cacahuates',
        '1 manzana, 1 puñado de cacahuates',
        '1 manzana, 1 puñado de cacahuates',
        '1 manzana, 1 puñado de cacahuates'
    ]
}

# Creating a DataFrame
df_es_local = pd.DataFrame(diet_plan_es_local)

# Saving the diet plan to an Excel file in Spanish with local ingredients
file_path_es_local = '/mnt/data/plan_de_dieta_local.xlsx'
df_es_local.to_excel(file_path_es_local, index=False)

file_path_es_local