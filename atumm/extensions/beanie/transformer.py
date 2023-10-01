from typing import Type, TypeVar

from beanie import Document
from pydantic import BaseModel

DomainEntity = TypeVar("DomainEntity", bound=BaseModel)
BeanieEntity = TypeVar("BeanieEntity", bound=Document)


class BeanieTransformer:
    domain_model: Type[DomainEntity]
    beanie_model: Type[BeanieEntity]

    def to_domain_entity(self, beanie_entity: BeanieEntity) -> DomainEntity:
        data = beanie_entity.dict()
        return self.domain_model(**data)

    def to_beanie_entity(self, domain_entity: DomainEntity) -> BeanieEntity:
        return self.beanie_model(**domain_entity.dict())
