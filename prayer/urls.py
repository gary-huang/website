from django.urls import path
from prayer import views

urlpatterns = [
    path('react/<str:pr_id>/<str:emoji>', views.prayer_request_react, name='prayer-request-react'),
    path('create', views.submit_prayer_form, name='create-prayer-request'),
    path('delete/<str:id>', views.delete_prayer_request, name='delete-prayer-request'),
]
