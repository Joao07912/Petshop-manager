# Petshop Manager

Sistema de controle de petshop com cadastro de pets e registro de serviços.

## Tecnologias

- **Backend**: Python FastAPI + PostgreSQL
- **Frontend**: Angular + TypeScript
- **Banco**: PostgreSQL

## Funcionalidades

### Pets
- ✅ Cadastrar pets (nome, espécie, tutor)
- ✅ Listar pets com busca por nome
- ✅ Filtrar pets por espécie
- ✅ Excluir pets com confirmação

### Serviços
- ✅ Adicionar serviços a um pet
- ✅ Visualizar histórico de serviços
- ✅ Listar últimos 5 serviços por pet

## Instalação e Execução

### 1. Banco de Dados PostgreSQL

```bash
# Instalar PostgreSQL (se não tiver)
# Criar banco e tabelas
psql -U postgres -f db/init.sql
```

### 2. Backend (FastAPI)

```bash
cd backend-python

# Criar ambiente virtual
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Instalar dependências
pip install -r requirements.txt

# Configurar variáveis de ambiente
copy .env.example .env
# Editar .env com suas configurações do PostgreSQL

# Executar servidor
python main.py
```

O backend será executado em: http://localhost:8000

### 3. Frontend (Angular)

```bash
cd frontend-angular

# Instalar dependências
npm install

# Executar aplicação
npm start
```

O frontend será executado em: http://localhost:4200

## Estrutura do Projeto

```
problema2_petshop/
├── db/
│   └── init.sql                 # Script de criação das tabelas
├── backend-python/
│   ├── main.py                  # API FastAPI
│   ├── requirements.txt         # Dependências Python
│   └── .env.example            # Exemplo de variáveis de ambiente
├── frontend-angular/
│   ├── src/app/
│   │   ├── components/         # Componentes Angular
│   │   ├── services/          # Serviços para API
│   │   ├── models/            # Modelos TypeScript
│   │   ├── app.component.*    # Componente principal
│   │   └── app.module.ts      # Módulo principal
│   ├── package.json           # Dependências Node.js
│   └── angular.json           # Configuração Angular
└── README.md
```

## API Endpoints

### Pets
- `GET /pets?busca=&especie=` - Listar pets com filtros
- `POST /pets` - Criar novo pet
- `DELETE /pets/{id}` - Excluir pet

### Serviços
- `POST /pets/{id}/servicos` - Adicionar serviço a um pet
- `GET /pets/{id}/servicos?limite=5` - Listar serviços de um pet

### Outros
- `GET /health` - Health check da API

## Banco de Dados

### Tabela pets
```sql
CREATE TABLE pets (
    id SERIAL PRIMARY KEY,
    nome TEXT NOT NULL,
    especie TEXT NOT NULL CHECK (especie IN ('Cachorro','Gato','Outro')),
    tutor TEXT NOT NULL,
    criado_em TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```

### Tabela servicos
```sql
CREATE TABLE servicos (
    id SERIAL PRIMARY KEY,
    pet_id INT NOT NULL REFERENCES pets(id) ON DELETE CASCADE,
    descricao TEXT NOT NULL,
    data TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```

## Demonstração

### Tela Principal
- Lista de pets cadastrados
- Filtros por nome e espécie
- Botões de ação (Histórico, Excluir)

### Cadastro de Pet
- Formulário com validação
- Campos: nome, espécie, tutor

### Histórico de Serviços
- Modal com últimos serviços
- Formulário para adicionar novo serviço
- Exibição com data/hora

## Configuração do Banco

**Credenciais padrão:**
- Host: localhost
- Port: 5432
- Database: petshop
- User: postgres
- Password: user

Altere no arquivo `.env` conforme sua configuração.