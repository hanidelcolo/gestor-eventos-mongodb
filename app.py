
import json
import os
from database import MongoDBConnection
from queries import EventManagerQueries
from menu import MenuApp

def cargar_datos(db_connection):
    """
    Carga los datos desde los archivos JSON a MongoDB
    
    Args:
        db_connection: Instancia de MongoDBConnection
    """
    # Cargar invitados
    try:
        with open('invitados.json', 'r', encoding='utf-8') as f:
            invitados_data = json.load(f)
            db_connection.load_data('invitados', invitados_data)
    except FileNotFoundError:
        print("Archivo invitados.json no encontrado")
    except Exception as e:
        print(f"Error cargando invitados: {e}")
    
    # Cargar eventos
    try:
        with open('eventos.json', 'r', encoding='utf-8') as f:
            eventos_data = json.load(f)
            db_connection.load_data('eventos', eventos_data)
    except FileNotFoundError:
        print("Archivo eventos.json no encontrado")
    except Exception as e:
        print(f"Error cargando eventos: {e}")

def main():
    """
    Función principal de la aplicación
    """
    print("=" * 70)
    print("  INICIANDO GESTOR DE EVENTOS E INVITADOS")
    print("  Evaluación Sumativa - Unidad 3")
    print("  TI3032 - Bases de Datos No Estructuradas")
    print("=" * 70)
    print()
    
    # 1. Conectar a MongoDB
    db_connection = MongoDBConnection()
    db = db_connection.connect()
    
    if not db:
        print("No se pudo establecer conexión con MongoDB")
        print("Asegúrate de que MongoDB esté ejecutándose")
        return
    
    # 2. Cargar datos desde JSON
    print("\nCargando datos desde archivos JSON...")
    cargar_datos(db_connection)
    
    # 3. Inicializar consultas y menú
    queries = EventManagerQueries(db_connection)
    menu = MenuApp(queries)
    
    # 4. Ejecutar menú
    print("\n" + "=" * 70)
    print("  Sistema listo para usar")
    print("=" * 70)
    input("\nPresiona Enter para continuar...")
    
    try:
        menu.run()
    except KeyboardInterrupt:
        print("\n\n¡Hasta luego!")
    finally:
        db_connection.disconnect()

if __name__ == "__main__":
    main()