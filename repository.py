# Este archivo contiene la clase Repository para manejar las operaciones CRUD en la base de datos.

from sqlalchemy.orm import Session

class Repository:
    """
    Clase para manejar operaciones CRUD genéricas en la base de datos.
    Atributos:
        session (Session): Sesión de SQLAlchemy para interactuar con la base de datos.
    """
    def __init__(self, session: Session):
        """Inicializa el repositorio con una sesión de SQLAlchemy."""
        self.session = session

    def add(self, entity):
        """Agrega una nueva entidad a la base de datos."""
        self.session.add(entity)
        self.session.commit()

    def get(self, entity_class, id):
        """Obtiene una entidad por su ID."""
        return self.session.query(entity_class).get(id)

    def get_all(self, entity_class):
        """Obtiene todas las entidades de una clase específica."""
        return self.session.query(entity_class).all()

    def get_by_codigo(self, entity_class, codigo):
        """Obtiene una entidad por su código (usado para empleados)."""
        return self.session.query(entity_class).filter_by(_codigo=codigo).first()

    def get_by_numero(self, entity_class, numero):
        """Obtiene una entidad por su número (usado para mesas)."""
        return self.session.query(entity_class).filter_by(_numero=numero).first()

    def update(self, entity):
        """Actualiza una entidad existente en la base de datos."""
        self.session.commit()

    def delete(self, entity):
        """Elimina una entidad de la base de datos."""
        self.session.delete(entity)
        self.session.commit()