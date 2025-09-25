from django.urls import path
from .views import login_request_code, verify_code, logout_view

app_name = 'accounts'

urlpatterns = [
    path('login/', login_request_code, name='login'),
    path('verify/', verify_code, name='verify'),
    path('logout/', logout_view, name='logout'),
]
