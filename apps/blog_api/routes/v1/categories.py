# DRF
# django-ninja
from ninja import Router
from ninja.errors import ValidationError
from apps.main.models import Category
from apps.blog_api.schemas.category import CategorySchema, CategoryCreateSchema, CategoryUpdateSchema
from django.shortcuts import get_object_or_404
from ninja_jwt.authentication import JWTAuth


categories_router = Router(tags=['Categories'])


# GET, POST, PUT, PATCH, DELETE
# http://127.0.0.1:8000/api/categories/

@categories_router.get('/api/categories/', response=list[CategorySchema])  # обрабатывает GET запрос
def get_categories(request):
    categories = Category.objects.all()
    return categories


@categories_router.get('/api/categories/{category_id}/', response=CategorySchema)
def get_category(request, category_id: int):
    category = get_object_or_404(Category, id=category_id)  # Category
    return category


@categories_router.post('/api/categories/', response=CategorySchema, auth=JWTAuth())
def create_category(request, category_data: CategoryCreateSchema):
    user = request.auth
    if not user.is_superuser:
        raise ValidationError('no permissions')

    is_category_exists = Category.objects.filter(name=category_data.name).exists()
    if is_category_exists:
        raise ValidationError(f'Category with name {category_data.name} already exists')

    new_category = Category.objects.create(name=category_data.name)
    return new_category


@categories_router.put('/api/categories/{category_id}/update/', response=CategorySchema, auth=JWTAuth())
def update_category(request, category_id: int, data: CategoryUpdateSchema):
    user = request.auth
    if not user.is_superuser:
        raise ValidationError('no permissions')
    category = get_object_or_404(Category, id=category_id)
    category.name = data.name
    category.save()
    return category


@categories_router.delete('/api/categories/{category_id}/delete/', auth=JWTAuth())
def delete_category(request, category_id: int):
    user = request.auth
    if not user.is_superuser:
        raise ValidationError('no permissions')
    category = get_object_or_404(Category, id=category_id)
    category.delete()
    return {"success": True}
