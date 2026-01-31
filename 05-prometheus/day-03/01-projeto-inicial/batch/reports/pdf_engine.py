"""
TechCommerce - Engine de Geração de PDF
======================================

Módulo responsável pela geração de relatórios PDF usando templates HTML.
"""

import os
import logging
from datetime import datetime
from typing import Dict, Any

import pdfkit
from jinja2 import Environment, FileSystemLoader, Template

logger = logging.getLogger(__name__)


class PDFEngine:
    """Engine para geração de PDFs a partir de templates HTML."""
    
    def __init__(self, templates_dir: str = "/app/templates"):
        """
        Inicializa engine de PDF.
        
        Args:
            templates_dir: Diretório com templates HTML
        """
        self.templates_dir = templates_dir
        self._setup_jinja_env()
        self._setup_wkhtmltopdf_options()
    
    def _setup_jinja_env(self) -> None:
        """Configura ambiente Jinja2 para templates."""
        try:
            self.jinja_env = Environment(
                loader=FileSystemLoader(self.templates_dir),
                autoescape=True,  # Segurança contra XSS
                trim_blocks=True,
                lstrip_blocks=True
            )
            logger.debug(f"✅ Jinja2 configurado com templates em: {self.templates_dir}")
            
        except Exception as e:
            logger.error(f"❌ Erro ao configurar Jinja2: {e}")
            raise
    
    def _setup_wkhtmltopdf_options(self) -> None:
        """Configura opções padrão do wkhtmltopdf."""
        self.pdf_options = {
            # Formato da página
            'page-size': 'A4',
            'orientation': 'Portrait',
            
            # Margens
            'margin-top': '0.75in',
            'margin-right': '0.75in',
            'margin-bottom': '0.75in',
            'margin-left': '0.75in',
            
            # Codificação e qualidade
            'encoding': 'UTF-8',
            'no-outline': None,
            'enable-local-file-access': None,
            
            # Otimizações para relatórios
            'print-media-type': None,
            'disable-smart-shrinking': None,
            'zoom': 1.0,
            
            # Headers/Footers desabilitados (usamos no HTML)
            'disable-external-links': None,
            'disable-internal-links': None
        }
    
    def render_template(self, template_name: str, context: Dict[str, Any]) -> str:
        """
        Renderiza template HTML com contexto.
        
        Args:
            template_name: Nome do arquivo de template
            context: Dados para o template
            
        Returns:
            HTML renderizado como string
        """
        try:
            template = self.jinja_env.get_template(template_name)
            
            # Adicionar funções auxiliares ao contexto
            enhanced_context = self._enhance_context(context)
            
            html_content = template.render(**enhanced_context)
            logger.debug(f"✅ Template {template_name} renderizado")
            
            return html_content
            
        except Exception as e:
            logger.error(f"❌ Erro ao renderizar template {template_name}: {e}")
            raise
    
    def _enhance_context(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Adiciona funções auxiliares e dados extras ao contexto.
        
        Args:
            context: Contexto original
            
        Returns:
            Contexto melhorado com funções auxiliares
        """
        enhanced = context.copy()
        
        # Adicionar timestamp de geração se não existir
        if 'generation_timestamp' not in enhanced:
            enhanced['generation_timestamp'] = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        
        # Calcular percentuais para distribuição horária se necessário
        if 'hourly_data' in enhanced and enhanced['hourly_data']:
            total_orders = sum(h['orders_count'] for h in enhanced['hourly_data'])
            for hour_data in enhanced['hourly_data']:
                if total_orders > 0:
                    percentage = (hour_data['orders_count'] / total_orders) * 100
                else:
                    percentage = 0
                hour_data['percentage'] = percentage
        
        # Adicionar funções auxiliares
        enhanced['format_currency'] = lambda value: f"R$ {value:.2f}"
        enhanced['format_percentage'] = lambda value: f"{value:.1f}%"
        
        return enhanced
    
    def generate_pdf(self, html_content: str, output_path: str, 
                    custom_options: Dict[str, Any] = None) -> int:
        """
        Gera PDF a partir de conteúdo HTML.
        
        Args:
            html_content: HTML renderizado
            output_path: Caminho de saída do PDF
            custom_options: Opções personalizadas do wkhtmltopdf
            
        Returns:
            Tamanho do arquivo PDF em bytes
        """
        try:
            # Combinar opções padrão com personalizadas
            options = self.pdf_options.copy()
            if custom_options:
                options.update(custom_options)
            
            # Garantir que diretório de saída existe
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            # Gerar PDF
            logger.info(f"🔄 Gerando PDF: {output_path}")
            pdfkit.from_string(html_content, output_path, options=options)
            
            # Verificar se arquivo foi criado e obter tamanho
            if os.path.exists(output_path):
                file_size = os.path.getsize(output_path)
                logger.info(f"✅ PDF gerado com sucesso: {file_size / 1024:.1f} KB")
                return file_size
            else:
                raise FileNotFoundError(f"PDF não foi criado: {output_path}")
                
        except Exception as e:
            logger.error(f"❌ Erro ao gerar PDF: {e}")
            raise
    
    def generate_from_template(self, template_name: str, context: Dict[str, Any], 
                              output_path: str, custom_options: Dict[str, Any] = None) -> int:
        """
        Gera PDF diretamente a partir de template.
        
        Args:
            template_name: Nome do template HTML
            context: Dados para o template
            output_path: Caminho de saída do PDF
            custom_options: Opções personalizadas do wkhtmltopdf
            
        Returns:
            Tamanho do arquivo PDF em bytes
        """
        # Renderizar template
        html_content = self.render_template(template_name, context)
        
        # Gerar PDF
        return self.generate_pdf(html_content, output_path, custom_options)
    
    def validate_template(self, template_name: str) -> bool:
        """
        Valida se template existe e está acessível.
        
        Args:
            template_name: Nome do template a validar
            
        Returns:
            True se template válido, False caso contrário
        """
        try:
            self.jinja_env.get_template(template_name)
            return True
        except Exception as e:
            logger.error(f"❌ Template inválido {template_name}: {e}")
            return False
    
    def get_available_templates(self) -> list:
        """
        Lista templates disponíveis no diretório.
        
        Returns:
            Lista de nomes de templates disponíveis
        """
        try:
            return self.jinja_env.list_templates(extensions=['html', 'htm'])
        except Exception as e:
            logger.error(f"❌ Erro ao listar templates: {e}")
            return []


def create_pdf_engine(templates_dir: str = None) -> PDFEngine:
    """
    Factory function para criar engine de PDF.
    
    Args:
        templates_dir: Diretório de templates (opcional)
        
    Returns:
        Instância configurada de PDFEngine
    """
    if templates_dir is None:
        # Detectar diretório de templates automaticamente
        current_dir = os.path.dirname(os.path.abspath(__file__))
        templates_dir = os.path.join(os.path.dirname(current_dir), 'templates')
    
    engine = PDFEngine(templates_dir)
    
    # Validar se diretório existe
    if not os.path.exists(templates_dir):
        logger.warning(f"⚠️ Diretório de templates não encontrado: {templates_dir}")
    
    return engine