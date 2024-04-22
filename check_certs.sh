#!/bin/bash

get_certificate_info() {
    local site="$1"
    echo "=== Сертификат для $site ==="
    timeout 7 openssl s_client -showcerts -connect "$site":443 </dev/null 2>/dev/null | \
        openssl x509 -noout -issuer -subject
}

sites_file="BlockingLists/russianWebsites.txt"

while IFS= read -r site || [ -n "$site" ]; do
    get_certificate_info "$site"
done < "$sites_file"
