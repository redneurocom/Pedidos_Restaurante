from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from datetime import datetime

Base = declarative_base()

class Empleado(Base):
    __tablename__ = 'empleados'
    id = Column(Integer, primary_key=True)
    _codigo = Column(String(20), unique=True)
    _nombre = Column(String(100))
    _rol = Column(String(50))
    _clave = Column(String(128))

    @property
    def codigo(self):
        return self._codigo

    @property
    def nombre(self):
        return self._nombre

    @property
    def rol(self):
        return self._rol

    def _verificar_clave(self, clave):
        return self._clave == clave

class Mesa(Base):
    __tablename__ = 'mesas'
    id = Column(Integer, primary_key=True)
    _numero = Column(Integer, unique=True)
    _estado = Column(String(20), default="Libre")
    pedidos = relationship("Pedido", back_populates="mesa")

    @property
    def numero(self):
        return self._numero

    @property
    def estado(self):
        return self._estado

    def _cambiar_estado(self, estado):
        if estado in ["Libre", "Ocupada"]:
            self._estado = estado

class Pedido(Base):
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
        return self._estado

    def _cambiar_estado(self, nuevo_estado):
        allowed_states = ["Pedido realizado", "En preparación", "Entregado", "Finalizado"]
        if nuevo_estado not in allowed_states:
            return
        current_index = allowed_states.index(self._estado)
        new_index = allowed_states.index(nuevo_estado)
        if new_index <= current_index:
            return  # No se permite retroceder
        if nuevo_estado == "Finalizado":
            self._fecha_fin = datetime.now()
        self._estado = nuevo_estado

class DetallePedido(Base):
    __tablename__ = 'detalles_pedido'
    id = Column(Integer, primary_key=True, autoincrement=True)
    _pedido_id = Column(Integer, ForeignKey('pedidos.id'))
    _producto_id = Column(Integer, ForeignKey('productos.id'))
    _estado = Column(String(30), default="Pedido realizado")
    # Se reemplaza _fecha_inicio por _fecha_creacion y se agregan nuevos campos
    _fecha_creacion = Column(DateTime, default=datetime.now)
    _inicio_preparacion = Column(DateTime, nullable=True)
    _fin_preparacion = Column(DateTime, nullable=True)
    _fin_finalizacion = Column(DateTime, nullable=True)
    _duracion_preparacion = Column(Float, nullable=True)

    pedido = relationship("Pedido", back_populates="detalles")
    producto = relationship("Producto")

    @property
    def estado(self):
        return self._estado

    def _cambiar_estado(self, nuevo_estado):
        allowed_states = ["Pedido realizado", "En preparación", "Entregado", "Finalizado"]
        if nuevo_estado not in allowed_states:
            return
        current_index = allowed_states.index(self._estado)
        new_index = allowed_states.index(nuevo_estado)
        if new_index <= current_index:
            return  # No se permite retroceder
        if nuevo_estado == "En preparación":
            if not self._inicio_preparacion:
                self._inicio_preparacion = datetime.now()
        elif nuevo_estado == "Entregado":
            if self._inicio_preparacion and not self._fin_preparacion:
                self._fin_preparacion = datetime.now()
                diff = self._fin_preparacion - self._inicio_preparacion
                self._duracion_preparacion = diff.total_seconds() / 60.0
        elif nuevo_estado == "Finalizado":
            if not self._fin_finalizacion:
                self._fin_finalizacion = datetime.now()
        self._estado = nuevo_estado

class Producto(Base):
    __tablename__ = 'productos'
    id = Column(Integer, primary_key=True)
    _nombre = Column(String(100))
    _categoria = Column(String(50))
    _precio = Column(Float)

    @property
    def nombre(self):
        return self._nombre

    @property
    def precio(self):
        return self._precio

class Factura(Base):
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
        self._total = sum(detalle.subtotal for detalle in self.detalles)


# python - Archivo: models.py (Clase DetalleFactura)
class DetalleFactura(Base):
    __tablename__ = 'detalles_factura'
    id = Column(Integer, primary_key=True, autoincrement=True)
    _factura_id = Column(Integer, ForeignKey('facturas.id'), nullable=False)
    _pedido_id = Column(Integer, ForeignKey('pedidos.id'))
    _producto_id = Column(Integer, ForeignKey('productos.id'), nullable=False)
    _cantidad = Column(Integer, nullable=False, default=1)
    _precio_unitario = Column(Float, nullable=False)
    _subtotal = Column(Float, nullable=False)

    factura = relationship("Factura", back_populates="detalles")
    pedido = relationship("Pedido")
    producto = relationship("Producto")

    @property
    def producto_id(self):
        return self._producto_id

    @producto_id.setter
    def producto_id(self, value):
        self._producto_id = value

    @property
    def cantidad(self):
        return self._cantidad

    @cantidad.setter
    def cantidad(self, value):
        self._cantidad = value
        self._update_subtotal()

    @property
    def precio_unitario(self):
        return self._precio_unitario

    @precio_unitario.setter
    def precio_unitario(self, value):
        self._precio_unitario = value
        self._update_subtotal()

    @property
    def subtotal(self):
        return self._subtotal

    @subtotal.setter
    def subtotal(self, value):
        self._subtotal = value

    def _update_subtotal(self):
        if self._precio_unitario is None or self._cantidad is None:
            self._subtotal = 0.0
        else:
            self._subtotal = self._cantidad * self._precio_unitario

engine = create_engine('mysql+pymysql://root:@localhost/restaurante')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)