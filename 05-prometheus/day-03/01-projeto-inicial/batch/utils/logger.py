"""
TechCommerce - Configuração de Logging
=====================================

Módulo para configuração padronizada de logging.
"""

import logging
import sys
from typing import Optional


def setup_logging(level: str = "INFO", 
                 format_string: Optional[str] = None) -> logging.Logger:
    """
    Configura logging para o job batch.
    
    Args:
        level: Nível de log (DEBUG, INFO, WARNING, ERROR)
        format_string: Formato personalizado (opcional)
        
    Returns:
        Logger configurado
    """
    
    # Formato padrão com timestamp e contexto
    if format_string is None:
        format_string = (
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
    
    # Configurar logging básico
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format=format_string,
        datefmt='%Y-%m-%d %H:%M:%S',
        stream=sys.stdout,
        force=True  # Sobrescrever configuração anterior se existir
    )
    
    # Configurar loggers específicos
    logger = logging.getLogger('techcommerce')
    
    # Reduzir verbosidade de bibliotecas externas
    logging.getLogger('sqlalchemy.engine').setLevel(logging.WARNING)
    logging.getLogger('urllib3').setLevel(logging.WARNING)
    logging.getLogger('requests').setLevel(logging.WARNING)
    
    return logger


def get_logger(name: str) -> logging.Logger:
    """
    Retorna logger com nome específico.
    
    Args:
        name: Nome do logger (geralmente __name__)
        
    Returns:
        Logger configurado
    """
    return logging.getLogger(f'techcommerce.{name}')