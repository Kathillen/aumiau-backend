
from fastapi import APIRouter
from database import get_supabase

router = APIRouter(
    prefix="/services",
    tags=["Serviços"]
)


@router.get("/")
def listar_servicos():
    db = get_supabase()

    return (
        db.table("servicos")
        .select("*")
        .execute()
        .data
    )
