import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_produto_imagem'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pedido',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cliente_nome', models.CharField(max_length=200)),
                ('cliente_email', models.EmailField(max_length=254)),
                ('status', models.CharField(
                    choices=[
                        ('pendente', 'Pendente'),
                        ('confirmado', 'Confirmado'),
                        ('enviado', 'Enviado'),
                        ('entregue', 'Entregue'),
                        ('cancelado', 'Cancelado'),
                    ],
                    default='pendente',
                    max_length=20,
                )),
                ('total', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('criado_em', models.DateTimeField(auto_now_add=True)),
                ('atualizado_em', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Pedido',
                'verbose_name_plural': 'Pedidos',
                'ordering': ['-criado_em'],
            },
        ),
        migrations.CreateModel(
            name='ItemPedido',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantidade', models.PositiveIntegerField(default=1)),
                ('preco_unitario', models.DecimalField(decimal_places=2, max_digits=10)),
                ('pedido', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='itens',
                    to='api.pedido',
                )),
                ('produto', models.ForeignKey(
                    on_delete=django.db.models.deletion.PROTECT,
                    related_name='itens_pedido',
                    to='api.produto',
                )),
            ],
            options={
                'verbose_name': 'Item do Pedido',
                'verbose_name_plural': 'Itens do Pedido',
            },
        ),
    ]
