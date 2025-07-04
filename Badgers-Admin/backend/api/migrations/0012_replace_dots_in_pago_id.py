from django.db import migrations

def replace_dots_and_dashes_in_pago_id(apps, schema_editor):
    Pago = apps.get_model('api', 'Pago')
    for pago in Pago.objects.all():
        nuevo_id = pago.id.replace('.', '_').replace('-', '_')
        if nuevo_id != pago.id:
            # Si ya existe un pago con ese nuevo_id, no lo cambiamos para evitar colisiones
            if not Pago.objects.filter(id=nuevo_id).exists():
                pago.id = nuevo_id
                pago.save()

class Migration(migrations.Migration):
    dependencies = [
        ('api', '0011_fix_en_vacaciones'),
    ]
    operations = [
        migrations.RunPython(replace_dots_and_dashes_in_pago_id),
    ] 