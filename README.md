# Petshop Manager

Sistema completo de gestão de petshop com cadastro de pets e registro de serviços, desenvolvido com Angular, Python FastAPI e PostgreSQL.

## Funcionalidades

### Gestão de Pets
- Cadastrar pets (nome, espécie, tutor)
- Listar pets com busca por nome em tempo real
- Filtrar pets por espécie (Cachorro, Gato, Outro)
- Excluir pets com confirmação de segurança
- Interface responsiva e moderna

### Gestão de Serviços
- Adicionar serviços a um pet (banho, tosa, consulta, etc.)
- Visualizar histórico completo de serviços
- Modal interativo para gerenciar serviços
- Registro automático de data/hora dos serviços

## Tecnologias Utilizadas

### Backend
- **Python 3.8+** - Linguagem principal
- **FastAPI** - Framework web moderno e rápido
- **Pydantic** - Validação de dados
- **psycopg2** - Driver PostgreSQL
- **Uvicorn** - Servidor ASGI

### Frontend
- **Angular 17** - Framework frontend
- **TypeScript** - Linguagem tipada
- **RxJS** - Programação reativa
- **Angular Material** - Componentes UI

### Banco de Dados
- **PostgreSQL 12+** - Banco relacional
- **Relacionamentos** - Chaves estrangeiras
- **Constraints** - Validação de dados

## Pré-requisitos

- **Node.js** 18+ e npm
- **Python** 3.8+ e pip
- **PostgreSQL** 12+
- **Angular CLI** (`npm install -g @angular/cli`)

## Instalação e Execução

### 1. Clone o repositório
```bash
git clone https://github.com/Joao07912/petshop-manager.git
cd petshop-manager
```

### 2. Configurar Banco de Dados PostgreSQL

```bash
# Instalar PostgreSQL (se não tiver)
# Windows: Baixar do site oficial
# Linux: sudo apt install postgresql postgresql-contrib
# Mac: brew install postgresql

# Criar banco e tabelas
psql -U postgres -c "CREATE DATABASE petshop;"
psql -U postgres -d petshop -f db/init.sql
```

### 3. Backend (FastAPI)

```bash
cd backend-python

# Criar ambiente virtual (recomendado)
python -m venv venv

# Ativar ambiente virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
# source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt

# Configurar variáveis de ambiente
copy .env.example .env
# Editar .env com suas configurações do PostgreSQL

# Executar servidor
python main.py
```

**Backend rodando em:** http://localhost:8001

### 4. Frontend (Angular)

```bash
cd frontend-angular

# Instalar dependências
npm install

# Executar aplicação
ng serve
```

**Frontend rodando em:** http://localhost:4200

## Estrutura do Projeto

```
petshop-manager/
├── db/
│   └── init.sql                 # Script de criação das tabelas
├── backend-python/
│   ├── main.py                  # API FastAPI principal
│   ├── requirements.txt         # Dependências Python
│   └── .env.example            # Exemplo de variáveis de ambiente
├── frontend-angular/
│   ├── src/app/
│   │   ├── app.component.*     # Componente principal
│   │   ├── app.module.ts       # Módulo principal Angular
│   │   ├── models/
│   │   │   └── pet.model.ts    # Interfaces TypeScript
│   │   └── services/
│   │       └── pet.service.ts  # Serviço HTTP
│   ├── package.json            # Dependências Node.js
│   └── angular.json            # Configuração Angular
├── .gitignore                  # Arquivos ignorados pelo Git
└── README.md                   # Documentação
```

## API Endpoints

### Pets
| Método | Endpoint | Descrição | Parâmetros |
|--------|----------|-----------|------------|
| `GET` | `/pets` | Listar pets com filtros | `?busca=nome&especie=Cachorro` |
| `POST` | `/pets` | Criar novo pet | `{ nome, especie, tutor }` |
| `DELETE` | `/pets/{id}` | Excluir pet | `id` do pet |

### Serviços
| Método | Endpoint | Descrição | Parâmetros |
|--------|----------|-----------|------------|
| `POST` | `/pets/{id}/servicos` | Adicionar serviço | `{ descricao }` |
| `GET` | `/pets/{id}/servicos` | Listar serviços | `?limite=5` |

### Outros
| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `GET` | `/health` | Health check da API |

### Exemplos de Requisições

**Criar Pet:**
```json
POST /pets
{
  "nome": "Rex",
  "especie": "Cachorro",
  "tutor": "João Silva"
}
```

**Adicionar Serviço:**
```json
POST /pets/1/servicos
{
  "descricao": "Banho e tosa completa"
}
```

## Banco de Dados

### Tabela `pets`
```sql
CREATE TABLE pets (
    id SERIAL PRIMARY KEY,
    nome TEXT NOT NULL,
    especie TEXT NOT NULL CHECK (especie IN ('Cachorro','Gato','Outro')),
    tutor TEXT NOT NULL,
    criado_em TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```

### Tabela `servicos`
```sql
CREATE TABLE servicos (
    id SERIAL PRIMARY KEY,
    pet_id INT NOT NULL REFERENCES pets(id) ON DELETE CASCADE,
    descricao TEXT NOT NULL,
    data TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```

### Relacionamentos
- Um pet pode ter **vários serviços** (1:N)
- Exclusão em cascata: ao excluir pet, remove todos os serviços

## Interface do Usuário

### Tela Principal
- **Lista responsiva** de pets cadastrados
- **Filtros dinâmicos** por nome e espécie
- **Contadores** de pets por categoria
- **Botões de ação** (Histórico, Excluir)

### Cadastro de Pet
- **Formulário validado** com campos obrigatórios
- **Seleção de espécie** com dropdown
- **Feedback visual** de sucesso/erro

### Histórico de Serviços
- **Modal elegante** com histórico completo
- **Formulário inline** para novos serviços
- **Ordenação cronológica** (mais recentes primeiro)
- **Formatação de datas** em português brasileiro

## Configuração do Banco

**Arquivo `.env` (backend-python/):**
```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=petshop
DB_USER=postgres
DB_PASSWORD=user
```

**Credenciais padrão do projeto:**
- Host: `localhost`
- Port: `5432`
- Database: `petshop`
- User: `postgres`
- Password: `user`

## Deploy em Produção

### Backend
1. Configure variáveis de ambiente de produção
2. Use Gunicorn ou similar para servir a aplicação
3. Configure proxy reverso (Nginx)
4. Ative HTTPS

### Frontend
1. Build de produção: `ng build --prod`
2. Servir arquivos estáticos
3. Configure roteamento SPA
4. Otimize assets e cache

### Banco de Dados
1. Configure backup automático
2. Otimize índices para consultas frequentes
3. Configure monitoramento
4. Implemente políticas de retenção

## Segurança

- **Validação de entrada** com Pydantic
- **Sanitização SQL** com parâmetros preparados
- **CORS configurado** para domínios específicos
- **Validação de tipos** com TypeScript
- **Constraints de banco** para integridade

## Compatibilidade

### Frontend
- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+
- Dispositivos móveis

### Backend
- Python 3.8+
- PostgreSQL 12+
- Sistemas Unix/Linux
- Windows 10+

## Próximas Funcionalidades

- [ ] Autenticação de usuários
- [ ] Relatórios de faturamento
- [ ] Agendamento de serviços
- [ ] Notificações por email/SMS
- [ ] Dashboard com métricas
- [ ] Backup automático de dados