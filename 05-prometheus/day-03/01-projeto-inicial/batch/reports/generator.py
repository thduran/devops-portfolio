"""
TechCommerce - Gerador de Relatórios
===================================

Módulo principal para orquestração da geração de relatórios.
"""

import logging
import time
from datetime import datetime
from typing import Dict, Any, Optional
from dataclasses import dataclass

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.queries import SalesRepository
from reports.pdf_engine import PDFEngine
from metrics.definitions import MetricsCollector
from metrics.publisher import MetricsPublisher
from config.settings import ReportConfig

logger = logging.getLogger(__name__)


@dataclass
class ReportResult:
    """Resultado da geração de um relatório."""
    success: bool
    filename: str
    file_size_bytes: int
    generation_duration: float
    query_duration: float
    pdf_duration: float
    metrics_pushed: bool
    error_message: Optional[str] = None


class DailySalesReportGenerator:
    """Gerador de relatórios de vendas diárias."""
    
    def __init__(self, 
                 sales_repository: SalesRepository,
                 pdf_engine: PDFEngine,
                 metrics_collector: MetricsCollector,
                 metrics_publisher: MetricsPublisher):
        """
        Inicializa gerador de relatórios.
        
        Args:
            sales_repository: Repositório de dados de vendas
            pdf_engine: Engine para geração de PDF
            metrics_collector: Coletor de métricas
            metrics_publisher: Publicador de métricas
        """
        self.sales_repo = sales_repository
        self.pdf_engine = pdf_engine
        self.metrics = metrics_collector
        self.publisher = metrics_publisher
    
    def generate_report(self, config: ReportConfig) -> ReportResult:
        """
        Gera relatório completo de vendas diárias.
        
        Args:
            config: Configurações do relatório
            
        Returns:
            Resultado da geração do relatório
        """
        start_time = time.time()
        
        logger.info(f"🚀 Iniciando geração de relatório para {config.date.strftime('%d/%m/%Y')}")
        
        try:
            # 1. Coletar dados de vendas
            logger.info("📊 Coletando dados de vendas...")
            query_start = time.time()
            
            sales_data = self.sales_repo.get_all_sales_data(
                config.date, 
                config.top_products_limit
            )
            
            query_duration = time.time() - query_start
            logger.info(f"✅ Dados coletados em {query_duration:.2f}s")
            
            # 2. Validar se há dados suficientes
            self._validate_sales_data(sales_data, config.date)
            
            # 3. Gerar PDF
            logger.info("📄 Gerando arquivo PDF...")
            pdf_start = time.time()
            
            pdf_size = self._generate_pdf_report(sales_data, config)
            
            pdf_duration = time.time() - pdf_start
            logger.info(f"✅ PDF gerado em {pdf_duration:.2f}s")
            
            # 4. Atualizar métricas
            total_duration = time.time() - start_time
            self._update_metrics(sales_data, total_duration, pdf_size, 
                               query_duration, pdf_duration)
            
            # 5. Publicar métricas
            logger.info("📊 Publicando métricas...")
            metrics_pushed = self.publisher.push_metrics(self.metrics.registry)
            
            # 6. Resultado final
            total_duration = time.time() - start_time
            
            result = ReportResult(
                success=True,
                filename=config.filename,
                file_size_bytes=pdf_size,
                generation_duration=total_duration,
                query_duration=query_duration,
                pdf_duration=pdf_duration,
                metrics_pushed=metrics_pushed
            )
            
            logger.info(f"🎉 Relatório gerado com sucesso em {total_duration:.2f}s")
            return result
            
        except Exception as e:
            total_duration = time.time() - start_time
            
            result = ReportResult(
                success=False,
                filename=config.filename,
                file_size_bytes=0,
                generation_duration=total_duration,
                query_duration=0,
                pdf_duration=0,
                metrics_pushed=False,
                error_message=str(e)
            )
            
            logger.error(f"❌ Erro na geração do relatório: {e}")
            return result
    
    def _validate_sales_data(self, sales_data: Dict[str, Any], report_date: datetime) -> None:
        """
        Valida se os dados de vendas são suficientes para o relatório.
        
        Args:
            sales_data: Dados de vendas coletados
            report_date: Data do relatório
            
        Raises:
            ValueError: Se dados insuficientes
        """
        summary = sales_data['summary']
        
        if summary['total_orders'] == 0:
            # Verificar se existem dados no sistema
            validation = self.sales_repo.validate_data_availability(report_date)
            
            if validation['total_orders_system'] == 0:
                raise ValueError(
                    "Nenhum pedido encontrado no sistema. "
                    "Execute a aplicação e faça alguns pedidos primeiro."
                )
            elif not validation['date_in_range']:
                date_range = f"{validation['first_order_date']} a {validation['last_order_date']}"
                raise ValueError(
                    f"Nenhum pedido na data {report_date.strftime('%d/%m/%Y')}. "
                    f"Pedidos disponíveis de {date_range}."
                )
            else:
                logger.warning(
                    f"⚠️ Nenhum pedido na data {report_date.strftime('%d/%m/%Y')}, "
                    "mas continuando geração com dados vazios."
                )
    
    def _generate_pdf_report(self, sales_data: Dict[str, Any], config: ReportConfig) -> int:
        """
        Gera arquivo PDF do relatório.
        
        Args:
            sales_data: Dados de vendas
            config: Configurações do relatório
            
        Returns:
            Tamanho do arquivo em bytes
        """
        # Preparar contexto para o template
        template_context = {
            'summary': sales_data['summary'],
            'top_products': sales_data['top_products'],
            'hourly_data': sales_data['hourly_data'],
            'report_date_formatted': config.date.strftime('%d/%m/%Y'),
            'generation_timestamp': datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        }
        
        # Gerar PDF usando template
        return self.pdf_engine.generate_from_template(
            'daily_sales.html',
            template_context,
            config.output_path
        )
    
    def _update_metrics(self, 
                       sales_data: Dict[str, Any],
                       total_duration: float,
                       pdf_size: int,
                       query_duration: float,
                       pdf_duration: float) -> None:
        """
        Atualiza todas as métricas com os resultados da geração.
        
        Args:
            sales_data: Dados de vendas
            total_duration: Duração total da geração
            pdf_size: Tamanho do PDF em bytes
            query_duration: Duração das queries
            pdf_duration: Duração da geração do PDF
        """
        self.metrics.update_all(
            sales_data=sales_data,
            total_duration=total_duration,
            pdf_size_bytes=pdf_size,
            timestamp=time.time(),
            query_duration=query_duration,
            pdf_duration=pdf_duration
        )
        
        # Log das métricas principais
        metrics_summary = self.metrics.get_metrics_summary()
        logger.info(f"📊 Métricas atualizadas: {metrics_summary}")
    
    def generate_preview(self, config: ReportConfig) -> str:
        """
        Gera prévia HTML do relatório sem salvar PDF.
        
        Args:
            config: Configurações do relatório
            
        Returns:
            HTML renderizado do relatório
        """
        logger.info("👀 Gerando prévia do relatório...")
        
        # Coletar dados
        sales_data = self.sales_repo.get_all_sales_data(
            config.date, 
            config.top_products_limit
        )
        
        # Preparar contexto
        template_context = {
            'summary': sales_data['summary'],
            'top_products': sales_data['top_products'],
            'hourly_data': sales_data['hourly_data'],
            'report_date_formatted': config.date.strftime('%d/%m/%Y'),
            'generation_timestamp': datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        }
        
        # Renderizar template
        return self.pdf_engine.render_template('daily_sales.html', template_context)
    
    def validate_setup(self) -> Dict[str, bool]:
        """
        Valida se o gerador está configurado corretamente.
        
        Returns:
            Dict com status de cada componente
        """
        validation = {}
        
        # Testar conexão do banco
        try:
            validation['database'] = self.sales_repo.db.test_connection()
        except Exception:
            validation['database'] = False
        
        # Testar template engine
        try:
            validation['template'] = self.pdf_engine.validate_template('daily_sales.html')
        except Exception:
            validation['template'] = False
        
        # Testar Push Gateway
        try:
            validation['push_gateway'] = self.publisher.test_connectivity()
        except Exception:
            validation['push_gateway'] = False
        
        logger.info(f"🔍 Validação do setup: {validation}")
        return validation


def create_report_generator(sales_repo: SalesRepository,
                          pdf_engine: PDFEngine,
                          metrics_collector: MetricsCollector,
                          metrics_publisher: MetricsPublisher) -> DailySalesReportGenerator:
    """
    Factory function para criar gerador de relatórios.
    
    Args:
        sales_repo: Repositório de vendas
        pdf_engine: Engine de PDF
        metrics_collector: Coletor de métricas
        metrics_publisher: Publicador de métricas
        
    Returns:
        Instância configurada do gerador
    """
    generator = DailySalesReportGenerator(
        sales_repo, pdf_engine, metrics_collector, metrics_publisher
    )
    
    # Validar setup na criação
    validation = generator.validate_setup()
    
    if not all(validation.values()):
        failed_components = [k for k, v in validation.items() if not v]
        logger.warning(f"⚠️ Componentes com problemas: {failed_components}")
    
    return generator