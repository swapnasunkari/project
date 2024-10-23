# urls.py

from django.contrib import admin  # Import the admin module
from django.urls import path
from .views import home_view, create_rule_view, evaluate_rule_view, rule_engine_view  # Import your views

urlpatterns = [
    path('admin/', admin.site.urls),  # Admin panel URL
    path('', home_view, name='home'),  # Home view
    path('api/create_rule/', create_rule_view, name='create_rule'),  # Create rule API
    path('api/evaluate_rule/', evaluate_rule_view, name='evaluate_rule'),  # Evaluate rule API
    path('rule_engine/', rule_engine_view, name='rule_engine'),  # Rule engine view
]
