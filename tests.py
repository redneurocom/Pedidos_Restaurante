# Este archivo contiene pruebas unitarias para validar los servicios.

import unittest
from models import Empleado, Mesa, Producto, Pedido, DetallePedido, Factura
from repository import Repository
from services import PedidoService, FacturaService
from sqlalchemy.orm import Session

class TestRestaurante(unittest.TestCase):
    """Clase para pruebas unitarias del sistema de restaurante."""
    def setUp(self):
        """Configura el entorno de prueba antes de cada test."""
        self.session = Session()
        self.repo = Repository(self.session)

        # Crear datos de prueba
        empleado = Empleado(_codigo="TEST001", _nombre="Test Mesero", _rol="Mesero", _clave="1234")
        mesa = Mesa(_numero=1, _estado="Libre")
        producto = Producto(_nombre="Test Plato", _categoria="Test", _precio=10.0)

        self.repo.add(empleado)
        self.repo.add(mesa)
        self.repo.add(producto)

        self.empleado_id = empleado.id
        self.mesa_id = mesa.id
        self.producto_id = producto.id

    def tearDown(self):
        """Limpia el entorno de prueba después de cada test."""
        self.session.rollback()
        self.session.close()

    def test_crear_pedido(self):
        """Prueba la creación de un pedido."""
        pedido_service = PedidoService(self.repo)
        productos = [(self.producto_id, 2)]
        pedido_service.crear_pedido(1, self.empleado_id, productos)

        mesa = self.repo.get_by_numero(Mesa, 1)
        self.assertEqual(mesa.estado, "Ocupada")

        pedidos = [p for p in mesa.pedidos if p.mesero_id == self.empleado_id]
        self.assertEqual(len(pedidos), 1)
        self.assertEqual(pedidos[0].estado, "Pedido realizado")
        self.assertEqual(len(pedidos[0].detalles), 1)
        self.assertEqual(pedidos[0].detalles[0]._cantidad, 2)

    def test_facturar_mesa(self):
        """Prueba la facturación de una mesa."""
        pedido_service = PedidoService(self.repo)
        factura_service = FacturaService(self.repo)

        # Crear pedido
        productos = [(self.producto_id, 2)]
        pedido_service.crear_pedido(1, self.empleado_id, productos)

        # Cambiar estado a Finalizado
        pedido = self.repo.get_all(Pedido)[0]
        pedido_service.cambiar_estado(pedido.id, "Finalizado")

        # Facturar
        factura_service.facturar_mesa(1)

        mesa = self.repo.get_by_numero(Mesa, 1)
        self.assertEqual(mesa.estado, "Libre")

        facturas = self.repo.get_all(Factura)
        self.assertEqual(len(facturas), 1)
        self.assertEqual(facturas[0]._total, 20.0)  # 2 * 10.0

if __name__ == '__main__':
    unittest.main()
