
from uuid import UUID
from fastapi import APIRouter, HTTPException, Header

from database import get_supabase, get_usuario_autenticado

router = APIRouter(
    prefix="/payments",
    tags=["Pagamentos"]
)


@router.patch("/{appointment_id}/confirm")
def confirmar_pagamento(
    appointment_id: UUID,
    authorization: str = Header(...)
):
    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=401,
            detail="Token de autenticação inválido."
        )

    token = authorization.replace("Bearer ", "", 1)
    usuario = get_usuario_autenticado(token)

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

    return {
        "message": "Pagamento simulado confirmado.",
        "simulated": True,
        "appointment": result.data[0]
    }
