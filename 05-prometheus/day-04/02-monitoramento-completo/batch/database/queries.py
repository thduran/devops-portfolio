"""
TechCommerce - Queries e Repositório de Dados
=============================================

Módulo responsável por todas as consultas SQL e acesso a dados.
"""

import logging
from datetime import datetime
from typing import Dict, List

from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.connection import DatabaseConnection

logger = logging.getLogger(__name__)


class SalesQueries:
    """Constantes com queries SQL para relatórios de vendas."""
    
    DAILY_SUMMARY = """
        SELECT 
            COUNT(*) as total_orders,
            COALESCE(SUM(total_price), 0) as total_revenue,
            COALESCE(AVG(total_price), 0) as avg_ticket
        FROM orders 
        WHERE DATE(created_at) = :report_date
          AND is_open = false
    """
    
    TOP_PRODUCTS = """
        SELECT 
            p.name as product_name,
            SUM(oi.quantity) as quantity_sold,
            SUM(oi.quantity * oi.price) as product_revenue
        FROM order_items oi
        JOIN orders o ON oi.order_id = o.id
        JOIN products p ON oi.product_id = p.id
        WHERE DATE(o.created_at) = :report_date
          AND o.is_open = false
        GROUP BY p.id, p.name
        ORDER BY quantity_sold DESC
        LIMIT :limit
    """
    
    HOURLY_DISTRIBUTION = """
        SELECT 
            EXTRACT(HOUR FROM created_at) as hour,
            COUNT(*) as orders_count
        FROM orders
        WHERE DATE(created_at) = :report_date
          AND is_open = false
        GROUP BY EXTRACT(HOUR FROM created_at)
        ORDER BY hour
    """
    
    # Queries adicionais para validação
    ORDERS_COUNT_CHECK = """
        SELECT COUNT(*) as total_orders
        FROM orders 
        WHERE is_open = false
    """
    
    DATE_RANGE_CHECK = """
        SELECT 
            MIN(DATE(created_at)) as first_order,
            MAX(DATE(created_at)) as last_order,
            COUNT(*) as total_orders
        FROM orders 
        WHERE is_open = false
    """


class SalesRepository:
    """Repositório para dados de vendas com métodos de alto nível."""
    
    def __init__(self, db_connection: DatabaseConnection):
        """
        Inicializa repositório com conexão do banco.
        
        Args:
            db_connection: Instância de DatabaseConnection
        """
        self.db = db_connection
    
    def get_daily_summary(self, report_date: datetime) -> Dict[str, float]:
        """
        Busca resumo financeiro do dia.
        
        Args:
            report_date: Data do relatório
            
        Returns:
            Dict com total_orders, total_revenue, avg_ticket
            
        Raises:
            SQLAlchemyError: Erro na execução da query
        """
        try:
            with self.db.get_connection() as conn:
                result = conn.execute(
                    text(SalesQueries.DAILY_SUMMARY),
                    {"report_date": report_date.date()}
                ).fetchone()
                
            summary = {
                'total_orders': int(result.total_orders),
                'total_revenue': float(result.total_revenue),
                'avg_ticket': float(result.avg_ticket)
            }
            
            logger.info(f"📊 Resumo coletado: {summary['total_orders']} pedidos, "
                       f"R$ {summary['total_revenue']:.2f}")
            
            return summary
            
        except SQLAlchemyError as e:
            logger.error(f"❌ Erro ao buscar resumo diário: {e}")
            raise
    
    def get_top_products(self, report_date: datetime, limit: int = 5) -> List[Dict[str, any]]:
        """
        Busca produtos mais vendidos do dia.
        
        Args:
            report_date: Data do relatório
            limit: Número máximo de produtos a retornar
            
        Returns:
            Lista de dicts com product_name, quantity_sold, product_revenue
        """
        try:
            with self.db.get_connection() as conn:
                results = conn.execute(
                    text(SalesQueries.TOP_PRODUCTS),
                    {"report_date": report_date.date(), "limit": limit}
                ).fetchall()
            
            products = [
                {
                    'product_name': row.product_name,
                    'quantity_sold': int(row.quantity_sold),
                    'product_revenue': float(row.product_revenue)
                }
                for row in results
            ]
            
            logger.info(f"🏆 Top produtos coletados: {len(products)} produtos")
            
            return products
            
        except SQLAlchemyError as e:
            logger.error(f"❌ Erro ao buscar top produtos: {e}")
            raise
    
    def get_hourly_distribution(self, report_date: datetime) -> List[Dict[str, int]]:
        """
        Busca distribuição de pedidos por hora.
        
        Args:
            report_date: Data do relatório
            
        Returns:
            Lista de dicts com hour, orders_count
        """
        try:
            with self.db.get_connection() as conn:
                results = conn.execute(
                    text(SalesQueries.HOURLY_DISTRIBUTION),
                    {"report_date": report_date.date()}
                ).fetchall()
            
            hourly_data = [
                {
                    'hour': int(row.hour),
                    'orders_count': int(row.orders_count)
                }
                for row in results
            ]
            
            logger.info(f"⏰ Distribuição horária coletada: {len(hourly_data)} horas com vendas")
            
            return hourly_data
            
        except SQLAlchemyError as e:
            logger.error(f"❌ Erro ao buscar distribuição horária: {e}")
            raise
    
    def get_all_sales_data(self, report_date: datetime, top_products_limit: int = 5) -> Dict:
        """
        Busca todos os dados de vendas em uma operação.
        
        Args:
            report_date: Data do relatório
            top_products_limit: Limite de produtos no ranking
            
        Returns:
            Dict completo com summary, top_products, hourly_data
        """
        logger.info(f"📊 Coletando dados de vendas para {report_date.strftime('%d/%m/%Y')}")
        
        try:
            # Coletar todos os dados
            summary = self.get_daily_summary(report_date)
            top_products = self.get_top_products(report_date, top_products_limit)
            hourly_data = self.get_hourly_distribution(report_date)
            
            return {
                'summary': summary,
                'top_products': top_products,
                'hourly_data': hourly_data,
                'report_date': report_date
            }
            
        except SQLAlchemyError as e:
            logger.error(f"❌ Erro ao coletar dados de vendas: {e}")
            raise
    
    def validate_data_availability(self, report_date: datetime) -> Dict[str, any]:
        """
        Valida se há dados disponíveis para a data especificada.
        
        Args:
            report_date: Data a validar
            
        Returns:
            Dict com informações de disponibilidade de dados
        """
        try:
            with self.db.get_connection() as conn:
                # Verificar total de pedidos no sistema
                total_result = conn.execute(text(SalesQueries.ORDERS_COUNT_CHECK)).fetchone()
                
                # Verificar range de datas disponíveis
                range_result = conn.execute(text(SalesQueries.DATE_RANGE_CHECK)).fetchone()
                
                # Verificar dados para a data específica
                date_result = conn.execute(
                    text(SalesQueries.DAILY_SUMMARY),
                    {"report_date": report_date.date()}
                ).fetchone()
            
            validation = {
                'total_orders_system': int(total_result.total_orders),
                'first_order_date': range_result.first_order,
                'last_order_date': range_result.last_order,
                'orders_for_date': int(date_result.total_orders),
                'has_data_for_date': int(date_result.total_orders) > 0,
                'date_in_range': (
                    range_result.first_order <= report_date.date() <= range_result.last_order
                    if range_result.first_order and range_result.last_order
                    else False
                )
            }
            
            logger.info(f"✅ Validação de dados: {validation['orders_for_date']} pedidos na data")
            
            return validation
            
        except SQLAlchemyError as e:
            logger.error(f"❌ Erro na validação de dados: {e}")
            raise