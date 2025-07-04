from django.contrib import admin
from .models import Pago, Socio, Producto, Gasto, Venta

# Registra los modelos para que aparezcan en el panel de admin
admin.site.register(Pago)
admin.site.register(Socio)
admin.site.register(Producto)
admin.site.register(Gasto)
admin.site.register(Venta)