from pymongo import MongoClient

import certifi

MONGO = 'mongodb+srv://andresinfantepaez:andresinfantepaez@cluster0.vwi4ort.mongodb.net/?retryWrites=true&w=majority'

certificado = certifi.where()


def Conexion():
    try:
        client = MongoClient(MONGO, tlsCAFile = certificado) #Hace la conexión
        bd = client["bd_personas"] #Crea la colección
    except ConnectionError:
        print("No se ha podido conectar a la base de datos")
    return bd #Devuelve la colección

