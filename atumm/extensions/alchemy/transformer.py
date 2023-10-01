from typing import Type, TypeVar

from atumm.extensions.alchemy import Base
from pydantic import BaseModel

DomainEntity = TypeVar("DomainEntity", bound=BaseModel)
AlchemyEntity = TypeVar("AlchemyEntity", bound=Base)


class AlchemyTransformer:
    domain_model: Type[DomainEntity]
    alchemy_model: Type[AlchemyEntity]

    def to_domain_entity(self, alchemy_entity: AlchemyEntity) -> DomainEntity:
        return self.domain_model(**alchemy_entity.__dict__)

    def to_alchemy_entity(self, domain_entity: DomainEntity) -> AlchemyEntity:
        return self.alchemy_model(**domain_entity.dict())
