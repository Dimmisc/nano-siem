import os
import threading
import time
import socket
import json
import requests
# здесь мы инициализируем токен агента (его в идеале стоит проверять на эндпоинтах SOC) и url SOC
AGENT_TOKEN = os.environ.get("AGENT_TOKEN", "web_agent1")
SOC_URL = os.environ.get("SOC_URL", "http://localhost:8081/api2/logs")

HOSTNAME = socket.gethostname()

# здесь указываем какие файлы мы хотим мониторить (nginx-логи и ssh-логи))
files = [
    {"path": "/var/log/target/access.log", "source": "nginx"},
    {"path": "/var/log/target_ssh/auth.log", "source": "ssh"}
]

FILES = json.loads(os.environ.get("FILES", json.dumps(files)))

BATCH_SIZE = 50

BATCH_INTERVAL = 5

# эта функция отправляет список логов на эндпоинты SOC (делает три попытки в случае ошибки)


def send_batch(source: str, batch_list: list[str]):
    payload = {
        "hostname": HOSTNAME,
        "source": source,
        "logs": batch_list
    }
    headers = {"X-Agent-Token": AGENT_TOKEN}
    for attempt in range(3):
        try:
            response = requests.post(SOC_URL, json=payload, headers=headers)
            response.raise_for_status()
            print(f"Sent a batch type {source} with {len(batch_list)} logs")
            return
        except requests.exceptions.RequestException as e:
            print(
                f"Error sending batch type {source}: {e}. Attempt {attempt+1}/3")
            time.sleep(2)
    print(
        f"Failed to send batch type {source} after 3 attempts. Dropping {len(batch_list)} logs.")

# эта функция читает файл логов и формирует батчи (список логов) для отправки на эндпоинты SOC. Мы используем батчи, чтобы запрос не был слишком большим и не перегружал сеть.


def tail_file(file_path: str, source: str):
    batch_list = []
    last_batch_flush = time.time()
    while not os.path.exists(file_path):
        print(
            f"File {file_path} does not exist. Waiting for it to be created...")
        time.sleep(5)
    cur_pos = 0
    with open(file_path, "r") as f:
        f.seek(cur_pos)
        # цикл читает построчно файл логов, если есть лог, то добавляем в список, если нет, то проверяем, не был лли перезаписан файл (например, при ротации логов)
        while True:
            line = f.readline()
            if line:
                batch_list.append(line.strip())
            else:
                cur_file_size = os.path.getsize(file_path)
                if cur_file_size < f.tell():
                    print(
                        f"File {file_path} was truncated. Resetting position to 0.")
                    f = open(file_path, "r")
                    f.seek(0)

            is_flush_time = (
                # если прошёл определённый интервал времени или размер батча достиг определённого значения, то отправляем батч на эндпоинт SOC
                time.time()-last_batch_flush) >= BATCH_INTERVAL or len(batch_list) >= BATCH_SIZE
            if is_flush_time and batch_list:
                send_batch(source, batch_list)
                batch_list = []
                last_batch_flush = time.time()
            time.sleep(0.1)
            continue

# в основной функции мы создаём два потока: один для чтения логов nginx, другой - для чтения логов ssh.


def main():
    threads = [threading.Thread(target=tail_file, args=(
        file["path"], file["source"])) for file in FILES]
    for thread in threads:
        thread.start()
    print("Agent started. Tailing files...")
    try:
        while (True):
            time.sleep(1)
    except KeyboardInterrupt:
        print("Agent stopped by user.")


if __name__ == "__main__":
    main()
