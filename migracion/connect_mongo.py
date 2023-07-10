from pymongo import MongoClient

def conexion_mongo():
    # Establecer conexión con MongoDB
    client = MongoClient('mongodb://localhost:27017/')

    # Acceder a la base de datos
    db = client['monitoring_db']

    # Acceder a la colección
    collection = db['compute_data']

    # Realizar consulta en la colección
    documents = collection.find()


    #Lista de instancias
    lista_instancias = []
    for document in documents:
        # Procesar cada documento según tus necesidades
        valor_instance = document['instance']
        # print(valor_instance)
        cantidad_ver = lista_instancias.count(valor_instance)
        if not(cantidad_ver > 0):
            lista_instancias.append(valor_instance)
            
    print(lista_instancias)

    diccionario_instancias = {}
    for nombre_instancia in lista_instancias:
        diccionario_valores = {}
        documents2 = collection.find()
        for document in documents2:
            nombre_db = document['instance']
            if nombre_instancia == nombre_db:
                timestamp = document['timestamp']
                cpu_total = document['cpu']['total']
                diccionario_valores[timestamp] = cpu_total
        diccionario_instancias[nombre_instancia] = diccionario_valores

    print(diccionario_instancias)
    # Cerrar la conexión a MongoDB
    client.close()
    return diccionario_instancias