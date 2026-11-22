from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import TicketViewSet,CategoryList,StatsView
router=DefaultRouter()
router.register("tickets",TicketViewSet,basename="tickets")
urlpatterns=[path("categories/",CategoryList.as_view()),path("stats/",StatsView.as_view()),path("",include(router.urls))]
