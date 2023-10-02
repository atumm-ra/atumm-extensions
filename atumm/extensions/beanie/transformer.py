from typing import Type, TypeVar

from beanie import Document
from pydantic import BaseModel

DomainEntity = TypeVar("DomainEntity", bound=BaseModel)
BeanieEntity = TypeVar("BeanieEntity", bound=Document)


class BeanieTransformer:
    domain_entity: Type[DomainEntity]
    beanie_entity: Type[BeanieEntity]

    def to_domain_entity(self, beanie_entity: BeanieEntity) -> DomainEntity:
        data = beanie_entity.dict()
        return self.domain_entity(**data)

    def to_beanie_entity(self, domain_entity: DomainEntity) -> BeanieEntity:
        return self.beanie_entity(**domain_entity.dict())
