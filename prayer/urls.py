from django.urls import path
from prayer import views

urlpatterns = [
    path('react/<str:pr_id>/<str:emoji>', views.prayer_request_react, name='prayer-request-react'),
    path('edit/', views.submit_prayer_form, name='edit-prayer-request'),
    path('edit/<str:pr_id>', views.submit_prayer_form, name='edit-prayer-request'),
    path('delete/<str:id>', views.delete_prayer_request, name='delete-prayer-request'),
]
