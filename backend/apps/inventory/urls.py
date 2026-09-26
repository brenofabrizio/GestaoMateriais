from django.urls import path

from apps.inventory.api_views import (
    IssueStockView,
    ReceiveStockView,
    ReleaseStockView,
    ReserveStockView,
    TransferStockView,
)

urlpatterns = [
    path('receive/', ReceiveStockView.as_view(), name='inventory-receive'),
    path('issue/', IssueStockView.as_view(), name='inventory-issue'),
    path('reserve/', ReserveStockView.as_view(), name='inventory-reserve'),
    path('release/', ReleaseStockView.as_view(), name='inventory-release'),
    path('transfer/', TransferStockView.as_view(), name='inventory-transfer'),
]
