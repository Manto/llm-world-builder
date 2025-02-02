from typing import List, Optional, Dict, Any
from datetime import datetime
import uuid
import strawberry
from app.models.entity import Entity, EntityType


@strawberry.type
class GenerationTemplate:
    fields: List[str]
    systemPrompt: str


@strawberry.type
class EntityTypeGQL:
    id: str  # UUID as string
    name: str
    defaultFields: List[str]

    @classmethod
    def from_db(cls, db_type: EntityType) -> "EntityTypeGQL":
        return cls(
            id=str(db_type.id), name=db_type.name, defaultFields=db_type.default_fields
        )


@strawberry.type
class EntityGQL:
    id: str  # UUID as string
    name: str
    description: Optional[str]
    attributes: strawberry.scalars.JSON
    typeDef: EntityTypeGQL
    createdAt: datetime
    updatedAt: datetime
    children: List["EntityGQL"]
    parents: List["EntityGQL"]

    @classmethod
    async def from_db(cls, db_entity: Entity) -> "EntityGQL":
        return cls(
            id=str(db_entity.id),
            name=db_entity.name,
            description=db_entity.description,
            attributes=db_entity.attributes,
            typeDef=EntityTypeGQL.from_db(await db_entity.awaitable_attrs.type_def),
            createdAt=db_entity.created_at,
            updatedAt=db_entity.updated_at,
            children=[
                cls.from_db(child) for child in await db_entity.awaitable_attrs.children
            ],
            parents=[
                cls.from_db(parent)
                for parent in await db_entity.awaitable_attrs.parents
            ],
        )


@strawberry.input
class EntityTypeInput:
    name: str
    defaultFields: List[str]


@strawberry.input
class EntityTypeUpdateInput:
    name: Optional[str] = None
    defaultFields: Optional[List[str]] = None


@strawberry.input
class EntityInput:
    name: str
    typeId: str  # UUID as string
    description: Optional[str] = None
    attributes: Optional[strawberry.scalars.JSON] = None
    parentIds: Optional[List[str]] = None  # UUIDs as strings


@strawberry.input
class EntityUpdateInput:
    name: Optional[str] = None
    description: Optional[str] = None
    attributes: Optional[strawberry.scalars.JSON] = None
    parentIds: Optional[List[str]] = None  # UUIDs as strings
