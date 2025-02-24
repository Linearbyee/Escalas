from sqlalchemy import Column, Integer, String, Date, ForeignKey, CheckConstraint, Index
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Membro(Base):
    __tablename__ = 'membros'

    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False, unique=True)

    habilidades = relationship("Habilidade", back_populates="membro", cascade="all, delete-orphan")
    bloqueios = relationship("Bloqueio", back_populates="membro", cascade="all, delete-orphan")

class Funcao(Base):
    __tablename__ = 'funcoes'

    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False, unique=True)

    habilidades = relationship("Habilidade", back_populates="funcao", cascade="all, delete-orphan")

class Habilidade(Base):
    __tablename__ = 'habilidades'

    id = Column(Integer, primary_key=True)
    membro_id = Column(Integer, ForeignKey('membros.id', ondelete="CASCADE"))
    funcao_id = Column(Integer, ForeignKey('funcoes.id', ondelete="CASCADE"))
    nivel = Column(Integer, default=3, nullable=False)

    membro = relationship("Membro", back_populates="habilidades")
    funcao = relationship("Funcao", back_populates="habilidades")

    __table_args__ = (CheckConstraint("nivel BETWEEN 1 AND 5", name="check_nivel"),)

class Bloqueio(Base):
    __tablename__ = 'bloqueios'

    id = Column(Integer, primary_key=True)
    membro_id = Column(Integer, ForeignKey('membros.id', ondelete="CASCADE"))
    data = Column(Date, nullable=False)

    membro = relationship("Membro", back_populates="bloqueios")

    __table_args__ = (Index("idx_bloqueio_data", "data"),)

# Criando conexão com banco SQLite
engine = create_engine("sqlite:///database.db", echo=True)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()
