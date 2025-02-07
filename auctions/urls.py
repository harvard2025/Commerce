from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('create', views.creatListing, name='create'),
    path('desplayCat', views.desplayCat , name='desplayCat'),
    path('listing/<int:id>', views.listing, name='listing'),
    path('RemoveWatchList/<int:id>', views.RemoveWatchList, name='RemoveWatchList'),
    path('AddWatchList/<int:id>', views.AddWatchList, name='AddWatchList'),
    path('WatchList', views.desplayWatchList, name='WatchList'),
    path('addComment/<int:id>', views.addComment, name='addComment'),
    path('addBid/<int:id>', views.addBid, name='addBid'),
    path('closeAuction/<int:id>', views.closeAuction, name='closeAution'),

]
