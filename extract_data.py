import pandas as pd
import os

# Ruta del archivo Excel
file_path = r'\\ACT_40000008781\ShareEstadisticas\27 Practicantes\Alan Martinez\Prueba A\Data Validation PI 2024.xlsm'

# Ruta de destino para los archivos JSON
output_dir = r'\\ACT_40000008781\ShareEstadisticas\27 Practicantes\Alan Martinez\Prueba A'

# Crear la ruta de destino si no existe
os.makedirs(output_dir, exist_ok=True)

# Cargar solo las columnas necesarias y asegurarse de que los códigos se carguen como cadenas de texto
clientes_segmentacion = pd.read_excel(file_path, sheet_name='Clientes Segmentacion', usecols="A:H", dtype=str)

# Renombrar las columnas para consistencia
clientes_segmentacion.columns = ['Centro', 'Ruta', 'Codigo_Cliente', 'Nombre_de_Negocio', 'Nombre_de_Cliente', 'Tipo_de_Cluster','Direccion', 'Codigo_Cliente_HTML']

# Imprimir las columnas actuales del DataFrame para verificar
print(clientes_segmentacion.columns)

# Cargar las restricciones y asegurarse de que los códigos se carguen como cadenas de texto
restricciones_j = pd.read_excel(file_path, sheet_name='Clientes Segmentacion', usecols="J", dtype=str)
restricciones_n = pd.read_excel(file_path, sheet_name='Clientes Segmentacion', usecols="N", dtype=str)
restricciones_q = pd.read_excel(file_path, sheet_name='Clientes Segmentacion', usecols="Q", dtype=str)
restricciones_t = pd.read_excel(file_path, sheet_name='Clientes Segmentacion', usecols="T", dtype=str)
restricciones_v = pd.read_excel(file_path, sheet_name='Clientes Segmentacion', usecols="V", dtype=str)

# Renombrar las columnas para consistencia
restricciones_j.columns = ['Codigo']
restricciones_n.columns = ['Codigo']
restricciones_q.columns = ['Codigo']
restricciones_t.columns = ['Codigo']
restricciones_v.columns = ['Codigo']

# Mantener solo los primeros 13 dígitos en las restricciones
restricciones_j['Codigo'] = restricciones_j['Codigo'].str[:13]
restricciones_n['Codigo'] = restricciones_n['Codigo'].str[:13]
restricciones_q['Codigo'] = restricciones_q['Codigo'].str[:13]
restricciones_t['Codigo'] = restricciones_t['Codigo'].str[:13]
restricciones_v['Codigo'] = restricciones_v['Codigo'].str[:13]

# Agregar las razones para las restricciones
restricciones_j['No_Aplica_Por'] = 'plan big cola'
restricciones_n['No_Aplica_Por'] = 'plan lealtad'
restricciones_q['No_Aplica_Por'] = 'activo en promorack'
restricciones_t['No_Aplica_Por'] = 'cluster mantener'
restricciones_v['No_Aplica_Por'] = 'cluster optimizar'

# Combinar todas las restricciones en un solo DataFrame
restricciones = pd.concat([restricciones_j, restricciones_n, restricciones_q, restricciones_t, restricciones_v])

# Agrupar restricciones por código
restricciones_agrupadas = restricciones.groupby('Codigo')['No_Aplica_Por'].apply(lambda x: ', '.join(x)).reset_index()

# Convertir los DataFrames a JSON
clientes_segmentacion_json = clientes_segmentacion.to_json(orient='records')
restricciones_json = restricciones_agrupadas.to_json(orient='records')

# Guardar los datos en archivos JSON para su uso posterior
clientes_segmentacion_json_path = os.path.join(output_dir, 'clientes_segmentacion.json')
restricciones_json_path = os.path.join(output_dir, 'restricciones.json')

with open(clientes_segmentacion_json_path, 'w') as f:
    f.write(clientes_segmentacion_json)

with open(restricciones_json_path, 'w') as f:
    f.write(restricciones_json)

print("Archivos JSON generados correctamente.")
