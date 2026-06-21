"""
Módulo de consultas para MongoDB
"""
from pymongo import MongoClient
from database import MongoDBConnection

class EventManagerQueries:
    """
    Clase que contiene todas las consultas para la gestión de eventos
    """
    
    def __init__(self, db_connection):
        """
        Inicializa el gestor de consultas
        
        Args:
            db_connection: Instancia de MongoDBConnection
        """
        self.db = db_connection.db
        self.invitados = db_connection.get_collection('invitados')
        self.eventos = db_connection.get_collection('eventos')
    
    # ============================================================
    # ACTIVIDAD 1: Filtros y condiciones
    # ============================================================
    
    def listar_todos_los_eventos(self):
        """
        Lista todos los eventos con su información básica
        
        Returns:
            list: Lista de eventos ordenados por fecha
        """
        return list(self.eventos.find(
            {},
            {
                'codigo': 1, 
                'nombre': 1, 
                'fecha': 1, 
                'lugar': 1, 
                'categoria': 1,
                '_id': 0
            }
        ).sort('fecha', 1))
    
    def listar_invitados_activos(self):
        """
        Lista todos los invitados con estado 'activo'
        
        Returns:
            list: Lista de invitados activos
        """
        return list(self.invitados.find(
            {'estado': 'activo'},
            {'_id': 0}
        ))
    
    def filtrar_invitados_por_empresa(self, empresa):
        """
        Filtra invitados por empresa
        
        Args:
            empresa (str): Nombre de la empresa
            
        Returns:
            list: Lista de invitados de esa empresa
        """
        return list(self.invitados.find(
            {'empresa': empresa},
            {'_id': 0}
        ))
    
    def filtrar_eventos_por_categoria(self, categoria):
        """
        Filtra eventos por categoría
        
        Args:
            categoria (str): Categoría del evento
            
        Returns:
            list: Lista de eventos de esa categoría
        """
        return list(self.eventos.find(
            {'categoria': categoria},
            {'_id': 0}
        ))
    
    # ============================================================
    # ACTIVIDAD 2: Expresiones Regulares (Regex)
    # ============================================================
    
    def buscar_invitados_por_nombre(self, patron):
        """
        Busca invitados por nombre usando regex (insensible a mayúsculas)
        
        Args:
            patron (str): Patrón de búsqueda
            
        Returns:
            list: Lista de invitados que coinciden con el patrón
        """
        # Usar $regex con opción 'i' para insensible a mayúsculas
        return list(self.invitados.find(
            {'nombre': {'$regex': patron, '$options': 'i'}},
            {'_id': 0}
        ))
    
    def buscar_invitados_por_dominio_correo(self, dominio):
        """
        Busca invitados por dominio de correo usando regex
        
        Args:
            dominio (str): Dominio de correo (ej: 'empresa.cl')
            
        Returns:
            list: Lista de invitados con ese dominio
        """
        # Buscar correos que terminen con el dominio
        return list(self.invitados.find(
            {'correo': {'$regex': f'@{dominio}$', '$options': 'i'}},
            {'_id': 0}
        ))
    
    def buscar_eventos_por_palabra(self, palabra):
        """
        Busca eventos que contengan una palabra en el nombre
        
        Args:
            palabra (str): Palabra a buscar
            
        Returns:
            list: Lista de eventos que contienen la palabra
        """
        return list(self.eventos.find(
            {'nombre': {'$regex': palabra, '$options': 'i'}},
            {'_id': 0}
        ))
    
    # ============================================================
    # ACTIVIDAD 3: Búsquedas en Subdocumentos
    # ============================================================
    
    def obtener_eventos_con_invitado(self, rut_invitado):
        """
        Obtiene todos los eventos donde aparece un invitado específico
        
        Args:
            rut_invitado (str): RUT del invitado
            
        Returns:
            list: Lista de eventos donde aparece el invitado
        """
        # Buscar en el arreglo de invitados
        return list(self.eventos.find(
            {'invitados.rut': rut_invitado},
            {'_id': 0}
        ))
    
    def verificar_confirmacion_evento(self, codigo_evento, rut_invitado):
        """
        Verifica si un invitado está confirmado en un evento específico
        
        Args:
            codigo_evento (str): Código del evento
            rut_invitado (str): RUT del invitado
            
        Returns:
            dict: Información del invitado en el evento o None
        """
        # Usar $elemMatch para buscar en el arreglo
        resultado = self.eventos.find_one(
            {
                'codigo': codigo_evento,
                'invitados': {
                    '$elemMatch': {
                        'rut': rut_invitado,
                        'estado': 'confirmado'
                    }
                }
            },
            {
                'codigo': 1,
                'nombre': 1,
                'invitados.$': 1,
                '_id': 0
            }
        )
        return resultado
    
    def contar_confirmados_por_evento(self, codigo_evento):
        """
        Cuenta cuántos invitados confirmados tiene un evento
        
        Args:
            codigo_evento (str): Código del evento
            
        Returns:
            int: Número de invitados confirmados
        """
        evento = self.eventos.find_one(
            {'codigo': codigo_evento},
            {'invitados': 1, '_id': 0}
        )
        
        if evento and 'invitados' in evento:
            confirmados = sum(1 for inv in evento['invitados'] 
                            if inv.get('estado') == 'confirmado')
            return confirmados
        return 0
    
    # ============================================================
    # ACTIVIDAD 4: Consultas con $lookup y Agregaciones
    # ============================================================
    
    def obtener_eventos_con_detalles_invitados(self, codigo_evento=None):
        """
        Obtiene eventos con los detalles completos de los invitados usando $lookup
        
        Args:
            codigo_evento (str, optional): Código del evento específico
            
        Returns:
            list: Lista de eventos con datos enriquecidos
        """
        # Pipeline de agregación
        pipeline = []
        
        # Filtro por código si se especifica
        if codigo_evento:
            pipeline.append({'$match': {'codigo': codigo_evento}})
        
        # $lookup para combinar con la colección invitados
        pipeline.extend([
            {
                '$lookup': {
                    'from': 'invitados',  # Colección a unir
                    'localField': 'invitados.rut',  # Campo local
                    'foreignField': 'rut',  # Campo foráneo
                    'as': 'invitados_detalle'  # Nombre del nuevo campo
                }
            },
            {
                '$project': {
                    'codigo': 1,
                    'nombre': 1,
                    'fecha': 1,
                    'lugar': 1,
                    'categoria': 1,
                    'invitados': 1,  # Datos originales del evento
                    'invitados_detalle': {
                        'nombre': 1,
                        'correo': 1,
                        'empresa': 1,
                        'estado': 1
                    },
                    '_id': 0
                }
            }
        ])
        
        return list(self.eventos.aggregate(pipeline))
    
    def top_eventos_mas_confirmados(self, limite=3):
        """
        Obtiene el top N de eventos con más invitados confirmados
        
        Args:
            limite (int): Número de eventos a mostrar
            
        Returns:
            list: Top eventos con conteo de confirmados
        """
        pipeline = [
            # Descomponer el arreglo de invitados
            {'$unwind': '$invitados'},
            # Filtrar solo confirmados
            {'$match': {'invitados.estado': 'confirmado'}},
            # Agrupar por evento
            {
                '$group': {
                    '_id': {
                        'codigo': '$codigo',
                        'nombre': '$nombre',
                        'categoria': '$categoria',
                        'lugar': '$lugar'
                    },
                    'total_confirmados': {'$sum': 1}
                }
            },
            # Ordenar de mayor a menor
            {'$sort': {'total_confirmados': -1}},
            # Limitar resultados
            {'$limit': limite},
            # Proyectar formato final
            {
                '$project': {
                    'codigo': '$_id.codigo',
                    'nombre': '$_id.nombre',
                    'categoria': '$_id.categoria',
                    'lugar': '$_id.lugar',
                    'total_confirmados': 1,
                    '_id': 0
                }
            }
        ]
        
        return list(self.eventos.aggregate(pipeline))
    
    def validar_acceso_evento(self, rut_invitado, codigo_evento):
        """
        Valida si un invitado tiene acceso a un evento
        
        Args:
            rut_invitado (str): RUT del invitado
            codigo_evento (str): Código del evento
            
        Returns:
            dict: Resultado de la validación
        """
        # Verificar si el invitado existe y está activo
        invitado = self.invitados.find_one(
            {'rut': rut_invitado},
            {'_id': 0}
        )
        
        if not invitado:
            return {'acceso': False, 'razon': 'Invitado no encontrado'}
        
        if invitado.get('estado') != 'activo':
            return {'acceso': False, 'razon': 'Invitado bloqueado'}
        
        # Verificar si está confirmado en el evento
        evento = self.verificar_confirmacion_evento(codigo_evento, rut_invitado)
        
        if not evento:
            return {'acceso': False, 'razon': 'No confirmado en este evento'}
        
        return {
            'acceso': True,
            'razon': 'Acceso permitido',
            'invitado': invitado,
            'evento': evento
        }