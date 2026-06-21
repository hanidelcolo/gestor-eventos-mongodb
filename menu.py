"""
Módulo de menú para la aplicación
"""
import os
import sys
from datetime import datetime

class MenuApp:
    """
    Clase para gestionar el menú de navegación
    """
    
    def __init__(self, queries):
        """
        Inicializa el menú con las consultas
        
        Args:
            queries: Instancia de EventManagerQueries
        """
        self.queries = queries
        self.running = True
    
    def clear_screen(self):
        """Limpia la pantalla según el sistema operativo"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def print_header(self, title):
        """
        Imprime el encabezado de la aplicación
        
        Args:
            title (str): Título de la sección
        """
        self.clear_screen()
        print("=" * 70)
        print(f"  🎯 GESTOR DE EVENTOS E INVITADOS - {title}")
        print("=" * 70)
        print()
    
    def print_results(self, results, title="Resultados"):
        """
        Imprime los resultados de una consulta
        
        Args:
            results (list): Lista de resultados
            title (str): Título de la sección
        """
        print(f"\n📋 {title}:")
        print("-" * 70)
        
        if not results:
            print("  ⚠️ No se encontraron resultados")
        else:
            for i, result in enumerate(results, 1):
                print(f"  {i}. {result}")
        
        print("-" * 70)
        print(f"  Total: {len(results)} registros")
        input("\nPresiona Enter para continuar...")
    
    def print_eventos(self, eventos):
        """
        Imprime eventos en formato tabla
        """
        print("\n📅 LISTADO DE EVENTOS")
        print("-" * 80)
        print(f"{'Código':<15} {'Nombre':<30} {'Fecha':<20} {'Lugar':<15} {'Categoría':<12}")
        print("-" * 80)
        
        for ev in eventos:
            fecha = ev.get('fecha', '')
            try:
                fecha_dt = datetime.fromisoformat(fecha.replace('Z', '+00:00'))
                fecha = fecha_dt.strftime('%Y-%m-%d %H:%M')
            except:
                pass
            
            print(f"{ev.get('codigo', ''):<15} "
                  f"{ev.get('nombre', '')[:28]:<30} "
                  f"{fecha:<20} "
                  f"{ev.get('lugar', ''):<15} "
                  f"{ev.get('categoria', ''):<12}")
        
        print("-" * 80)
        print(f"Total: {len(eventos)} eventos")
    
    def print_invitados(self, invitados, title="INVITADOS"):
        """
        Imprime invitados en formato tabla
        """
        print(f"\n👤 {title}")
        print("-" * 80)
        print(f"{'RUT':<14} {'Nombre':<25} {'Correo':<30} {'Empresa':<15} {'Estado':<10}")
        print("-" * 80)
        
        for inv in invitados:
            print(f"{inv.get('rut', ''):<14} "
                  f"{inv.get('nombre', '')[:23]:<25} "
                  f"{inv.get('correo', '')[:28]:<30} "
                  f"{inv.get('empresa', ''):<15} "
                  f"{inv.get('estado', ''):<10}")
        
        print("-" * 80)
        print(f"Total: {len(invitados)} invitados")
    
    def print_top_eventos(self, top_eventos):
        """
        Imprime el top de eventos
        """
        print("\n🏆 TOP EVENTOS CON MÁS CONFIRMADOS")
        print("-" * 70)
        print(f"{'#':<3} {'Código':<15} {'Nombre':<30} {'Confirmados':<12}")
        print("-" * 70)
        
        for i, ev in enumerate(top_eventos, 1):
            print(f"{i:<3} {ev.get('codigo', ''):<15} "
                  f"{ev.get('nombre', '')[:28]:<30} "
                  f"{ev.get('total_confirmados', 0):<12}")
        
        print("-" * 70)
    
    def print_validacion_acceso(self, resultado):
        """
        Imprime el resultado de validación de acceso
        """
        print("\n🔐 VALIDACIÓN DE ACCESO")
        print("-" * 50)
        
        if resultado['acceso']:
            print("✅ ACCESO PERMITIDO")
            print(f"   Invitado: {resultado['invitado']['nombre']}")
            print(f"   Evento: {resultado['evento']['nombre']}")
        else:
            print("❌ ACCESO DENEGADO")
            print(f"   Razón: {resultado['razon']}")
        
        print("-" * 50)
    
    def menu_principal(self):
        """
        Muestra el menú principal
        """
        self.print_header("MENÚ PRINCIPAL")
        
        print("  ACTIVIDAD 1: Filtros y condiciones")
        print("  ────────────────────────────────────")
        print("  1.  📅 Listar todos los eventos")
        print("  2.  👤 Listar invitados activos")
        print("  3.  🏢 Filtrar invitados por empresa")
        print("  4.  🏷️ Filtrar eventos por categoría")
        print()
        print("  ACTIVIDAD 2: Expresiones Regulares")
        print("  ────────────────────────────────────")
        print("  5.  🔍 Buscar invitados por nombre")
        print("  6.  📧 Buscar invitados por dominio de correo")
        print("  7.  🔎 Buscar eventos por palabra")
        print()
        print("  ACTIVIDAD 3: Búsquedas en Subdocumentos")
        print("  ────────────────────────────────────────")
        print("  8.  📋 Eventos donde aparece un invitado")
        print("  9.  ✅ Verificar confirmación en evento")
        print("  10. 📊 Contar confirmados por evento")
        print()
        print("  ACTIVIDAD 4: $lookup y Agregaciones")
        print("  ──────────────────────────────────────")
        print("  11. 🔗 Eventos con detalles de invitados")
        print("  12. 🏆 Top 3 eventos con más confirmados")
        print("  13. 🔐 Validar acceso a evento")
        print()
        print("  ──────────────────────────────────────")
        print("  0.  Salir")
        print("=" * 50)
    
    def run(self):
        """
        Ejecuta el bucle principal del menú
        """
        while self.running:
            self.menu_principal()
            
            try:
                opcion = input("\nSelecciona una opción: ").strip()
                
                if opcion == '0':
                    print("\n👋 ¡Hasta luego!")
                    self.running = False
                    break
                
                self.ejecutar_opcion(opcion)
                
            except KeyboardInterrupt:
                print("\n\n👋 ¡Hasta luego!")
                self.running = False
                break
            except Exception as e:
                print(f"\n❌ Error: {e}")
                input("Presiona Enter para continuar...")
    
    def ejecutar_opcion(self, opcion):
        """
        Ejecuta la opción seleccionada
        
        Args:
            opcion (str): Opción del menú
        """
        # ACTIVIDAD 1
        if opcion == '1':
            self.print_header("Listar Eventos")
            eventos = self.queries.listar_todos_los_eventos()
            self.print_eventos(eventos)
            input("\nPresiona Enter para continuar...")
            
        elif opcion == '2':
            self.print_header("Invitados Activos")
            invitados = self.queries.listar_invitados_activos()
            self.print_invitados(invitados)
            input("\nPresiona Enter para continuar...")
            
        elif opcion == '3':
            self.print_header("Filtrar por Empresa")
            empresa = input("Ingresa el nombre de la empresa: ").strip()
            if empresa:
                invitados = self.queries.filtrar_invitados_por_empresa(empresa)
                self.print_invitados(invitados, f"INVITADOS DE {empresa.upper()}")
            input("\nPresiona Enter para continuar...")
            
        elif opcion == '4':
            self.print_header("Filtrar por Categoría")
            categoria = input("Ingresa la categoría (charla, workshop, meetup): ").strip()
            if categoria:
                eventos = self.queries.filtrar_eventos_por_categoria(categoria)
                self.print_eventos(eventos)
            input("\nPresiona Enter para continuar...")
            
        # ACTIVIDAD 2
        elif opcion == '5':
            self.print_header("Buscar por Nombre")
            patron = input("Ingresa el patrón de búsqueda: ").strip()
            if patron:
                invitados = self.queries.buscar_invitados_por_nombre(patron)
                self.print_invitados(invitados, f"RESULTADOS: '{patron}'")
            input("\nPresiona Enter para continuar...")
            
        elif opcion == '6':
            self.print_header("Buscar por Dominio")
            dominio = input("Ingresa el dominio (ej: empresa.cl): ").strip()
            if dominio:
                invitados = self.queries.buscar_invitados_por_dominio_correo(dominio)
                self.print_invitados(invitados, f"DOMINIO: @{dominio}")
            input("\nPresiona Enter para continuar...")
            
        elif opcion == '7':
            self.print_header("Buscar en Eventos")
            palabra = input("Ingresa la palabra a buscar: ").strip()
            if palabra:
                eventos = self.queries.buscar_eventos_por_palabra(palabra)
                self.print_eventos(eventos)
            input("\nPresiona Enter para continuar...")
            
        # ACTIVIDAD 3
        elif opcion == '8':
            self.print_header("Eventos por Invitado")
            rut = input("Ingresa el RUT del invitado (ej: 11.009.876-3): ").strip()
            if rut:
                eventos = self.queries.obtener_eventos_con_invitado(rut)
                self.print_eventos(eventos)
            input("\nPresiona Enter para continuar...")
            
        elif opcion == '9':
            self.print_header("Verificar Confirmación")
            codigo = input("Ingresa el código del evento: ").strip()
            rut = input("Ingresa el RUT del invitado: ").strip()
            if codigo and rut:
                resultado = self.queries.verificar_confirmacion_evento(codigo, rut)
                if resultado:
                    print(f"\n✅ Invitado CONFIRMADO en {resultado.get('nombre')}")
                else:
                    print("\n❌ Invitado NO confirmado en este evento")
            input("\nPresiona Enter para continuar...")
            
        elif opcion == '10':
            self.print_header("Contar Confirmados")
            codigo = input("Ingresa el código del evento: ").strip()
            if codigo:
                total = self.queries.contar_confirmados_por_evento(codigo)
                print(f"\n📊 Evento {codigo} tiene {total} invitados confirmados")
            input("\nPresiona Enter para continuar...")
            
        # ACTIVIDAD 4
        elif opcion == '11':
            self.print_header("Eventos con Detalles")
            codigo = input("Ingresa código del evento (Enter para todos): ").strip()
            codigo = codigo if codigo else None
            eventos = self.queries.obtener_eventos_con_detalles_invitados(codigo)
            self.print_eventos(eventos)
            input("\nPresiona Enter para continuar...")
            
        elif opcion == '12':
            self.print_header("Top Eventos")
            top = self.queries.top_eventos_mas_confirmados(3)
            self.print_top_eventos(top)
            input("\nPresiona Enter para continuar...")
            
        elif opcion == '13':
            self.print_header("Validar Acceso")
            rut = input("Ingresa el RUT del invitado: ").strip()
            codigo = input("Ingresa el código del evento: ").strip()
            if rut and codigo:
                resultado = self.queries.validar_acceso_evento(rut, codigo)
                self.print_validacion_acceso(resultado)
            input("\nPresiona Enter para continuar...")
            
        else:
            print("\n⚠️ Opción no válida")
            input("Presiona Enter para continuar...")