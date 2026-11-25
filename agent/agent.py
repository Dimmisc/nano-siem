import os
import threading
import time
import socket
import json
import requests
import signal
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
stop_event = threading.Event()
# эта функция отправляет список логов на эндпоинты SOC (делает три попытки в случае ошибки)


class FileOffsets:
    def __init__(self, base_dir):
        self._path = base_dir
        self._lock = threading.Lock()
        self._data: dict[str, int] = {}
        try:
            with open(self._path, "r") as f:
                self._data = json.load(f)
        except Exception as e:
            print(
                f"Error loading offsets from {self._path}: {e}. Starting with empty offsets.")
            self._data = {}

    def get_offset(self, file_path: str) -> int:
        with self._lock:
            return self._data.get(file_path, 0)

    def set_offset(self, file_path: str, offset: int):
        with self._lock:
            self._data[file_path] = offset
            try:
                with open(self._path, "w") as f:
                    json.dump(self._data, f)
            except Exception as e:
                print(f"Error saving offsets to {self._path}: {e}.")


file_offsets = FileOffsets("file_offsets.json")


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
    while not os.path.exists(file_path) and stop_event.is_set() == False:
        print(
            f"File {file_path} does not exist. Waiting for it to be created...")
        time.sleep(5)
    cur_pos = file_offsets.get_offset(file_path)
    if (stop_event.is_set()):
        return
    with open(file_path, "r") as f:
        f.seek(cur_pos)
        # цикл читает построчно файл логов, если есть лог, то добавляем в список, если нет, то проверяем, не был лли перезаписан файл (например, при ротации логов)
        while stop_event.is_set() == False:
            line = f.readline()
            if line:
                batch_list.append(line.strip())

            else:
                '''код для случая ротации логов'''
            #     cur_file_size = os.path.getsize(file_path)
            #     if cur_file_size < f.tell():
            #         print(
            #             f"File {file_path} was truncated. Resetting position to 0.")
            #         f = open(file_path, "r")
            #         f.seek(0)
            #         file_offsets.set_offset(file_path, f.tell())

                is_flush_time = (
                    # если прошёл определённый интервал времени, то отправляем батч на эндпоинт SOC (даже если не превышен BATCH_SIZE)
                    time.time()-last_batch_flush) >= BATCH_INTERVAL
                if is_flush_time and batch_list:
                    send_batch(source, batch_list)
                    file_offsets.set_offset(file_path, f.tell())
                    batch_list = []
                    last_batch_flush = time.time()

            # если превышен размер батча, то отправляем батч на эндпоинт SOC
            if len(batch_list) >= BATCH_SIZE:
                send_batch(source, batch_list)
                file_offsets.set_offset(file_path, f.tell())
                batch_list = []
                last_batch_flush = time.time()

            time.sleep(0.1)
            continue

        if batch_list:
            send_batch(source, batch_list)
            file_offsets.set_offset(file_path, f.tell())


def event_handler(signum, frame):
    print(f"Received signal {signum}. Sending remaining logs and exiting...")
    stop_event.set()

# в основной функции мы создаём два потока: один для чтения логов nginx, другой - для чтения логов ssh.


def main():
    signal.signal(signal.SIGTERM, event_handler)
    signal.signal(signal.SIGINT, event_handler)
    threads = [threading.Thread(target=tail_file, args=(
        file["path"], file["source"])) for file in FILES]
    for thread in threads:
        thread.start()
    print("Agent started. Tailing files...")


if __name__ == "__main__":
    main()
