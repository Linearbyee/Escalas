from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, declarative_base
from datetime import datetime

# 🔹 Conexão com o banco de dados SQLite
engine = create_engine("sqlite:///database.db", echo=True)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

# 🔹 Modelo de Membro
class Membro(Base):
    __tablename__ = "membros"

    id = Column(Integer, primary_key=True)
    nome = Column(String, unique=True, nullable=False)
    funcoes = relationship("FuncaoMembro", back_populates="membro")
    bloqueios = relationship("Bloqueio", back_populates="membro")

# 🔹 Modelo de Função
class Funcao(Base):
    __tablename__ = "funcoes"

    id = Column(Integer, primary_key=True)
    nome = Column(String, unique=True, nullable=False)

# 🔹 Relacionamento entre Membros e Funções
class FuncaoMembro(Base):
    __tablename__ = "funcoes_membros"

    id = Column(Integer, primary_key=True)
    membro_id = Column(Integer, ForeignKey("membros.id"))
    funcao_id = Column(Integer, ForeignKey("funcoes.id"))
    nivel = Column(Integer, nullable=False)  # Nível de habilidade de 1 a 5

    membro = relationship("Membro", back_populates="funcoes")
    funcao = relationship("Funcao")

# 🔹 Modelo de Culto
class Culto(Base):
    __tablename__ = "cultos"

    id = Column(Integer, primary_key=True)
    data = Column(Date, nullable=False)
    turno = Column(String, nullable=False)

# 🔹 Modelo de Escala
class Escala(Base):
    __tablename__ = "escalas"

    id = Column(Integer, primary_key=True)
    culto_id = Column(Integer, ForeignKey("cultos.id"))
    funcao_id = Column(Integer, ForeignKey("funcoes.id"))
    membro_id = Column(Integer, ForeignKey("membros.id"), nullable=True)

    culto = relationship("Culto")
    funcao = relationship("Funcao")
    membro = relationship("Membro")

# 🔹 Modelo de Bloqueio
class Bloqueio(Base):
    __tablename__ = "bloqueios"

    id = Column(Integer, primary_key=True)
    membro_id = Column(Integer, ForeignKey("membros.id"))
    data = Column(Date, nullable=False)

    membro = relationship("Membro", back_populates="bloqueios")

# Criar tabelas no banco de dados
Base.metadata.create_all(engine)

# 🔹 Funções para manipulação de dados
def carregar_membros():
    return session.query(Membro).all()

def carregar_funcoes():
    return session.query(Funcao).all()

def carregar_cultos():
    return session.query(Culto).all()

def carregar_escalas():
    return session.query(Escala).all()

def carregar_bloqueios():
    return session.query(Bloqueio).all()

def adicionar_pessoa(nome):
    if not session.query(Membro).filter_by(nome=nome).first():
        session.add(Membro(nome=nome))
        session.commit()

def adicionar_funcao(nome):
    if not session.query(Funcao).filter_by(nome=nome).first():
        session.add(Funcao(nome=nome))
        session.commit()

def adicionar_bloqueio(membro_id, data):
    data_formatada = datetime.strptime(data, "%Y-%m-%d").date()
    session.add(Bloqueio(membro_id=membro_id, data=data_formatada))
    session.commit()

def gerar_escala():
    session.query(Escala).delete()  # Limpa a escala anterior
    session.commit()

def adicionar_culto(data, turno):
    data_formatada = datetime.strptime(data, "%Y-%m-%d").date()
    novo_culto = Culto(data=data_formatada, turno=turno)
    session.add(novo_culto)
    session.commit()

def excluir_culto(culto_id):
    culto = session.query(Culto).filter_by(id=culto_id).first()
    if culto:
        session.delete(culto)
        session.commit()


    cultos = carregar_cultos()
    funcoes = carregar_funcoes()
    membros = carregar_membros()
    bloqueios = {b.membro_id: b.data for b in carregar_bloqueios()}

    escala_gerada = []

    for culto in cultos:
        for funcao in funcoes:
            candidatos = [m for m in membros if m.id not in bloqueios or bloqueios[m.id] != culto.data]
            if candidatos:
                escolhido = candidatos[0]
                nova_escala = Escala(culto_id=culto.id, funcao_id=funcao.id, membro_id=escolhido.id)
                session.add(nova_escala)
                escala_gerada.append((culto.data, culto.turno, funcao.nome, escolhido.nome))

    session.commit()
    return escala_gerada
