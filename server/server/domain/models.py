from sqlalchemy import Column, Integer, String, DateTime, Numeric, Sequence
from domain import Base, session, ENGINE


class IPDevice(Base):
    __tablename__ = "ip_device"
    id = Column(Integer, Sequence("id"), primary_key=True)
    ip = Column(String(16))
    mac = Column(String(17))
    hostname = Column(String(64))
    name = Column(String(128))

    def get_by_id(id):
        return session.query(IPDevice).filter(IPDevice.id == id).first()

    def get_all():  # type: ignore
        return session.query(IPDevice).all()

    def save(self):
        session.add(self)
        session.commit()

    def delete(self):
        session.delete(self)
        session.commit()


Base.metadata.create_all(bind=ENGINE)
