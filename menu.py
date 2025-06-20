# Este archivo contiene la interfaz de consola para interactuar con el sistema del restaurante.
# Incluye el menú principal, la gestión de sesiones de usuario y la carga de datos iniciales.
from datetime import date

from models import Empleado, Mesa, Producto, Pedido, Factura
from repository import Repository
from services import PedidoService, FacturaService
from getpass import getpass
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker
from models import engine
# Configurar la sesión ligada al engine
SessionLocal = sessionmaker(bind=engine)
class SesionUsuario:
    """
    Clase Singleton para manejar la sesión del usuario.
    Atributos:
        _instance (SesionUsuario): Instancia única de la clase.
        _empleado_actual (Empleado): Empleado actualmente logueado (privado).
    """
    _instance = None

    def __new__(cls):
        """Crea o retorna la instancia única de la clase."""
        if cls._instance is None:
            cls._instance = super(SesionUsuario, cls).__new__(cls)
            cls._instance._empleado_actual = None
        return cls._instance

    def login(self, repo: Repository, codigo: str, clave: str) -> bool:
        """
        Inicia sesión con el código y clave del empleado.
        Parámetros:
            repo (Repository): Repositorio para acceder a la base de datos.
            codigo (str): Código del empleado.
            clave (str): Clave del empleado.
        Retorna:
            bool: True si el login es exitoso, False si falla.
        """
        empleado = repo.get_by_codigo(Empleado, codigo)
        if empleado and empleado._verificar_clave(clave):
            self._empleado_actual = empleado
            return True
        return False

    def logout(self):
        """Cierra la sesión actual del empleado."""
        self._empleado_actual = None

    @property
    def empleado_actual(self):
        """Propiedad para acceder al empleado actualmente logueado."""
        return self._empleado_actual

def cargar_datos_iniciales(repo: Repository):
    """
    Carga datos iniciales de empleados, mesas y productos si no existen en la base de datos.
    Parámetros:
        repo (Repository): Repositorio para operaciones CRUD.
    """
    # Cargar empleados (solo si no existen)
    if not repo.get_all(Empleado):
        empleados = [
            # Meseros
            Empleado(_codigo="M001", _nombre="Juan Pérez", _rol="Mesero", _clave="1234"),
            Empleado(_codigo="M002", _nombre="María Gómez", _rol="Mesero", _clave="1234"),
            Empleado(_codigo="M003", _nombre="Carlos López", _rol="Mesero", _clave="1234"),
            # Cocineros
            Empleado(_codigo="C001", _nombre="Ana Ramírez", _rol="Cocinero", _clave="1234"),
            Empleado(_codigo="C002", _nombre="Pedro Sánchez", _rol="Cocinero", _clave="1234"),
            Empleado(_codigo="C003", _nombre="Luisa Fernández", _rol="Cocinero", _clave="1234"),
            # Ayudantes de cocina
            Empleado(_codigo="A001", _nombre="Sofía Torres", _rol="Ayudante de Cocina", _clave="1234"),
            Empleado(_codigo="A002", _nombre="Diego Vargas", _rol="Ayudante de Cocina", _clave="1234"),
            # Vajilleros
            Empleado(_codigo="V001", _nombre="Clara Morales", _rol="Vajillero", _clave="1234"),
            Empleado(_codigo="V002", _nombre="Raúl Castro", _rol="Vajillero", _clave="1234"),
            # Encargado/Cajero
            Empleado(_codigo="E001", _nombre="Laura Mendoza", _rol="Encargado/Cajero", _clave="1234"),
            # Bartender
            Empleado(_codigo="B001", _nombre="Gabriel Rojas", _rol="Bartender", _clave="1234"),
            # Vigilante
            Empleado(_codigo="G001", _nombre="Miguel Herrera", _rol="Vigilante", _clave="1234"),
        ]
        for emp in empleados:
            repo.add(emp)
        print("Empleados cargados exitosamente.")

    # Cargar mesas (1 a 15)
    if not repo.get_all(Mesa):
        for i in range(1, 16):
            mesa = Mesa(_numero=i, _estado="Libre")
            repo.add(mesa)
        print("Mesas cargadas exitosamente.")

    # Cargar productos (carta completa del restaurante)
    if not repo.get_all(Producto):
        productos = [
            # Al Fuego
            Producto(_nombre="Lomo Fino", _categoria="Al Fuego", _precio=48),
            Producto(_nombre="Baby Beef", _categoria="Al Fuego", _precio=48),
            Producto(_nombre="Bife Angosto", _categoria="Al Fuego", _precio=42),
            Producto(_nombre="Bife Ancho", _categoria="Al Fuego", _precio=42),
            Producto(_nombre="Pierna o Pecho", _categoria="Al Fuego", _precio=35),
            # Aperitivos
            Producto(_nombre="Hamburguesa Smash", _categoria="Aperitivos", _precio=29),
            Producto(_nombre="Langostinos al Panko", _categoria="Aperitivos", _precio=32),
            Producto(_nombre="Tiradito de Lenguado o Corvina", _categoria="Aperitivos", _precio=50),
            Producto(_nombre="Pulpo a la Parrilla", _categoria="Aperitivos", _precio=48),
            Producto(_nombre="Osobuco con Aligot de Papas", _categoria="Aperitivos", _precio=38),
            Producto(_nombre="Salchiwok", _categoria="Aperitivos", _precio=39),
            Producto(_nombre="Salchipremium", _categoria="Aperitivos", _precio=35),
            # Postres
            Producto(_nombre="Brownie con Helado", _categoria="Postres", _precio=18),
            Producto(_nombre="Pizza de Nutella", _categoria="Postres", _precio=26),
            # Piqueos
            Producto(_nombre="Pan al Ajo (4 unidades)", _categoria="Piqueos", _precio=12),
            Producto(_nombre="Pan al Ajo (8 unidades)", _categoria="Piqueos", _precio=20),
            Producto(_nombre="Tequeños Fusión", _categoria="Piqueos", _precio=28),
            Producto(_nombre="Tequeños Clásicos", _categoria="Piqueos", _precio=23),
            # Pizzas Roll
            Producto(_nombre="Pizza Roll Americana", _categoria="Pizzas Roll", _precio=13.90),
            Producto(_nombre="Pizza Roll Hawaiana", _categoria="Pizzas Roll", _precio=14.90),
            Producto(_nombre="Pizza Roll Pollo BBQ", _categoria="Pizzas Roll", _precio=18.90),
            Producto(_nombre="Pizza Roll Huachana", _categoria="Pizzas Roll", _precio=19.90),
            # Pizzas Clásicas
            Producto(_nombre="Pizza Americana", _categoria="Pizzas Clásicas", _precio=49),
            Producto(_nombre="Pizza Hawaiana", _categoria="Pizzas Clásicas", _precio=52),
            Producto(_nombre="Pizza Peperoni", _categoria="Pizzas Clásicas", _precio=50),
            Producto(_nombre="Pizza Fugazzeta", _categoria="Pizzas Clásicas", _precio=47),
            Producto(_nombre="Pizza Champiñones", _categoria="Pizzas Clásicas", _precio=55),
            # Pizzas Fusión
            Producto(_nombre="Pizza de Lomo Saltado", _categoria="Pizzas Fusión", _precio=68),
            Producto(_nombre="Pizza Sabor & Sazón", _categoria="Pizzas Fusión", _precio=69),
            Producto(_nombre="Pizza al Pesto Norteño", _categoria="Pizzas Fusión", _precio=68),
            Producto(_nombre="Pizza de Ají de Gallina", _categoria="Pizzas Fusión", _precio=58),
            Producto(_nombre="Pizza Pollo BBQ", _categoria="Pizzas Fusión", _precio=60),
            Producto(_nombre="Pizza New York", _categoria="Pizzas Fusión", _precio=60),
            Producto(_nombre="Pizza Parrillera", _categoria="Pizzas Fusión", _precio=61),
            Producto(_nombre="Pizza Napolitana", _categoria="Pizzas Fusión", _precio=55),
            Producto(_nombre="Pizza Huachana", _categoria="Pizzas Fusión", _precio=55),
            # Especialidad de la Casa
            Producto(_nombre="Lomo Fino Saltado", _categoria="Especialidad de la Casa", _precio=38),
            # Pastas
            Producto(_nombre="Pasta a la Huancaína con Lomo", _categoria="Pastas", _precio=38),
            Producto(_nombre="Pasta Sabor & Sazón", _categoria="Pastas", _precio=39),
            Producto(_nombre="Pasta de Langostinos", _categoria="Pastas", _precio=43),
            Producto(_nombre="Pasta al Alfredo", _categoria="Pastas", _precio=31),
            Producto(_nombre="Pasta a la Boloñesa", _categoria="Pastas", _precio=35),
            Producto(_nombre="Pasta a la Carbonara", _categoria="Pastas", _precio=34),
            Producto(_nombre="Ravioles con Carne al Vino", _categoria="Pastas", _precio=39),
            # Lasagnas
            Producto(_nombre="Lasagna Bolognesa", _categoria="Lasagnas", _precio=36),
            Producto(_nombre="Lasagna de Lomo Saltado", _categoria="Lasagnas", _precio=39),
            Producto(_nombre="Lasagna Sabor & Sazón", _categoria="Lasagnas", _precio=41),
            Producto(_nombre="Lasagna de Seco a la Huachana", _categoria="Lasagnas", _precio=41),
        ]
        for prod in productos:
            repo.add(prod)
        print("Productos cargados exitosamente.")

def mostrar_menu_productos(repo: Repository):
    """
    Muestra la lista de productos disponibles en la consola.
    Parámetros:
        repo (Repository): Repositorio para acceder a los productos.
    """
    productos = repo.get_all(Producto)
    print("\nProductos disponibles:")
    for prod in productos:
        print(f"ID: {prod.id}, {prod.nombre} ({prod._categoria}) - S/. {prod.precio:.2f}")

def tomar_pedido(repo: Repository, pedido_service: PedidoService, mesero_id: int):
    """
    Permite al mesero tomar un pedido para una mesa.
    Parámetros:
        repo (Repository): Repositorio para operaciones CRUD.
        pedido_service (PedidoService): Servicio para gestionar pedidos.
        mesero_id (int): ID del mesero logueado.
    """
    try:
        mesa_numero = int(input("Número de la mesa (1-15): "))
        if mesa_numero < 1 or mesa_numero > 15:
            raise ValueError("Número de mesa inválido.")

        mostrar_menu_productos(repo)
        productos = []
        while True:
            prod_id = input("ID del producto (0 para terminar): ")
            if prod_id == "0":
                break
            cantidad = int(input("Cantidad: "))
            productos.append((int(prod_id), cantidad))

        if not productos:
            print("No se seleccionaron productos.")
            return

        pedido_service.crear_pedido(mesa_numero, mesero_id, productos)
    except ValueError as e:
        print(f"Error: {e}")

def ver_cola_pedidos(repo: Repository):
    """
    Muestra la cola de pedidos con sus estados, fechas y meseros.
    Parámetros:
        repo (Repository): Repositorio para acceder a los pedidos.
    """
    pedidos = repo.get_all(Pedido)
    if not pedidos:
        print("No hay pedidos en la cola.")
        return

    print("\nCola de Pedidos:")
    for pedido in pedidos:
        print(f"Pedido ID: {pedido.id}, Mesa: {pedido.mesa.numero}, Estado: {pedido.estado}")
        print(f"Mesero: {pedido.mesero.nombre}, Inicio: {pedido._fecha_inicio}")
        if pedido._fecha_fin:
            print(f"Finalizado: {pedido._fecha_fin}")
        print("Detalles:")
        for detalle in pedido.detalles:
            print(f"  {detalle.producto.nombre} x{detalle._cantidad}")
        print("-" * 50)

def solicitar_login(repo: Repository, sesion: SesionUsuario):
    """Solicita código y clave hasta login exitoso."""
    while True:
        codigo = input("Código de empleado: ")
        clave = input("Clave: ")
        if sesion.login(repo, codigo, clave):
            print(f"Bienvenido, {sesion.empleado_actual.nombre}")
            break
        print("Credenciales incorrectas, intente de nuevo.")


def ver_disponibilidad_mesas(repo: Repository):
    """
    Muestra el estado de todas las mesas (Libre/Ocupada).
    Parámetros:
        repo (Repository): Repositorio para acceder a las mesas.
    """
    mesas = repo.get_all(Mesa)
    print("\nDisponibilidad de Mesas:")
    for mesa in mesas:
        print(f"Mesa {mesa.numero}: {mesa.estado}")

def menu():
    """
    Menú principal del sistema para interactuar con las funcionalidades del restaurante.
    Inicializa los servicios y ejecuta el bucle del menú.
    """
    session = SessionLocal()
    repo = Repository(session)
    pedido_service = PedidoService(repo)
    factura_service = FacturaService(repo)
    sesion = SesionUsuario()

    # Cargar datos iniciales
    cargar_datos_iniciales(repo)
    solicitar_login(repo, sesion)

    while True:
        print("\n--- Menú del Restaurante ---")
        print("1. Cambiar Usuario")
        print("2. Tomar Pedido")
        print("3. Ver Cola de Pedidos")
        print("4. Facturar Mesa")
        print("5. Ver Disponibilidad de Mesas")
        print("6. Cambiar Estado de Pedido")
        print("7. Resumen Facturación Diaria")
        print("8. Salir")
        opcion = input("Seleccione una opción: ")

        try:
            if opcion == "1":
                sesion.logout()
                solicitar_login(repo, sesion)
            elif opcion == "2":
                if not sesion.empleado_actual:
                    print("Debe iniciar sesión primero.")
                    continue
                tomar_pedido(repo, pedido_service, sesion.empleado_actual.id)
            elif opcion == "3":
                ver_cola_pedidos(repo)
            elif opcion == "4":
                if not sesion.empleado_actual:
                    print("Debe iniciar sesión primero.")
                    continue
                mesa_numero = int(input("Número de la mesa (1-15): "))
                factura_service.facturar_mesa(mesa_numero)
            elif opcion == "5":
                ver_disponibilidad_mesas(repo)
            elif opcion == "6":
                if not sesion.empleado_actual:
                    print("Debe iniciar sesión primero.")
                    continue
                pedido_id = int(input("ID del pedido: "))
                estados = ["Pedido realizado", "En preparación", "Finalizado"]
                print("Seleccione nuevo estado:")
                for i, e in enumerate(estados, 1):
                    print(f"{i}. {e}")
                idx = int(input("Opción (1-3): "))
                if 1 <= idx <= len(estados):
                    nuevo_estado = estados[idx - 1]
                    pedido_service.cambiar_estado(pedido_id, nuevo_estado)
                else:
                    print("Opción de estado inválida.")
            elif opcion == "7":
                facturas = repo.get_all(Factura)
                if not facturas:
                    print("No hay facturas registradas.")
                else:
                    from collections import defaultdict
                    grupos = defaultdict(list)
                    # Solo facturas con total calculado
                    for f in facturas:
                        if f._total is None:
                            continue
                        grupos[f._fecha_hora.date()].append(f)
                    for fecha in sorted(grupos):
                        print(f"\n=== Resumen de Facturación {fecha:%Y-%m-%d} ===")
                        total_fecha = sum(f._total for f in grupos[fecha])
                        for f in grupos[fecha]:
                            hora = f._fecha_hora.strftime("%H:%M")
                            print(f"Mesa {f.mesa.numero} | Hora {hora} | Mesero {f.mesero.nombre} | Total S/. {f._total:.2f}")
                        print(f"Total del día S/. {total_fecha:.2f}")
            elif opcion == "8":
                print("Saliendo del sistema…")
                session.close()
                break
            else:
                print("Opción no válida, intente de nuevo.")
        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Error inesperado: {e}")

if __name__ == "__main__":
    menu()

# Fin de menu.py