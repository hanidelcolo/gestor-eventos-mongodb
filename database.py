"""
Módulo de conexión a MongoDB
"""
import os
from pymongo import MongoClient
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

class MongoDBConnection:
    """
    Clase para gestionar la conexión a MongoDB
    """
    
    def __init__(self):
        """Inicializa la conexión a MongoDB"""
        # Configuración desde variables de entorno
        self.host = os.getenv('MONGODB_HOST', 'localhost')
        self.port = int(os.getenv('MONGODB_PORT', 27017))
        self.database_name = os.getenv('MONGODB_DATABASE', 'prueba3')
        
        # Inicializar conexión
        self.client = None
        self.db = None
        
    def connect(self):
        """
        Establece la conexión con MongoDB
        
        Returns:
            MongoDatabase: Instancia de la base de datos
        """
        try:
            # Crear cliente de MongoDB
            self.client = MongoClient(f'mongodb://{self.host}:{self.port}/')
            
            # Verificar conexión
            self.client.admin.command('ping')
            
            # Seleccionar base de datos
            self.db = self.client[self.database_name]
            
            print(f"✅ Conectado exitosamente a MongoDB en {self.host}:{self.port}")
            print(f"📊 Base de datos: {self.database_name}")
            
            return self.db
            
        except Exception as e:
            print(f"❌ Error al conectar a MongoDB: {e}")
            return None
    
    def disconnect(self):
        """Cierra la conexión a MongoDB"""
        if self.client:
            self.client.close()
            print("🔌 Conexión cerrada")
    
    def get_collection(self, collection_name):
        """
        Obtiene una colección de la base de datos
        
        Args:
            collection_name (str): Nombre de la colección
            
        Returns:
            Collection: Instancia de la colección
        """
        if not self.db:
            self.connect()
        return self.db[collection_name]
    
    def load_data(self, collection_name, data):
        """
        Carga datos en una colección (limpia antes de insertar)
        
        Args:
            collection_name (str): Nombre de la colección
            data (list): Lista de documentos a insertar
        """
        collection = self.get_collection(collection_name)
        
        # Limpiar colección existente
        collection.delete_many({})
        
        # Insertar nuevos datos
        if data:
            collection.insert_many(data)
            print(f"Cargados {len(data)} documentos en {collection_name}")