from django.conf.urls import url


from django.urls import path
from django.contrib import admin
from myapp.views import *
from .views.customer import *
from .views import *


app_name="myapp"



urlpatterns = [
    # path('', admin.site.urls),
    path('admin/', admin.site.urls),
    path('cards/<int:name_on_card_id>/',CustomerListView.as_view(),name='cards'),
    path('login/',LoginView.as_view(),name='login'),
    path('',LoginView.as_view(),name='login'),
    path('cards/<int:name_on_card_id>/add',CreateCardView.as_view(),name='add_card'),
    path('cards/<int:name_on_card_id>/<int:pk>/edit',UpdateCardView.as_view(),name='edit_card'),
    path('cards/<int:name_on_card_id>/<int:pk>/delete',DeleteCardView.as_view(),name='edit_card'),
    path('logout/',logout_user,name='logout')
]