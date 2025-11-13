import json
import logging
import boto3
from datetime import datetime
from decimal import Decimal

# Configurar CloudWatch Logs
logger = logging.getLogger()
logger.setLevel(logging.INFO)

class MonetizedApiLogic:
    """
    Classe que contém a lógica da API monetizada de cotação de câmbio.
    Retorna cotações de dólar em tempo real.
    """
    
    def __init__(self):
        self.logger = logger
        self.cloudwatch = boto3.client('logs')
    
    def get_exchange_rate(self, currency_from: str = "USD", currency_to: str = "BRL") -> dict:
        """
        Obtém a cotação de câmbio entre duas moedas.
        
        Args:
            currency_from: Moeda de origem (padrão: USD)
            currency_to: Moeda de destino (padrão: BRL)
        
        Returns:
            dict: Contendo a cotação e metadados
        """
        try:
            self.logger.info(f"Buscando cotação: {currency_from} -> {currency_to}")
            
            # Simulando dados de cotação (em produção, usar API real como Alpha Vantage, Open Exchange Rates, etc)
            exchange_rates = {
                ("USD", "BRL"): 5.15,
                ("USD", "EUR"): 0.92,
                ("USD", "GBP"): 0.79,
                ("BRL", "USD"): 0.19,
            }
            
            key = (currency_from, currency_to)
            if key in exchange_rates:
                rate = exchange_rates[key]
                response = {
                    "status": "success",
                    "from": currency_from,
                    "to": currency_to,
                    "rate": rate,
                    "timestamp": datetime.utcnow().isoformat(),
                    "source": "MonetizedApiLogic"
                }
                self.logger.info(f"Cotação obtida com sucesso: {rate}")
                return response
            else:
                self.logger.warning(f"Par de moedas não suportado: {currency_from}/{currency_to}")
                return {
                    "status": "error",
                    "message": f"Par de moedas não suportado: {currency_from}/{currency_to}"
                }
        
        except Exception as e:
            self.logger.error(f"Erro ao obter cotação: {str(e)}")
            return {
                "status": "error",
                "message": f"Erro ao processar requisição: {str(e)}"
            }
    
    def get_multiple_rates(self, currency_from: str = "USD") -> dict:
        """
        Obtém cotações de múltiplos pares de moedas.
        
        Args:
            currency_from: Moeda de origem (padrão: USD)
        
        Returns:
            dict: Contendo múltiplas cotações
        """
        try:
            self.logger.info(f"Buscando múltiplas cotações para: {currency_from}")
            
            rates = {
                "BRL": 5.15,
                "EUR": 0.92,
                "GBP": 0.79
            }
            
            response = {
                "status": "success",
                "from": currency_from,
                "rates": rates,
                "timestamp": datetime.utcnow().isoformat()
            }
            self.logger.info("Múltiplas cotações obtidas com sucesso")
            return response
        
        except Exception as e:
            self.logger.error(f"Erro ao obter múltiplas cotações: {str(e)}")
            return {
                "status": "error",
                "message": f"Erro ao processar requisição: {str(e)}"
            }


def lambda_handler(event, context):
    """
    Handler principal da função Lambda.
    
    Args:
        event: Evento disparado pela API Gateway
        context: Contexto da execução Lambda
    
    Returns:
        dict: Resposta formatada para API Gateway
    """
    logger.info(f"Evento recebido: {json.dumps(event)}")
    
    try:
        # Inicializar a lógica monetizada
        api_logic = MonetizedApiLogic()
        
        # Extrair parâmetros da requisição
        query_params = event.get('queryStringParameters', {}) or {}
        currency_from = query_params.get('from', 'USD')
        currency_to = query_params.get('to', 'BRL')
        
        # Determinar o tipo de requisição
        path = event.get('path', '')
        
        if 'multiple' in path:
            result = api_logic.get_multiple_rates(currency_from)
        else:
            result = api_logic.get_exchange_rate(currency_from, currency_to)
        
        # Formatar resposta
        status_code = 200 if result.get('status') == 'success' else 400
        
        response = {
            'statusCode': status_code,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps(result, default=str)
        }
        
        logger.info(f"Resposta enviada: {json.dumps(response)}")
        return response
    
    except Exception as e:
        logger.error(f"Erro não tratado: {str(e)}")
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({
                'status': 'error',
                'message': 'Erro interno do servidor'
            })
        }
