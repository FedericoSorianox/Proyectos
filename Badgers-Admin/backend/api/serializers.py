# api/serializers.py
from rest_framework import serializers
from .models import Socio, Pago, Producto, Venta, Gasto # Asegúrate de que todas tus importaciones estén aquí arriba
from .utils import upload_to_s3 
import os # <-- 1. IMPORTANTE: Añade esta importación al principio del archivo

class SocioSerializer(serializers.ModelSerializer):
    # Campo para RECIBIR el archivo de imagen al subirlo
    foto = serializers.ImageField(write_only=True, required=False, allow_null=True)
    
    # Campo para MOSTRAR la URL guardada en la base de datos
    foto_url = serializers.CharField(source='foto', read_only=True)
    
    fecha_registro = serializers.DateField(format="%Y-%m-%d", read_only=True)

    class Meta:
        model = Socio
        fields = '__all__'
        # Agregamos 'foto_url' para que aparezca en la respuesta de la API
        extra_kwargs = {
            'foto_url': {'source': 'foto'}
        }

    def create(self, validated_data):
        bucket_name = os.environ.get('AWS_STORAGE_BUCKET_NAME')
        region = os.environ.get('AWS_S3_REGION_NAME')
        
        foto_file = validated_data.pop('foto', None)
        foto_url_final = None

        if foto_file:
            if not bucket_name:
                raise serializers.ValidationError("El nombre del bucket de S3 no está configurado.")

            # Cambiamos la ruta para que sea específica de socios
            success, object_name = upload_to_s3(
                foto_file, 
                bucket_name,
                f"media/socios_fotos/{foto_file.name}"
            )

            if not success:
                raise serializers.ValidationError("Error: No se pudo subir la imagen del socio a S3.")
            
            foto_url_final = f"https://{bucket_name}.s3.{region}.amazonaws.com/{object_name}"

        socio = Socio.objects.create(foto=foto_url_final, **validated_data)
        return socio

    def update(self, instance, validated_data):
        bucket_name = os.environ.get('AWS_STORAGE_BUCKET_NAME')
        region = os.environ.get('AWS_S3_REGION_NAME')
        
        foto_file = validated_data.pop('foto', None)
        
        if foto_file:
            if not bucket_name:
                raise serializers.ValidationError("El nombre del bucket de S3 no está configurado.")

            success, object_name = upload_to_s3(
                foto_file, 
                bucket_name, 
                f"media/socios_fotos/{foto_file.name}"
            )

            if not success:
                raise serializers.ValidationError("Error: No se pudo subir la nueva imagen del socio.")

            instance.foto = f"https://{bucket_name}.s3.{region}.amazonaws.com/{object_name}"
        
        return super().update(instance, validated_data)

class PagoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pago
        fields = '__all__'

#class ProductoSerializer(serializers.ModelSerializer):
    # --- CAMBIO 1: Usamos un SerializerMethodField para un cálculo explícito ---
 #  ganancia = serializers.ReadOnlyField()

  #  class Meta:
 #      model = Producto
  #      fields = '__all__'
    
    # --- CAMBIO 2: Añadimos la función que calcula el valor para 'ganancia' ---
#    def get_ganancia(self, obj):
 #       # obj es la instancia del producto
  #      if obj.precio_venta is not None and obj.precio_costo is not None:
 #           return obj.precio_venta - obj.precio_costo
  #      return 0

class ProductoSerializer(serializers.ModelSerializer):
    # 1. Este campo es para RECIBIR el archivo de imagen.
    #    Solo se usa para escribir/subir, no se muestra en la respuesta.
    #    Se llama 'foto' para que coincida con lo que envía el frontend.
    foto = serializers.ImageField(write_only=True, required=False, allow_null=True)
    
    # 2. Este campo es para MOSTRAR la URL guardada en la base de datos.
    #    Es de solo lectura. Le decimos que su valor viene del campo 'foto' del modelo.
    foto_url = serializers.CharField(source='foto', read_only=True)
    
    ganancia = serializers.ReadOnlyField()

    class Meta:
        model = Producto
        # 3. Lista de campos corregida, sin duplicados y con los nombres correctos.
        fields = [
            'id', 
            'nombre', 
            'precio_costo', 
            'precio_venta', 
            'stock', 
            'ganancia', 
            'foto',      # Campo de escritura para la subida
            'foto_url'   # Campo de lectura para mostrar la URL
        ]

    def create(self, validated_data):
        # --- CAMBIO CLAVE AQUÍ ---
        # 2. Leemos el nombre y la región del bucket desde las variables de entorno
        bucket_name = os.environ.get('AWS_STORAGE_BUCKET_NAME')
        region = os.environ.get('AWS_S3_REGION_NAME')
        
        foto_file = validated_data.pop('foto', None)
        foto_url_final = None

        if foto_file:
            if not bucket_name:
                raise serializers.ValidationError("El nombre del bucket de S3 no está configurado.")

            # 3. Pasamos el nombre correcto del bucket a la función de subida
            success, object_name = upload_to_s3(
                foto_file, 
                bucket_name, # Usamos la variable en lugar de un nombre fijo
                f"media/productos_fotos/{foto_file.name}"
            )

            if not success:
                raise serializers.ValidationError("Error: No se pudo subir la imagen a S3.")
            
            # 4. Construimos la URL final usando también las variables
            foto_url_final = f"https://{bucket_name}.s3.{region}.amazonaws.com/{object_name}"

        producto = Producto.objects.create(foto=foto_url_final, **validated_data)
        return producto

    def update(self, instance, validated_data):
        # Repetimos la misma lógica para el método de actualización
        bucket_name = os.environ.get('AWS_STORAGE_BUCKET_NAME')
        region = os.environ.get('AWS_S3_REGION_NAME')
        
        foto_file = validated_data.pop('foto', None)
        
        if foto_file:
            if not bucket_name:
                raise serializers.ValidationError("El nombre del bucket de S3 no está configurado.")

            success, object_name = upload_to_s3(
                foto_file, 
                bucket_name, 
                f"media/productos_fotos/{foto_file.name}"
            )

            if not success:
                raise serializers.ValidationError("Error: No se pudo subir la nueva imagen.")

            # Si la subida es exitosa, actualizamos la URL en el campo 'foto'
            instance.foto = f"https://{bucket_name}.s3.{region}.amazonaws.com/{object_name}"
        
        # Llama al método 'update' del padre para guardar los otros campos
        return super().update(instance, validated_data)    


class VentaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venta
        fields = '__all__'

class GastoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gasto
        fields = '__all__'
        
#class Meta:
 #       model = Producto
  #      fields = ['id', 'nombre', 'precio_costo', 'precio_venta', 'stock', 'ganancia'] # <-- Añade 'ganancia'        