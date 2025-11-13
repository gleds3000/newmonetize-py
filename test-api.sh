# 1️⃣ Cotação Simples: USD -> BRL
curl -X GET "https://seu-api-gateway-url/exchange?from=USD&to=BRL" \
  -H "Content-Type: application/json"

# 2️⃣ Cotação: USD -> EUR
curl -X GET "https://seu-api-gateway-url/exchange?from=USD&to=EUR" \
  -H "Content-Type: application/json"

# 3️⃣ Múltiplas Cotações
curl -X GET "https://seu-api-gateway-url/exchange/multiple?from=USD" \
  -H "Content-Type: application/json"

# 4️⃣ Cotação: BRL -> USD
curl -X GET "https://seu-api-gateway-url/exchange?from=BRL&to=USD" \
  -H "Content-Type: application/json"

# 5️⃣ Requisição POST com JSON
curl -X POST "https://seu-api-gateway-url/exchange" \
  -H "Content-Type: application/json" \
  -d '{"from": "USD", "to": "BRL"}'

# 6️⃣ Teste de Erro - Par não suportado
curl -X GET "https://seu-api-gateway-url/exchange?from=XYZ&to=ABC" \
  -H "Content-Type: application/json"
