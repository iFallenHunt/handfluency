-- Esquema gerado automaticamente para o Supabase


-- Habilitar extensões necessárias
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- Função para atualizar o campo 'updated_at'
CREATE OR REPLACE FUNCTION update_timestamp()
RETURNS TRIGGER AS $$
BEGIN
   NEW.updated_at = now(); 
   RETURN NEW;
END;
$$ language 'plpgsql';

-- Tabelas para o app rest_framework

-- Tabelas para o app rest_framework_simplejwt

-- Tabelas para o app drf_yasg

-- Tabelas para o app django_extensions

-- Tabelas para o app users

-- Tabela: users
CREATE TABLE users (
    password VARCHAR(128) NOT NULL,
    last_login TIMESTAMP WITH TIME ZONE NULL,
    is_superuser BOOLEAN NOT NULL DEFAULT false,
    username VARCHAR(150) NOT NULL,
    first_name VARCHAR(150) NOT NULL,
    last_name VARCHAR(150) NOT NULL,
    email VARCHAR(254) NOT NULL,
    is_staff BOOLEAN NOT NULL DEFAULT false,
    is_active BOOLEAN NOT NULL DEFAULT true,
    date_joined TIMESTAMP WITH TIME ZONE NOT NULL,
    id UUID NOT NULL,
    user_type VARCHAR(10) NOT NULL DEFAULT student,
    bio TEXT NOT NULL,
    profile_picture VARCHAR(100) NULL,
    specializations VARCHAR(255) NOT NULL,
    level VARCHAR(50) NOT NULL,
    google_id VARCHAR(100) NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

CREATE TRIGGER update_users_timestamp
BEFORE UPDATE ON users
FOR EACH ROW
EXECUTE FUNCTION update_timestamp();
                        
-- Tabela: user_profiles
CREATE TABLE user_profiles (
    id UUID NOT NULL,
    phone_number VARCHAR(20) NOT NULL,
    notification_preferences JSONB NOT NULL,
    available_hours JSONB NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL
);

-- Tabelas para o app courses

-- Tabela: courses_course
CREATE TABLE courses_course (
    id BIGSERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    slug VARCHAR(50) NOT NULL,
    description TEXT NOT NULL,
    level VARCHAR(20) NOT NULL DEFAULT basic,
    cover_image VARCHAR(100) NULL,
    preview_video VARCHAR(200) NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL,
    average_rating DECIMAL(3,2) NOT NULL DEFAULT 0.0
);

-- Tabela: courses_module
CREATE TABLE courses_module (
    id BIGSERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    description TEXT NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL
);

-- Tabela: courses_lesson
CREATE TABLE courses_lesson (
    id BIGSERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    description TEXT NOT NULL,
    video_url VARCHAR(200) NOT NULL,
    is_free BOOLEAN NOT NULL DEFAULT false,
    is_active BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL,
    supplementary_material TEXT NOT NULL
);

-- Tabela: courses_enrollment
CREATE TABLE courses_enrollment (
    id BIGSERIAL PRIMARY KEY,
    enrolled_at TIMESTAMP WITH TIME ZONE NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT true,
    completed BOOLEAN NOT NULL DEFAULT false,
    last_accessed TIMESTAMP WITH TIME ZONE NULL
);

-- Tabela: courses_courserating
CREATE TABLE courses_courserating (
    id BIGSERIAL PRIMARY KEY,
    comment TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL
);

-- Tabelas para o app scheduling

-- Tabela: scheduling_teacheravailability
CREATE TABLE scheduling_teacheravailability (
    id BIGSERIAL PRIMARY KEY,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL
);

-- Tabela: scheduling_scheduledclass
CREATE TABLE scheduling_scheduledclass (
    id BIGSERIAL PRIMARY KEY,
    date DATE NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT scheduled,
    topic VARCHAR(200) NOT NULL,
    notes TEXT NOT NULL,
    meeting_link VARCHAR(200) NOT NULL,
    feedback TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL
);

-- Tabela: scheduling_classnotification
CREATE TABLE scheduling_classnotification (
    id BIGSERIAL PRIMARY KEY,
    notification_type VARCHAR(20) NOT NULL,
    message TEXT NOT NULL,
    sent_at TIMESTAMP WITH TIME ZONE NOT NULL,
    read BOOLEAN NOT NULL DEFAULT false,
    read_at TIMESTAMP WITH TIME ZONE NULL
);

-- Tabelas para o app quizzes

-- Tabela: quizzes_quiz
CREATE TABLE quizzes_quiz (
    id BIGSERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    description TEXT NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL
);

-- Tabela: quizzes_question
CREATE TABLE quizzes_question (
    id BIGSERIAL PRIMARY KEY,
    text TEXT NOT NULL,
    question_type VARCHAR(20) NOT NULL DEFAULT multiple_choice,
    image VARCHAR(100) NULL,
    video_url VARCHAR(200) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL
);

-- Tabela: quizzes_answer
CREATE TABLE quizzes_answer (
    id BIGSERIAL PRIMARY KEY,
    text VARCHAR(255) NOT NULL,
    is_correct BOOLEAN NOT NULL DEFAULT false,
    explanation TEXT NOT NULL
);

-- Tabela: quizzes_quizattempt
CREATE TABLE quizzes_quizattempt (
    id BIGSERIAL PRIMARY KEY,
    status VARCHAR(20) NOT NULL DEFAULT in_progress,
    score_percentage DECIMAL(5,2) NOT NULL DEFAULT 0.0,
    started_at TIMESTAMP WITH TIME ZONE NOT NULL,
    completed_at TIMESTAMP WITH TIME ZONE NULL
);

-- Tabela: quizzes_questionresponse
CREATE TABLE quizzes_questionresponse (
    id BIGSERIAL PRIMARY KEY,
    text_response TEXT NOT NULL,
    video_response_url VARCHAR(200) NOT NULL,
    is_correct BOOLEAN NOT NULL DEFAULT false,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL
);

-- Tabelas para o app progress

-- Tabela: progress_lessonprogress
CREATE TABLE progress_lessonprogress (
    id BIGSERIAL PRIMARY KEY,
    status VARCHAR(20) NOT NULL DEFAULT not_started,
    last_accessed TIMESTAMP WITH TIME ZONE NOT NULL,
    completed_at TIMESTAMP WITH TIME ZONE NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL
);

-- Tabela: progress_courseprogress
CREATE TABLE progress_courseprogress (
    id BIGSERIAL PRIMARY KEY,
    status VARCHAR(20) NOT NULL DEFAULT not_started,
    last_accessed TIMESTAMP WITH TIME ZONE NOT NULL,
    completed_at TIMESTAMP WITH TIME ZONE NULL,
    quiz_average_score DECIMAL(5,2) NOT NULL DEFAULT 0.0,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL
);

-- Tabela: progress_achievement
CREATE TABLE progress_achievement (
    id BIGSERIAL PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    description TEXT NOT NULL,
    achievement_type VARCHAR(20) NOT NULL,
    icon VARCHAR(100) NULL,
    requirement_description VARCHAR(255) NOT NULL,
    is_secret BOOLEAN NOT NULL DEFAULT false
);

-- Tabela: progress_studentachievement
CREATE TABLE progress_studentachievement (
    id BIGSERIAL PRIMARY KEY,
    earned_at TIMESTAMP WITH TIME ZONE NOT NULL,
    is_viewed BOOLEAN NOT NULL DEFAULT false
);


-- Chaves Estrangeiras


ALTER TABLE user_profiles
ADD CONSTRAINT fk_user_profiles_user_id
FOREIGN KEY (user_id)
REFERENCES users (id)
ON DELETE CASCADE;


ALTER TABLE courses_course
ADD CONSTRAINT fk_courses_course_created_by_id
FOREIGN KEY (created_by_id)
REFERENCES users (id)
ON DELETE CASCADE;


ALTER TABLE courses_module
ADD CONSTRAINT fk_courses_module_course_id
FOREIGN KEY (course_id)
REFERENCES courses_course (id)
ON DELETE CASCADE;


ALTER TABLE courses_lesson
ADD CONSTRAINT fk_courses_lesson_module_id
FOREIGN KEY (module_id)
REFERENCES courses_module (id)
ON DELETE CASCADE;


ALTER TABLE courses_enrollment
ADD CONSTRAINT fk_courses_enrollment_student_id
FOREIGN KEY (student_id)
REFERENCES users (id)
ON DELETE CASCADE;


ALTER TABLE courses_enrollment
ADD CONSTRAINT fk_courses_enrollment_course_id
FOREIGN KEY (course_id)
REFERENCES courses_course (id)
ON DELETE CASCADE;


ALTER TABLE courses_courserating
ADD CONSTRAINT fk_courses_courserating_student_id
FOREIGN KEY (student_id)
REFERENCES users (id)
ON DELETE CASCADE;


ALTER TABLE courses_courserating
ADD CONSTRAINT fk_courses_courserating_course_id
FOREIGN KEY (course_id)
REFERENCES courses_course (id)
ON DELETE CASCADE;


ALTER TABLE scheduling_teacheravailability
ADD CONSTRAINT fk_scheduling_teacheravailability_teacher_id
FOREIGN KEY (teacher_id)
REFERENCES users (id)
ON DELETE CASCADE;


ALTER TABLE scheduling_scheduledclass
ADD CONSTRAINT fk_scheduling_scheduledclass_student_id
FOREIGN KEY (student_id)
REFERENCES users (id)
ON DELETE CASCADE;


ALTER TABLE scheduling_scheduledclass
ADD CONSTRAINT fk_scheduling_scheduledclass_teacher_id
FOREIGN KEY (teacher_id)
REFERENCES users (id)
ON DELETE CASCADE;


ALTER TABLE scheduling_classnotification
ADD CONSTRAINT fk_scheduling_classnotification_scheduled_class_id
FOREIGN KEY (scheduled_class_id)
REFERENCES scheduling_scheduledclass (id)
ON DELETE CASCADE;


ALTER TABLE scheduling_classnotification
ADD CONSTRAINT fk_scheduling_classnotification_recipient_id
FOREIGN KEY (recipient_id)
REFERENCES users (id)
ON DELETE CASCADE;


ALTER TABLE quizzes_quiz
ADD CONSTRAINT fk_quizzes_quiz_course_id
FOREIGN KEY (course_id)
REFERENCES courses_course (id)
ON DELETE CASCADE;


ALTER TABLE quizzes_quiz
ADD CONSTRAINT fk_quizzes_quiz_lesson_id
FOREIGN KEY (lesson_id)
REFERENCES courses_lesson (id)
ON DELETE SET NULL;


ALTER TABLE quizzes_quiz
ADD CONSTRAINT fk_quizzes_quiz_created_by_id
FOREIGN KEY (created_by_id)
REFERENCES users (id)
ON DELETE CASCADE;


ALTER TABLE quizzes_question
ADD CONSTRAINT fk_quizzes_question_quiz_id
FOREIGN KEY (quiz_id)
REFERENCES quizzes_quiz (id)
ON DELETE CASCADE;


ALTER TABLE quizzes_answer
ADD CONSTRAINT fk_quizzes_answer_question_id
FOREIGN KEY (question_id)
REFERENCES quizzes_question (id)
ON DELETE CASCADE;


ALTER TABLE quizzes_quizattempt
ADD CONSTRAINT fk_quizzes_quizattempt_student_id
FOREIGN KEY (student_id)
REFERENCES users (id)
ON DELETE CASCADE;


ALTER TABLE quizzes_quizattempt
ADD CONSTRAINT fk_quizzes_quizattempt_quiz_id
FOREIGN KEY (quiz_id)
REFERENCES quizzes_quiz (id)
ON DELETE CASCADE;


ALTER TABLE quizzes_questionresponse
ADD CONSTRAINT fk_quizzes_questionresponse_attempt_id
FOREIGN KEY (attempt_id)
REFERENCES quizzes_quizattempt (id)
ON DELETE CASCADE;


ALTER TABLE quizzes_questionresponse
ADD CONSTRAINT fk_quizzes_questionresponse_question_id
FOREIGN KEY (question_id)
REFERENCES quizzes_question (id)
ON DELETE CASCADE;


ALTER TABLE progress_lessonprogress
ADD CONSTRAINT fk_progress_lessonprogress_student_id
FOREIGN KEY (student_id)
REFERENCES users (id)
ON DELETE CASCADE;


ALTER TABLE progress_lessonprogress
ADD CONSTRAINT fk_progress_lessonprogress_lesson_id
FOREIGN KEY (lesson_id)
REFERENCES courses_lesson (id)
ON DELETE CASCADE;


ALTER TABLE progress_courseprogress
ADD CONSTRAINT fk_progress_courseprogress_student_id
FOREIGN KEY (student_id)
REFERENCES users (id)
ON DELETE CASCADE;


ALTER TABLE progress_courseprogress
ADD CONSTRAINT fk_progress_courseprogress_course_id
FOREIGN KEY (course_id)
REFERENCES courses_course (id)
ON DELETE CASCADE;


ALTER TABLE progress_studentachievement
ADD CONSTRAINT fk_progress_studentachievement_student_id
FOREIGN KEY (student_id)
REFERENCES users (id)
ON DELETE CASCADE;


ALTER TABLE progress_studentachievement
ADD CONSTRAINT fk_progress_studentachievement_achievement_id
FOREIGN KEY (achievement_id)
REFERENCES progress_achievement (id)
ON DELETE CASCADE;


ALTER TABLE progress_studentachievement
ADD CONSTRAINT fk_progress_studentachievement_related_course_id
FOREIGN KEY (related_course_id)
REFERENCES courses_course (id)
ON DELETE SET NULL;


-- Índices

CREATE UNIQUE INDEX idx_users_username ON users (username);
CREATE UNIQUE INDEX idx_users_id ON users (id);
CREATE UNIQUE INDEX idx_users_google_id ON users (google_id);

CREATE UNIQUE INDEX idx_user_profiles_id ON user_profiles (id);
CREATE UNIQUE INDEX idx_user_profiles_user_id ON user_profiles (user_id);

CREATE UNIQUE INDEX idx_courses_course_id ON courses_course (id);
CREATE UNIQUE INDEX idx_courses_course_slug ON courses_course (slug);
CREATE INDEX idx_courses_course_created_by_id ON courses_course (created_by_id);

CREATE UNIQUE INDEX idx_courses_module_id ON courses_module (id);
CREATE INDEX idx_courses_module_course_id ON courses_module (course_id);

CREATE UNIQUE INDEX idx_courses_lesson_id ON courses_lesson (id);
CREATE INDEX idx_courses_lesson_module_id ON courses_lesson (module_id);

CREATE UNIQUE INDEX idx_courses_enrollment_id ON courses_enrollment (id);
CREATE INDEX idx_courses_enrollment_student_id ON courses_enrollment (student_id);
CREATE INDEX idx_courses_enrollment_course_id ON courses_enrollment (course_id);

CREATE UNIQUE INDEX idx_courses_courserating_id ON courses_courserating (id);
CREATE INDEX idx_courses_courserating_student_id ON courses_courserating (student_id);
CREATE INDEX idx_courses_courserating_course_id ON courses_courserating (course_id);

CREATE UNIQUE INDEX idx_scheduling_teacheravailability_id ON scheduling_teacheravailability (id);
CREATE INDEX idx_scheduling_teacheravailability_teacher_id ON scheduling_teacheravailability (teacher_id);

CREATE UNIQUE INDEX idx_scheduling_scheduledclass_id ON scheduling_scheduledclass (id);
CREATE INDEX idx_scheduling_scheduledclass_student_id ON scheduling_scheduledclass (student_id);
CREATE INDEX idx_scheduling_scheduledclass_teacher_id ON scheduling_scheduledclass (teacher_id);

CREATE UNIQUE INDEX idx_scheduling_classnotification_id ON scheduling_classnotification (id);
CREATE INDEX idx_scheduling_classnotification_scheduled_class_id ON scheduling_classnotification (scheduled_class_id);
CREATE INDEX idx_scheduling_classnotification_recipient_id ON scheduling_classnotification (recipient_id);

CREATE UNIQUE INDEX idx_quizzes_quiz_id ON quizzes_quiz (id);
CREATE INDEX idx_quizzes_quiz_course_id ON quizzes_quiz (course_id);
CREATE INDEX idx_quizzes_quiz_lesson_id ON quizzes_quiz (lesson_id);
CREATE INDEX idx_quizzes_quiz_created_by_id ON quizzes_quiz (created_by_id);

CREATE UNIQUE INDEX idx_quizzes_question_id ON quizzes_question (id);
CREATE INDEX idx_quizzes_question_quiz_id ON quizzes_question (quiz_id);

CREATE UNIQUE INDEX idx_quizzes_answer_id ON quizzes_answer (id);
CREATE INDEX idx_quizzes_answer_question_id ON quizzes_answer (question_id);

CREATE UNIQUE INDEX idx_quizzes_quizattempt_id ON quizzes_quizattempt (id);
CREATE INDEX idx_quizzes_quizattempt_student_id ON quizzes_quizattempt (student_id);
CREATE INDEX idx_quizzes_quizattempt_quiz_id ON quizzes_quizattempt (quiz_id);

CREATE UNIQUE INDEX idx_quizzes_questionresponse_id ON quizzes_questionresponse (id);
CREATE INDEX idx_quizzes_questionresponse_attempt_id ON quizzes_questionresponse (attempt_id);
CREATE INDEX idx_quizzes_questionresponse_question_id ON quizzes_questionresponse (question_id);

CREATE UNIQUE INDEX idx_progress_lessonprogress_id ON progress_lessonprogress (id);
CREATE INDEX idx_progress_lessonprogress_student_id ON progress_lessonprogress (student_id);
CREATE INDEX idx_progress_lessonprogress_lesson_id ON progress_lessonprogress (lesson_id);

CREATE UNIQUE INDEX idx_progress_courseprogress_id ON progress_courseprogress (id);
CREATE INDEX idx_progress_courseprogress_student_id ON progress_courseprogress (student_id);
CREATE INDEX idx_progress_courseprogress_course_id ON progress_courseprogress (course_id);

CREATE UNIQUE INDEX idx_progress_achievement_id ON progress_achievement (id);

CREATE UNIQUE INDEX idx_progress_studentachievement_id ON progress_studentachievement (id);
CREATE INDEX idx_progress_studentachievement_student_id ON progress_studentachievement (student_id);
CREATE INDEX idx_progress_studentachievement_achievement_id ON progress_studentachievement (achievement_id);
CREATE INDEX idx_progress_studentachievement_related_course_id ON progress_studentachievement (related_course_id);

