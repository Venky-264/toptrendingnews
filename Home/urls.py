from django.urls import path
from . import views

urlpatterns =[
    path('',views.Homepage),
    path('login/',views.Login),
    path('register/',views.register),
    path('register/verification/',views.verification),
    path('register/verification/validate/',views.validate),
    path('news/<str:interest>',views.News,name='news'),
    path('search',views.interests),
    path('yourinterest',views.yourinterests),
    path('login/validateuser/',views.validateuser),
]