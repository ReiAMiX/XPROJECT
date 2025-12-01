from ninja import NinjaAPI
from .routes.v1.categories import categories_router
from .routes.v1.faqs import faqs_router
from .routes.v1.posts import posts_router
from .routes.v1.users import users_router
from ninja_extra import NinjaExtraAPI
from ninja_jwt.controller import NinjaJWTDefaultController

api_app = NinjaExtraAPI()

# регистрируем класс, содержащий маршруты для работы с JWT
api_app.register_controllers(NinjaJWTDefaultController)

api_app.add_router('', categories_router)  # добавляем все ссылки из маршрутизатора для категорий
api_app.add_router('', faqs_router)
api_app.add_router('', posts_router)
api_app.add_router('', users_router)


# TODO: добавить маршруты для удаления и добавления FAQ
