
from django.urls import path
from .views import DataSchemaListView, DataSchemaCreateView, DataSchemaDetailView,SchemaUpdateView,SchemaDeleteView, generate_csv


urlpatterns = [
    path('', DataSchemaListView.as_view(), name='schemas'),
    path('schema/create', DataSchemaCreateView.as_view(), name='create_schema'),
    path('schemas/<int:pk>/', DataSchemaDetailView.as_view(),name='schema_detail'),
    path("schema/update/<int:pk>/", SchemaUpdateView.as_view(), name="schema_update"),
    path("schema/delete/<int:pk>/", SchemaDeleteView.as_view(), name="schema_delete"),
    path('generate_data/<int:pk>/', DataSchemaDetailView.as_view(), name='generate_data'),
    path('download/csv/', generate_csv, name='generate_csv'),
]
