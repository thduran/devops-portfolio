from prometheus_client import Counter, Gauge, Histogram, Summary
import psutil
import time

# ===============================================================================
# MÉTRICA COUNTER - Só pode crescer, nunca diminui
# ===============================================================================
# CONCEITO: Counter é como um odômetro de carro - sempre aumenta
# QUANDO USAR: Contagem de eventos que sempre crescem (requests, erros, vendas)
# MÉTODO: .inc() para incrementar

cart_additions_total = Counter(
    'ecommerce_cart_additions_total',
    'Total de adições ao carrinho por produto',
    ['product_id']  # Labels permitem segmentar dados (filtrar por produto)
)

errors_total = Counter(
    'ecommerce_errors_total',
    'Total de erros no sistema por tipo',
    ['error_type', 'endpoint', 'status_code']  # Labels para classificar erros
)

# ===============================================================================
# MÉTRICA GAUGE - Pode subir e descer como um velocímetro
# ===============================================================================
# CONCEITO: Gauge é como um termômetro - mostra valor atual, pode variar
# QUANDO USAR: Valores instantâneos (CPU, memória, usuários online, fila)
# MÉTODO: .set() para definir valor absoluto, .inc()/.dec() para alterar

active_sessions_gauge = Gauge(
    'ecommerce_active_sessions',
    'Número atual de sessões com carrinho ativo'
    # SEM LABELS: métrica simples, um valor global
)

cpu_usage_gauge = Gauge(
    'ecommerce_cpu_usage_percent',
    'Percentual atual de uso de CPU do sistema'
    # ATUALIZADA SOB DEMANDA: quando /metrics é acessado
)

# ===============================================================================
# MÉTRICA HISTOGRAM - Mede distribuição de valores em buckets
# ===============================================================================
# CONCEITO: Histogram é como um gráfico de barras - agrupa valores em faixas
# QUANDO USAR: Latência, tamanhos de request, duração de operações
# MÉTODO: .observe(valor) para registrar medição
# GERA AUTOMATICAMENTE: _count (total), _sum (soma), _bucket (distribuição)

request_duration_histogram = Histogram(
    'ecommerce_request_duration_seconds',
    'Tempo de resposta de requisições HTTP em segundos',
    ['method', 'endpoint', 'status_code'],  # Labels para segmentar por rota
    buckets=[0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0]
    # BUCKETS: faixas de tempo em segundos (10ms até 10s)
    # PERMITE CALCULAR: percentis (P50, P95, P99) no Prometheus
)


# ===============================================================================
# FUNÇÕES AUXILIARES - Atualização das métricas Gauge
# ===============================================================================
# PADRÃO: Gauge precisa ser atualizada ativamente (push model)
# DIFERENTE: Counter incrementa automaticamente quando evento ocorre

def update_cpu_usage():
    """
    DIDÁTICA: Exemplo de Gauge para monitoramento de sistema
    QUANDO CHAMAR: No endpoint /metrics para ter valor atualizado
    """
    try:
        cpu_percent = psutil.cpu_percent()
        # GAUGE: .set() define valor absoluto (não .inc() que incrementa)
        cpu_usage_gauge.set(cpu_percent)
        print(f"🖥️ CPU atualizada: {cpu_percent}%")
    except Exception as e:
        print(f"Erro ao atualizar CPU: {e}")

def update_active_sessions():
    """
    DIDÁTICA: Exemplo de Gauge para métricas de negócio
    QUANDO CHAMAR: Sempre que carrinho é criado/fechado
    CONCEITO: Reconta total (não incrementa), mostra valor atual
    """
    try:
        from models.order import Order
        # PADRÃO: Recontar total em vez de incrementar/decrementar
        active_count = Order.query.filter_by(is_open=True).count()
        # GAUGE: .set() para valor absoluto atual
        active_sessions_gauge.set(active_count)
        print(f"📊 Sessões ativas: {active_count}")
    except Exception as e:
        print(f"Erro ao atualizar sessões ativas: {e}")

