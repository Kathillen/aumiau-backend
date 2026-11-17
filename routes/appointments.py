from datetime import datetime
from uuid import UUID

from fastapi import APIRouter, HTTPException, Header
from pydantic import BaseModel, Field

from database import get_supabase, get_usuario_autenticado

router = APIRouter(
    prefix="/appointments",
    tags=["Agendamentos"]
)


class PetDados(BaseModel):
    nome: str
    peso: float
    porte: str


class AgendamentoCreate(BaseModel):
    pet: PetDados
    data: datetime
    servicos: list[str] = Field(default_factory=list)


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
def listar_agendamentos(
    authorization: str = Header(...)
):
    token, usuario = autenticar(authorization)

    db = get_supabase()
    db.postgrest.auth(token)

    result = (
        db.table("agendamentos")
        .select("*")
        .eq("id_usuario", usuario.id)
        .execute()
    )

    return result.data


@router.post("/")
def criar_agendamento(
    dados: AgendamentoCreate,
    authorization: str = Header(...)
):
    token, usuario = autenticar(authorization)

    db = get_supabase()
    db.postgrest.auth(token)

    pet_criado = None

    try:
        # 1. Cadastrar o pet
        resultado_pet = (
            db.table("pets")
            .insert({
                "id_usuario": usuario.id,
                "nome": dados.pet.nome,
                "peso": dados.pet.peso,
                "porte": dados.pet.porte
            })
            .execute()
        )

        if not resultado_pet.data:
            raise HTTPException(
                status_code=400,
                detail="Não foi possível cadastrar o pet."
            )

        pet_criado = resultado_pet.data[0]

        # 2. Cadastrar o agendamento
        resultado_agendamento = (
            db.table("agendamentos")
            .insert({
                "id_usuario": usuario.id,
                "id_pet": pet_criado["id"],
                "data": dados.data.isoformat(),
                "status": "pendente"
            })
            .execute()
        )

        if not resultado_agendamento.data:
            raise HTTPException(
                status_code=400,
                detail="Não foi possível criar o agendamento."
            )

        agendamento_criado = resultado_agendamento.data[0]

        return {
            "message": "Pet e agendamento cadastrados com sucesso.",
            "pet": pet_criado,
            "agendamento": agendamento_criado
        }

    except HTTPException:
        if pet_criado:
            db.table("pets").delete().eq(
                "id", pet_criado["id"]
            ).eq(
                "id_usuario", usuario.id
            ).execute()

        raise

    except Exception as erro:
        if pet_criado:
            db.table("pets").delete().eq(
                "id", pet_criado["id"]
            ).eq(
                "id_usuario", usuario.id
            ).execute()

        raise HTTPException(
            status_code=500,
            detail=f"Erro ao criar agendamento: {str(erro)}"
        )


@router.get("/{appointment_id}")
def buscar_agendamento(
    appointment_id: UUID,
    authorization: str = Header(...)
):
    token, usuario = autenticar(authorization)

    db = get_supabase()
    db.postgrest.auth(token)

    result = (
        db.table("agendamentos")
        .select("*")
        .eq("id", str(appointment_id))
        .eq("id_usuario", usuario.id)
        .execute()
    )

    if not result.data:
        raise HTTPException(
            status_code=404,
            detail="Agendamento não encontrado."
        )

    return result.data[0]
