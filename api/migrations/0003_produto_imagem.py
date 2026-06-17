from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_categoria_produto_categoria'),
    ]

    operations = [
        migrations.AddField(
            model_name='produto',
            name='imagem',
            field=models.ImageField(blank=True, null=True, upload_to='produtos/'),
        ),
    ]
