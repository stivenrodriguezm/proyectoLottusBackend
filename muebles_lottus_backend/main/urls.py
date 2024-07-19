# main/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ClienteViewSet, VendedorViewSet, ProveedorViewSet, CategoriaViewSet, ProductoViewSet, OrdenCompraViewSet, OrdenPedidoViewSet, InventarioViewSet, FacturaProveedorViewSet, RemisionViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register(r'clientes', ClienteViewSet)
router.register(r'vendedores', VendedorViewSet)
router.register(r'proveedores', ProveedorViewSet)
router.register(r'categorias', CategoriaViewSet)
router.register(r'productos', ProductoViewSet)
router.register(r'ordenes-compra', OrdenCompraViewSet)
router.register(r'ordenes-pedido', OrdenPedidoViewSet)
router.register(r'inventarios', InventarioViewSet)
router.register(r'facturas-proveedor', FacturaProveedorViewSet)
router.register(r'remisiones', RemisionViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('clientes/search/', ClienteViewSet.as_view({'get': 'search'}), name='cliente-search'),
]
