from datetime import date
from models import Empleado, Mesa, Producto, Pedido, Factura, DetallePedido
from repository import Repository
from services import PedidoService, FacturaService
from getpass import getpass
from sqlalchemy.orm import sessionmaker
from models import engine

SessionLocal = sessionmaker(bind=engine)

class SesionUsuario:
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SesionUsuario, cls).__new__(cls)
            cls._instance._empleado_actual = None
        return cls._instance

    def login(self, repo: Repository, codigo: str, clave: str) -> bool:
        empleado = repo.get_by_codigo(Empleado, codigo)
        if empleado and empleado._verificar_clave(clave):
            self._empleado_actual = empleado
            return True
        return False

    def logout(self):
        self._empleado_actual = None

    @property
    def empleado_actual(self):
        return self._empleado_actual

def cargar_datos_iniciales(repo: Repository):
    if not repo.get_all(Empleado):
        empleados = [
            Empleado(_codigo="M001", _nombre="Juan Pérez", _rol="Mesero", _clave="1234"),
            Empleado(_codigo="M002", _nombre="María Gómez", _rol="Mesero", _clave="1234"),
            Empleado(_codigo="M003", _nombre="Carlos López", _rol="Mesero", _clave="1234"),
            Empleado(_codigo="C001", _nombre="Ana Ramírez", _rol="Cocinero", _clave="1234"),
            Empleado(_codigo="C002", _nombre="Pedro Sánchez", _rol="Cocinero", _clave="1234"),
            Empleado(_codigo="C003", _nombre="Luisa Fernández", _rol="Cocinero", _clave="1234"),
            Empleado(_codigo="A001", _nombre="Sofía Torres", _rol="Ayudante de Cocina", _clave="1234"),
            Empleado(_codigo="A002", _nombre="Diego Vargas", _rol="Ayudante de Cocina", _clave="1234"),
            Empleado(_codigo="V001", _nombre="Clara Morales", _rol="Vajillero", _clave="1234"),
            Empleado(_codigo="V002", _nombre="Raúl Castro", _rol="Vajillero", _clave="1234"),
            Empleado(_codigo="E001", _nombre="Laura Mendoza", _rol="Encargado/Cajero", _clave="1234"),
            Empleado(_codigo="B001", _nombre="Gabriel Rojas", _rol="Bartender", _clave="1234"),
            Empleado(_codigo="G001", _nombre="Miguel Herrera", _rol="Vigilante", _clave="1234"),
        ]
        for emp in empleados:
            repo.add(emp)
        print("Empleados cargados exitosamente.")
    if not repo.get_all(Mesa):
        for i in range(1, 16):
            mesa = Mesa(_numero=i, _estado="Libre")
            repo.add(mesa)
        print("Mesas cargadas exitosamente.")
    if not repo.get_all(Producto):
        productos = [
            Producto(_nombre="Lomo Fino", _categoria="Al Fuego", _precio=48),
            Producto(_nombre="Baby Beef", _categoria="Al Fuego", _precio=48),
            Producto(_nombre="Bife Angosto", _categoria="Al Fuego", _precio=42),
            Producto(_nombre="Bife Ancho", _categoria="Al Fuego", _precio=42),
            Producto(_nombre="Pierna o Pecho", _categoria="Al Fuego", _precio=35),
            Producto(_nombre="Hamburguesa Smash", _categoria="Aperitivos", _precio=29),
            Producto(_nombre="Langostinos al Panko", _categoria="Aperitivos", _precio=32),
            Producto(_nombre="Tiradito de Lenguado o Corvina", _categoria="Aperitivos", _precio=50),
            Producto(_nombre="Pulpo a la Parrilla", _categoria="Aperitivos", _precio=48),
            Producto(_nombre="Osobuco con Aligot de Papas", _categoria="Aperitivos", _precio=38),
            Producto(_nombre="Salchiwok", _categoria="Aperitivos", _precio=39),
            Producto(_nombre="Salchipremium", _categoria="Aperitivos", _precio=35),
            Producto(_nombre="Brownie con Helado", _categoria="Postres", _precio=18),
            Producto(_nombre="Pizza de Nutella", _categoria="Postres", _precio=26),
            Producto(_nombre="Pan al Ajo (4 unidades)", _categoria="Piqueos", _precio=12),
            Producto(_nombre="Pan al Ajo (8 unidades)", _categoria="Piqueos", _precio=20),
            Producto(_nombre="Tequeños Fusión", _categoria="Piqueos", _precio=28),
            Producto(_nombre="Tequeños Clásicos", _categoria="Piqueos", _precio=23),
            Producto(_nombre="Pizza Roll Americana", _categoria="Pizzas Roll", _precio=13.90),
            Producto(_nombre="Pizza Roll Hawaiana", _categoria="Pizzas Roll", _precio=14.90),
            Producto(_nombre="Pizza Roll Pollo BBQ", _categoria="Pizzas Roll", _precio=18.90),
            Producto(_nombre="Pizza Roll Huachana", _categoria="Pizzas Roll", _precio=19.90),
            Producto(_nombre="Pizza Americana", _categoria="Pizzas Clásicas", _precio=49),
            Producto(_nombre="Pizza Hawaiana", _categoria="Pizzas Clásicas", _precio=52),
            Producto(_nombre="Pizza Peperoni", _categoria="Pizzas Clásicas", _precio=50),
            Producto(_nombre="Pizza Fugazzeta", _categoria="Pizzas Clásicas", _precio=47),
            Producto(_nombre="Pizza Champiñones", _categoria="Pizzas Clásicas", _precio=55),
            Producto(_nombre="Pizza de Lomo Saltado", _categoria="Pizzas Fusión", _precio=68),
            Producto(_nombre="Pizza Sabor \\& Sazón", _categoria="Pizzas Fusión", _precio=69),
            Producto(_nombre="Pizza al Pesto Norteño", _categoria="Pizzas Fusión", _precio=68),
            Producto(_nombre="Pizza de Ají de Gallina", _categoria="Pizzas Fusión", _precio=58),
            Producto(_nombre="Pizza Pollo BBQ", _categoria="Pizzas Fusión", _precio=60),
            Producto(_nombre="Pizza New York", _categoria="Pizzas Fusión", _precio=60),
            Producto(_nombre="Pizza Parrillera", _categoria="Pizzas Fusión", _precio=61),
            Producto(_nombre="Pizza Napolitana", _categoria="Pizzas Fusión", _precio=55),
            Producto(_nombre="Pizza Huachana", _categoria="Pizzas Fusión", _precio=55),
            Producto(_nombre="Lomo Fino Saltado", _categoria="Especialidad de la Casa", _precio=38),
            Producto(_nombre="Pasta a la Huancaína con Lomo", _categoria="Pastas", _precio=38),
            Producto(_nombre="Pasta Sabor \\& Sazón", _categoria="Pastas", _precio=39),
            Producto(_nombre="Pasta de Langostinos", _categoria="Pastas", _precio=43),
            Producto(_nombre="Pasta al Alfredo", _categoria="Pastas", _precio=31),
            Producto(_nombre="Pasta a la Boloñesa", _categoria="Pastas", _precio=35),
            Producto(_nombre="Pasta a la Carbonara", _categoria="Pastas", _precio=34),
            Producto(_nombre="Ravioles con Carne al Vino", _categoria="Pastas", _precio=39),
            Producto(_nombre="Lasagna Bolognesa", _categoria="Lasagnas", _precio=36),
            Producto(_nombre="Lasagna de Lomo Saltado", _categoria="Lasagnas", _precio=39),
            Producto(_nombre="Lasagna Sabor \\& Sazón", _categoria="Lasagnas", _precio=41),
            Producto(_nombre="Lasagna de Seco a la Huachana", _categoria="Lasagnas", _precio=41),
        ]
        for prod in productos:
            repo.add(prod)
        print("Productos cargados exitosamente.")

def mostrar_menu_productos(repo: Repository):
    productos = repo.get_all(Producto)
    print("\nProductos disponibles:")
    for prod in productos:
        print(f"ID: {prod.id}, {prod.nombre} ({prod._categoria}) - S/. {prod.precio:.2f}")

def tomar_pedido(repo: Repository, pedido_service: PedidoService, mesero_id: int):
    try:
        mesa_numero = int(input("Número de la mesa (1-15): "))
        if mesa_numero < 1 or mesa_numero > 15:
            raise ValueError("Número de mesa inválido.")
        mesa = repo.get_by_numero(Mesa, mesa_numero)
        if not mesa:
            raise ValueError(f"Mesa {mesa_numero} no existe.")
        if mesa.estado != "Libre":
            print(f"Error: la mesa {mesa_numero} ya está ocupada.")
            return
        mostrar_menu_productos(repo)
        productos = []
        while True:
            prod_input = input("ID del producto (0 para terminar): ")
            if prod_input == "0":
                break
            try:
                prod_id = int(prod_input)
            except ValueError:
                print("Error: ID inválido.")
                continue
            productos_disponibles = repo.get_all(Producto)
            producto_encontrado = next((prod for prod in productos_disponibles if prod.id == prod_id), None)
            if not producto_encontrado:
                print("Error: Producto no existe.")
                continue
            try:
                cantidad = int(input("Cantidad: "))
            except ValueError:
                print("Error: cantidad inválida.")
                continue
            if cantidad <= 0:
                print("Error: la cantidad debe ser mayor que cero.")
                continue
            productos.append((prod_id, cantidad))
        if not productos:
            print("No se seleccionaron productos.")
            return
        pedido_service.crear_pedido(mesa_numero, mesero_id, productos)
    except ValueError as e:
        print(f"Error: {e}")

# python
# python
def ver_cola_pedidos(repo: Repository):
    pedidos = repo.get_all(Pedido)
    if not pedidos:
        print("No hay pedidos en la cola.")
        return
    print("\nCola de Pedidos:")
    for pedido in pedidos:
        mesero_nombre = pedido.mesero.nombre if pedido.mesero else "Sin Mesero"
        print(f"Pedido ID: {pedido.id}, Mesa: {pedido.mesa.numero}, Estado: {pedido.estado}, Mesero: {mesero_nombre}")
        print("Detalles:")
        for idx, detalle in enumerate(pedido.detalles, start=1):
            linea = f"  Item {idx}: Producto: {detalle.producto.nombre}, Estado: {detalle.estado}"
            if detalle.estado == "Pedido realizado":
                linea += f", Creado: {detalle._fecha_creacion:%H:%M:%S}"
            elif detalle.estado == "En preparación":
                if detalle._inicio_preparacion:
                    linea += f", Inicio preparación: {detalle._inicio_preparacion:%H:%M:%S}"
            elif detalle.estado == "Entregado":
                if detalle._inicio_preparacion and detalle._fin_preparacion:
                    linea += f", Inicio: {detalle._inicio_preparacion:%H:%M:%S}, Fin: {detalle._fin_preparacion:%H:%M:%S}, Duración: {detalle._duracion_preparacion:.2f} min"
            elif detalle.estado == "Finalizado":
                if detalle._fin_finalizacion:
                    linea += f", Finalizado: {detalle._fin_finalizacion:%H:%M:%S}"
            print(linea)
        print("-" * 50)

def cambiar_estado_global(repo: Repository, pedido_service: PedidoService):
    pedidos_cambiables = [p for p in repo.get_all(Pedido) if p.estado in ["Pedido realizado", "En preparación", "Entregado"]]
    if not pedidos_cambiables:
        print("No hay pedidos que permitan cambio global de estado.")
        return
    print("Pedidos disponibles para cambio global:")
    for idx, pedido in enumerate(pedidos_cambiables, 1):
        print(f"{idx}. Pedido ID: {pedido.id}, Mesa: {pedido.mesa.numero}, Estado: {pedido.estado}")
    opcion = int(input("Seleccione el pedido a modificar: "))
    if 1 <= opcion <= len(pedidos_cambiables):
        pedido_seleccionado = pedidos_cambiables[opcion - 1]
    else:
        print("Opción inválida.")
        return
    if pedido_seleccionado.estado == "Pedido realizado":
        nuevos_estados = ["En preparación"]
    elif pedido_seleccionado.estado == "En preparación":
        nuevos_estados = ["Entregado"]
    elif pedido_seleccionado.estado == "Entregado":
        nuevos_estados = ["Finalizado"]
    else:
        print("El pedido no puede cambiar de estado.")
        return
    print("Seleccione nuevo estado global:")
    for i, estado in enumerate(nuevos_estados, 1):
        print(f"{i}. {estado}")
    idx = int(input("Opción: "))
    if 1 <= idx <= len(nuevos_estados):
        nuevo_estado = nuevos_estados[idx - 1]
        pedido_service.cambiar_estado(pedido_seleccionado.id, nuevo_estado)
    else:
        print("Opción inválida.")

def cambiar_estado_detalle(repo: Repository, pedido_service: PedidoService):
    # Se agrupan los detalles cambiables por pedido
    agrupados = {}
    for pedido in repo.get_all(Pedido):
        detalles_cambiables = []
        for detalle in pedido.detalles:
            if detalle.estado in ["Pedido realizado", "En preparación", "Entregado"]:
                detalles_cambiables.append(detalle)
        if detalles_cambiables:
            agrupados[pedido.id] = detalles_cambiables

    if not agrupados:
        print("No hay detalles que permitan cambio de estado individual.")
        return

    # Se crea un mapeo de opción secuencial a un detalle
    opcion_map = {}
    opcion_num = 1
    print("Detalles agrupados por Pedido:")
    for pedido_id, detalles in agrupados.items():
        pedido = repo.get(Pedido, pedido_id)
        print(f"Pedido ID: {pedido_id}, Mesa: {pedido.mesa.numero}, Mesero: {pedido.mesero.nombre}")
        for idx, detalle in enumerate(detalles, start=1):
            print(f"  {opcion_num}. Item {idx}: Producto: {detalle.producto.nombre}, Estado: {detalle.estado}")
            opcion_map[opcion_num] = detalle
            opcion_num += 1

    try:
        opcion = int(input("Seleccione el número de opción del detalle a modificar: "))
    except ValueError:
        print("Opción inválida.")
        return

    if opcion not in opcion_map:
        print("Opción inválida.")
        return

    detalle_seleccionado = opcion_map[opcion]
    if detalle_seleccionado.estado == "Pedido realizado":
        nuevos_estados = ["En preparación"]
    elif detalle_seleccionado.estado == "En preparación":
        nuevos_estados = ["Entregado"]
    elif detalle_seleccionado.estado == "Entregado":
        nuevos_estados = ["Finalizado"]
    else:
        print("El detalle no puede cambiar de estado.")
        return

    print("Seleccione nuevo estado para el detalle:")
    for i, estado in enumerate(nuevos_estados, 1):
        print(f"{i}. {estado}")
    try:
        idx = int(input("Opción: "))
    except ValueError:
        print("Opción inválida.")
        return

    if 1 <= idx <= len(nuevos_estados):
        nuevo_estado = nuevos_estados[idx - 1]
        pedido_service.cambiar_estado_detalle(detalle_seleccionado.id, nuevo_estado)
    else:
        print("Opción inválida.")

def ver_disponibilidad_mesas(repo: Repository):
    mesas = repo.get_all(Mesa)
    print("\nDisponibilidad de Mesas:")
    for mesa in mesas:
        print(f"Mesa {mesa.numero}: {mesa.estado}")

def menu():
    session = SessionLocal()
    repo = Repository(session)
    pedido_service = PedidoService(repo)
    factura_service = FacturaService(repo)
    sesion = SesionUsuario()
    cargar_datos_iniciales(repo)
    while True:
        if not sesion.empleado_actual:
            codigo = input("Código de empleado: ")
            clave = input("Clave: ")
            if sesion.login(repo, codigo, clave):
                print(f"Bienvenido, {sesion.empleado_actual.nombre}")
            else:
                print("Credenciales incorrectas, intente de nuevo.")
                continue
        print("\n--- Menú del Restaurante ---")
        print("1. Cambiar Usuario")
        print("2. Tomar Pedido")
        print("3. Ver Cola de Pedidos")
        print("4. Facturar Mesa")
        print("5. Ver Disponibilidad de Mesas")
        print("6. Cambiar estado de pedido global")
        print("7. Cambiar estado de detalle de pedido individual")
        print("8. Resumen Facturación Diaria")
        print("9. Salir")
        opcion = input("Seleccione una opción: ")
        try:
            if opcion == "1":
                sesion.logout()
            elif opcion == "2":
                tomar_pedido(repo, pedido_service, sesion.empleado_actual.id)
            elif opcion == "3":
                ver_cola_pedidos(repo)
            elif opcion == "4":
                mesas_finalizadas = [mesa for mesa in repo.get_all(Mesa) if any(p.estado == "Finalizado" for p in mesa.pedidos)]
                if not mesas_finalizadas:
                    print("No hay órdenes finalizadas para facturar.")
                else:
                    print("\nÓrdenes finalizadas disponibles para facturar:")
                    for idx, mesa in enumerate(mesas_finalizadas, 1):
                        pedidos_finalizados = [p for p in mesa.pedidos if p.estado == "Finalizado"]
                        print(f"{idx}. Mesa {mesa.numero} (Pedidos finalizados: {len(pedidos_finalizados)})")
                    opcion_mesa = int(input("Seleccione la opción de mesa a facturar: "))
                    if 1 <= opcion_mesa <= len(mesas_finalizadas):
                        mesa_seleccionada = mesas_finalizadas[opcion_mesa - 1]
                        factura_service.facturar_mesa(mesa_seleccionada.numero)
                    else:
                        print("Opción inválida.")
            elif opcion == "5":
                ver_disponibilidad_mesas(repo)
            elif opcion == "6":
                cambiar_estado_global(repo, pedido_service)
            elif opcion == "7":
                cambiar_estado_detalle(repo, pedido_service)
            elif opcion == "8":
                facturas = repo.get_all(Factura)
                if not facturas:
                    print("No hay facturas registradas.")
                else:
                    from collections import defaultdict
                    grupos = defaultdict(list)
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
            elif opcion == "9":
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