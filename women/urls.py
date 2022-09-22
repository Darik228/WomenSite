from django.urls import path
from .views import *
from django.views.decorators.cache import cache_page


urlpatterns = [
    path('', WomenHome.as_view(), name='home'),
    path('about/', about, name='about'),
    path('add_page/', AddPage.as_view(), name='add_page'),
    path('contact/', ContactFormView.as_view(), name='contact'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('register', RegisterUser.as_view(), name='register'),
    path('post/<slug:post_slug>/', ShowPost.as_view(), name='post'),
    path('category/<slug:cat_slug>/', cache_page(60)(WomenCategory.as_view()), name='category'),
    path('delete/<slug:post_slug>/', DeletePost.as_view(), name='delete'),
    path('update/<slug:post_slug>/', WomenUpdate.as_view(), name='update')

    #  path('categories/<int:cat_id>/', categories),
]