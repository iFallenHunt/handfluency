## Development

### Migrations

1. Apply migrations:
   ```bash
   python manage.py migrate
   ```

2. Create new migrations:
   ```bash
   python manage.py makemigrations
   ```

### Commit Log

- Added users, courses, scheduling, quizzes, progress apps (`b6f9d1f`)
- Modified migration order so that apps use user's app migration first (`1b8d10d`)
- Added Supabase connection configuration (`6ffc12e`) 
- Fixed UserProfile db_table name conflict (`5a23f4b`)
- Added script to generate SQL schema for Supabase (`3c8091e`)
- Fixed linter issues in settings.py (`abe1dd5`)

### Supabase Schema Generation

The project includes a script to generate a SQL schema compatible with Supabase:

```bash
cd backend
python3 generate_supabase_schema.py
```

This will create a `supabase_schema.sql` file that contains:
- Table definitions for all models
- Foreign key relationships
- Indexes
- Triggers for timestamp fields (created_at/updated_at)

This is useful when:
- Setting up a new Supabase instance
- Syncing your Django models with Supabase
- Checking database structure compatibility 