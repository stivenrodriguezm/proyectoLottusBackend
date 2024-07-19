from django.db import models

class Cliente(models.Model):
    cedula = models.CharField(max_length=100, unique=True)
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=255)
    ciudad = models.CharField(max_length=100)
    email = models.EmailField()
    telefono1 = models.CharField(max_length=20)
    telefono2 = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.nombre

class Vendedor(models.Model):
    nombre = models.CharField(max_length=100)
    correo = models.EmailField(max_length=100)
    esJefe = models.BooleanField(default=False)
    nombreContactoEmergencia = models.CharField(max_length=100)
    numeroContactoEmergencia = models.CharField(max_length=20)
    estado = models.CharField(max_length=50, choices=[('activo', 'Activo'), ('inactivo', 'Inactivo')], default='activo')

    def __str__(self):
        return self.nombre

class Proveedor(models.Model):
    nombreEmpresa = models.CharField(max_length=100)
    nombreEncargado = models.CharField(max_length=100)
    nit = models.CharField(max_length=20)
    correo = models.EmailField(max_length=100)
    direccion = models.CharField(max_length=100)
    nombreContacto1 = models.CharField(max_length=100)
    numeroContacto1 = models.CharField(max_length=20)
    nombreContacto2 = models.CharField(max_length=100, null=True, blank=True)
    numeroContacto2 = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return self.nombreEmpresa

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    proveedor = models.ForeignKey('Proveedor', on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre

class OrdenCompra(models.Model):
    cliente = models.ForeignKey('Cliente', on_delete=models.CASCADE)
    vendedor = models.ForeignKey('Vendedor', on_delete=models.CASCADE)
    fecha = models.DateField()
    total = models.DecimalField(max_digits=20, decimal_places=2)
    estado = models.CharField(max_length=50, choices=[('pendiente', 'Pendiente'), ('completa', 'Completa')])
    numero_orden = models.CharField(max_length=20, unique=True)
    fecha_entrega = models.DateField()

    def __str__(self):
        return f"Orden {self.numero_orden} - {self.cliente.nombre}"

class OrdenPedido(models.Model):
    orden_compra = models.ForeignKey('OrdenCompra', on_delete=models.CASCADE)
    proveedor = models.ForeignKey('Proveedor', on_delete=models.CASCADE)
    fecha_generacion = models.DateField(auto_now_add=True)
    fecha_despacho = models.DateField()
    estado = models.CharField(max_length=50, choices=[('pendiente', 'Pendiente'), ('aprobado', 'Aprobado'), ('enviado', 'Enviado')], default='pendiente')

    def __str__(self):
        return f"Pedido {self.id} - {self.proveedor.nombreEmpresa}"

class ProductoOrdenPedido(models.Model):
    orden_pedido = models.ForeignKey(OrdenPedido, related_name='productos', on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    descripcion = models.TextField()

class Inventario(models.Model):
    nombre = models.CharField(max_length=100, null=True)
    categoria = models.ForeignKey('Categoria', on_delete=models.CASCADE, null=True)
    descripcion = models.TextField(null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    proveedor = models.ForeignKey('Proveedor', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.nombre
    
class FacturaProveedor(models.Model):
    numero_factura = models.CharField(max_length=100, unique=True)
    proveedor = models.ForeignKey('Proveedor', on_delete=models.CASCADE, null=True)
    fecha_recibido = models.DateField(null=True)
    fecha_pago = models.DateField(null=True)
    pagado = models.BooleanField(default=False, null=True)
    valor = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    nota = models.TextField(blank=True, null=True)
    productos = models.ManyToManyField(Inventario, related_name='facturas', null=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        for producto in self.productos.all():
            inventario_item, created = Inventario.objects.get_or_create(
                nombre=producto.nombre,
                categoria=producto.categoria,
                descripcion=producto.descripcion,
                precio=producto.precio,
                proveedor=producto.proveedor
            )
            if not created:
                inventario_item.cantidad += producto.cantidad
                inventario_item.save()

    def __str__(self):
        return self.numero_factura
    
# models.py

class Remision(models.Model):
    orden_compra = models.ForeignKey('OrdenCompra', on_delete=models.CASCADE, null=True)
    cliente = models.ForeignKey('Cliente', on_delete=models.CASCADE, null=True)
    fecha_entrega = models.DateField(null=True)
    nota = models.TextField(blank=True, null=True)
    productos = models.ManyToManyField(Inventario, related_name='remisiones',null=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        for producto in self.productos.all():
            inventario_item = Inventario.objects.get(id=producto.id)
            inventario_item.cantidad -= producto.cantidad
            inventario_item.save()

    def __str__(self):
        return f"Remisión {self.id}"


class ProductoFactura(models.Model):
    factura = models.ForeignKey(FacturaProveedor, on_delete=models.CASCADE, related_name='factura_productos')
    inventario = models.ForeignKey(Inventario, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    descripcion = models.TextField()