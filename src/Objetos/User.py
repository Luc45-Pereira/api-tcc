class User:
    def __init__(self, connection, id=0, name="", email="", password="", type=""):
        self.connection = connection
        self.id = id
        self.name = name
        self.email = email
        self.password = password
        self.type = type

    def __str__(self):
        return (
            f"User: {self.id}, {self.name}, {self.email}, {self.password}, {self.type}"
        )

    # getters and setters
    def get_id(self) -> int:
        return self.id

    def get_name(self) -> str:
        return self.name

    def get_email(self) -> str:
        return self.email

    def get_password(self) -> str:
        return self.password

    def get_type(self) -> str:
        return self.type

    def set_name(self, name):
        self.name = name

    def set_email(self, email):
        self.email = email

    def set_password(self, password):
        self.password = password

    def set_type(self, type):
        self.type = type

    # Transforma o objeto em um dicionário
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "password": self.password,
            "type": self.type,
        }

    # Cadastra o objeto no banco de dados
    def cadastrar(self):
        cursor = self.connection.get_cursor()
        cursor.execute(
            f"INSERT INTO users (name, email, password, type) VALUES ('{self.name}', '{self.email}', '{self.password}', '{self.type}')"
        )
        self.connection.commit()

    # Atualiza o objeto no banco de dados
    def atualizar(self):
        cursor = self.connection.get_cursor()
        cursor.execute(
            f"UPDATE users SET name = '{self.name}', email = '{self.email}', password = '{self.password}', type = '{self.type}' WHERE id = {self.id}"
        )
        self.connection.commit()

    # Deleta o objeto no banco de dados
    def deletar(self):
        cursor = self.connection.get_cursor()
        cursor.execute(f"DELETE FROM users WHERE id = {self.id}")
        self.connection.commit()

    # Busca o objeto no banco de dados
    def buscar(self, id):
        cursor = self.connection.get_cursor()
        cursor.execute(f"SELECT * FROM users WHERE id = {id}")
        result = cursor.fetchone()
        self.id = result[0]
        self.name = result[1]
        self.email = result[2]
        self.password = result[3]
        self.type = result[4]

    # Busca todos os objetos no banco de dados
    def buscar_todos(self):
        cursor = self.connection.get_cursor()
        cursor.execute(f"SELECT * FROM users")
        result = cursor.fetchall()
        return self.all_to_dict(result)

    # Transforma a busca geral em um dicionário
    def all_to_dict(self, result):
        users = []
        for user in result:
            users.append(
                {
                    "id": user[0],
                    "name": user[1],
                    "email": user[2],
                    "password": user[3],
                    "type": user[4],
                }
            )
        return users
