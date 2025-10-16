#!/bin/bash

DOMAIN="cidadedasrosas"
TOKEN="8e9ff8f2-893e-40a7-8d99-082845aa5b27"
LOG_DIR="/opt/PI02-v4/duckdns"
LOG_FILE="$LOG_DIR/duck.log"

# Criar diretório de log se não existir
mkdir -p "$LOG_DIR"

# Registrar data/hora
echo "=== $(date) ===" >> "$LOG_FILE"

# Atualizar DuckDNS
RESPONSE=$(curl -s -w "\n%{http_code}" "https://www.duckdns.org/update?domains=$DOMAIN&token=$TOKEN&ip=")
HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
RESPONSE_CONTENT=$(echo "$RESPONSE" | head -n1)

echo "HTTP Code: $HTTP_CODE" >> "$LOG_FILE"
echo "Response: $RESPONSE_CONTENT" >> "$LOG_FILE"

# Verificar se foi bem-sucedido
if [ "$HTTP_CODE" -eq 200 ] && [ "$RESPONSE_CONTENT" = "OK" ]; then
    echo "SUCCESS: DuckDNS updated successfully" >> "$LOG_FILE"
    exit 0
else
    echo "ERROR: Failed to update DuckDNS" >> "$LOG_FILE"
    exit 1
fi
