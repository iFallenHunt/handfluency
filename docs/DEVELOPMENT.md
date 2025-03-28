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
   - `refactor: otimizar modelos para uso com Supabase` (`a7d83b7`)
   - `fix: corrigir acesso a atributos de ForeignKey nos modelos` (`69be012`)
   - `feat: implement optimized Quiz models for Supabase` (`6a4fda2`)

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

## Implementações Realizadas

Este documento registra as principais implementações, mudanças e decisões de design do projeto.

### Configuração do Ambiente

- Criação do ambiente virtual e instalação das dependências (`2184dda`)
- Configuração inicial do projeto Django (`f6e2c45`)

### Modelagem de Dados

- Criação dos modelos principais: User, Course, Module, Lesson (`3b71f82`)
- Implementação das relações entre modelos e validações (`5e9ad91`)

### Commits Realizados

- Configuração inicial do projeto Django (`f6e2c45`)
- Implementação do modelo de usuário customizado (`3b71f82`)
- Criação dos modelos de cursos e aulas (`5e9ad91`)
- Implementação do sistema de permissões (`7d4ef08`)
- Criação do app de progresso dos alunos (`b6932c1`) 
- Adição de documentação técnica inicial (`d49a760`)
- Criação de migrações iniciais (`1a8ef2b`)
- Implementação do admin para gerenciamento de dados (`a3c6f09`)
- Implementação dos modelos de quiz e questões (`e5f7ab3`)
- Configuração do ambiente de desenvolvimento (`9c81d5e`)
- Implementação dos modelos de agendamento de aulas (`c4a7f2e`)
- Adição de apps users, courses, scheduling, quizzes, progress (`b6f9d1f`)
- Modificação da ordem de migração para usar migração de app de usuário primeiro (`1b8d10d`)
- Adição da configuração de conexão com Supabase (`6ffc12e`)
- Resolução do conflito de nome db_table no UserProfile (`5a23f4b`)
- Adição de script para gerar schema SQL para Supabase (`3c8091e`)
- Resolução de problemas linter em settings.py (`abe1dd5`)
- Otimização de acesso a ForeignKey e correção de validação de tipo em modelos (`aa5ead9`)
- Refatoração dos modelos para otimização com Supabase (`090972a`)
- Implementação de modelos otimizados para Quizzes (`6a4fda2`)

### Geração de Schema para Supabase

Foi implementado um script para gerar automaticamente um schema SQL compatível com o Supabase a partir dos modelos Django:

```bash
python backend/generate_supabase_schema.py
```

Este script gera um arquivo `supabase_schema.sql` que pode ser importado no Supabase para criar todas as tabelas necessárias, incluindo:

1. Definição de tipos de dados apropriados para PostgreSQL
2. Criação de UUIDs para chaves primárias
3. Configuração de chaves estrangeiras e relacionamentos 
4. Criação de índices para otimizar consultas

### Otimização de Modelos para Supabase

Na refatoração dos modelos (`090972a`), foram implementadas várias otimizações e melhorias:

1. **Implementação de Modelo Base**:
   - Criação da classe `SupabaseBaseModel` com campos comuns para todos os modelos
   - Uso de UUIDs para chaves primárias, compatíveis com Supabase
   - Gerenciamento automático de timestamps de criação e atualização

2. **Otimização de Acesso a Objetos Relacionados**:
   - Implementação da classe `RelatedObjectCache` para minimizar consultas ao banco
   - Funções utilitárias para acesso seguro a atributos de objetos relacionados
   - Tratamento robusto de exceções nas referências entre modelos

3. **Conversão de Campos de Mídia**:
   - Alteração de `ImageField` para `URLField` para compatibilidade com buckets do Supabase
   - Aumento do tamanho máximo das URLs para acomodar URLs do Storage do Supabase

4. **Melhoria na Definição de Índices**:
   - Adição de índices específicos para campos de busca frequente
   - Definição explícita de nomes de tabelas via `db_table` para controle no PostgreSQL
   
5. **Tipagem Segura**:
   - Adição de tipagem Python em métodos e propriedades
   - Uso do módulo `typing` para definir tipos genéricos e retornos de métodos 

## Otimizações para Modelos no Supabase

### Implementação Base
- Criação da classe `SupabaseBaseModel` que estende `models.Model` com campos comuns
- Implementação do sistema de cache para objetos relacionados usando `RelatedObjectCache`
- Conversão de campos `ImageField` para `URLField` para integração com storage do Supabase
- Melhoria nos índices para consultas mais eficientes
- Manipulação robusta de exceções ao acessar objetos relacionados
- Tipagem estrita em Python usando o módulo `typing`

### Modelos Otimizados

#### Usuários
Modelos no app `users` foram refatorados para:
- Usar o modelo base do Supabase
- Implementar cache de objetos relacionados
- Definir índices otimizados para consultas frequentes

#### Cursos
Modelos no app `courses` foram refatorados para:
- Usar o modelo base do Supabase
- Implementar cache para consulta eficiente de objetos relacionados
- Tratamento seguro de acesso a Foreign Keys
- Índices personalizados para ordenação e filtragem

#### Quizzes
Modelos no app `quizzes` foram implementados com:
- Estrutura base do Supabase com cache de objetos relacionados
- Métodos de conveniência para cálculo de pontuação e verificação de respostas
- Armazenamento otimizado para mídia usando URLs
- Índices estratégicos para consultas frequentes
- Tratamento seguro de acesso a objetos relacionados
- Campos específicos para rastreamento de tentativas e respostas

Os modelos implementados incluem:
- Quiz - Para avaliações com configurações como tempo limite e nota mínima
- Question - Para perguntas com diversos tipos (múltipla escolha, V/F, etc.)
- Answer - Para opções de resposta com indicação de corretude
- QuizAttempt - Para registrar tentativas dos alunos
- QuestionResponse - Para registrar as respostas específicas 