# Documentação da AP2

**Disciplina:** Big Data e Cloud Computing — IBMEC 2026.1  
**Aluno:** Guilherme Araujo  
**Link da aplicação:** http://api-produtos-guilherme-env.eba-fppma8iz.us-east-1.elasticbeanstalk.com/admin/login/?next=/admin/

---

## Etapas Realizadas

### 1. Ponto de partida — AP1
O projeto da AP1 já possuía uma API Django REST com os modelos `Produto` e `Categoria`, deployada no Elastic Beanstalk com SQLite local.

### 2. Migração para RDS MySQL
Criei uma instância MySQL no AWS RDS (`db-produtos2`) e ajustamos o `settings.py` para ler as credenciais via variáveis de ambiente. As migrações foram executadas automaticamente no primeiro deploy via script de predeploy.

### 3. Integração com S3
Criei o bucket `produtos-imagens-guilherme` com leitura pública e integrei o Django ao S3 usando `django-storages` e `boto3`. O campo `ImageField` do modelo `Produto` passou a salvar automaticamente as imagens no bucket.

### 4. Evolução do modelo de dados
Adicionei os modelos `Pedido` e `ItemPedido` para implementar o carrinho de compras, relacionando-os com o modelo `Produto` já existente.

### 5. Django Admin
Registrei todos os modelos no Django Admin e criei o superusuário `root` automaticamente via script de deploy.

### 6. Deploy final
Realizei múltiplos deploys incrementais no Elastic Beanstalk (v1 a v11), cada um adicionando ou corrigindo uma funcionalidade, até atingir o estado final com todos os requisitos funcionando.

---

## Principais Decisões Técnicas

**PyMySQL como driver MySQL**  
Optei pelo `PyMySQL` (driver puro Python) em vez do `mysqlclient` (que exige compilação de binários nativos) pois o ambiente do Elastic Beanstalk não possui as dependências de sistema necessárias para compilar o mysqlclient. Foi necessário adicionar um patch de versão no `__init__.py` para satisfazer a verificação de versão mínima do Django.

**django-storages + boto3 para o S3**  
Usei a biblioteca `django-storages` que se integra nativamente ao `ImageField` do Django — ao salvar um produto com imagem, o upload para o S3 acontece de forma transparente, sem necessidade de código adicional nas views.

**AWS_QUERYSTRING_AUTH = False**  
Configurei essa opção para gerar URLs públicas permanentes das imagens, sem parâmetros de autenticação temporária (`AWSAccessKeyId`, `Signature`, `Expires`). Isso é possível porque o bucket tem política de leitura pública configurada.

**Script de predeploy automatizado**  
Utilizei o hook `.platform/hooks/predeploy/01_django_setup.sh` para executar automaticamente `collectstatic`, `migrate` e criação do superusuário a cada deploy, garantindo que o ambiente esteja sempre sincronizado sem intervenção manual.

**Variáveis de ambiente para todos os segredos**  
Nenhuma credencial foi inserida diretamente no código. Todas as configurações sensíveis (host do RDS, senha, nome do bucket) são lidas via `os.environ.get()` e configuradas nas propriedades do ambiente do Elastic Beanstalk.

---

## Dificuldades e Soluções

**Problema: `mysqlclient 2.2.1 or newer is required`**  
O Django 4.2 exige que o driver MySQL se identifique como versão `>= 2.2.1`, mas o `PyMySQL` reportava a versão `1.4.6`. Solução: adicionei `pymysql.version_info = (2, 2, 1, "final", 0)` no `myproject/__init__.py` antes do `install_as_MySQLdb()`.

**Problema: `Column 'pedido_id' cannot be null` (500 ao criar ItemPedido)**  
O campo `pedido` estava ausente na lista `fields` do `ItemPedidoSerializer`, então o Django não conseguia mapear o valor recebido para a FK. Solução: adicionei `pedido` explicitamente na lista de campos do serializer.

**Problema: URLs de imagens com parâmetros de autenticação temporária**  
O S3 gerava URLs com `AWSAccessKeyId`, `Signature` e `Expires`, tornando os links temporários. Solução: adicionei `AWS_QUERYSTRING_AUTH = False` no `settings.py`, que força a geração de URLs públicas permanentes.


**Problema: `IntegrityError` ao salvar ItemPedido com `calcular_total` no `save()`**  
O método `save()` customizado do `ItemPedido` chamava `calcular_total()` que por sua vez chamava `Pedido.save()`, criando um conflito de transação no MySQL. Solução: removi o override do `save()` e simplifiquei o modelo, deixando o cálculo do total como responsabilidade da camada de aplicação.
