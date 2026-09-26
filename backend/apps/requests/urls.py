from django.urls import path

from apps.requests.api_views import (
    RequestApproveView,
    RequestDetailView,
    RequestListCreateView,
    RequestRejectView,
    RequestSubmitView,
)

urlpatterns = [
    path('', RequestListCreateView.as_view(), name='request-list-create'),
    path('<int:pk>/', RequestDetailView.as_view(), name='request-detail'),
    path('<int:pk>/submit/', RequestSubmitView.as_view(), name='request-submit'),
    path('<int:pk>/approve/', RequestApproveView.as_view(), name='request-approve'),
    path('<int:pk>/reject/', RequestRejectView.as_view(), name='request-reject'),
]
