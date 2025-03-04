```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nome VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    telefone VARCHAR(20) NOT NULL,
    senha VARCHAR(255) NOT NULL,
    cpf VARCHAR(14) UNIQUE NOT NULL,
    rg VARCHAR(20),
    endereco TEXT,
    data_nasc DATE,
    foto_perfil TEXT,
    tipo VARCHAR(20) CHECK (tipo IN ('admin', 'professor', 'aluno')) NOT NULL,
    data_criacao TIMESTAMP DEFAULT now()
);

CREATE TABLE permissions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    admin_id UUID REFERENCES users(id) ON DELETE CASCADE,
    permissao TEXT NOT NULL
);

CREATE TABLE subscriptions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    aluno_id UUID REFERENCES users(id) ON DELETE CASCADE,
    plano VARCHAR(20) CHECK (plano IN ('gravadas', 'grupo', 'particular', 'full')) NOT NULL,
    status VARCHAR(20) CHECK (status IN ('ativo', 'cancelado', 'expirado')) NOT NULL,
    data_inicio TIMESTAMP DEFAULT now(),
    data_fim TIMESTAMP,
    auto_renovacao BOOLEAN DEFAULT FALSE
);

CREATE TABLE courses (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nome VARCHAR(255) NOT NULL,
    descricao TEXT,
    lingua VARCHAR(20) CHECK (lingua IN ('Libras', 'ASL', 'BSL')) NOT NULL,
    ativo BOOLEAN DEFAULT TRUE
);

CREATE TABLE modules (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    curso_id UUID REFERENCES courses(id) ON DELETE CASCADE,
    titulo TEXT NOT NULL,
    ordem INT NOT NULL
);

CREATE TABLE lessons (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    modulo_id UUID REFERENCES modules(id) ON DELETE CASCADE,
    titulo TEXT NOT NULL,
    descricao TEXT,
    ordem INT NOT NULL
);

CREATE TABLE videos (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    aula_id UUID REFERENCES lessons(id) ON DELETE CASCADE,
    url TEXT NOT NULL,
    duracao INT NOT NULL
);

CREATE TABLE progress (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    aluno_id UUID REFERENCES users(id) ON DELETE CASCADE,
    aula_id UUID REFERENCES lessons(id) ON DELETE CASCADE,
    video_id UUID REFERENCES videos(id) ON DELETE CASCADE,
    completo BOOLEAN DEFAULT FALSE
);

CREATE TABLE quizzes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    aula_id UUID REFERENCES lessons(id) ON DELETE CASCADE,
    pergunta TEXT NOT NULL,
    opcoes JSONB NOT NULL,
    resposta TEXT NOT NULL
);

CREATE TABLE live_sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    professor_id UUID REFERENCES users(id) ON DELETE CASCADE,
    curso_id UUID REFERENCES courses(id) ON DELETE CASCADE,
    data_hora TIMESTAMP NOT NULL,
    tipo VARCHAR(20) CHECK (tipo IN ('particular', 'grupo')) NOT NULL,
    limite_alunos INT NOT NULL CHECK (limite_alunos > 0)
);

CREATE TABLE live_enrollments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    aluno_id UUID REFERENCES users(id) ON DELETE CASCADE,
    aula_id UUID REFERENCES live_sessions(id) ON DELETE CASCADE
);

CREATE TABLE gamification (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    aluno_id UUID REFERENCES users(id) ON DELETE CASCADE,
    tipo VARCHAR(20) CHECK (tipo IN ('video', 'quiz', 'modulo', 'aula_ao_vivo')) NOT NULL,
    pontos INT NOT NULL CHECK (pontos >= 0)
);

CREATE TABLE leaderboard (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    aluno_id UUID REFERENCES users(id) ON DELETE CASCADE,
    pontos INT NOT NULL CHECK (pontos >= 0),
    periodo VARCHAR(20) CHECK (periodo IN ('semanal', 'mensal')) NOT NULL
);

CREATE TABLE reviews (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    aula_id UUID REFERENCES live_sessions(id) ON DELETE CASCADE,
    aluno_id UUID REFERENCES users(id) ON DELETE CASCADE,
    nota INT CHECK (nota BETWEEN 1 AND 5) NOT NULL,
    comentario TEXT
);
```

### **Explicações e Melhorias**
- **UUID como chave primária**: Usei `gen_random_uuid()` para gerar UUIDs automaticamente.  
- **Enumeração simulada com `CHECK`**: Como o PostgreSQL não tem `ENUM` nativo em todas as versões, usei `CHECK` para restringir valores.  
- **Restrição de dados (`CHECK`)**: Evita valores inválidos, como notas fora do intervalo 1-5.  
- **Relacionamentos (`FOREIGN KEY` com `ON DELETE CASCADE`)**: Se um usuário for deletado, tudo relacionado a ele é removido automaticamente.  
