"""
{{ cookiecutter.domain_name.title() }} domain entities.
"""

from pydantic import BaseModel


class DomainEntity(BaseModel):
    """Entidade principal do domínio."""
    pass


class DomainRequest(BaseModel):
    """Modelo de requisição."""
    pass 