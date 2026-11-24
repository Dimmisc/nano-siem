#!/bin/sh
# Комбинированный сценарий: nikto -> sqlmap -> hydra, по очереди,
# с паузами между шагами, чтобы на дашборде было видно, как алерты

set -e

TARGET_HOST="${TARGET_HOST:-127.0.0.1}"
TARGET_PORT="${TARGET_PORT:-8080}"          
TARGET_SSH_PORT="${TARGET_SSH_PORT:-2222}"
SSH_USER="${SSH_USER:-test_user}"             
WORDLIST="${WORDLIST:-wordlists/wrong_passwords.txt}"

BASE_URL="http://${TARGET_HOST}:${TARGET_PORT}"

echo "======================================================"
echo " Комбинированная атака: ${BASE_URL} и SSH :${TARGET_SSH_PORT}"
echo "======================================================"

echo
echo "--- Шаг 1/3: сканирование путей и конфигурации (nikto) ---"
perl nikto/program/nikto.pl -h "${BASE_URL}" -Tuning 1237b -maxtime 60s || true
sleep 5

echo
echo "--- Шаг 2/3: SQL-инъекция в поиске (sqlmap) ---"
sqlmap -u "${BASE_URL}/api/login" \
  --data="login=admin&password=123456" \
  --batch --level=1 --risk=1 --technique=U --skip-heuristics --ignore-code=403,401 || true
sleep 5

echo
echo "--- Шаг 3/3: перебор пароля по SSH (hydra) ---"
hydra -l "${SSH_USER}" -P "${WORDLIST}" -t 4 -w 5 \
  "ssh://${TARGET_HOST}:${TARGET_SSH_PORT}" || true

echo
echo "======================================================"
echo " Готово. Проверить алерты: /var/log/target/access.log /var/log/target_ssh/auth.log"
echo "======================================================"

