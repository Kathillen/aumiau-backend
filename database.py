
import os
from dotenv import load_dotenv
from fastapi import HTTPException
from supabase import create_client

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_ANON_KEY")

supabase = None

if SUPABASE_URL and SUPABASE_KEY:
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


def get_supabase():
    if supabase is None:
        raise HTTPException(
            status_code=503,
            detail="Supabase não configurado. Verifique o arquivo .env."
        )

    return supabase


def get_usuario_autenticado(token: str):
    db = get_supabase()

    try:
        resposta = db.auth.get_user(token)

        if not resposta.user:
            raise HTTPException(
                status_code=401,
                detail="Usuário não autenticado."
            )

        return resposta.user

    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Token inválido ou expirado."
        )
