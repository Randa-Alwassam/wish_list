from django.urls import path, include

from . import views
urlpatterns = [
    path('', views.index),
    path('main', views.index),
    path('register', views.register),
    path('login', views.login),
    path('dashboard', views.dashboard),
    path('logout', views.logout),
    path('wish_items/create', views.createItem),
    path('delete/<int:item_id>', views.deleteItem),
    path('addList/<int:item_id>', views.addList),
    path('removeList/<int:item_id>', views.removeList),
    path('wish_items/<int:item_id>', views.itemView),
]