# handfluency

tive essa ideia ontem estudando ingles na fluency academy, a ideia seria uma plataforma parecida para aulas de libras, onde os professores sao contratados para dar aula na plataforma como pj, sao pagos por aulas ministradas, materias fornecidos pela plataforma, o professor apenas aplica o material

Podemos estruturar os acessos assim:  

1. **Alunos de aulas gravadas** – Têm acesso apenas à plataforma com módulos e vídeos organizados por nível.  
2. **Alunos de aulas de conversação** – Conseguem agendar aulas ao vivo com professores, mas sem acesso ao conteúdo gravado.  
3. **Alunos com acesso completo** – Podem acessar tanto os vídeos gravados quanto agendar aulas ao vivo.  

Isso significa que o sistema de usuários precisa de permissões bem definidas. Podemos criar um painel onde o administrador (ou o próprio aluno) escolhe o plano de acesso, e o sistema libera ou restringe as funcionalidades automaticamente.  

Para o agendamento, o ideal seria algo parecido com um Google Calendar integrado, onde os professores definem horários disponíveis, e os alunos escolhem os horários livres. Assim, conseguimos um fluxo simples e funcional.  

Agora que temos a stack definida, o próximo passo é organizar a arquitetura do projeto. Pensa assim:  

- **Backend (Django)**  
  - Django REST Framework para a API  
  - Autenticação JWT + integração com login Google  
  - Modelos para usuários, cursos, aulas e progresso do aluno  
  - Webhooks para sincronizar pagamentos do Hotmart  

- **Banco de Dados (Supabase)**  
  - PostgreSQL gerenciado com suporte a autenticação e realtime  
  - Armazenamento de dados do usuário, progresso e quizzes  

- **Frontend (React + Next.js)**  
  - Interface moderna com Tailwind CSS  
  - Integração com API do Django para buscar cursos e vídeos  
  - Sistema de autenticação e controle de acesso  

- **Player de Vídeo**  
  - Desenvolvimento do player próprio com tracking de progresso  
  - Integração com vídeos do Vimeo sem redirecionamento externo  


 # regras da ia 

  ## **Projeto: Plataforma de Aulas de Libras**  

### **Visão Geral**  
O projeto é uma plataforma completa para ensino de Libras, com aulas gravadas e um sistema de agendamento de aulas ao vivo. O objetivo é garantir escalabilidade, segurança e uma experiência fluida para os usuários.  


## **Tecnologias Utilizadas**  

### **Backend (Django + DRF)**  
- **Django (Última versão estável)** – [Documentação](https://docs.djangoproject.com/en/stable/)  
- **Django REST Framework (Última versão estável)** – [Documentação](https://www.django-rest-framework.org/)  
- **Django-Allauth** (para login social com Google) – [Documentação](https://django-allauth.readthedocs.io/en/latest/)  
- **Django-CORS-Headers** (para permitir comunicação entre frontend e backend) – [Documentação](https://pypi.org/project/django-cors-headers/)  
- **PyJWT** (para autenticação JWT) – [Documentação](https://pyjwt.readthedocs.io/en/stable/)  

### **Banco de Dados (Supabase - PostgreSQL)**  
- **Supabase (Última versão)** – [Documentação](https://supabase.com/docs/)  
- **PostgreSQL (Banco de dados relacional escalável)** – [Documentação](https://www.postgresql.org/docs/)  

### **Frontend (React + Next.js)**  
- **React (Última versão estável)** – [Documentação](https://react.dev/)  
- **Next.js (Última versão estável)** – [Documentação](https://nextjs.org/docs)  
- **Tailwind CSS (para estilização rápida e moderna)** – [Documentação](https://tailwindcss.com/docs)  
- **Zustand (para gerenciamento de estado simples e eficiente)** – [Documentação](https://docs.pmnd.rs/zustand)  

### **Player de Vídeo (Desenvolvimento Próprio)**  
- **Custom Video Player**  
  - Play/Pause  
  - Ajuste de velocidade  
  - Tracking de progresso  

### **Autenticação e Segurança**  
- **JWT (JSON Web Tokens para autenticação segura)** – [Documentação](https://jwt.io/)  
- **OAuth (Login social via Google)** – [Documentação](https://developers.google.com/identity)  

### **Integração de Pagamentos (Hotmart)**  
- **Hotmart Webhooks** – [Documentação](https://developers.hotmart.com/docs/en/webhooks)  

---

## **Padrões de Código e Qualidade**  

### **1. Padrão de Estrutura do Projeto**  
O projeto seguirá a estrutura modular, organizada para facilitar a escalabilidade e manutenção:  

```
plataforma-libras/
├── backend/ (Django)
│   ├── core/
│   │   ├── settings.py
│   │   ├── urls.py
│   │   ├── wsgi.py
│   ├── apps/
│   │   ├── users/
│   │   ├── courses/
│   │   ├── quizzes/
│   │   ├── live_classes/
│   ├── requirements.txt
│   ├── manage.py
│   ├── Dockerfile
│   ├── .env
│   └── ...
├── frontend/ (React + Next.js)
│   ├── components/
│   ├── pages/
│   ├── styles/
│   ├── public/
│   ├── package.json
│   ├── .eslintrc.js
│   ├── .prettierrc
│   ├── next.config.js
│   ├── tsconfig.json
│   ├── Dockerfile
│   └── ...
```

---

### **2. Padrões de Código**
Todas as tecnologias seguirão os padrões recomendados para evitar retrabalho e garantir código limpo e eficiente.

#### **Backend (Django)**
- **PEP 8** – Guia oficial de estilo de código Python  
- **PEP 20** – Princípios do Zen do Python  
- **Uso de DRF ViewSets** – Para manter a API organizada  
- **Factory Boy + Pytest** – Para testes unitários  

#### **Frontend (React + Next.js)**
- **Uso de Functional Components e Hooks** – Evitar classes para código mais limpo  
- **TypeScript** – Tipagem estática para evitar erros  
- **ESLint + Prettier** – Garantia de código formatado corretamente  
- **Atomic Design** – Organização de componentes reutilizáveis  

---

### **3. Padrão de Commits**
Usaremos **Conventional Commits**, garantindo histórico claro e organizado:

**Formato:**  
```
<tipo>(escopo opcional): descrição breve
```
**Exemplos:**  
```
feat(auth): adiciona login com Google
fix(video-player): corrige bug no tracking de progresso
refactor(api): melhora estrutura de endpoints para cursos
docs(readme): adiciona documentação inicial
```

**Tipos aceitos:**  
- **feat** – Nova funcionalidade  
- **fix** – Correção de bug  
- **refactor** – Refatoração sem mudança de funcionalidade  
- **docs** – Mudança na documentação  
- **test** – Adição ou modificação de testes  
- **chore** – Alterações sem impacto no código (configurações, dependências)  

---

## **Fluxo de Desenvolvimento**
1. **Setup inicial do repositório** – Criar estrutura base do Django e Next.js  
2. **Implementar autenticação** – Backend (JWT e Google OAuth) e Frontend (integração)  
3. **Criar modelagem do banco de dados** – Cursos, módulos, aulas, quizzes e agendamentos  
4. **Desenvolver API REST** – Endpoints para acesso aos dados  
5. **Criar player de vídeo** – Implementação do reprodutor customizado  
6. **Desenvolver interface** – Criar UI moderna e responsiva  
7. **Testes e validação** – Garantir funcionamento correto  
8. **Deploy e integração com Hotmart** – Configuração para produção  

---