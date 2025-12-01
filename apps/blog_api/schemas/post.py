from datetime import datetime
from ninja import Schema
from .category import CategorySchema


class PostSchema(Schema):
    id: int
    name: str
    short_description: str
    views_qty: int
    preview: str | None = None
    category: CategorySchema
    created_at: datetime


class PaginatedPostsSchema(Schema):
    limit: int
    offset: int
    total: int
    posts: list[PostSchema]


class PostCreateSchema(Schema):
    name: str
    short_description: str
    full_description: str | None = None
    category_id: int
    author_id: int


class PostUpdateSchema(Schema):
    name: str | None = None
    short_description: str | None = None
    full_description: str | None = None
    category_id: int | None = None
    author_id: int | None = None

class PostAuthorSchema(Schema):
    id: int
    username: str


class PostCommentSchema(Schema):
    id: int
    text: str
    author: PostAuthorSchema
    created_at: datetime


class PostCommentCreateSchema(Schema):
    text: str
    author_id: int


class PostPhotoSchema(Schema):
    id: int
    photo: str


class PostDetailSchema(Schema):
    id: int
    name: str
    full_description: str | None = None
    views_qty: int
    category: CategorySchema
    author: PostAuthorSchema
    preview: str | None = None
    total_likes: int
    total_dislikes: int
    total_comments: int
    comments: list[PostCommentSchema]
    photos: list[PostPhotoSchema]
    created_at: datetime

    @staticmethod
    def resolve_total_likes(obj):
        return obj.likes.user.all().count()

    @staticmethod
    def resolve_total_dislikes(obj):
        return obj.dislikes.user.all().count()

    @staticmethod
    def resolve_total_comments(obj):
        return obj.comments.all().count()
# id
# name
# short_description
# views
# created_at datetime
