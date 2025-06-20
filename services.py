# Este archivo contiene la lógica de negocio para pedidos y facturación.

from models import Mesa, Pedido, DetallePedido, Producto, Factura, DetalleFactura
from repository import Repository


class PedidoService:
    """
    Servicio para gestionar pedidos en el restaurante.
    Atributos:
        repo (Repository): Instancia del repositorio para operaciones CRUD.
    """
    def __init__(self, repo: Repository):
        """Inicializa el servicio con un repositorio."""
        self.repo = repo

    def crear_pedido(self, mesa_numero: int, mesero_id: int, productos: list):
        """
        Crea un nuevo pedido para una mesa específica.
        Parámetros:
            mesa_numero (int): Número de la mesa.
            mesero_id (int): ID del mesero.
            productos (list): Lista de tuplas (producto_id, cantidad).
        """
        try:
            mesa = self.repo.get_by_numero(Mesa, mesa_numero)
            if not mesa:
                raise ValueError(f"Mesa {mesa_numero} no existe.")
            if mesa.estado == "Ocupada":
                raise ValueError("La mesa ya está ocupada.")

            pedido = Pedido(_mesa_id=mesa.id, _mesero_id=mesero_id)
            self.repo.add(pedido)  # Asegura que el pedido tenga un ID

            for prod_id, cantidad in productos:
                producto = self.repo.get(Producto, prod_id)
                if not producto:
                    raise ValueError(f"Producto con ID {prod_id} no existe.")
                if cantidad <= 0:
                    raise ValueError("La cantidad debe ser mayor a 0.")
                detalle = DetallePedido(_pedido_id=pedido.id, _producto_id=prod_id, _cantidad=cantidad)
                self.repo.add(detalle)

            mesa._cambiar_estado("Ocupada")
            self.repo.update(mesa)
            print(f"Pedido creado para la mesa {mesa_numero}.")
        except Exception as e:
            self.repo.session.rollback()
            raise e

    def cambiar_estado(self, pedido_id: int, nuevo_estado: str):
        """
        Cambia el estado de un pedido existente.
        Parámetros:
            pedido_id (int): ID del pedido.
            nuevo_estado (str): Nuevo estado del pedido.
        """
        try:
            pedido = self.repo.get(Pedido, pedido_id)
            if not pedido:
                raise ValueError("Pedido no encontrado.")
            pedido._cambiar_estado(nuevo_estado)
            self.repo.update(pedido)
            print(f"Estado del pedido {pedido_id} actualizado a {nuevo_estado}.")
        except Exception as e:
            self.repo.session.rollback()
            raise e

class FacturaService:
    """
    Servicio para gestionar la facturación de mesas.
    Atributos:
        repo (Repository): Instancia del repositorio para operaciones CRUD.
    """
    def __init__(self, repo: Repository):
        """Inicializa el servicio con un repositorio."""
        self.repo = repo

    def facturar_mesa(self, mesa_numero: int):
        """
        Genera una factura para una mesa con pedidos finalizados.
        Parámetros:
            mesa_numero (int): Número de la mesa a facturar.
        """
        try:
            mesa = self.repo.get_by_numero(Mesa, mesa_numero)
            if not mesa:
                raise ValueError(f"Mesa {mesa_numero} no existe.")
            if mesa.estado == "Libre":
                raise ValueError("La mesa está libre.")

            pedidos_finalizados = [p for p in mesa.pedidos if p.estado == "Finalizado"]
            if not pedidos_finalizados:
                raise ValueError("No hay pedidos finalizados para facturar.")

            factura = Factura(_mesa_id=mesa.id, _mesero_id=pedidos_finalizados[0]._mesero_id)
            self.repo.add(factura)  # Asegura que la factura tenga un ID

            for pedido in pedidos_finalizados:
                subtotal = sum(d.producto.precio * d._cantidad for d in pedido.detalles)
                detalle = DetalleFactura(_factura_id=factura.id, _pedido_id=pedido.id, _subtotal=subtotal)
                factura.detalles.append(detalle)
                self.repo.add(detalle)

            factura._calcular_total()
            self.repo.update(factura)

            mesa._cambiar_estado("Libre")
            self.repo.update(mesa)

            print(f"\nFactura para Mesa {mesa_numero}")
            print(f"Mesero: {pedidos_finalizados[0].mesero.nombre}")
            print("Detalles:")
            for detalle in factura.detalles:
                pedido = detalle.pedido
                for d in pedido.detalles:
                    print(f"  {d.producto.nombre} x{d._cantidad}: S/. {d.producto.precio * d._cantidad:.2f}")
            print(f"Total: S/. {factura._total:.2f}")
        except Exception as e:
            self.repo.session.rollback()
            raise e