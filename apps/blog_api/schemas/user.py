from datetime import datetime
from ninja import Schema

from apps.blog_api.schemas.post import PostCommentSchema, PostSchema


class UserSchema(Schema):
    id: int
    username: str


class UserProfileSchema(Schema):
    id: int
    username: str
    email: str | None = None
    date_joined: datetime
    comments: list[PostCommentSchema]
    posts: list[PostSchema]


class UserRegistrationSchema(Schema):
    username: str
    email: str
    first_name: str
    password: str
    password2: str


