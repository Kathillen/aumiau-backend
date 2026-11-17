
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes import pets, services, appointments, payments

app = FastAPI(
    title="Aumiau API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "https://aumiau-v2.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(pets.router)
app.include_router(services.router)
app.include_router(appointments.router)
app.include_router(payments.router)


@app.get("/")
def home():
    return {"message": "API Aumiau funcionando!"}


@app.get("/health")
def health():
    return {"status": "ok"}
