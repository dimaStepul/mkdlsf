#!/bin/bash

HOST="vk.com"

echo -e "=== TLS Handshake ===\n"
openssl s_client -connect $HOST:443

echo -e "\n=== Certificate ===\n"
echo | openssl s_client -showcerts -servername $HOST -connect $HOST:443 2>/dev/null | openssl x509 -text -noout
