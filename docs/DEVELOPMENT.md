# Documentação de Desenvolvimento - Plataforma de Aulas de Libras

Este documento mantém o registro do progresso de desenvolvimento e os próximos passos planejados para a plataforma.

## Índice
1. [Setup Inicial](#setup-inicial)
2. [Backend](#backend)
3. [Frontend](#frontend)
4. [Integrações](#integrações)
5. [Testes](#testes)
6. [Deploy](#deploy)

## Setup Inicial

### ✅ Completado

1. Estrutura do Projeto
   - [x] Criação da estrutura de diretórios
   - [x] Configuração do README.md
   - [x] Configuração dos .gitignore

2. Backend (Django)
   - [x] Inicialização do projeto Django
   - [x] Criação dos apps principais:
     - users
     - courses
     - scheduling
     - quizzes
     - progress
   - [x] Configuração do ambiente virtual
   - [x] Instalação das dependências iniciais
   - [x] Configuração do template de variáveis de ambiente

3. Frontend (Next.js)
   - [x] Inicialização do projeto Next.js com TypeScript
   - [x] Configuração do Tailwind CSS
   - [x] Configuração do ESLint
   - [x] Instalação do Zustand
   - [x] Configuração do template de variáveis de ambiente

### 🔄 Próximos Passos

## Backend

### Configuração do Django REST Framework
- [x] Configurar DRF no settings.py
- [x] Configurar autenticação JWT
- [x] Configurar CORS
- [x] Configurar Swagger/OpenAPI

### Modelos de Dados
- [x] Users
  - [x] Modelo de usuário customizado
  - [x] Perfis (Aluno/Professor)
  - [x] Autenticação social (Google)
  
- [x] Courses
  - [x] Modelo de Curso
  - [x] Modelo de Módulo
  - [x] Modelo de Aula
  - [x] Sistema de progresso
  
- [x] Scheduling
  - [x] Modelo de Agendamento
  - [x] Disponibilidade de professores
  - [x] Sistema de notificações
  
- [x] Quizzes
  - [x] Modelo de Quiz
  - [x] Modelo de Questão
  - [x] Sistema de pontuação
  
- [x] Progress
  - [x] Tracking de progresso do aluno
  - [x] Relatórios de desempenho
  - [x] Gamificação

### APIs
- [ ] Endpoints de Autenticação
  - [ ] Login/Registro
  - [ ] Login social
  - [ ] Recuperação de senha
  
- [ ] Endpoints de Cursos
  - [ ] CRUD de cursos
  - [ ] Listagem e filtros
  - [ ] Upload de vídeos
  
- [ ] Endpoints de Agendamento
  - [ ] Gerenciamento de horários
  - [ ] Confirmações
  - [ ] Cancelamentos
  
- [ ] Endpoints de Quiz
  - [ ] Gerenciamento de quizzes
  - [ ] Submissão de respostas
  - [ ] Avaliação

## Frontend

### Estrutura Base
- [ ] Configuração de rotas
- [ ] Layout base
- [ ] Componentes comuns
- [ ] Temas e estilos globais

### Autenticação
- [ ] Páginas de login/registro
- [ ] Integração com Google OAuth
- [ ] Gerenciamento de estado de autenticação
- [ ] Proteção de rotas

### Área do Aluno
- [ ] Dashboard
- [ ] Catálogo de cursos
- [ ] Player de vídeo customizado
- [ ] Sistema de progresso
- [ ] Agendamento de aulas
- [ ] Quizzes interativos

### Área do Professor
- [ ] Dashboard
- [ ] Gerenciamento de cursos
- [ ] Agenda de aulas
- [ ] Análise de desempenho

### Componentes
- [ ] Player de vídeo customizado
  - [ ] Controles básicos
  - [ ] Ajuste de velocidade
  - [ ] Tracking de progresso
  
- [ ] Sistema de quiz
  - [ ] Diferentes tipos de questões
  - [ ] Feedback instantâneo
  - [ ] Pontuação

## Integrações

### Supabase
- [ ] Configuração inicial
- [ ] Migração do banco de dados
- [ ] Backup automático

### Hotmart
- [ ] Configuração da API
- [ ] Webhooks de pagamento
- [ ] Liberação de acesso

### Google OAuth
- [ ] Configuração do projeto
- [ ] Integração com backend
- [ ] Fluxo de autenticação

## Testes

### Backend
- [ ] Testes unitários
- [ ] Testes de integração
- [ ] Testes de API

### Frontend
- [ ] Testes de componentes
- [ ] Testes de integração
- [ ] Testes E2E

## Deploy

### Backend
- [ ] Configuração do servidor
- [ ] Configuração do gunicorn
- [ ] Configuração do nginx
- [ ] SSL/HTTPS

### Frontend
- [ ] Build de produção
- [ ] Configuração do CDN
- [ ] Otimização de performance
- [ ] Monitoramento

## Monitoramento e Analytics
- [ ] Logs de erro
- [ ] Métricas de uso
- [ ] Análise de desempenho
- [ ] Relatórios automáticos

## Segurança
- [ ] Auditoria de segurança
- [ ] Proteção contra ataques comuns
- [ ] Backup e recuperação
- [ ] Conformidade com LGPD

## Commits Realizados

1. Setup Inicial:
   - `docs: initial project documentation and setup instructions`
   - `chore: add backend gitignore configuration`
   - `chore: add frontend gitignore configuration`

2. Backend:
   - `feat: initialize django project with core apps structure`
   - `build: add initial python dependencies`
   - `chore: add environment variables template`
   - `feat: configure django rest framework and dependencies in settings.py`
   - `feat: add jwt authentication configuration`
   - `feat: enhance cors configuration and security headers`
   - `feat: setup swagger/openapi documentation`
   - `feat: implement data models for all apps`
   - `fix: resolve database migration issues`
   - `feat: add users, courses, scheduling, quizzes, progress apps` (`b6f9d1f`)
   - `fix: modify migration order so that apps use user's app migration first` (`1b8d10d`)
   - `feat: add Supabase connection configuration` (`6ffc12e`)
   - `fix: resolve UserProfile db_table name conflict` (`5a23f4b`)
   - `feat: add script to generate SQL schema for Supabase` (`3c8091e`)
   - `fix: resolve linter issues in settings.py` (`abe1dd5`)

3. Frontend:
   - `feat: initialize next.js project with typescript and tailwind`
   - `build: add initial npm dependencies`
   - `chore: add frontend configuration files`
   - `feat: add initial public assets`
   - `chore: add frontend environment variables template`

## Geração de Schema para Supabase

O projeto inclui um script para gerar um schema SQL compatível com o Supabase:

```bash
cd backend
python3 generate_supabase_schema.py
```

Este script irá criar um arquivo `supabase_schema.sql` que contém:
- Definições de tabelas para todos os modelos
- Relacionamentos de chave estrangeira
- Índices
- Triggers para campos de timestamp (created_at/updated_at)

Isso é útil quando:
- Configurando uma nova instância do Supabase
- Sincronizando seus modelos Django com o Supabase
- Verificando a compatibilidade da estrutura do banco de dados

## Notas de Desenvolvimento

### Convenções
1. Commits seguem o padrão Conventional Commits
2. Código segue PEP 8 (Python) e ESLint/Prettier (JavaScript/TypeScript)
3. Documentação em português, commits em inglês
4. Nunca usar `git add .`

### Ambiente de Desenvolvimento
- Python 3.x
- Node.js LTS
- PostgreSQL
- VS Code com extensões recomendadas 