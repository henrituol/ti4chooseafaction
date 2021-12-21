
from django.urls import path
from . import views


urlpatterns = [
    path('', views.mainform),
    path('<int:numberOfPlayers>-<int:numberOfNegativeWeights>-<int:game_id>/', views.emailform),
    path('<int:numberOfPlayers>-<int:numberOfNegativeWeights>-<int:game_id>/<int:player_id>/choose-your-factions/', views.factionform),
    path('<int:numberOfPlayers>-<int:numberOfNegativeWeights>-<int:game_id>/<int:player_id>/negative-weights/', views.negativeweightsform),
    path('<int:numberOfPlayers>-<int:numberOfNegativeWeights>-<int:game_id>/thank-you-for-using-TI4-tools/', views.thankyoupage)
]
