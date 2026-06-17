# API de Produtos — AP2: Django REST + AWS RDS + S3

**Disciplina:** Big Data e Cloud Computing — IBMEC 2026.1  
**Aluno:** Guilherme Araujo  

---

## Arquitetura da Solução (AP1 → AP2)

```
AP1                                 AP2
────────────────────────            ────────────────────────────────────
Django REST Framework               Django REST Framework
SQLite (local)              ──▶     AWS RDS MySQL (gerenciado)
Sem armazenamento de mídia  ──▶     AWS S3 (imagens de produtos)
Modelos: Produto, Categoria ──▶     + Pedido, ItemPedido (carrinho)
Deploy: Elastic Beanstalk           Deploy: Elastic Beanstalk (mantido)
```

```
Internet
   │
   ▼
[Elastic Beanstalk]  ←── app.zip (Django + Gunicorn)
   │
   ├──▶ [RDS MySQL]  ←── produtos_db (dados relacionais)
   │
   └──▶ [S3 Bucket]  ←── produtos-imagens-guilherme (imagens)
```

---

## Endpoints da API

| Método | URL | Ação |
|--------|-----|------|
| GET | `/api/health/` | Health check |
| GET/POST | `/api/categorias/` | Categorias |
| GET/POST | `/api/produtos/` | Produtos |
| GET/POST | `/api/pedidos/` | Pedidos |
| GET/POST | `/api/itens-pedido/` | Itens do pedido |

---

## Execução Local

```bash
# 1. Clonar e instalar
git clone https://github.com/GuiAraujo/BDCC-AP1.git
cd BDCC-AP1
python -m venv venv && venv\Scripts\activate  # Windows
pip install -r requirements.txt

# 2. Migrar e rodar
python manage.py migrate
python manage.py runserver
```

API: `http://localhost:8000/api/`  
Admin: `http://localhost:8000/admin/`

---

## Deploy na AWS

1. Criar instância **RDS MySQL** (`produtos_db`) e copiar o endpoint
2. Criar **bucket S3** (`produtos-imagens-guilherme`) com leitura pública
3. Adicionar `AmazonS3FullAccess` ao IAM role `aws-elasticbeanstalk-ec2-role`
4. Gerar o `app.zip` com o `manage.py` na raiz
5. Criar ambiente no **Elastic Beanstalk** (Python 3.11) com as variáveis de ambiente:

| Variável | Valor |
|----------|-------|
| `RDS_HOSTNAME` | endpoint do RDS |
| `RDS_PORT` | `3306` |
| `RDS_DB_NAME` | `produtos_db` |
| `RDS_USERNAME` | `admin` |
| `RDS_PASSWORD` | `****` |
| `AWS_STORAGE_BUCKET_NAME` | `produtos-imagens-guilherme` |
| `AWS_S3_REGION_NAME` | `us-east-1` |
| `DJANGO_DEBUG` | `False` |

---

## Link da API em Produção

http://api-produtos-guilherme-env.eba-fppma8iz.us-east-1.elasticbeanstalk.com/admin/login/?next=/admin/


Login: root

Senha: root1234

---

## Evidências

**RDS** — resposta de `GET /api/produtos/` com dados do banco MySQL:
```json
{
    "id": 1,
    "nome": "Notebook Dell",
    "preco": "3999.90",
    "estoque": 10,
    "categoria_detalhes": { "id": 1, "nome": "Eletrônicos" },
    "criado_em": "2026-06-16T14:06:58.076265-03:00"
}
```

**S3** — URL pública de imagem salva no bucket após POST com `form-data`:
```
https://produtos-imagens-guilherme.s3.amazonaws.com/produtos/Captura_de_tela_2026-01-15_214949.png
```
