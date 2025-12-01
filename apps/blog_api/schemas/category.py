from ninja import Schema


class CategorySchema(Schema):
    id: int
    name: str


class CategoryCreateSchema(Schema):
    name: str


class CategoryUpdateSchema(Schema):
    name: str
