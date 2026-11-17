
from uuid import UUID
from fastapi import APIRouter, HTTPException, Header
from pydantic import BaseModel

from database import get_supabase, get_usuario_autenticado

router = APIRouter(prefix="/pets", tags=["Pets"])


class PetCreate(BaseModel):
    nome: str
    peso: float
    porte: str


def autenticar(authorization: str):
    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=401,
            detail="Token de autenticação inválido."
        )

    token = authorization.replace("Bearer ", "", 1)
    usuario = get_usuario_autenticado(token)

    return token, usuario


@router.get("/")
def listar_pets(authorization: str = Header(...)):
    token, usuario = autenticar(authorization)

    db = get_supabase()
    db.postgrest.auth(token)

    result = (
        db.table("pets")
        .select("*")
        .eq("id_usuario", usuario.id)
        .execute()
    )

    return result.data


@router.post("/")
def criar_pet(
    dados: PetCreate,
    authorization: str = Header(...)
):
    token, usuario = autenticar(authorization)

    db = get_supabase()
    db.postgrest.auth(token)

    result = (
        db.table("pets")
        .insert({
            "id_usuario": usuario.id,
            "nome": dados.nome,
            "peso": dados.peso,
            "porte": dados.porte
        })
        .execute()
    )

    if not result.data:
        raise HTTPException(
            status_code=400,
            detail="Não foi possível cadastrar o pet."
        )

    return result.data[0]


@router.put("/{pet_id}")
def atualizar_pet(
    pet_id: UUID,
    dados: PetCreate,
    authorization: str = Header(...)
):
    token, usuario = autenticar(authorization)

    db = get_supabase()
    db.postgrest.auth(token)

    result = (
        db.table("pets")
        .update(dados.model_dump())
        .eq("id", str(pet_id))
        .eq("id_usuario", usuario.id)
        .execute()
    )

    if not result.data:
        raise HTTPException(
            status_code=404,
            detail="Pet não encontrado."
        )

    return result.data[0]


@router.delete("/{pet_id}")
def excluir_pet(
    pet_id: UUID,
    authorization: str = Header(...)
):
    token, usuario = autenticar(authorization)

    db = get_supabase()
    db.postgrest.auth(token)

    result = (
        db.table("pets")
        .delete()
        .eq("id", str(pet_id))
        .eq("id_usuario", usuario.id)
        .execute()
    )

    if not result.data:
        raise HTTPException(
            status_code=404,
            detail="Pet não encontrado."
        )

    return {"message": "Pet excluído com sucesso."}
