from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import Cliente, Vendedor, Proveedor, Producto, OrdenCompra, OrdenPedido, Inventario

admin.site.register(Cliente)
admin.site.register(Vendedor)
admin.site.register(Proveedor)
admin.site.register(Producto)
admin.site.register(OrdenCompra)
admin.site.register(OrdenPedido)
admin.site.register(Inventario)