from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'produtos', views.ProdutoViewSet, basename='produto')
router.register(r'categorias', views.CategoriaViewSet, basename='categoria')
router.register(r'pedidos', views.PedidoViewSet, basename='pedido')
router.register(r'itens-pedido', views.ItemPedidoViewSet, basename='item-pedido')

urlpatterns = [
    path('health/', views.health_check, name='health-check'),
    path('', include(router.urls)),
]
