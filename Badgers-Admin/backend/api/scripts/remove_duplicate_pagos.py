import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'badgers_project.settings_local')
django.setup()

from api.models import Pago
from collections import defaultdict

# Agrupar pagos por (ci_normalizado, mes, año)
pagos_map = defaultdict(list)
for pago in Pago.objects.all():
    ci_normalizado = pago.socio.ci.replace('.', '_').replace('-', '_')
    key = (ci_normalizado, pago.mes, pago.año)
    pagos_map[key].append(pago)

duplicados = 0
for key, pagos in pagos_map.items():
    if len(pagos) > 1:
        # Ordenar por fecha_pago descendente y conservar el más reciente
        pagos.sort(key=lambda p: p.fecha_pago, reverse=True)
        pagos_a_borrar = pagos[1:]
        print(f'Duplicados para {key}:')
        for p in pagos_a_borrar:
            print(f'  Eliminando id={p.id}, socio={p.socio.ci}, monto={p.monto}, fecha={p.fecha_pago}')
            p.delete()
            duplicados += 1

print(f'Eliminados {duplicados} pagos duplicados.') 