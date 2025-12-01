from ninja import Schema


class FAQSchema(Schema):
    id: int
    question: str
    answer: str


class FAQCreateSchema(Schema):
    question: str
    answer: str

