
from django.urls import path
from .import views
from django.contrib.auth.views import LoginView,LogoutView

urlpatterns = [
    path('', views.index, name="home"),
    path("register/",views.register,name="register"),
    path("login/",views.login,name="login"),
    path("logout/",views.signout,name="logout"),
    path("profile/",views.profile,name="userprofile"),
    path("news/",views.news,name="news"),
    path("changepassword/",views.changepassword,name="changepassword"),
    path("addrecipe/",views.addrecipe,name="addrecipe"),
    path("search/",views.search_recipes,name="search"),
    path("myrecipes/",views.myrecipes,name="myrecipes"),
    path('detail/<int:id>',views.detail,name='detail'),
    path('editrecipe/<int:id>',views.editrecipe,name='editrecipe'),
    path('review/<int:id>',views.postreview,name='review'),
    path('recipebycat/<int:id>',views.recipebycat,name='recipebycat'),
    path('delrecipe/<int:id>',views.delrecipe,name='delrecipe'),



]
