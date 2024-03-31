"""" Arquivo principal da API """
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from internal.routers import user, endereco, entrada, saida, cartao
import dotenv

dotenv.load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(user.router, prefix="/user", tags=["user"])
app.include_router(endereco.router, prefix="/endereco", tags=["endereco"])
app.include_router(entrada.router, prefix="/entrada", tags=["entrada"])
app.include_router(saida.router, prefix="/saida", tags=["saida"])
app.include_router(cartao.router, prefix="/cartao", tags=["cartao"])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)