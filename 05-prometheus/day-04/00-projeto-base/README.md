# 🛍️ E-commerce TechCommerce - Projeto Base

## 📋 Visão Geral

Este é o **projeto base** do e-commerce TechCommerce, uma aplicação Flask completa **sem instrumentação Prometheus**. O objetivo desta etapa é você conhecer a aplicação e entender seu funcionamento antes de adicionar monitoramento.

## 🎯 Objetivo desta Etapa

- Conhecer a arquitetura da aplicação e-commerce
- Entender o fluxo de funcionalidades (catálogo, carrinho, checkout)
- Executar e testar a aplicação localmente
- Preparar o ambiente para as próximas etapas de instrumentação

## 🏗️ Arquitetura

```
┌─────────────────────────────────┐
│     Flask Application           │
│     (Python 3.x)                │
│                                 │
│  Rotas:                         │
│  - /              (catálogo)    │
│  - /shop          (produtos)    │
│  - /detail/<id>   (detalhes)    │
│  - /add_to_cart   (adicionar)   │
│  - /cart          (carrinho)    │
│  - /checkout      (finalizar)   │
│                                 │
└────────────┬────────────────────┘
             │
             │ SQLAlchemy
             ↓
┌─────────────────────────────────┐
│     PostgreSQL Database         │
│                                 │
│  Tabelas:                       │
│  - products                     │
│  - orders                       │
│  - order_items                  │
└─────────────────────────────────┘
```

## 🚀 Como Executar

### 1. Iniciar com Docker Compose

```bash
# Subir aplicação e banco de dados
docker-compose up -d

# Verificar se está rodando
docker-compose ps
```

### 2. Acessar a Aplicação

- **URL**: http://localhost:5000
- **Interface**: Catálogo de produtos com sistema de carrinho completo

### 3. Testar Funcionalidades

```bash
# Navegar pela aplicação
open http://localhost:5000

# Ou usar curl
curl http://localhost:5000
```

## 📦 Funcionalidades Disponíveis

### Catálogo de Produtos
- Listagem de produtos com imagens
- Detalhes de cada produto
- Sistema de categorias

### Sistema de Carrinho
- Adicionar produtos ao carrinho
- Atualizar quantidades
- Remover itens
- Cálculo automático de totais

### Checkout
- Formulário de dados do usuário
- Informações de entrega
- Dados de pagamento
- Confirmação de pedido

## 🗄️ Modelos de Dados

### Product
```python
- id: Integer (Primary Key)
- name: String
- price: Float
- description: Text
- image: String (URL)
```

### Order
```python
- id: Integer (Primary Key)
- uuid: UUID (Cookie tracking)
- is_open: Boolean (carrinho ativo)
- order_number: String (após checkout)
- user_name, user_email, mobile
- address1, address2, city, state, country, zip_code
- card_name, card_number, expiry_date, cvv
```

### OrderItem
```python
- id: Integer (Primary Key)
- order_id: Foreign Key → Order
- product_id: Foreign Key → Product
- quantity: Integer
- price: Float (snapshot do preço)
```

## 🔧 Tecnologias

- **Backend**: Flask 3.0
- **ORM**: SQLAlchemy
- **Database**: PostgreSQL 15
- **Migrations**: Alembic (Flask-Migrate)
- **Frontend**: HTML/CSS/Bootstrap + Jinja2
- **Container**: Docker + Gunicorn

## 📝 Variáveis de Ambiente

| Variável | Padrão | Descrição |
|----------|---------|-----------|
| `DB_HOST` | localhost | Host do PostgreSQL |
| `DB_USER` | ecommerce | Usuário do banco |
| `DB_PASSWORD` | Pg1234 | Senha do banco |
| `DB_NAME` | ecommerce | Nome do banco |
| `DB_PORT` | 5432 | Porta do PostgreSQL |

## 🛠️ Comandos Úteis

```bash
# Ver logs da aplicação
docker-compose logs -f app

# Acessar banco de dados
docker-compose exec postgres psql -U ecommerce -d ecommerce

# Parar ambiente
docker-compose down

# Limpar volumes (reseta banco)
docker-compose down -v
```

## 🎓 Próxima Etapa

Após conhecer a aplicação base, você irá para a **01-instrumentacao-basica/** onde aprenderá a adicionar:

- **Counter**: Contar eventos (adições ao carrinho, erros)
- **Gauge**: Métricas instantâneas (sessões ativas, CPU)
- **Histogram**: Distribuição de valores (latência de requests)

---

**Versão**: 1.0
**Autor**: TechCommerce DevOps Team
**Curso**: Introdução à Instrumentação Prometheus
