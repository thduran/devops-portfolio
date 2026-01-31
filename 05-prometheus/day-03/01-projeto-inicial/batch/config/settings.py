"""
TechCommerce - Configurações do Sistema
======================================

Módulo centralizado de configurações para o job batch.
Utiliza variáveis de ambiente com valores padrão.
"""

import os
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Optional


@dataclass
class DatabaseConfig:
    """Configurações de conexão com PostgreSQL."""
    host: str
    user: str
    password: str
    name: str
    port: int

    @property
    def url(self) -> str:
        """Retorna URL de conexão SQLAlchemy."""
        return f"postgresql+psycopg2://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"

    @property
    def safe_url(self) -> str:
        """Retorna URL sem senha para logs."""
        return f"postgresql://{self.user}:***@{self.host}:{self.port}/{self.name}"


@dataclass
class PushGatewayConfig:
    """Configurações do Push Gateway."""
    url: str
    job_name: str = "daily-sales-report"

    @property
    def gateway_address(self) -> str:
        """Retorna endereço sem protocolo para push_to_gateway."""
        return self.url.replace('http://', '').replace('https://', '')


@dataclass
class ReportConfig:
    """Configurações do relatório."""
    date: datetime
    output_dir: str = "./pdf-reports"
    top_products_limit: int = 5

    @property
    def filename(self) -> str:
        """Retorna nome do arquivo PDF baseado na data."""
        return f"daily-sales-{self.date.strftime('%Y-%m-%d')}.pdf"

    @property
    def output_path(self) -> str:
        """Retorna caminho completo do arquivo de saída."""
        return f"{self.output_dir}/{self.filename}"


@dataclass
class AppSettings:
    """Configurações principais da aplicação."""
    database: DatabaseConfig
    pushgateway: PushGatewayConfig
    report: ReportConfig
    log_level: str = "INFO"


def parse_report_date(date_str: str) -> datetime:
    """
    Converte string de data em datetime.
    
    Formatos suportados:
    - 'yesterday': dia anterior
    - 'today': dia atual  
    - 'YYYY-MM-DD': data específica
    """
    if date_str == 'yesterday':
        return datetime.now() - timedelta(days=1)
    elif date_str == 'today':
        return datetime.now()
    else:
        try:
            return datetime.strptime(date_str, '%Y-%m-%d')
        except ValueError:
            raise ValueError(f"Formato de data inválido: {date_str}. Use 'yesterday', 'today' ou 'YYYY-MM-DD'")


def load_settings() -> AppSettings:
    """
    Carrega configurações a partir de variáveis de ambiente.
    
    Variáveis de ambiente suportadas:
    - DB_HOST, DB_USER, DB_PASSWORD, DB_NAME, DB_PORT
    - PUSHGATEWAY_URL
    - REPORT_DATE
    - LOG_LEVEL
    """
    
    # Configurações de banco
    database = DatabaseConfig(
        host=os.getenv('DB_HOST', 'localhost'),
        user=os.getenv('DB_USER', 'ecommerce'),
        password=os.getenv('DB_PASSWORD', 'Pg1234'),
        name=os.getenv('DB_NAME', 'ecommerce'),
        port=int(os.getenv('DB_PORT', '5432'))
    )
    
    # Configurações Push Gateway
    pushgateway = PushGatewayConfig(
        url=os.getenv('PUSHGATEWAY_URL', 'http://localhost:9091')
    )
    
    # Configurações do relatório
    report_date_str = os.getenv('REPORT_DATE', 'today')
    report_date = parse_report_date(report_date_str)
    
    report = ReportConfig(
        date=report_date,
        output_dir=os.getenv('REPORT_OUTPUT_DIR', './pdf-reports'),
        top_products_limit=int(os.getenv('TOP_PRODUCTS_LIMIT', '5'))
    )
    
    return AppSettings(
        database=database,
        pushgateway=pushgateway,
        report=report,
        log_level=os.getenv('LOG_LEVEL', 'INFO')
    )


def validate_settings(settings: AppSettings) -> None:
    """
    Valida se as configurações estão corretas.
    Raises ValueError se alguma configuração for inválida.
    """
    
    # Validar configurações de banco
    if not all([
        settings.database.host,
        settings.database.user,
        settings.database.password,
        settings.database.name
    ]):
        raise ValueError("Configurações de banco incompletas")
    
    if not (1 <= settings.database.port <= 65535):
        raise ValueError(f"Porta do banco inválida: {settings.database.port}")
    
    # Validar Push Gateway
    if not settings.pushgateway.url:
        raise ValueError("URL do Push Gateway não configurada")
    
    # Validar configurações do relatório
    if settings.report.top_products_limit < 1:
        raise ValueError("Limite de produtos deve ser >= 1")