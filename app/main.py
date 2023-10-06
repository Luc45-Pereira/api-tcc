"""" Arquivo principal da API """
from fastapi import FastAPI
from app.routers import user, endereco, entrada, saida
import dotenv

dotenv.load_dotenv()

app = FastAPI()

app.include_router(user.router, prefix="/user", tags=["user"])
app.include_router(endereco.router, prefix="/endereco", tags=["endereco"])
app.include_router(entrada.router, prefix="/entrada", tags=["entrada"])
app.include_router(saida.router, prefix="/saida", tags=["saida"])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)