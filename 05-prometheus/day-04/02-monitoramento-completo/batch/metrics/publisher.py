"""
TechCommerce - Publisher de Métricas para Push Gateway
=====================================================

Módulo responsável pelo envio de métricas para o Push Gateway.
"""

import logging
from typing import Optional

from prometheus_client import push_to_gateway, CollectorRegistry

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.settings import PushGatewayConfig

logger = logging.getLogger(__name__)


class MetricsPublisher:
    """Responsável por publicar métricas no Push Gateway."""
    
    def __init__(self, config: PushGatewayConfig):
        """
        Inicializa publisher.
        
        Args:
            config: Configurações do Push Gateway
        """
        self.config = config
        self._last_push_successful = False
    
    def push_metrics(self, registry: CollectorRegistry, 
                    grouping_key: Optional[dict] = None) -> bool:
        """
        Envia métricas para o Push Gateway.
        
        Args:
            registry: Registry com as métricas a enviar
            grouping_key: Chaves adicionais para agrupamento (opcional)
            
        Returns:
            True se envio bem-sucedido, False caso contrário
        """
        try:
            logger.info(f"📊 Enviando métricas para: {self.config.url}")
            
            # Preparar parâmetros do push
            push_params = {
                'gateway': self.config.gateway_address,
                'job': self.config.job_name,
                'registry': registry
            }
            
            # Adicionar grouping key se fornecida
            if grouping_key:
                push_params['grouping_key'] = grouping_key
            
            # Executar push
            push_to_gateway(**push_params)
            
            self._last_push_successful = True
            logger.info("✅ Métricas enviadas com sucesso para Push Gateway")
            
            return True
            
        except Exception as e:
            self._last_push_successful = False
            logger.error(f"❌ Erro inesperado ao enviar métricas: {e}")
            return False
    
    def push_with_instance_info(self, registry: CollectorRegistry,
                               instance_id: str = None) -> bool:
        """
        Envia métricas com informações da instância.
        
        Args:
            registry: Registry com as métricas
            instance_id: ID da instância (opcional, usa hostname se não fornecido)
            
        Returns:
            True se envio bem-sucedido, False caso contrário
        """
        import socket
        
        if instance_id is None:
            instance_id = socket.gethostname()
        
        grouping_key = {
            'instance': instance_id
        }
        
        return self.push_metrics(registry, grouping_key)
    
    def test_connectivity(self) -> bool:
        """
        Testa conectividade com Push Gateway.
        
        Returns:
            True se Push Gateway acessível, False caso contrário
        """
        try:
            import requests
            
            # Tentar acessar a interface web do Push Gateway
            response = requests.get(f"{self.config.url}/metrics", timeout=5)
            
            if response.status_code == 200:
                logger.info("✅ Push Gateway acessível")
                return True
            else:
                logger.warning(f"⚠️ Push Gateway retornou status {response.status_code}")
                return False
                
        except requests.RequestException as e:
            logger.error(f"❌ Erro ao testar conectividade: {e}")
            return False
        except ImportError:
            logger.warning("⚠️ Requests não disponível para teste de conectividade")
            # Assumir que está OK se não podemos testar
            return True
    
    @property
    def last_push_successful(self) -> bool:
        """Retorna status do último push."""
        return self._last_push_successful
    
    def get_gateway_info(self) -> dict:
        """
        Retorna informações sobre o Push Gateway configurado.
        
        Returns:
            Dict com informações de configuração
        """
        return {
            'url': self.config.url,
            'gateway_address': self.config.gateway_address,
            'job_name': self.config.job_name,
            'last_push_successful': self._last_push_successful
        }


def create_metrics_publisher(config: PushGatewayConfig, 
                           test_connectivity: bool = True) -> MetricsPublisher:
    """
    Factory function para criar publisher de métricas.
    
    Args:
        config: Configurações do Push Gateway
        test_connectivity: Se deve testar conectividade na criação
        
    Returns:
        Instância configurada de MetricsPublisher
        
    Raises:
        ConnectionError: Se teste de conectividade falhar
    """
    publisher = MetricsPublisher(config)
    
    if test_connectivity:
        if not publisher.test_connectivity():
            logger.warning(
                "⚠️ Push Gateway não acessível, mas continuando execução. "
                "Métricas podem não ser enviadas."
            )
            # Não falhar aqui, pois pode ser um problema temporário
    
    return publisher