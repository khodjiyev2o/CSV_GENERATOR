
from django.urls import path
from .views import DataSchemaListView, LoginView, DataSchemaCreateView, DataSchemaDetailView,logout_view, generate_csv


urlpatterns = [
    path('', DataSchemaListView.as_view(), name='schemas'),
    path('schema/create', DataSchemaCreateView.as_view(), name='create_schema'),
    path('schema-detail:<int:pk>/', DataSchemaDetailView.as_view(),name='schema-detail'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),

    path('download/csv/', generate_csv, name='generate_csv'),
]
