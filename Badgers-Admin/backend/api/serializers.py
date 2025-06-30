# api/serializers.py
from rest_framework import serializers
from .models import Socio, Pago, Producto, Venta, Gasto


class SocioSerializer(serializers.ModelSerializer):
    # --- CAMBIO CLAVE AQUÍ ---
    # 1. Definimos el campo 'fecha_registro' explícitamente.
    # 2. Usamos DateTimeField que es más flexible para manejar el objeto que viene de la base de datos.
    # 3. Con `format="%Y-%m-%d"`, le decimos que lo represente como un string de solo fecha (AAAA-MM-DD).
    # 4. Con `read_only=True`, confirmamos que este campo no se puede escribir a través de la API.
    fecha_registro = serializers.DateField(format="%Y-%m-%d", read_only=True)
    #foto = serializers.SerializerMethodField()

    class Meta:
        model = Socio
        # La forma más sencilla es usar '__all__' para incluir todos los campos.
        fields = '__all__'
        # Opcionalmente, puedes listar todos los campos como lo tenías antes, 
        # solo asegúrate de que 'foto' esté en la lista.
        read_only_fields = ['fecha_registro']
    
    def get_foto(self, obj):
        if obj.foto:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.foto.url)
            return obj.foto.url
        return None

class PagoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pago
        fields = '__all__'

class ProductoSerializer(serializers.ModelSerializer):
    # --- CAMBIO 1: Usamos un SerializerMethodField para un cálculo explícito ---
    ganancia = serializers.ReadOnlyField()

    class Meta:
        model = Producto
        fields = '__all__'
    
    # --- CAMBIO 2: Añadimos la función que calcula el valor para 'ganancia' ---
    def get_ganancia(self, obj):
        # obj es la instancia del producto
        if obj.precio_venta is not None and obj.precio_costo is not None:
            return obj.precio_venta - obj.precio_costo
        return 0
    
   

class VentaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venta
        fields = '__all__'

class GastoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gasto
        fields = '__all__'
        
class Meta:
        model = Producto
        fields = ['id', 'nombre', 'precio_costo', 'precio_venta', 'stock', 'ganancia'] # <-- Añade 'ganancia'        