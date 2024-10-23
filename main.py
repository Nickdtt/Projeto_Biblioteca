from http import HTTPStatus
from sqlalchemy import select
from sqlalchemy.orm import selectinload
import uvicorn
from fastapi import FastAPI, HTTPException, status, Depends
from database import engine, Base, SessionLocal
from schemas import Usuario_Schema, Livro_Schema, Token_Schema
from models import Usuario, Livro, Emprestimos
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordRequestForm
from security.security import (
    create_access_token,
    get_password_hash,
    verify_password,
)





#funcao para iniciar conexao com o banco de dados




app = FastAPI(title= "Projeto Biblioteca")


async def get_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    db = SessionLocal()
    try:
        yield db
    finally:
        await db.close()



@app.post("/api/cadastrar_usuario", response_model=None, status_code= status.HTTP_201_CREATED)
async def cadastrar_usuario(usuario: Usuario_Schema, db: AsyncSession = Depends(get_db) ):
    novo_usuario = Usuario(id = usuario.id, nome_usuario = usuario.nome_usuario, senha = get_password_hash(usuario.senha))
    db.add(novo_usuario)
    await db.commit()
    await db.refresh(novo_usuario)
    return novo_usuario

@app.post("/api/cadastrar_livro", status_code= status.HTTP_201_CREATED)
async def cadastrar_livro(livro: Livro_Schema, db: AsyncSession = Depends(get_db)):
    novo_livro = Livro(id = livro.id, nome_livro = livro.nome_livro, autor = livro.autor)
    db.add(novo_livro)
    await db.commit()
    await db.refresh(novo_livro)
    return novo_livro


@app.get("/api/lista_livros", response_model=list[Livro_Schema], status_code=status.HTTP_200_OK)
async def listar_livros(db:AsyncSession = Depends(get_db)):
    stmt = select(Livro)
    lista_atual = await db.execute(stmt)
    return lista_atual.scalars().all()

@app.get("/api/livro/{identification}")
async def buscar_livro(identification: int, db:AsyncSession = Depends(get_db)):
    stmt = select(Livro).where(Livro.id == identification)
    livro = await db.execute(stmt)
    return livro.scalars().all()

@app.post("/api/realizar_emprestimo")
async def realizar_emprestimo(livro_id: int, usuario_id: int, db: AsyncSession = Depends(get_db)):
    stmt1 = select(Livro).where(Livro.id == livro_id).options(selectinload(Livro.emprestimos_livros))
    stmt2 = select(Usuario).where(Usuario.id == usuario_id).options(selectinload(Usuario.emprestimos_users))

    livro_f = await db.execute(stmt1)
    usuario_f = await db.execute(stmt2)

    livro_teste = livro_f.scalars().one()
    usuario_teste = usuario_f.scalars().one()

    novo_emprestimo = Emprestimos(nome_livro = livro_teste.nome_livro, nome_usuario = usuario_teste.nome_usuario)
    db.add(novo_emprestimo)

    await db.commit()
    await db.refresh(novo_emprestimo)
    
    return novo_emprestimo

@app.post("/token", response_model= Token_Schema)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
):
    stmt1 = await db.execute(select(Usuario).where(Usuario.nome_usuario == form_data.username))
     
    user = stmt1.scalars.one()

    if not user:
        raise HTTPException(
            status_code= HTTPStatus.BAD_REQUEST,
            detail='Usuario já existe'
        )

    if not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code= HTTPStatus.BAD_REQUEST,
            detail= 'Usuario ou senha incorretas'
        )


    access_token = create_access_token(data={'sub': user.nome_usuario})

    return {'access token': access_token, 'token_type': 'bearer'}



    








if __name__ == '__main__':
    uvicorn.run(app, port=8000)