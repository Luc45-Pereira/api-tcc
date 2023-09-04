# Repositório destinado a API do projeto

## Pontos a serem desenvolvidos

- Objetos:
    - Um objeto por tabela
    - Serão utilizados pelo `app.py`
    - Devem ter os principais métodos `CRUD` (get,set,list) e métodos específicos para cada ação `login, cadastro`

- Querys:
    - Para facilitar vamos criar as as querys em `.sql` na pasta `src/Querys/`
    - Serão separados por Objetos, então teremos pastas diferentes com o nome do Objeto `src/Querys/Objeto1`

- Repositorio:
    - Terá um script para cada objeto
    - Esses scripts devem ter apenas requisições mais complexas, como uma query que necessita de um outro objeto, ou que será utilizado por outro objeto

- `app.py`
    - Script que será a API
    - Terá diversas rotas para cada ação do usuário (login, listagem, gráficos, filtros, etc)
    - Utilizaremos FastApi para criação destas rotas e testes unitários
    - Não deve ter cálculos ou regra de negócios, apenas getters e setters nos Objetos

- `.env`
    - Arquivo para guardar toda e qualquer informação de variáveis que pode mudar dependendo do ambiente, por exemplo o caminho para uma pasta pasta