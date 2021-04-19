from django.db import models

class SqlServerConn(models.Model):
    base_de_datos = models.CharField(max_length=200)
    nombre_corporacion = models.CharField(max_length=200)
    id_cliente_proveedor = models.IntegerField()
    razon_social = models.CharField(max_length=200)
    rfc = models.CharField(max_length=100)
    fecha_alta = models.CharField(max_length=100)
    estatus = models.CharField(max_length=100)
    id_agente_venta = models.IntegerField()
    