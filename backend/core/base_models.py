"""
Módulo contendo classes de modelo base que serão utilizadas por todos os apps.
Otimizado para uso com Supabase como banco de dados.
"""

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
import uuid
from typing import cast, Optional, TypeVar, Generic, Type

# Tipo genérico para modelos
T = TypeVar("T", bound=models.Model)


class SupabaseBaseModel(models.Model):
    """
    Modelo base para todos os modelos que serão armazenados no Supabase.

    Implementa campos comuns como id (UUID), timestamps para criação
    e atualização, e funcionalidades de acesso seguro.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        help_text=_("Identificador único universal"),
    )
    created_at = models.DateTimeField(
        _("criado em"),
        default=timezone.now,
        help_text=_("Data e hora de criação do registro"),
    )
    updated_at = models.DateTimeField(
        _("atualizado em"),
        auto_now=True,
        help_text=_("Data e hora da última atualização do registro"),
    )

    class Meta:
        abstract = True


class RelatedObjectCache(Generic[T]):
    """
    Classe utilitária para armazenar em cache objetos relacionados.

    Implementa um padrão de acesso seguro a objetos relacionados,
    armazenando-os em cache para evitar múltiplas consultas ao banco.
    """

    def __init__(self, model_class: Type[T]):
        self.model_class = model_class
        self._cache: Optional[T] = None

    def get(self, instance: models.Model, field_name: str) -> Optional[T]:
        """
        Recupera o objeto relacionado, usando cache quando disponível.

        Args:
            instance: Instância do modelo que possui o relacionamento
            field_name: Nome do campo ForeignKey ou OneToOne

        Returns:
            O objeto relacionado ou None se não encontrado
        """
        if self._cache is not None:
            return self._cache

        try:
            related_field = getattr(instance, field_name)
            if related_field is None:
                return None

            obj = cast(self.model_class, related_field)
            self._cache = obj
            return obj
        except Exception:
            return None

    def set(self, obj: Optional[T]) -> None:
        """
        Define explicitamente o objeto em cache.

        Args:
            obj: Objeto a ser armazenado em cache
        """
        self._cache = obj

    def clear(self) -> None:
        """Limpa o cache."""
        self._cache = None


# Funções utilitárias para acesso seguro a atributos
def safe_get_related_str_field(
    obj: Optional[models.Model], field_name: str, default: str = ""
) -> str:
    """
    Acessa de forma segura um campo de texto de um objeto relacionado.

    Args:
        obj: Objeto relacionado (possivelmente None)
        field_name: Nome do campo a ser acessado
        default: Valor padrão se o campo não existir

    Returns:
        Valor do campo como string ou o valor padrão
    """
    if obj is None:
        return default

    try:
        value = getattr(obj, field_name, default)
        return str(value)
    except Exception:
        return default


def get_display_name(
    instance: models.Model, id_field: str = "id", prefix: str = "Item"
) -> str:
    """
    Gera um nome de exibição genérico para um objeto.

    Args:
        instance: Instância do modelo
        id_field: Nome do campo de ID
        prefix: Prefixo a ser usado no nome gerado

    Returns:
        String formatada como "Prefixo {id}"
    """
    try:
        obj_id = getattr(instance, id_field)
        return f"{prefix} {obj_id}"
    except Exception:
        return f"{prefix} desconhecido"
