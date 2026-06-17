#!/bin/bash
# Ativa o ambiente virtual do Elastic Beanstalk
source /var/app/venv/*/bin/activate

echo "=== Coletando arquivos estáticos ==="
python manage.py collectstatic --noinput

echo "=== Aplicando migrações do banco ==="
if python manage.py migrate --noinput; then
    echo "=== Migrações aplicadas com sucesso ==="
else
    echo "=== AVISO: migrate falhou — verifique o Security Group do RDS e as variáveis de ambiente ==="
    echo "=== O app será iniciado mesmo assim; corrija o banco e faça redeploy ==="
fi

echo "=== Criando superusuário admin (se não existir) ==="
python manage.py shell << 'PYEOF'
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='root').exists():
    User.objects.create_superuser('root', 'root@admin.com', 'root1234')
    print("Superusuário 'root' criado com sucesso!")
else:
    print("Superusuário 'root' já existe.")
PYEOF
