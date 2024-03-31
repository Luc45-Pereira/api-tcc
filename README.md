# API do projeto

- API Desenvolvida para conexão e autenticação de usuarios com uso de JWT

# Pacotes utilizados
- FastAPI 
- pydantic (criaçåo de dataclasses)
- SQLAlchemy (ORM)
- jwt (autenticação de Login)

```mermaid
%%{init: {'theme':'neutral'}}%%

flowchart TD
    A[API] --> JWT

    JWT --> B[Routes]

    B --> C{Cartao}
    B --> D{Entrada}
    B --> E{Saida}
    B --> F{User}
    B --> G{Endereco}

    Chamadas[Create Read Update Delete ReadAll]

    C --> Chamadas

    D --> Chamadas

    E --> Chamadas

    F --> Chamadas

    G --> Chamadas


    SQLAlchemy
    Chamadas --> SQLAlchemy

    Banco[Banco de dados]

    SQLAlchemy --> Banco
    
  
    
´´´
