from ninja import Router
from django.contrib.auth.models import User
from apps.blog_api.schemas.user import UserSchema, UserProfileSchema, UserRegistrationSchema
from ninja_jwt.authentication import JWTAuth
from ninja.errors import ValidationError

users_router = Router(tags=['Users'])

# TODO: добавить маршрут получающий всех пользователей
# TODO: добавить файл для схем пользователя
# TODO: зарегистрировать роутер для пользователей в апи


@users_router.get('/api/users', response=list[UserSchema])
def get_users(request):
    users = User.objects.all()
    return users


@users_router.get('/api/users/me', auth=JWTAuth(), response=UserProfileSchema)
def get_user_me(request):
    user = request.auth
    return user


@users_router.post('/api/users/', response=UserSchema)
def create_user(request, user_data: UserRegistrationSchema):
    is_username_exists = User.objects.filter(username=user_data.username).exists()

    if is_username_exists:
        raise ValidationError(f'Username with username={user_data.username} already exists')

    is_email_exists = User.objects.filter(email=user_data.email).exists()
    if is_username_exists:
        raise ValidationError(f'Username with email={user_data.email} already exists')

    if user_data.password1 != user_data.password2:
        raise ValidationError(f'Password must match')

    user = User.objects.create_user(
        username=user_data.username,
        email=user_data.email,
        password=user_data.password1,
        first_name=user_data.first_name,
    )
    return user