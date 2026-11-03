from django.urls import path
from .views import PredictPriorityView

urlpatterns = [
    path("predict/priority/", PredictPriorityView.as_view(), name="predict-priority"),
]