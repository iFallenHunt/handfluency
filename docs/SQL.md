

## **Modelagem do Banco de Dados** 📊  

### **📌 Usuários (`users`)**  
Armazena informações de alunos, professores e administradores.  

| Campo         | Tipo         | Descrição |
|--------------|-------------|-----------|
| `id`         | UUID (PK)   | Identificador único |
| `nome`       | VARCHAR(255) | **Obrigatório** |
| `email`      | VARCHAR(255) | **Único e obrigatório** |
| `telefone`   | VARCHAR(20)  | **Obrigatório** |
| `senha`      | VARCHAR(255) | Hash da senha |
| `cpf`        | VARCHAR(14)  | **Único e obrigatório** |
| `rg`         | VARCHAR(20)  | Opcional |
| `endereco`   | TEXT         | Completo (rua, cidade, estado, CEP) |
| `data_nasc`  | DATE         | Data de nascimento |
| `foto_perfil`| TEXT         | URL da foto (opcional) |
| `tipo`       | ENUM        | **admin, professor, aluno** |
| `data_criacao` | TIMESTAMP  | Registro de criação |

---

### **📌 Permissões (`permissions`)**  
Define permissões extras para administradores.  

| Campo         | Tipo       | Descrição |
|--------------|-----------|-----------|
| `id`         | UUID (PK) | Identificador único |
| `admin_id`   | UUID (FK) | Referência para `users(id)` |
| `permissao`  | TEXT      | Nome da permissão concedida |

---

### **📌 Assinaturas (`subscriptions`)**  
Registra os planos adquiridos pelos alunos.  

| Campo         | Tipo         | Descrição |
|--------------|-------------|-----------|
| `id`         | UUID (PK)   | Identificador único |
| `aluno_id`   | UUID (FK)   | Referência para `users(id)` |
| `plano`      | ENUM        | **gravadas, grupo, particular, full** |
| `status`     | ENUM        | **ativo, cancelado, expirado** |
| `data_inicio`| TIMESTAMP   | Data de início |
| `data_fim`   | TIMESTAMP   | Data de término |
| `auto_renovacao` | BOOLEAN | Indica renovação automática |

---

### **📌 Cursos (`courses`)**  
Os cursos disponíveis na plataforma.  

| Campo       | Tipo         | Descrição |
|------------|-------------|-----------|
| `id`       | UUID (PK)   | Identificador único |
| `nome`     | VARCHAR(255)| Nome do curso |
| `descricao`| TEXT        | Descrição detalhada |
| `lingua`   | ENUM        | **Libras, ASL, BSL** (expandível no futuro) |
| `ativo`    | BOOLEAN     | Curso ativo ou não |

---

### **📌 Módulos (`modules`)**  
Cada curso contém módulos organizados.  

| Campo       | Tipo       | Descrição |
|------------|-----------|-----------|
| `id`       | UUID (PK) | Identificador único |
| `curso_id` | UUID (FK) | Referência para `courses(id)` |
| `titulo`   | TEXT      | Nome do módulo |
| `ordem`    | INT       | Ordem no curso |

---

### **📌 Aulas (`lessons`)**  
Cada módulo contém várias aulas.  

| Campo       | Tipo       | Descrição |
|------------|-----------|-----------|
| `id`       | UUID (PK) | Identificador único |
| `modulo_id`| UUID (FK) | Referência para `modules(id)` |
| `titulo`   | TEXT      | Nome da aula |
| `descricao`| TEXT      | Descrição da aula |
| `ordem`    | INT       | Ordem no módulo |

---

### **📌 Vídeos (`videos`)**  
Cada aula pode conter múltiplos vídeos.  

| Campo       | Tipo       | Descrição |
|------------|-----------|-----------|
| `id`       | UUID (PK) | Identificador único |
| `aula_id`  | UUID (FK) | Referência para `lessons(id)` |
| `url`      | TEXT      | URL do vídeo |
| `duracao`  | INT       | Duração em segundos |

---

### **📌 Progresso (`progress`)**  
Registra o avanço do aluno.  

| Campo       | Tipo       | Descrição |
|------------|-----------|-----------|
| `id`       | UUID (PK) | Identificador único |
| `aluno_id` | UUID (FK) | Referência para `users(id)` |
| `aula_id`  | UUID (FK) | Aula concluída |
| `video_id` | UUID (FK) | Último vídeo visto |
| `completo` | BOOLEAN   | Se a aula foi concluída |

---

### **📌 Quizzes (`quizzes`)**  
Cada aula tem um quiz obrigatório.  

| Campo       | Tipo       | Descrição |
|------------|-----------|-----------|
| `id`       | UUID (PK) | Identificador único |
| `aula_id`  | UUID (FK) | Referência para `lessons(id)` |
| `pergunta` | TEXT      | Texto da pergunta |
| `opcoes`   | JSONB     | Opções de resposta |
| `resposta` | TEXT      | Resposta correta |

---

### **📌 Agendamentos de Aulas Ao Vivo (`live_sessions`)**  
As aulas ao vivo disponíveis.  

| Campo         | Tipo       | Descrição |
|--------------|-----------|-----------|
| `id`         | UUID (PK) | Identificador único |
| `professor_id` | UUID (FK) | Professor responsável |
| `curso_id`   | UUID (FK) | Curso relacionado |
| `data_hora`  | TIMESTAMP | Data e hora da aula |
| `tipo`       | ENUM      | **particular, grupo** |
| `limite_alunos` | INT    | Máximo de alunos permitidos |

---

### **📌 Inscrições nas Aulas Ao Vivo (`live_enrollments`)**  
Registra alunos inscritos.  

| Campo       | Tipo       | Descrição |
|------------|-----------|-----------|
| `id`       | UUID (PK) | Identificador único |
| `aluno_id` | UUID (FK) | Referência para `users(id)` |
| `aula_id`  | UUID (FK) | Referência para `live_sessions(id)` |

---

### **📌 Gamificação (`gamification`)**  
Registro de pontos por ação.  

| Campo        | Tipo       | Descrição |
|-------------|-----------|-----------|
| `id`        | UUID (PK) | Identificador único |
| `aluno_id`  | UUID (FK) | Referência para `users(id)` |
| `tipo`      | ENUM      | **video, quiz, modulo, aula_ao_vivo** |
| `pontos`    | INT       | Quantidade de pontos ganhos |

---

### **📌 Ranking de Pontuação (`leaderboard`)**  
Ranking semanal/mensal.  

| Campo       | Tipo       | Descrição |
|------------|-----------|-----------|
| `id`       | UUID (PK) | Identificador único |
| `aluno_id` | UUID (FK) | Referência para `users(id)` |
| `pontos`   | INT       | Total acumulado |
| `periodo`  | ENUM      | **semanal, mensal** |

---

### **📌 Avaliações (`reviews`)**  
Os alunos avaliam aulas ao vivo.  

| Campo       | Tipo       | Descrição |
|------------|-----------|-----------|
| `id`       | UUID (PK) | Identificador único |
| `aula_id`  | UUID (FK) | Aula avaliada |
| `aluno_id` | UUID (FK) | Aluno que avaliou |
| `nota`     | INT       | 1 a 5 estrelas |
| `comentario` | TEXT    | Texto opcional |

---
