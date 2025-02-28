# Plataforma de Aulas de Libras

Plataforma completa para ensino de Libras, com aulas gravadas e sistema de agendamento de aulas ao vivo.

## Tecnologias Utilizadas

### Backend
- Django + Django REST Framework
- PostgreSQL (Supabase)
- JWT + OAuth para autenticação
- Swagger para documentação da API

### Frontend
- React + Next.js
- TypeScript
- Tailwind CSS
- Zustand para gerenciamento de estado

## Estrutura do Projeto

```
handfluency/
├── backend/                 # Backend em Django
│   ├── core/               # Configuração principal
│   ├── users/              # Usuários e autenticação
│   ├── courses/            # Cursos, módulos e aulas
│   ├── scheduling/         # Agendamento de aulas ao vivo
│   ├── quizzes/            # Sistema de quizzes
│   └── progress/           # Controle de progresso do aluno
├── frontend/               # Frontend em React + Next.js
│   ├── src/
│   │   ├── app/           # Páginas principais
│   │   ├── components/    # Componentes reutilizáveis
│   │   └── lib/          # Utilitários e configurações
└── docs/                   # Documentação do projeto
```

## Configuração do Ambiente de Desenvolvimento

### Backend

1. Criar ambiente virtual Python:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
.\venv\Scripts\activate  # Windows
```

2. Instalar dependências:
```bash
pip install -r requirements.txt
```

3. Configurar variáveis de ambiente:
```bash
cp .env.example .env
# Editar .env com suas configurações
```

4. Executar migrações:
```bash
python manage.py migrate
```

5. Iniciar servidor de desenvolvimento:
```bash
python manage.py runserver
```

### Frontend

1. Instalar dependências:
```bash
cd frontend
npm install
```

2. Configurar variáveis de ambiente:
```bash
cp .env.example .env.local
# Editar .env.local com suas configurações
```

3. Iniciar servidor de desenvolvimento:
```bash
npm run dev
```

## Padrões de Código

- Backend segue PEP 8 e PEP 20
- Frontend utiliza ESLint e Prettier
- Commits seguem Conventional Commits

## Documentação

- API: Disponível em `/api/swagger/` após iniciar o backend
- Frontend: Documentação de componentes em `/docs`

## Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes. 