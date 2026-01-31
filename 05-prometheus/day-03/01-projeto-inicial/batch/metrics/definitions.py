"""
TechCommerce - Definições de Métricas Prometheus
===============================================

Módulo com todas as métricas Prometheus organizadas por categoria.
"""

from prometheus_client import Gauge, CollectorRegistry
from typing import Dict, Any


class BusinessMetrics:
    """Métricas de negócio relacionadas aos dados de vendas."""
    
    def __init__(self, registry: CollectorRegistry):
        """
        Inicializa métricas de negócio.
        
        Args:
            registry: Registry do Prometheus para este job
        """
        self.daily_revenue_total = Gauge(
            'daily_sales_revenue_total',
            'Faturamento total do dia em reais',
            registry=registry
        )
        
        self.daily_orders_count = Gauge(
            'daily_sales_orders_count',
            'Quantidade total de pedidos do dia',
            registry=registry
        )
        
        self.daily_avg_ticket = Gauge(
            'daily_sales_avg_ticket_amount',
            'Ticket médio do dia em reais',
            registry=registry
        )
        
        self.daily_top_product_revenue = Gauge(
            'daily_sales_top_product_revenue',
            'Receita do produto mais vendido do dia',
            registry=registry
        )
    
    def update_from_data(self, sales_data: Dict[str, Any]) -> None:
        """
        Atualiza todas as métricas de negócio com dados de vendas.
        
        Args:
            sales_data: Dict com dados de vendas (summary, top_products)
        """
        summary = sales_data['summary']
        top_products = sales_data['top_products']
        
        # Métricas básicas do resumo
        self.daily_revenue_total.set(summary['total_revenue'])
        self.daily_orders_count.set(summary['total_orders'])
        self.daily_avg_ticket.set(summary['avg_ticket'])
        
        # Receita do produto top (se existir)
        if top_products and len(top_products) > 0:
            self.daily_top_product_revenue.set(top_products[0]['product_revenue'])
        else:
            self.daily_top_product_revenue.set(0)


class TechnicalMetrics:
    """Métricas técnicas relacionadas à performance do job."""
    
    def __init__(self, registry: CollectorRegistry):
        """
        Inicializa métricas técnicas.
        
        Args:
            registry: Registry do Prometheus para este job
        """
        self.report_generation_duration = Gauge(
            'report_generation_duration_seconds',
            'Tempo total para gerar o relatório em segundos',
            registry=registry
        )
        
        self.report_pdf_size_kb = Gauge(
            'report_pdf_size_kilobytes',
            'Tamanho do arquivo PDF gerado em KB',
            registry=registry
        )
        
        self.report_last_run_timestamp = Gauge(
            'report_last_run_timestamp',
            'Timestamp Unix da última execução do job',
            registry=registry
        )
        
        self.report_database_query_duration = Gauge(
            'report_database_query_duration_seconds',
            'Tempo gasto executando queries no banco',
            registry=registry
        )
        
        self.report_pdf_generation_duration = Gauge(
            'report_pdf_generation_duration_seconds',
            'Tempo gasto gerando o arquivo PDF',
            registry=registry
        )
    
    def update_durations(self, 
                        total_duration: float,
                        query_duration: float = None,
                        pdf_duration: float = None) -> None:
        """
        Atualiza métricas de duração do job.
        
        Args:
            total_duration: Tempo total de execução
            query_duration: Tempo de queries (opcional)
            pdf_duration: Tempo de geração PDF (opcional)
        """
        self.report_generation_duration.set(total_duration)
        
        if query_duration is not None:
            self.report_database_query_duration.set(query_duration)
            
        if pdf_duration is not None:
            self.report_pdf_generation_duration.set(pdf_duration)
    
    def update_pdf_info(self, pdf_size_bytes: int) -> None:
        """
        Atualiza informações do arquivo PDF gerado.
        
        Args:
            pdf_size_bytes: Tamanho do PDF em bytes
        """
        self.report_pdf_size_kb.set(pdf_size_bytes / 1024)
    
    def update_timestamp(self, timestamp: float) -> None:
        """
        Atualiza timestamp da última execução.
        
        Args:
            timestamp: Timestamp Unix
        """
        self.report_last_run_timestamp.set(timestamp)


class MetricsCollector:
    """Coletor principal que gerencia todas as métricas."""
    
    def __init__(self):
        """Inicializa coletor com registry separado."""
        self.registry = CollectorRegistry()
        self.business = BusinessMetrics(self.registry)
        self.technical = TechnicalMetrics(self.registry)
    
    def update_all(self,
                   sales_data: Dict[str, Any],
                   total_duration: float,
                   pdf_size_bytes: int,
                   timestamp: float,
                   query_duration: float = None,
                   pdf_duration: float = None) -> None:
        """
        Atualiza todas as métricas de uma vez.
        
        Args:
            sales_data: Dados de vendas
            total_duration: Duração total do job
            pdf_size_bytes: Tamanho do PDF
            timestamp: Timestamp da execução
            query_duration: Duração das queries (opcional)
            pdf_duration: Duração da geração PDF (opcional)
        """
        # Atualizar métricas de negócio
        self.business.update_from_data(sales_data)
        
        # Atualizar métricas técnicas
        self.technical.update_durations(total_duration, query_duration, pdf_duration)
        self.technical.update_pdf_info(pdf_size_bytes)
        self.technical.update_timestamp(timestamp)
    
    def get_metrics_summary(self) -> Dict[str, float]:
        """
        Retorna resumo de todas as métricas para logging.
        
        Returns:
            Dict com valores atuais das métricas principais
        """
        return {
            'revenue_total': self.business.daily_revenue_total._value._value,
            'orders_count': self.business.daily_orders_count._value._value,
            'avg_ticket': self.business.daily_avg_ticket._value._value,
            'generation_duration': self.technical.report_generation_duration._value._value,
            'pdf_size_kb': self.technical.report_pdf_size_kb._value._value,
        }