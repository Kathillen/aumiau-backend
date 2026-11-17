# Aumiau - Backend

## Sobre o projeto

O backend do Aumiau é responsável pelo processamento das operações da plataforma, gerenciamento dos agendamentos, validação dos dados, autenticação dos usuários e comunicação com o banco de dados.

A aplicação foi desenvolvida em Python utilizando o framework FastAPI e utiliza o Supabase como serviço de banco de dados e autenticação.

## Tecnologias utilizadas

- Python
- FastAPI
- Supabase
- PostgreSQL
- Pydantic
- Uvicorn
- Python-dotenv

## Funcionalidades

- Autenticação de usuários por meio do Supabase.
- Cadastro e gerenciamento de pets.
- Criação de agendamentos.
- Consulta de agendamentos do usuário autenticado.
- Consulta de serviços disponíveis.
- Processamento da confirmação simulada de pagamento.
- Validação de dados recebidos pela API.
- Controle de acesso utilizando tokens de autenticação.

## Estrutura do projeto

```text
backend/
├── routes/
│   ├── appointments.py
│   ├── payments.py
│   ├── pets.py
│   └── services.py
├── tests/
├── database.py
├── main.py
├── requirements.txt
├── .env
└── .gitignore
```

## Descrição dos arquivos

- `main.py`: inicializa a aplicação FastAPI, configura o CORS e registra as rotas.
- `database.py`: realiza a configuração e conexão com o Supabase, além de fornecer funções relacionadas à autenticação.
- `appointments.py`: contém as operações relacionadas à criação e consulta de agendamentos.
- `payments.py`: gerencia as operações relacionadas à confirmação simulada de pagamentos.
- `pets.py`: contém as operações de cadastro e gerenciamento dos pets.
- `services.py`: disponibiliza os serviços cadastrados no banco de dados.
- `requirements.txt`: lista as dependências necessárias para executar o backend.
- `tests/`: diretório destinado aos testes da aplicação.

## Instalação e execução

### 1. Clonar o repositório

```bash
git clone URL_DO_REPOSITORIO
```

### 2. Acessar a pasta do projeto

```bash
cd backend
```

### 3. Criar o ambiente virtual

```bash
python -m venv .venv
```

### 4. Ativar o ambiente virtual

No Windows:

```powershell
.venv\Scripts\activate
```

### 5. Instalar as dependências

```bash
pip install -r requirements.txt
```

### 6. Configurar as variáveis de ambiente

Criar um arquivo `.env` na raiz do projeto:

```env
SUPABASE_URL=URL_DO_SUPABASE
SUPABASE_ANON_KEY=CHAVE_PUBLICA_DO_SUPABASE
DATABASE_URL=URL_DE_CONEXAO_DO_BANCO
CORS_ORIGINS=["http://localhost:5173","https://DOMINIO_DO_FRONTEND"]
```

### 7. Executar o servidor

```bash
python -m uvicorn main:app --reload
```

O backend estará disponível localmente em:

```text
http://127.0.0.1:8000
```

A documentação interativa da API pode ser acessada em:

```text
http://127.0.0.1:8000/docs
```

## Principais rotas

| Método | Rota | Descrição |
|---|---|---|
| GET | `/pets/` | Lista os pets do usuário |
| POST | `/pets/` | Cadastra um pet |
| GET | `/services/` | Lista os serviços |
| POST | `/appointments/` | Cria um agendamento |
| GET | `/appointments/` | Lista os agendamentos |
| GET | `/appointments/{appointment_id}` | Busca um agendamento |
| PATCH | `/payments/{appointment_id}/confirm` | Confirma o pagamento simulado |

## Banco de dados

O projeto utiliza o Supabase, que disponibiliza o PostgreSQL para armazenamento das informações.

Entre as principais entidades utilizadas estão:

- Usuários
- Pets
- Agendamentos
- Serviços
- Relacionamento entre agendamentos e serviços
- Pagamentos

O controle de acesso aos dados é realizado por meio das políticas de Row Level Security (RLS) do Supabase.

## Hospedagem

O backend está hospedado na Railway.

URL da API:

```text
https://aumiau-backend-production.up.railway.app
```

Documentação:

```text
https://aumiau-backend-production.up.railway.app/docs
```

## Observações

A confirmação de pagamento possui caráter de simulação e não realiza transações financeiras reais.

DOCUMENTAÇÃO:
https://docs.google.com/document/d/1gV6M4zQLlUmGyjDaYO2miUuS-Rh_RcQBVn5p3bW9La0/edit?usp=sharing
