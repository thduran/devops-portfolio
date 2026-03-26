"""
TechCommerce - Utilitários de Data
=================================

Módulo com funções auxiliares para manipulação de datas.
"""

from datetime import datetime, timedelta
from typing import Optional


def parse_date_string(date_str: str) -> datetime:
    """
    Converte string de data em datetime.
    
    Args:
        date_str: String com data em vários formatos
        
    Returns:
        Objeto datetime
        
    Raises:
        ValueError: Se formato não reconhecido
    """
    if date_str.lower() == 'yesterday':
        return datetime.now() - timedelta(days=1)
    elif date_str.lower() == 'today':
        return datetime.now()
    elif date_str.lower() == 'tomorrow':
        return datetime.now() + timedelta(days=1)
    else:
        # Tentar formatos comuns
        formats = [
            '%Y-%m-%d',          # 2025-09-22
            '%d/%m/%Y',          # 22/09/2025
            '%d-%m-%Y',          # 22-09-2025
            '%Y%m%d',            # 20250922
        ]
        
        for fmt in formats:
            try:
                return datetime.strptime(date_str, fmt)
            except ValueError:
                continue
        
        raise ValueError(f"Formato de data não reconhecido: {date_str}")


def format_date_for_filename(date: datetime) -> str:
    """
    Formata data para uso em nomes de arquivo.
    
    Args:
        date: Data a formatar
        
    Returns:
        String formatada (YYYY-MM-DD)
    """
    return date.strftime('%Y-%m-%d')


def format_date_for_display(date: datetime) -> str:
    """
    Formata data para exibição amigável.
    
    Args:
        date: Data a formatar
        
    Returns:
        String formatada (DD/MM/YYYY)
    """
    return date.strftime('%d/%m/%Y')


def get_date_range(start_date: datetime, days: int) -> list:
    """
    Gera lista de datas a partir de uma data inicial.
    
    Args:
        start_date: Data inicial
        days: Número de dias
        
    Returns:
        Lista de objetos datetime
    """
    return [start_date + timedelta(days=i) for i in range(days)]


def is_weekend(date: datetime) -> bool:
    """
    Verifica se data é fim de semana.
    
    Args:
        date: Data a verificar
        
    Returns:
        True se for sábado ou domingo
    """
    return date.weekday() >= 5  # 5=sábado, 6=domingo


def get_business_days_ago(days: int) -> datetime:
    """
    Retorna data de N dias úteis atrás.
    
    Args:
        days: Número de dias úteis
        
    Returns:
        Data de N dias úteis atrás
    """
    current = datetime.now()
    business_days = 0
    
    while business_days < days:
        current -= timedelta(days=1)
        if not is_weekend(current):
            business_days += 1
    
    return current