from django.urls import path
from . import views

urlpatterns = [
    path('', views.show_home_page, name='home'),
    path('categories/<int:category_id>/', views.show_category_articles_page, name='category-articles'),
    path('posts/<int:post_id>/', views.show_post_page, name='post-detail'),
    path('posts/<int:post_id>/update/', views.UpdatePost.as_view(), name='post-update'),
    path('posts/<int:post_id>/delete/', views.DeletePost.as_view(), name='post-delete'),
    path('comments/<int:comment_id>/delete/', views.delete_post_comment, name='delete-comment'),
    path('contacts/', views.show_contacts_page, name='contacts'),
    path('create/', views.show_create_post_page, name='create-post'),
    path('faq/', views.show_faq_page, name='faq'),
    path('login/', views.show_login_page, name='login'),
    path('registration/', views.show_registration_page, name='registration'),
    path('logout/', views.user_logout, name='logout'),
    path('users/<str:username>/profile/', views.show_author_profile_page, name='profile'),
    path('posts/<int:post_id>/<str:action>/', views.add_like_or_dislike, name='add-vote'),
    path('search/', views.search, name='search')
]

# http://127.0.0.1:8000/ - запускается show_home_page
# http://127.0.0.1:8000/contacts
# http://127.0.0.1:8000/about
# http://127.0.0.1:8000/articles