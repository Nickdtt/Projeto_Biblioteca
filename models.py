from sqlalchemy import Boolean, Integer, String, ForeignKey
from sqlalchemy.orm import mapped_column, relationship, Mapped
from database import Base





class Usuario(Base):
    __tablename__= 'bib_nf_usuarios'

    id = mapped_column(Integer, primary_key=True, index=True) 
    nome_usuario = mapped_column(String, index=True, unique=True)
    senha = mapped_column(String, index=True)

    emprestimos_users = relationship("Emprestimos", back_populates="usuario")


    


class Livro(Base):
    __tablename__= 'bib_nf_livros'

    id = mapped_column(Integer, primary_key=True, index=True)
    nome_livro = mapped_column(String(30), index=True, unique=True)
    autor = mapped_column(String(30), index=True)
    is_available = mapped_column(Boolean, default=True)

    emprestimos_livros = relationship("Emprestimos", back_populates="livros")

  


class Emprestimos(Base):
    __tablename__= 'emprestimos_nf_livros'
    id = mapped_column(Integer, primary_key=True, autoincrement= True, index=True)
    nome_livro = mapped_column(String, ForeignKey("bib_nf_livros.nome_livro", ondelete="CASCADE"))
    nome_usuario = mapped_column(String, ForeignKey("bib_nf_usuarios.nome_usuario", ondelete="CASCADE"), nullable=False)
    
    livros = relationship("Livro", back_populates="emprestimos_livros") 
    usuario = relationship("Usuario",back_populates="emprestimos_users")
    

    

