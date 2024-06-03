#!/bin/bash

echo "Content-Type: text/plain"
echo "Set-Cookie: session=authenticated; Path=/; Max-Age=3600" # Simula o cookie de autenticação
echo ""
echo "Cookie de autenticação definido com sucesso."

