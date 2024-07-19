# main/serializers.py

from rest_framework import serializers
from .models import Cliente, Categoria, Inventario, OrdenCompra, OrdenPedido, Producto, Proveedor, Vendedor, ProductoOrdenPedido, FacturaProveedor, Remision

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__'

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'

class InventarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventario
        fields = '__all__'

class OrdenCompraSerializer(serializers.ModelSerializer):
    cliente = serializers.PrimaryKeyRelatedField(queryset=Cliente.objects.all())
    vendedor = serializers.PrimaryKeyRelatedField(queryset=Vendedor.objects.all())

    class Meta:
        model = OrdenCompra
        fields = '__all__'

    def create(self, validated_data):
        cliente = validated_data.pop('cliente')
        vendedor = validated_data.pop('vendedor')
        orden_compra = OrdenCompra.objects.create(cliente=cliente, vendedor=vendedor, **validated_data)
        return orden_compra

class ProductoOrdenPedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductoOrdenPedido
        fields = ['producto', 'cantidad', 'descripcion']

class OrdenPedidoSerializer(serializers.ModelSerializer):
    productos = ProductoOrdenPedidoSerializer(many=True)

    class Meta:
        model = OrdenPedido
        fields = ['id', 'orden_compra', 'proveedor', 'fecha_generacion', 'fecha_despacho', 'estado', 'productos']

    def create(self, validated_data):
        productos_data = validated_data.pop('productos')
        orden_pedido = OrdenPedido.objects.create(**validated_data)
        for producto_data in productos_data:
            ProductoOrdenPedido.objects.create(orden_pedido=orden_pedido, **producto_data)
        return orden_pedido

    def update(self, instance, validated_data):
        productos_data = validated_data.pop('productos')
        instance = super().update(instance, validated_data)

        keep_productos = []
        for producto_data in productos_data:
            if 'id' in producto_data.keys():
                if ProductoOrdenPedido.objects.filter(id=producto_data['id']).exists():
                    p = ProductoOrdenPedido.objects.get(id=producto_data['id'])
                    p.orden_pedido = instance
                    p.producto = producto_data.get('producto', p.producto)
                    p.cantidad = producto_data.get('cantidad', p.cantidad)
                    p.descripcion = producto_data.get('descripcion', p.descripcion)
                    p.save()
                    keep_productos.append(p.id)
                else:
                    continue
            else:
                p = ProductoOrdenPedido.objects.create(orden_pedido=instance, **producto_data)
                keep_productos.append(p.id)

        for producto in instance.productos.all():
            if producto.id not in keep_productos:
                producto.delete()

        return instance

class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = '__all__'

class ProveedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proveedor
        fields = '__all__'

class VendedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendedor
        fields = ['id', 'nombre', 'correo', 'esJefe', 'nombreContactoEmergencia', 'numeroContactoEmergencia', 'estado']
        extra_kwargs = {
            'correo': {'validators': []},  # Asegurarse de que no haya validadores adicionales que puedan estar causando el problema
        }

class FacturaProveedorSerializer(serializers.ModelSerializer):
    productos = InventarioSerializer(many=True)

    class Meta:
        model = FacturaProveedor
        fields = '__all__'

    def create(self, validated_data):
        productos_data = validated_data.pop('productos')
        factura = FacturaProveedor.objects.create(**validated_data)
        for producto_data in productos_data:
            Inventario.objects.create(factura=factura, **producto_data)
        return factura
    
class RemisionSerializer(serializers.ModelSerializer):
    productos = InventarioSerializer(many=True)

    class Meta:
        model = Remision
        fields = '__all__'

    def create(self, validated_data):
        productos_data = validated_data.pop('productos')
        remision = Remision.objects.create(**validated_data)
        for producto_data in productos_data:
            Inventario.objects.create(remision=remision, **producto_data)
        return remision