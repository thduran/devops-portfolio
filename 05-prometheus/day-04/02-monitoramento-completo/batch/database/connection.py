"""
TechCommerce - Conexão com Banco de Dados
=========================================

Módulo responsável pela conexão e gerenciamento do PostgreSQL.
"""

import logging
from contextlib import contextmanager
from typing import Generator

from sqlalchemy import create_engine, Engine, text
from sqlalchemy.exc import SQLAlchemyError

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.settings import DatabaseConfig

logger = logging.getLogger(__name__)


class DatabaseConnection:
    """Gerenciador de conexão com PostgreSQL."""
    
    def __init__(self, config: DatabaseConfig):
        """
        Inicializa conexão com o banco.
        
        Args:
            config: Configurações de conexão do banco
        """
        self.config = config
        self._engine: Engine = None
    
    @property
    def engine(self) -> Engine:
        """Retorna engine SQLAlchemy, criando se necessário."""
        if self._engine is None:
            self._create_engine()
        return self._engine
    
    def _create_engine(self) -> None:
        """Cria engine SQLAlchemy com configurações otimizadas."""
        try:
            self._engine = create_engine(
                self.config.url,
                # Configurações para jobs batch (conexões temporárias)
                pool_size=2,
                max_overflow=0,
                pool_timeout=30,
                pool_recycle=3600,
                # Logging de SQL em modo debug
                echo=logger.level <= logging.DEBUG
            )
            logger.info(f"✅ Engine criada: {self.config.safe_url}")
            
        except SQLAlchemyError as e:
            logger.error(f"❌ Erro ao criar engine: {e}")
            raise
    
    def test_connection(self) -> bool:
        """
        Testa conectividade com o banco.
        
        Returns:
            True se conexão bem-sucedida, False caso contrário
        """
        try:
            with self.engine.connect() as conn:
                result = conn.execute(text("SELECT 1")).scalar()
                if result == 1:
                    logger.info("✅ Teste de conexão bem-sucedido")
                    return True
                else:
                    logger.error("❌ Teste de conexão falhou: resultado inesperado")
                    return False
                    
        except SQLAlchemyError as e:
            logger.error(f"❌ Teste de conexão falhou: {e}")
            return False
    
    @contextmanager
    def get_connection(self) -> Generator:
        """
        Context manager para conexões transacionais.
        
        Yields:
            Conexão SQLAlchemy para execução de queries
            
        Example:
            with db.get_connection() as conn:
                result = conn.execute(text("SELECT * FROM orders"))
        """
        connection = None
        try:
            connection = self.engine.connect()
            logger.debug("🔗 Conexão aberta")
            yield connection
            
        except SQLAlchemyError as e:
            logger.error(f"❌ Erro na conexão: {e}")
            if connection:
                connection.rollback()
            raise
            
        finally:
            if connection:
                connection.close()
                logger.debug("🔌 Conexão fechada")
    
    def close(self) -> None:
        """Fecha engine e todas as conexões."""
        if self._engine:
            self._engine.dispose()
            logger.info("🔌 Engine fechada")


def create_database_connection(config: DatabaseConfig) -> DatabaseConnection:
    """
    Factory function para criar conexão com banco.
    
    Args:
        config: Configurações do banco
        
    Returns:
        Instância configurada de DatabaseConnection
    """
    db = DatabaseConnection(config)
    
    # Testar conexão na criação
    if not db.test_connection():
        raise ConnectionError("Não foi possível conectar ao banco de dados")
    
    return db