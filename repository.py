from sqlalchemy.orm import Session

class Repository:
    def __init__(self, session: Session):
        self.session = session

    def add(self, entity):
        self.session.add(entity)
        self.session.commit()

    def get(self, entity_class, id):
        return self.session.query(entity_class).get(id)

    def get_all(self, entity_class):
        return self.session.query(entity_class).all()

    def get_by_codigo(self, entity_class, codigo):
        return self.session.query(entity_class).filter_by(_codigo=codigo).first()

    def get_by_numero(self, entity_class, numero):
        return self.session.query(entity_class).filter_by(_numero=numero).first()

    def update(self, entity):
        self.session.commit()

    def delete(self, entity):
        self.session.delete(entity)
        self.session.commit()