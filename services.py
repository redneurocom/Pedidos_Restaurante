from models import Mesa, Pedido, DetallePedido, Producto, Factura, DetalleFactura
from repository import Repository
from datetime import datetime

class PedidoService:
    def __init__(self, repo: Repository):
        self.repo = repo

    def crear_pedido(self, mesa_numero: int, mesero_id: int, productos: list):
        try:
            mesa = self.repo.get_by_numero(Mesa, mesa_numero)
            if not mesa:
                raise ValueError(f"Mesa {mesa_numero} no existe.")
            if mesa.estado == "Ocupada":
                raise ValueError("La mesa ya está ocupada.")

            # Crear el pedido
            pedido = Pedido(_mesa_id=mesa.id, _mesero_id=mesero_id)
            self.repo.add(pedido)  # Guardar el pedido para obtener su ID

            # Crear los detalles del pedido
            for prod_id, cantidad in productos:
                producto = self.repo.get(Producto, prod_id)
                if not producto:
                    raise ValueError(f"Producto con ID {prod_id} no existe.")
                if cantidad <= 0:
                    raise ValueError("La cantidad debe ser mayor que cero.")

                for _ in range(cantidad):
                    detalle = DetallePedido(
                        _pedido_id=pedido.id,
                        _producto_id=prod_id,
                        _estado="Pedido realizado",
                        _fecha_creacion=datetime.now()
                    )
                    self.repo.add(detalle)  # Guardar el detalle en la base de datos
                    pedido.detalles.append(detalle)  # Asociar el detalle al pedido

            # Cambiar el estado de la mesa a "Ocupada"
            mesa._cambiar_estado("Ocupada")
            self.repo.update(mesa)

            print(f"Pedido {pedido.id} creado con {len(pedido.detalles)} detalle(s) para la mesa {mesa_numero}.")
        except Exception as e:
            self.repo.session.rollback()
            raise e

    def cambiar_estado(self, pedido_id: int, nuevo_estado: str):
        try:
            pedido = self.repo.get(Pedido, pedido_id)
            if not pedido:
                raise ValueError("Pedido no encontrado.")
            detalles_actualizados = False
            allowed_states = ["Pedido realizado", "En preparación", "Entregado", "Finalizado"]
            for detalle in pedido.detalles:
                if detalle.estado in allowed_states:
                    detalle._cambiar_estado(nuevo_estado)
                    self.repo.update(detalle)
                    detalles_actualizados = True
            if detalles_actualizados and all(d.estado == nuevo_estado for d in pedido.detalles):
                pedido._cambiar_estado(nuevo_estado)
                self.repo.update(pedido)
                print(f"Pedido {pedido_id} y todos sus detalles actualizados a '{nuevo_estado}'.")
            else:
                print(f"Algunos detalles del pedido {pedido_id} no se pudieron actualizar.")
        except Exception as e:
            self.repo.session.rollback()
            raise e

    def cambiar_estado_detalle(self, detalle_id: int, nuevo_estado: str):
        try:
            detalle = self.repo.get(DetallePedido, detalle_id)
            if not detalle:
                raise ValueError("Detalle de pedido no encontrado.")
            detalle._cambiar_estado(nuevo_estado)
            self.repo.update(detalle)
            pedido = self.repo.get(Pedido, detalle._pedido_id)
            if all(d.estado == nuevo_estado for d in pedido.detalles):
                pedido._cambiar_estado(nuevo_estado)
                self.repo.update(pedido)
                print(f"Detalle {detalle_id} y pedido {pedido.id} sincronizados a '{nuevo_estado}'.")
            else:
                print(f"Estado del detalle {detalle_id} actualizado a '{nuevo_estado}'.")
        except Exception as e:
            self.repo.session.rollback()
            raise e



class FacturaService:
    def __init__(self, repo: Repository):
        self.repo = repo

    def facturar_mesa(self, mesa_numero: int):
        try:
            mesa = self.repo.get_by_numero(Mesa, mesa_numero)
            if not mesa:
                raise ValueError(f"Mesa {mesa_numero} no existe.")

            pedidos_finalizados = [p for p in mesa.pedidos if p.estado == "Finalizado"]
            if not pedidos_finalizados:
                raise ValueError("No hay pedidos finalizados para facturar.")

            items = {}
            fecha_pedido = None
            mesero_nombre = ""
            for pedido in pedidos_finalizados:
                if not fecha_pedido:
                    fecha_pedido = pedido._fecha_inicio
                if not mesero_nombre and pedido.mesero:
                    mesero_nombre = pedido.mesero.nombre
                for detalle in pedido.detalles:
                    prod = detalle.producto
                    if not prod:
                        continue
                    precio = prod.precio if prod.precio is not None else 0.0
                    if prod.id not in items:
                        items[prod.id] = {
                            "nombre": prod.nombre,
                            "cantidad": 0,
                            "precio_unitario": precio,
                            "pedido_id": pedido.id
                        }
                    else:
                        if items[prod.id]["precio_unitario"] is None:
                            items[prod.id]["precio_unitario"] = precio
                    items[prod.id]["cantidad"] += 1

            factura = Factura(
                _mesa_id=mesa.id,
                _mesero_id=pedidos_finalizados[0]._mesero_id,
                _fecha_hora=datetime.now(),
                _total=0
            )
            self.repo.add(factura)
            total_fac = 0.0

            for prod_id, info in items.items():
                cantidad = info["cantidad"]
                precio_unitario = info["precio_unitario"]
                subtotal = cantidad * precio_unitario
                total_fac += subtotal

                detalle_fac = DetalleFactura()
                detalle_fac._factura_id = factura.id
                detalle_fac._pedido_id = info["pedido_id"]
                detalle_fac.producto_id = prod_id
                # Asignar primero precio_unitario y luego cantidad
                detalle_fac.precio_unitario = precio_unitario
                detalle_fac.cantidad = cantidad

                factura.detalles.append(detalle_fac)
                self.repo.add(detalle_fac)

            factura._total = total_fac
            self.repo.update(factura)

            # Actualizar el estado de cada pedido finalizado a "Facturado"
            for pedido in pedidos_finalizados:
                pedido._estado = "Facturado"
                self.repo.update(pedido)

            # Liberar la mesa
            mesa._cambiar_estado("Libre")
            self.repo.update(mesa)

            print("\n===== FACTURA =====")
            print(f"Mesa: {mesa.numero}")
            print(f"Mesero: {mesero_nombre}")
            print(f"Fecha del pedido: {fecha_pedido:%Y-%m-%d %H:%M:%S}")
            print("\nDetalle de Ítems:")
            print("{:<30s} {:>5s} {:>10s} {:>10s}".format("Producto", "Cant", "Precio", "Subtotal"))
            for info in items.values():
                subtotal_display = info["cantidad"] * info["precio_unitario"]
                print("{:<30s} {:>5d} {:>10.2f} {:>10.2f}".format(
                    info["nombre"],
                    info["cantidad"],
                    info["precio_unitario"],
                    subtotal_display))
            print("-" * 60)
            print(f"Total: S/. {factura._total:.2f}")
        except Exception as e:
            self.repo.session.rollback()
            raise e