# Generated by Django 5.0.3 on 2024-05-16 16:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuairo', '0002_alter_cliente_ciudad_alter_cliente_departamento'),
    ]

    operations = [
        migrations.AlterField(
            model_name='factura',
            name='nombre',
            field=models.CharField(default='Orden-#', max_length=60),
        ),
        migrations.AlterField(
            model_name='pedido',
            name='talla',
            field=models.CharField(default='tallas:', max_length=60),
        ),
    ]
