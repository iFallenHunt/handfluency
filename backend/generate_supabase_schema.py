#!/usr/bin/env python
"""
Script para gerar o esquema SQL do Supabase a partir dos modelos Django.
Este script cria um arquivo SQL que pode ser usado para criar as tabelas
no Supabase de acordo com os modelos definidos no Django.
"""
import os
import django
import django.db.models
from textwrap import dedent

# Setup ambiente Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

# Imports do Django após setup
from django.apps import apps


def generate_schema():
    """
    Gera o esquema SQL completo para o Supabase.
    """
    sql_map = {
        'AutoField': 'SERIAL PRIMARY KEY',
        'BigAutoField': 'BIGSERIAL PRIMARY KEY',
        'CharField': 'VARCHAR({})',
        'TextField': 'TEXT',
        'BooleanField': 'BOOLEAN',
        'IntegerField': 'INTEGER',
        'BigIntegerField': 'BIGINT',
        'DecimalField': 'DECIMAL({},{})',
        'DateField': 'DATE',
        'DateTimeField': 'TIMESTAMP WITH TIME ZONE',
        'TimeField': 'TIME',
        'UUIDField': 'UUID',
        'EmailField': 'VARCHAR(254)',
        'URLField': 'VARCHAR(200)',
        'JSONField': 'JSONB',
        'FileField': 'VARCHAR(100)',
        'ImageField': 'VARCHAR(100)',
        'SlugField': 'VARCHAR(50)'
    }
    
    # Saída para o arquivo SQL
    with open('supabase_schema.sql', 'w') as sql_file:
        sql_file.write("-- Esquema gerado automaticamente para o Supabase\n\n")
        
        # Extensões necessárias
        sql_file.write(dedent("""
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
            
        """))
        
        # Criar tabelas para cada modelo
        for app_config in apps.get_app_configs():
            if (app_config.name.startswith('django.') or 
                app_config.name == 'corsheaders'):
                continue
            
            sql_file.write(f"-- Tabelas para o app {app_config.name}\n\n")
            
            for model in app_config.get_models():
                meta = model._meta
                table_name = (meta.db_table if hasattr(meta, 'db_table') 
                            else f"{meta.app_label}_{meta.model_name}")
                
                fields = []
                pk_field = None
                
                sql_file.write(f"-- Tabela: {table_name}\n")
                
                for field in meta.fields:
                    field_class = field.__class__.__name__
                    
                    # Ignorar chaves estrangeiras por enquanto
                    if field.is_relation:
                        continue
                    
                    # Identificar o campo PK
                    if field.primary_key:
                        pk_field = field.name
                    
                    field_def = ""
                    field_type = sql_map.get(field_class)
                    
                    if field_type:
                        if field_class == 'CharField' or field_class == 'SlugField':
                            field_type = field_type.format(field.max_length)
                        elif field_class == 'DecimalField':
                            field_type = field_type.format(
                                field.max_digits, field.decimal_places
                            )
                        
                        nullability = "NULL" if field.null else "NOT NULL"
                        default = ""
                        
                        if hasattr(field, 'default') and field.has_default():
                            if not callable(field.default):
                                default_val = field.default
                                if isinstance(default_val, bool):
                                    default_val = str(default_val).lower()
                                if default_val != "":
                                    default = f"DEFAULT {default_val}"
                        
                        if field_class in ['AutoField', 'BigAutoField']:
                            nullability = ""  # PRIMARY KEY implica NOT NULL
                            default = ""  # SERIAL implica autoincremento
                        
                        field_def = f"{field.column} {field_type} {nullability} {default}".strip()
                        fields.append(field_def)
                
                # Adicionar campos comuns para todos os modelos (se herdam de BaseModel)
                has_base_model = False
                for base in model.__bases__:
                    if base.__name__ == 'BaseModel':
                        has_base_model = True
                        break
                
                if has_base_model:
                    triggers = []
                    
                    # Campos de timestamp se herda de BaseModel
                    if not any(f.startswith('created_at') for f in fields):
                        fields.append("created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()")
                    if not any(f.startswith('updated_at') for f in fields):
                        fields.append("updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()")
                        # Trigger para atualizar o updated_at automaticamente
                        triggers.append(f"""
CREATE TRIGGER update_{table_name}_timestamp
BEFORE UPDATE ON {table_name}
FOR EACH ROW
EXECUTE FUNCTION update_timestamp();
                        """)
                
                # Se não temos uma chave primária definida explicitamente, adicionamos id
                if not pk_field and not any(f.startswith('id ') for f in fields):
                    fields.insert(0, "id SERIAL PRIMARY KEY")
                
                # Criar a tabela
                sql = f"CREATE TABLE {table_name} (\n"
                sql += ",\n".join(f"    {field}" for field in fields)
                sql += "\n);\n"
                
                sql_file.write(sql)
                
                # Adicionar triggers
                if has_base_model and triggers:
                    for trigger in triggers:
                        sql_file.write(trigger)
                
                sql_file.write("\n")
            
        # Segunda passagem: adicionar chaves estrangeiras
        sql_file.write("\n-- Chaves Estrangeiras\n\n")
        
        for app_config in apps.get_app_configs():
            if (app_config.name.startswith('django.') or 
                app_config.name == 'corsheaders'):
                continue
            
            for model in app_config.get_models():
                meta = model._meta
                table_name = (meta.db_table if hasattr(meta, 'db_table') 
                            else f"{meta.app_label}_{meta.model_name}")
                
                for field in meta.fields:
                    if field.is_relation and field.remote_field.model:
                        related_meta = field.remote_field.model._meta
                        related_table = (
                            related_meta.db_table if hasattr(related_meta, 'db_table')
                            else f"{related_meta.app_label}_{related_meta.model_name}"
                        )
                        
                        # Obter o nome da coluna da chave primária na tabela relacionada
                        pk_column = "id"
                        for f in related_meta.fields:
                            if f.primary_key:
                                pk_column = f.column
                                break
                        
                        fk_name = f"fk_{table_name}_{field.column}"
                        
                        on_delete = 'CASCADE'
                        if field.remote_field.on_delete != django.db.models.CASCADE:
                            on_delete = 'SET NULL'
                        
                        # Adicionar a chave estrangeira
                        sql_file.write(dedent(f"""
                            ALTER TABLE {table_name}
                            ADD CONSTRAINT {fk_name}
                            FOREIGN KEY ({field.column})
                            REFERENCES {related_table} ({pk_column})
                            ON DELETE {on_delete};
                            
                        """))
        
        # Índices
        sql_file.write("\n-- Índices\n\n")
        
        for app_config in apps.get_app_configs():
            if (app_config.name.startswith('django.') or 
                app_config.name == 'corsheaders'):
                continue
            
            for model in app_config.get_models():
                meta = model._meta
                table_name = (meta.db_table if hasattr(meta, 'db_table') 
                            else f"{meta.app_label}_{meta.model_name}")
                
                for field in meta.fields:
                    if field.db_index or field.unique:
                        index_name = f"idx_{table_name}_{field.column}"
                        unique = "UNIQUE " if field.unique else ""
                        
                        sql_file.write(
                            f"CREATE {unique}INDEX {index_name} "
                            f"ON {table_name} ({field.column});\n"
                        )
                
                # Adicionar índices para as Meta.indexes definidas
                if hasattr(meta, 'indexes'):
                    for index in meta.indexes:
                        fields_str = ", ".join(index.fields)
                        index_name = index.name or f"idx_{table_name}_{'_'.join(index.fields)}"
                        unique = "UNIQUE " if getattr(index, 'unique', False) else ""
                        
                        sql_file.write(
                            f"CREATE {unique}INDEX {index_name} "
                            f"ON {table_name} ({fields_str});\n"
                        )
                
                sql_file.write("\n")
    
    print(f"Esquema SQL gerado com sucesso! Arquivo: supabase_schema.sql")


if __name__ == "__main__":
    generate_schema()
