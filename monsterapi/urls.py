from django.urls import path
from .views import ListMonstersView, SingleMonstersView

urlpatterns = [
    path('monsters/all/', ListMonstersView.as_view(), name="monsters-all"),
    path('monsters/<str:picture_id>/', SingleMonstersView.as_view(), name="single-monster"),
]
