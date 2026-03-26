#!/usr/bin/env python3
"""
TechCommerce - Relatório de Vendas Diário
=========================================

Entry point principal do job batch para geração de relatórios de vendas.

Este job:
1. Conecta no PostgreSQL
2. Coleta dados de vendas do dia especificado
3. Gera PDF com relatório visual  
4. Envia métricas para Push Gateway
5. Container finaliza (efêmero)

Uso:
    python main.py

Variáveis de ambiente:
    DB_HOST, DB_USER, DB_PASSWORD, DB_NAME, DB_PORT
    PUSHGATEWAY_URL
    REPORT_DATE (yesterday, today, ou YYYY-MM-DD)
    LOG_LEVEL (DEBUG, INFO, WARNING, ERROR)

Autor: TechCommerce DevOps Team
"""

import sys
import os

# Adicionar diretório raiz ao Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# Importar módulos relativos
try:
    from config.settings import load_settings, validate_settings
    from database.connection import create_database_connection
    from database.queries import SalesRepository
    from reports.pdf_engine import create_pdf_engine
    from reports.generator import create_report_generator
    from metrics.definitions import MetricsCollector
    from metrics.publisher import create_metrics_publisher
    from utils.logger import setup_logging
except ImportError as e:
    print(f"❌ Erro de import: {e}")
    print(f"📁 Diretório atual: {current_dir}")
    print(f"🐍 Python path: {sys.path}")


def main() -> int:
    """
    Função principal do job batch.
    
    Returns:
        0 se sucesso, 1 se erro
    """
    
    try:
        # 1. Carregar e validar configurações
        settings = load_settings()
        validate_settings(settings)
        
        # 2. Configurar logging
        setup_logging(settings.log_level)
        logger = setup_logging(settings.log_level)
        
        logger.info("🚀 Iniciando TechCommerce - Relatório de Vendas Diário")
        logger.info(f"📅 Data do relatório: {settings.report.date.strftime('%d/%m/%Y')}")
        logger.info(f"🔗 Banco: {settings.database.safe_url}")
        logger.info(f"📊 Push Gateway: {settings.pushgateway.url}")
        
        # 3. Inicializar componentes
        logger.info("🔧 Inicializando componentes...")
        
        # Conexão com banco
        db_connection = create_database_connection(settings.database)
        sales_repository = SalesRepository(db_connection)
        
        # Engine de PDF
        pdf_engine = create_pdf_engine()
        
        # Métricas
        metrics_collector = MetricsCollector()
        metrics_publisher = create_metrics_publisher(settings.pushgateway)
        
        # Gerador de relatórios
        report_generator = create_report_generator(
            sales_repository,
            pdf_engine, 
            metrics_collector,
            metrics_publisher
        )
        
        logger.info("✅ Componentes inicializados com sucesso")
        
        # 4. Validar setup
        logger.info("🔍 Validando configuração...")
        validation = report_generator.validate_setup()
        
        failed_components = [k for k, v in validation.items() if not v]
        if failed_components:
            logger.warning(f"⚠️ Componentes com problemas: {failed_components}")
            logger.warning("Continuando execução, mas métricas podem não ser enviadas")
        
        # 5. Gerar relatório
        logger.info("📊 Gerando relatório de vendas...")
        result = report_generator.generate_report(settings.report)
        
        # 6. Processar resultado
        if result.success:
            logger.info(f"🎉 Relatório gerado com sucesso!")
            logger.info(f"📄 Arquivo: {result.filename}")
            logger.info(f"📏 Tamanho: {result.file_size_bytes / 1024:.1f} KB")
            logger.info(f"⏱️ Duração total: {result.generation_duration:.2f}s")
            logger.info(f"🗄️ Duração queries: {result.query_duration:.2f}s")
            logger.info(f"📄 Duração PDF: {result.pdf_duration:.2f}s")
            logger.info(f"📊 Métricas enviadas: {'✅' if result.metrics_pushed else '❌'}")
            
            if not result.metrics_pushed:
                logger.warning("⚠️ Métricas não foram enviadas ao Push Gateway")
            
            return 0
            
        else:
            logger.error(f"❌ Falha na geração do relatório: {result.error_message}")
            logger.error(f"⏱️ Duração até falha: {result.generation_duration:.2f}s")
            return 1
            
    except KeyboardInterrupt:
        logger.info("⏹️ Execução interrompida pelo usuário")
        return 1
        
    except Exception as e:
        logger.error(f"❌ Erro inesperado: {e}")
        logger.exception("Detalhes do erro:")
        return 1
        
    finally:
        # Cleanup
        try:
            if 'db_connection' in locals():
                db_connection.close()
                logger.info("🔌 Conexões de banco fechadas")
        except Exception as e:
            logger.warning(f"⚠️ Erro no cleanup: {e}")


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)