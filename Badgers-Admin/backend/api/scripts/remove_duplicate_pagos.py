import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'badgers_project.settings_local')
django.setup()

from api.models import Pago
from collections import defaultdict

# Agrupar pagos por (id normalizado: puntos y guiones a guiones bajos, mes, año)
pagos_map = defaultdict(list)
for pago in Pago.objects.all():
    id_normalizado = pago.id.replace('.', '_').replace('-', '_')
    # Extraer partes del id normalizado para agrupar correctamente
    partes = id_normalizado.split('_')
    if len(partes) >= 3:
        key = ('_'.join(partes[:-2]), partes[-2], partes[-1])
    else:
        key = (id_normalizado, '', '')
    pagos_map[key].append((pago, id_normalizado))

duplicados = 0
for key, pagos in pagos_map.items():
    if len(pagos) > 1:
        # Ordenar por fecha_pago descendente y conservar el más reciente
        pagos.sort(key=lambda x: x[0].fecha_pago, reverse=True)
        pagos_a_borrar = pagos[1:]
        print(f'Duplicados para {key}:')
        for p, _ in pagos_a_borrar:
            print(f'  Eliminando id={p.id}, socio={p.socio.ci}, monto={p.monto}, fecha={p.fecha_pago}')
            p.delete()
            duplicados += 1

# Renombrar todos los ids para que no quede ningún guion medio ni punto
total_renombrados = 0
for key, pagos in pagos_map.items():
    for p, id_normalizado in pagos:
        if p.id != id_normalizado:
            print(f'Renombrando {p.id} -> {id_normalizado}')
            p.id = id_normalizado
            p.save()
            total_renombrados += 1

print(f'Eliminados {duplicados} pagos duplicados.')
print(f'Renombrados {total_renombrados} pagos.') 