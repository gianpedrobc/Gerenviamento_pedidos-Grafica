# grafica/urls.py

from django.urls import path, include
from .views import (
    PedidoListView,
    PedidoDetailView,
    PedidoCreateView,
    PedidoUpdateView,
    PedidoDeleteView,
    HomePageView,
    upload_attachment_view,
    ManagerDashboardView,
    InventoryListView,
    ManagerCreateView,
    update_order_status_view,
    UserProfileView,
    ProdutoInternoCreateView,
    EntradaEstoqueCreateView
)
from grafica.views import HomePageView, SignUpView
urlpatterns = [
    path('', HomePageView.as_view(), name='home'),  
    path('pedidos/', PedidoListView.as_view(), name='pedido_list'),
    path('pedido/<int:pk>/', PedidoDetailView.as_view(), name='pedido_detail'),
    path('pedido/novo/', PedidoCreateView.as_view(), name='pedido_create'),
    path('pedido/<int:pk>/editar/', PedidoUpdateView.as_view(), name='pedido_update'),
    path('pedido/<int:pk>/deletar/', PedidoDeleteView.as_view(), name='pedido_delete'),
    path('contas/signup/', SignUpView.as_view(), name='signup'),
    path('contas/', include('django.contrib.auth.urls')),
    path('pedido/<int:order_id>/upload/', upload_attachment_view, name='upload_attachment'),
    path('gerente/dashboard/', ManagerDashboardView.as_view(), name='manager_dashboard'),
    path('gerente/estoque/', InventoryListView.as_view(), name='inventory_list'),
    path('gerente/novo/', ManagerCreateView.as_view(), name='create_manager'),
    path('pedido/<int:order_id>/update_status/', update_order_status_view, name='update_order_status'),
    path('contas/perfil/', UserProfileView.as_view(), name='profile'),
    path('gerente/estoque/novo/', ProdutoInternoCreateView.as_view(), name='produto_interno_create'),
    path('gerente/estoque/registrar_entrada/', EntradaEstoqueCreateView.as_view(), name='entrada_estoque_create'),
]