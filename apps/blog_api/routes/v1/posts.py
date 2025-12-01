from ninja import Router, File, UploadedFile
from ninja.errors import ValidationError
from apps.main.models import Post, Category, Comment, PostPhoto, Dislike, Like
from django.contrib.auth.models import User
from apps.blog_api.schemas.post import (
    PostSchema,
    PaginatedPostsSchema,
    PostDetailSchema,
    PostCreateSchema,
    PostCommentSchema,
    PostCommentCreateSchema,
    PostUpdateSchema
)
from ninja.pagination import paginate
from django.shortcuts import get_object_or_404
import os
from blog_project import settings
from ninja_jwt.authentication import JWTAuth

posts_router = Router(tags=['Posts'])

# limit - сколько записей с БД показывать
# offset - следующее количество записей для отображения
# ?limit=5&offset=5


# №2 способ
@posts_router.get('/api/posts/', response=list[PostSchema])
@paginate
def get_posts(request):
    posts = Post.objects.all()
    return posts


# №1 способ
# @posts_router.post('/api/posts/', response=PaginatedPostsSchema)
# def get_paginated_posts(request, limit: int = 3, offset: int = 0):
#     posts = Post.objects.all()
#     total_posts = posts.count()  # получаем общее кол-во статей
#     paginated_posts = [
#         PostSchema.model_validate(obj)
#         for obj in posts[offset:offset + limit]
#     ]
#     return PaginatedPostsSchema(
#         limit=limit,
#         offset=offset,
#         total=total_posts,
#         posts=paginated_posts
#     )


@posts_router.get('/api/posts/all/', response=list[PostSchema])
def get_all_posts(request):
    return Post.objects.all()


@posts_router.post('/api/posts/', response=PostDetailSchema, auth=JWTAuth())
def create_post(request, data: PostCreateSchema, preview: File[UploadedFile] = None,
                photos: File[list[UploadedFile]] = None):
    category_exists = Category.objects.filter(pk=data.category_id).exists()
    author_exists = User.objects.filter(pk=data.author_id).exists()

    if not category_exists:
        raise ValidationError('Category does not exist')

    if not author_exists:
        raise ValidationError('Author does not exist')

    new_post = Post.objects.create(
        name=data.name,
        short_description=data.short_description,
        full_description=data.full_description,
        category_id=data.category_id,
        author_id=data.author_id,
        preview=preview
    )
    try:
        new_post.likes
    except Exception as e:
        Like.objects.create(post=new_post)

    try:
        new_post.dislikes
    except Exception as e:
        Dislike.objects.create(post=new_post)

    if photos is not None:
        for photo in photos:
            PostPhoto.objects.create(
                post=new_post,
                photo=photo
            )

    return new_post


@posts_router.get('/api/posts/{post_id}/', response=PostDetailSchema)
def get_post(request, post_id: int):
    post = get_object_or_404(Post, pk=post_id)
    return post


@posts_router.patch('/api/posts/{post_id}/update/', response=PostDetailSchema, auth=JWTAuth())
def update_post(request, post_id: int, data: PostUpdateSchema, preview: File[UploadedFile] = None):
    user = request.auth

    post = get_object_or_404(Post, pk=post_id)

    if not user == post.author:
        raise ValidationError('You are not author of this post')

    for key, value in data.model_dump().items():
        if value is None:
            continue

        setattr(post, key, value)

    if preview is not None:
        if post.preview:
            print(f'removing {post.preview.url}')  # /media/posts/previews/file.jpg
            preview_path = os.path.join(settings.BASE_DIR, *post.preview.url.split('/'))
            os.remove(preview_path)

        post.preview = preview

    post.save()
    return post



@posts_router.delete('/api/posts/{post_id}/delete/')
def delete_post(request, post_id: int):
    post = get_object_or_404(Post, pk=post_id)
    post.delete()
    return {"success": True}


@posts_router.post('/api/posts/{post_id}/comments/create/', response=PostCommentSchema)
def create_comment(request, post_id: int, data: PostCommentCreateSchema):
    post = get_object_or_404(Post, pk=post_id)
    author = get_object_or_404(User, pk=data.author_id)

    comment = Comment.objects.create(text=data.text, author=author, post=post)
    return comment


# JWT - json web token
@posts_router.delete('/api/posts/{post_id}/comments/{comment_id}/delete/')
def delete_comment(request, post_id: int, comment_id: int):
    post = get_object_or_404(Post, pk=post_id)
    comment = get_object_or_404(Comment, pk=comment_id)

    comment.delete()
    return {"success": True}