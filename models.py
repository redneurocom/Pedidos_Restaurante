# Este archivo contiene las definiciones de las clases de modelo que representan las tablas de la base de datos.
# Las clases usan atributos privados, propiedades públicas y métodos protegidos según las buenas prácticas de POO.

from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from datetime import datetime

Base = declarative_base()

class Empleado(Base):
    """
    Clase que representa a un empleado del restaurante.
    Atributos:
        id (int): Identificador único del empleado.
        _codigo (str): Código único del empleado (privado).
        _nombre (str): Nombre del empleado (privado).
        _rol (str): Rol del empleado (e.g., mesero, cocinero) (privado).
        _clave (str): Clave de acceso del empleado (privado).
    """
    __tablename__ = 'empleados'
    id = Column(Integer, primary_key=True)
    _codigo = Column(String(20), unique=True)
    _nombre = Column(String(100))
    _rol = Column(String(50))
    _clave = Column(String(128))

    @property
    def codigo(self):
        """Propiedad para acceder al código del empleado."""
        return self._codigo

    @property
    def nombre(self):
        """Propiedad para acceder al nombre del empleado."""
        return self._nombre

    @property
    def rol(self):
        """Propiedad para acceder al rol del empleado."""
        return self._rol

    def _verificar_clave(self, clave):
        """Método protegido para verificar la clave del empleado."""
        return self._clave == clave

class Mesa(Base):
    """
    Clase que representa una mesa del restaurante.
    Atributos:
        id (int): Identificador único de la mesa.
        _numero (int): Número de la mesa (privado).
        _estado (str): Estado de la mesa (Libre/Ocupada) (privado).
    """
    __tablename__ = 'mesas'
    id = Column(Integer, primary_key=True)
    _numero = Column(Integer, unique=True)
    _estado = Column(String(20), default="Libre")
    pedidos = relationship("Pedido", back_populates="mesa")  # Relación con pedidos

    @property
    def numero(self):
        """Propiedad para acceder al número de la mesa."""
        return self._numero

    @property
    def estado(self):
        """Propiedad para acceder al estado de la mesa."""
        return self._estado

    def _cambiar_estado(self, estado):
        """Método protegido para cambiar el estado de la mesa."""
        if estado in ["Libre", "Ocupada"]:
            self._estado = estado

class Pedido(Base):
    """
    Clase que representa un pedido realizado en una mesa.
    Atributos:
        id (int): Identificador único del pedido.
        _mesa_id (int): ID de la mesa asociada (privado).
        _mesero_id (int): ID del mesero que tomó el pedido (privado).
        _estado (str): Estado del pedido (Pedido realizado, En preparación, Finalizado) (privado).
        _fecha_inicio (datetime): Fecha y hora de creación del pedido (privado).
        _fecha_fin (datetime): Fecha y hora de finalización del pedido (privado).
    """
    __tablename__ = 'pedidos'
    id = Column(Integer, primary_key=True)
    _mesa_id = Column(Integer, ForeignKey('mesas.id'))
    _mesero_id = Column(Integer, ForeignKey('empleados.id'))
    _estado = Column(String(30), default="Pedido realizado")
    _fecha_inicio = Column(DateTime, default=datetime.now)
    _fecha_fin = Column(DateTime, nullable=True)
    mesa = relationship("Mesa", back_populates="pedidos")
    mesero = relationship("Empleado")
    detalles = relationship("DetallePedido", back_populates="pedido")

    @property
    def estado(self):
        """Propiedad para acceder al estado del pedido."""
        return self._estado

    def _cambiar_estado(self, nuevo_estado):
        """Método protegido para cambiar el estado del pedido."""
        if nuevo_estado in ["Pedido realizado", "En preparación", "Finalizado"]:
            self._estado = nuevo_estado
            if nuevo_estado == "Finalizado":
                self._fecha_fin = datetime.now()

class DetallePedido(Base):
    """
    Clase que representa los detalles de un pedido (productos solicitados).
    Atributos:
        id (int): Identificador único del detalle.
        _pedido_id (int): ID del pedido asociado (privado).
        _producto_id (int): ID del producto solicitado (privado).
        _cantidad (int): Cantidad del producto (privado).
    """
    __tablename__ = 'detalles_pedido'
    id = Column(Integer, primary_key=True)
    _pedido_id = Column(Integer, ForeignKey('pedidos.id'))
    _producto_id = Column(Integer, ForeignKey('productos.id'))
    _cantidad = Column(Integer)
    pedido = relationship("Pedido", back_populates="detalles")
    producto = relationship("Producto")

class Producto(Base):
    """
    Clase que representa un producto del menú.
    Atributos:
        id (int): Identificador único del producto.
        _nombre (str): Nombre del producto (privado).
        _categoria (str): Categoría del producto (privado).
        _precio (float): Precio del producto (privado).
    """
    __tablename__ = 'productos'
    id = Column(Integer, primary_key=True)
    _nombre = Column(String(100))
    _categoria = Column(String(50))
    _precio = Column(Float)

    @property
    def nombre(self):
        """Propiedad para acceder al nombre del producto."""
        return self._nombre

    @property
    def precio(self):
        """Propiedad para acceder al precio del producto."""
        return self._precio

class Factura(Base):
    """
    Clase que representa una factura de una mesa.
    Atributos:
        id (int): Identificador único de la factura.
        _mesa_id (int): ID de la mesa asociada (privado).
        _mesero_id (int): ID del mesero que atendió (privado).
        _fecha_hora (datetime): Fecha y hora de la factura (privado).
        _total (float): Total de la factura (privado).
    """
    __tablename__ = 'facturas'
    id = Column(Integer, primary_key=True)
    _mesa_id = Column(Integer, ForeignKey('mesas.id'))
    _mesero_id = Column(Integer, ForeignKey('empleados.id'))
    _fecha_hora = Column(DateTime, default=datetime.now)
    _total = Column(Float)
    mesa = relationship("Mesa")
    mesero = relationship("Empleado")
    detalles = relationship("DetalleFactura", back_populates="factura")

    def _calcular_total(self):
        """Método protegido para calcular el total de la factura."""
        self._total = sum(detalle.subtotal for detalle in self.detalles)

class DetalleFactura(Base):
    """
    Clase que representa los detalles de una factura (pedidos incluidos).
    Atributos:
        id (int): Identificador único del detalle.
        _factura_id (int): ID de la factura asociada (privado).
        _pedido_id (int): ID del pedido incluido (privado).
        _subtotal (float): Subtotal del pedido (privado).
    """
    __tablename__ = 'detalles_factura'
    id = Column(Integer, primary_key=True)
    _factura_id = Column(Integer, ForeignKey('facturas.id'))
    _pedido_id = Column(Integer, ForeignKey('pedidos.id'))
    _subtotal = Column(Float)
    factura = relationship("Factura", back_populates="detalles")
    pedido = relationship("Pedido")

    @property
    def subtotal(self):
        """Propiedad pública para acceder al subtotal."""
        return self._subtotal

# Configuración de la base de datos
engine = create_engine('mysql+pymysql://root:@localhost/restaurante')
Base.metadata.create_all(engine)  # Crea las tablas automáticamente si no existen
Session = sessionmaker(bind=engine)