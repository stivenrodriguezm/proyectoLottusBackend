# main/views.py
from rest_framework import viewsets
from .models import Cliente, Vendedor, Proveedor, Categoria, Producto, OrdenCompra, OrdenPedido, Inventario, FacturaProveedor, Remision
from .serializers import ClienteSerializer, VendedorSerializer, ProveedorSerializer, CategoriaSerializer, ProductoSerializer, OrdenCompraSerializer, OrdenPedidoSerializer, InventarioSerializer, FacturaProveedorSerializer, RemisionSerializer
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status

class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def search(self, request):
        cedula = request.query_params.get('cedula', None)
        if cedula is not None:
            cliente = Cliente.objects.filter(cedula=cedula).first()
            if cliente:
                serializer = self.get_serializer(cliente)
                return Response(serializer.data)
            else:
                return Response({'detail': 'Cliente no encontrado'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'detail': 'Cédula no proporcionada'}, status=status.HTTP_400_BAD_REQUEST)

class VendedorViewSet(viewsets.ModelViewSet):
    queryset = Vendedor.objects.all()
    serializer_class = VendedorSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        estado = self.request.query_params.get('estado')
        if estado:
            queryset = queryset.filter(estado=estado)
        return queryset

class ProveedorViewSet(viewsets.ModelViewSet):
    queryset = Proveedor.objects.all()
    serializer_class = ProveedorSerializer
    permission_classes = [IsAuthenticated]

class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    permission_classes = [IsAuthenticated]

class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def filtrar(self, request):
        proveedor_id = request.query_params.get('proveedor')
        categoria_id = request.query_params.get('categoria')
        productos = self.queryset
        if proveedor_id:
            productos = productos.filter(proveedor_id=proveedor_id)
        if categoria_id:
            productos = productos.filter(categoria_id=categoria_id)
        serializer = self.get_serializer(productos, many=True)
        return Response(serializer.data)

class OrdenCompraViewSet(viewsets.ModelViewSet):
    queryset = OrdenCompra.objects.all()
    serializer_class = OrdenCompraSerializer
    permission_classes = [IsAuthenticated]

class OrdenPedidoViewSet(viewsets.ModelViewSet):
    queryset = OrdenPedido.objects.all()
    serializer_class = OrdenPedidoSerializer

    def create(self, request, *args, **kwargs):
        print("Request data:", request.data)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save()

    @action(detail=False, methods=['get'])
    def pendientes(self, request):
        queryset = OrdenCompra.objects.filter(estado='pendiente')
        serializer = OrdenCompraSerializer(queryset, many=True)
        return Response(serializer.data)

class InventarioViewSet(viewsets.ModelViewSet):
    queryset = Inventario.objects.all()
    serializer_class = InventarioSerializer
    permission_classes = [IsAuthenticated]

class FacturaProveedorViewSet(viewsets.ModelViewSet):
    queryset = FacturaProveedor.objects.all()
    serializer_class = FacturaProveedorSerializer

class RemisionViewSet(viewsets.ModelViewSet):
    queryset = Remision.objects.all()
    serializer_class = RemisionSerializer