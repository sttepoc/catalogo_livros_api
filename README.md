# BookHub - Sistema de Gerenciamento de Livros e Resenhas

Este projeto é uma aplicação web completa para gerenciar um catálogo de livros e resenhas, desenvolvida com Flask no backend e HTML/CSS/JavaScript no frontend.

## Pré-requisitos

- Python 3.7 ou superior
- pip (gerenciador de pacotes do Python)

## Configuração e Execução

Siga os passos abaixo para rodar a aplicação:

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/seu-usuario/bookhub.git
   cd bookhub
   ```

2. **Crie e ative um ambiente virtual (recomendado):**
   ```bash
   python -m venv venv
   
   # Linux/macOS:
   source venv/bin/activate
   
   # Windows:
   venv\Scripts\activate
   ```

3. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Inicialize o banco de dados:**
   ```bash
   flask shell
   ```
   ```python
   >>> from app import db
   >>> db.create_all()
   >>> exit()
   ```

5. **Execute a aplicação:**
   ```bash
   python run.py
   ```

6. **Acesse a aplicação:**
   Abra seu navegador em http://localhost:5000

## Estrutura de Arquivos

```
bookhub/
├── app/
│   ├── __init__.py
│   ├── auth.py
│   ├── models.py
│   └── routes.py
├── frontend_api/
│   ├── adicionar_livro.html
│   ├── index.html
│   ├── livros.html
│   ├── login.html
│   ├── register.html
│   ├── resenhas.html
│   └── js/
│       └── api.js
├── config.py
├── run.py
├── requirements.txt
└── README.md
```

## Funcionalidades Principais

### Autenticação
- Registro de novos usuários
- Login com token JWT
- Proteção de rotas com autenticação

### Livros
- Adição de novos livros
- Listagem de todos os livros
- Visualização de detalhes
- Edição e exclusão de livros

### Resenhas
- Criação de resenhas com classificação (1-5 estrelas)
- Listagem de todas as resenhas
- Edição e exclusão de resenhas
- Associação de resenhas a livros

## Rotas da API

### Autenticação
- `POST /api/auth/register` - Registrar novo usuário
- `POST /api/auth/login` - Fazer login

### Livros
- `GET /api/livros` - Listar todos os livros
- `POST /api/livros` - Adicionar novo livro
- `PUT /api/livros/<id>` - Atualizar livro
- `DELETE /api/livros/<id>` - Excluir livro

### Resenhas
- `GET /api/resenhas` - Listar todas as resenhas
- `POST /api/resenhas` - Adicionar nova resenha
- `PUT /api/resenhas/<id>` - Atualizar resenha
- `DELETE /api/resenhas/<id>` - Excluir resenha

## Tecnologias Utilizadas

### Backend
- Flask (Framework web Python)
- Flask-SQLAlchemy (ORM para banco de dados)
- Flask-JWT-Extended (Autenticação JWT)
- SQLite (Banco de dados)

### Frontend
- HTML5
- CSS3 (com Bootstrap 5)
- JavaScript
- Fetch API para comunicação com backend

## Fluxo de Autenticação

1. Usuário faz registro/login
2. Servidor gera token JWT
3. Token é armazenado no localStorage
4. Todas as requisições subsequentes incluem token no header Authorization
5. Servidor valida token antes de processar requisições

## Personalização

Você pode modificar as configurações no arquivo `config.py`:

- `SECRET_KEY`: Chave secreta da aplicação
- `SQLALCHEMY_DATABASE_URI`: Caminho do banco de dados
- `JWT_SECRET_KEY`: Chave para tokens JWT

## Dicas para Desenvolvimento

1. Para limpar o banco de dados, delete o arquivo `api.db`
2. Recrie as tabelas com `db.create_all()` no shell do Flask
3. Use o modo debug durante desenvolvimento:
   ```python
   if __name__ == '__main__':
       app.run(debug=True)
   ```
4. Para testar APIs, utilize ferramentas como Postman ou Thunder Client

## Contribuição

Contribuições são bem-vindas! Siga os passos:

1. Faça um fork do projeto
2. Crie uma branch com sua feature (`git checkout -b feature/awesome-feature`)
3. Faça commit das alterações (`git commit -m 'Add awesome feature'`)
4. Faça push para a branch (`git push origin feature/awesome-feature`)
5. Abra um Pull Request

## Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## Suporte

Se você encontrar algum problema ou tiver alguma dúvida, por favor abra uma issue no repositório do GitHub.