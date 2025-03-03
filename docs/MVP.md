# MVP (Minimum Viable Product) - Hand Fluency

## Objetivo
Criar uma plataforma funcional para ensino de Libras que permita:
1. Alunos assistirem aulas e fazerem exercícios básicos
2. Professores disponibilizarem conteúdo e acompanharem progresso
3. Agendamento de aulas particulares

## Tempo Total Estimado: 3 Semanas

## Funcionalidades Essenciais

### 1. Sistema de Autenticação Básico (3 dias)
- [x] Configuração inicial do Django REST Framework (4h)
- [x] Configuração de JWT e CORS (4h)
- [ ] Login/Registro simples (sem OAuth) (6h)
- [ ] Diferenciação Aluno/Professor (4h)
- [ ] Testes básicos (4h)

### 2. Gerenciamento de Cursos (5 dias)
#### Backend (3 dias)
- [ ] Modelo de Curso
  - Título, descrição, nível (2h)
  - Upload de vídeos (4h)
  - Organização em módulos (3h)
- [ ] APIs básicas
  - CRUD de cursos (4h)
  - Listagem e filtros simples (3h)
  - Controle de acesso (2h)
- [ ] Testes (4h)

#### Frontend (2 dias)
- [ ] Página de listagem de cursos (4h)
- [ ] Player de vídeo básico (4h)
- [ ] Interface de navegação entre aulas (4h)
- [ ] Testes de componentes (4h)

### 3. Sistema de Agendamento Simplificado (4 dias)
#### Backend (2 dias)
- [ ] Modelo de Agendamento
  - Data, horário, aluno, professor (3h)
  - Status (agendado/cancelado) (2h)
- [ ] APIs básicas
  - Criar/cancelar agendamento (4h)
  - Listar horários disponíveis (3h)
- [ ] Testes (4h)

#### Frontend (2 dias)
- [ ] Calendário simples (6h)
- [ ] Formulário de agendamento (4h)
- [ ] Lista de agendamentos (2h)
- [ ] Testes (4h)

### 4. Sistema de Exercícios Básico (3 dias)
#### Backend (2 dias)
- [ ] Modelo de Exercício
  - Questões de múltipla escolha (3h)
  - Correção automática (3h)
- [ ] APIs básicas
  - Submissão de respostas (3h)
  - Visualização de resultados (2h)
- [ ] Testes (3h)

#### Frontend (1 dia)
- [ ] Interface de exercícios (4h)
- [ ] Exibição de resultados (2h)
- [ ] Testes (2h)

## Requisitos Técnicos Mínimos

### Backend
- Django + DRF
- PostgreSQL
- Armazenamento de vídeos (local para MVP)
- Testes unitários básicos

### Frontend
- Next.js
- Tailwind CSS
- Player de vídeo básico
- Testes de componentes essenciais

## O que NÃO está no MVP
1. Autenticação social (Google, Facebook)
2. Sistema de gamificação
3. Analytics avançados
4. Chat em tempo real
5. Sistema de notificações
6. Upload de vídeos pelos professores (inicial será manual)
7. Pagamentos
8. App mobile

## Métricas de Sucesso do MVP
1. Alunos conseguem:
   - Se cadastrar e fazer login
   - Assistir aulas
   - Fazer exercícios básicos
   - Agendar aulas particulares

2. Professores conseguem:
   - Gerenciar seus horários
   - Ver alunos agendados
   - Acompanhar progresso básico

## Próximos Passos Pós-MVP
1. Implementar autenticação social
2. Adicionar sistema de pagamentos
3. Desenvolver analytics
4. Criar app mobile
5. Implementar chat em tempo real

## Estimativa de Custos Iniciais
1. Domínio e Hospedagem: ~$20/mês
2. Servidor de Produção: ~$30/mês
3. Armazenamento: ~$20/mês
4. Total Estimado: ~$70/mês

## Cronograma de Entregas

### Semana 1
- Setup inicial ✓
- Sistema de autenticação
- Modelos básicos de curso

### Semana 2
- APIs de cursos
- Frontend básico
- Sistema de agendamento

### Semana 3
- Sistema de exercícios
- Testes e correções
- Deploy inicial

## Checkpoints Diários
- Reunião de 15min no início do dia
- Code review ao final do dia
- Atualização do DEVELOPMENT.md

## Definition of Done (DoD)
- Código testado
- Code review realizado
- Documentação atualizada
- Funcionalidade testada em ambiente de desenvolvimento
- Sem erros no console
- Responsivo em desktop/tablet 