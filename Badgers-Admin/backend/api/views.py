# api/views.py
import csv
import io
from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import viewsets, status, filters 
from rest_framework.views import APIView
from .models import Socio, Pago, Producto, Venta, Gasto
from .serializers import SocioSerializer, PagoSerializer, ProductoSerializer, VentaSerializer, GastoSerializer
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.db.models import Q
from datetime import datetime

# Función de ayuda para procesar fechas de forma robusta
def parse_date_from_csv(date_str):
    if not date_str:
        return None
    for fmt in ('%Y-%m-%d', '%d/%m/%Y', '%d-%m-%Y'):
        try:
            return datetime.strptime(date_str.strip(), fmt).date()
        except (ValueError, TypeError):
            continue
    return None


class SocioViewSet(viewsets.ModelViewSet):
    queryset = Socio.objects.all().order_by('nombre')
    serializer_class = SocioSerializer
    pagination_class = None
    lookup_field = 'ci'
    filter_backends = [filters.SearchFilter]
    search_fields = ['nombre', 'ci']
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['post'], parser_classes=[MultiPartParser])
    def import_csv(self, request, *args, **kwargs):
        csv_file = request.FILES.get('file')
        if not csv_file:
            return Response({"error": "No se proporcionó ningún archivo"}, status=status.HTTP_400_BAD_REQUEST)

        decoded_file = csv_file.read().decode('utf-8')
        io_string = io.StringIO(decoded_file)
        reader = csv.DictReader(io_string)

        success_count = 0
        error_count = 0
        errors = []

        for row in reader:
            try:
                Socio.objects.update_or_create(
                    ci=row['ci'],
                    defaults={
                        'nombre': row.get('nombre', ''),
                        'celular': row.get('celular'),
                        'contacto_emergencia': row.get('contacto_emergencia'),
                        'emergencia_movil': row.get('emergencia_movil'),
                        'fecha_nacimiento': parse_date_from_csv(row.get('fecha_nacimiento')),
                        'tipo_cuota': row.get('tipo_cuota'),
                        'enfermedades': row.get('enfermedades'),
                        'comentarios': row.get('comentarios'),
                        # El campo foto no se importa desde CSV
                    }
                )
                success_count += 1
            except Exception as e:
                error_count += 1
                errors.append(f"Fila con CI {row.get('ci', 'N/A')}: {str(e)}")

        return Response({
            "message": f"Importación completada. {success_count} socios importados/actualizados, {error_count} errores.",
            "errors": errors
        }, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        ci_original = kwargs.get('ci')
        ci_nuevo = request.data.get('ci')

        if ci_original != ci_nuevo:
            if Socio.objects.filter(ci=ci_nuevo).exists():
                return Response({'error': 'Ya existe un socio con ese CI.'}, status=status.HTTP_400_BAD_REQUEST)
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_destroy(instance)
            self.perform_create(serializer)
            return Response(serializer.data)
        else:
            return super().update(request, *args, **kwargs)


class PagoViewSet(viewsets.ModelViewSet):
    queryset = Pago.objects.all().order_by('-fecha_pago')
    serializer_class = PagoSerializer
    pagination_class = None  # Desactivamos la paginación
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['post'], parser_classes=[MultiPartParser])
    def import_csv(self, request, *args, **kwargs):
        csv_file = request.FILES.get('file')
        if not csv_file:
            return Response({"error": "No se proporcionó ningún archivo"}, status=status.HTTP_400_BAD_REQUEST)

        decoded_file = csv_file.read().decode('utf-8')
        io_string = io.StringIO(decoded_file)
        reader = csv.DictReader(io_string)
        
        success_count = 0
        error_count = 0
        errors = []

        for row in reader:
            try:
                # El ID se genera a partir de los datos
                pago_id = f"{row['ci']}_{row['mes']}_{row['año']}"
                Pago.objects.update_or_create(
                    id=pago_id,
                    defaults={
                        'socio_id': row['ci'],
                        'mes': int(row['mes']),
                        'año': int(row['año']),
                        'monto': float(row['monto']),
                        'fecha_pago': parse_date_from_csv(row.get('fecha_pago')),
                        'metodo_pago': row.get('metodo_pago'),
                    }
                )
                success_count += 1
            except Exception as e:
                error_count += 1
                pago_id = f"{row.get('ci', 'N/A')}_{row.get('mes', 'N/A')}_{row.get('año', 'N/A')}"
                errors.append(f"Fila con ID {pago_id}: {str(e)}")

        return Response({
            "message": f"Importación completada. {success_count} pagos importados/actualizados, {error_count} errores.",
            "errors": errors
        }, status=status.HTTP_200_OK)


class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all().order_by('nombre')
    serializer_class = ProductoSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None  # Desactivamos la paginación
    
    @action(detail=False, methods=['post'], parser_classes=[MultiPartParser])
    def import_csv(self, request, *args, **kwargs):
        csv_file = request.FILES.get('file')
        if not csv_file:
            return Response({"error": "No se proporcionó ningún archivo"}, status=status.HTTP_400_BAD_REQUEST)

        decoded_file = csv_file.read().decode('utf-8')
        io_string = io.StringIO(decoded_file)
        reader = csv.DictReader(io_string)
        
        success_count = 0
        error_count = 0
        errors = []

        for row in reader:
            try:
                Producto.objects.update_or_create(
                    nombre=row['nombre'],
                    defaults={
                        'precio_venta': float(row.get('precio_venta', 0)),
                        'precio_costo': float(row.get('precio_costo', 0)),
                        'stock': int(row.get('stock', 0)),
                    }
                )
                success_count += 1
            except Exception as e:
                error_count += 1
                errors.append(f"Fila con Producto {row.get('nombre', 'N/A')}: {str(e)}")

        return Response({
            "message": f"Importación completada. {success_count} productos importados/actualizados, {error_count} errores.",
            "errors": errors
        }, status=status.HTTP_200_OK)


class VentaViewSet(viewsets.ModelViewSet):
    queryset = Venta.objects.all().order_by('-fecha_venta')
    serializer_class = VentaSerializer
    pagination_class = None  # Desactivamos la paginación
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        producto_id = data.get('producto')
        cantidad = int(data.get('cantidad', 1))
        try:
            producto = Producto.objects.get(id=producto_id)
        except Producto.DoesNotExist:
            return Response({'error': 'Producto no encontrado.'}, status=status.HTTP_400_BAD_REQUEST)
        if producto.stock < cantidad:
            return Response({'error': 'No hay suficiente stock disponible.'}, status=status.HTTP_400_BAD_REQUEST)
        # Descontar stock
        producto.stock -= cantidad
        producto.save()
        # Crear la venta normalmente
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=False, methods=['post'], parser_classes=[MultiPartParser])
    def import_csv(self, request, *args, **kwargs):
        csv_file = request.FILES.get('file')
        if not csv_file:
            return Response({"error": "No se proporcionó ningún archivo"}, status=status.HTTP_400_BAD_REQUEST)

        decoded_file = csv_file.read().decode('utf-8')
        io_string = io.StringIO(decoded_file)
        reader = csv.DictReader(io_string)
        
        success_count = 0
        error_count = 0
        errors = []

        for row in reader:
            try:
                # Buscar el producto por nombre
                producto_nombre = row.get('producto_nombre', '').strip()
                if not producto_nombre:
                    raise ValueError("El nombre del producto es requerido")
                
                try:
                    producto = Producto.objects.get(nombre=producto_nombre)
                except Producto.DoesNotExist:
                    raise ValueError(f"Producto '{producto_nombre}' no encontrado")
                
                cantidad = int(row.get('cantidad', 1))
                if cantidad <= 0:
                    raise ValueError("La cantidad debe ser mayor a 0")
                
                # Verificar stock disponible
                if producto.stock < cantidad:
                    raise ValueError(f"Stock insuficiente para '{producto_nombre}'. Disponible: {producto.stock}, Solicitado: {cantidad}")
                
                # Calcular total de venta
                total_venta = producto.precio_venta * cantidad
                
                # Crear la venta
                venta = Venta.objects.create(
                    producto=producto,
                    cantidad=cantidad,
                    total_venta=total_venta,
                    fecha_venta=parse_date_from_csv(row.get('fecha_venta')) or datetime.now()
                )
                
                # Actualizar stock del producto
                producto.stock -= cantidad
                producto.save()
                
                success_count += 1
            except Exception as e:
                error_count += 1
                errors.append(f"Fila con Producto {row.get('producto_nombre', 'N/A')}: {str(e)}")

        return Response({
            "message": f"Importación completada. {success_count} ventas importadas, {error_count} errores.",
            "errors": errors
        }, status=status.HTTP_200_OK)


class GastoViewSet(viewsets.ModelViewSet):
    queryset = Gasto.objects.all().order_by('-fecha')
    serializer_class = GastoSerializer
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['post'], parser_classes=[MultiPartParser])
    def import_csv(self, request, *args, **kwargs):
        csv_file = request.FILES.get('file')
        if not csv_file:
            return Response({"error": "No se proporcionó ningún archivo"}, status=status.HTTP_400_BAD_REQUEST)

        decoded_file = csv_file.read().decode('utf-8')
        io_string = io.StringIO(decoded_file)
        reader = csv.DictReader(io_string)
        
        success_count = 0
        error_count = 0
        errors = []

        for row in reader:
            try:
                concepto = row.get('concepto', '').strip()
                if not concepto:
                    raise ValueError("El concepto es requerido")
                
                monto = float(row.get('monto', 0))
                if monto <= 0:
                    raise ValueError("El monto debe ser mayor a 0")
                
                fecha = parse_date_from_csv(row.get('fecha'))
                if not fecha:
                    raise ValueError("La fecha es requerida y debe tener formato válido (YYYY-MM-DD, DD/MM/YYYY, o DD-MM-YYYY)")
                
                Gasto.objects.create(
                    concepto=concepto,
                    monto=monto,
                    fecha=fecha,
                    categoria=row.get('categoria', '').strip() or None,
                    descripcion=row.get('descripcion', '').strip() or None
                )
                
                success_count += 1
            except Exception as e:
                error_count += 1
                errors.append(f"Fila con Concepto {row.get('concepto', 'N/A')}: {str(e)}")

        return Response({
            "message": f"Importación completada. {success_count} gastos importados, {error_count} errores.",
            "errors": errors
        }, status=status.HTTP_200_OK)

class DashboardStatsView(APIView):
    def get(self, request, *args, **kwargs):
        active_socios_count = Socio.objects.filter(activo=True).count()
        products_in_inventory = Producto.objects.filter(stock__gt=0)
        products_in_inventory_count = products_in_inventory.count()

        stats = {
            'socios_activos': active_socios_count,
            'productos_en_inventario': products_in_inventory_count,
            'productos': ProductoSerializer(products_in_inventory, many=True, context={'request': request}).data
        }
        return Response(stats)

@api_view(['DELETE'])
def eliminar_socios_sin_ci(request):
    count, _ = Socio.objects.filter(ci__isnull=True).delete()
    count2, _ = Socio.objects.filter(ci='').delete()
    return Response({'message': f'Se eliminaron {count + count2} socios sin CI.'}, status=status.HTTP_200_OK)    