import json
import requests

def lambda_handler(event, context):
    # Placeholder for the exchange rate API endpoint
    api_url = "https://api.exchangeratesapi.io/latest"
    
    # Log the incoming event
    print("Received event: " + json.dumps(event))

    # Fetch exchange rates
    response = requests.get(api_url)
    if response.status_code != 200:
        return {
            'statusCode': response.status_code,
            'body': json.dumps({'error': 'Failed to retrieve exchange rates'})
        }

    exchange_rates = response.json()

    return {
        'statusCode': 200,
        'body': json.dumps(exchange_rates)
    }