from pathlib import Path
from typing_extensions import Annotated

from fastapi import Body, FastAPI, Form, HTTPException, Query
from fastapi.staticfiles import StaticFiles

from settings import settings

BASE_DIR = Path(__file__).parent

app = FastAPI(title="Login target")

# пока здесь один эндпоинт-заглушка, который сверяет переданный логи и пароль с локальнйо записью из файла .env.example
# скоро добавим полноценную бд для sql-уязвимостей


@app.post("/api/login")
def login(
    login: str = Form(min_length=1),
    password: str = Form(min_length=1),
) -> dict[str, str]:
    if login != settings.USER_LOGIN or password != settings.USER_PASS:
        raise HTTPException(
            status_code=401, detail="Неверный логин или пароль")

    return {"message": "Вход выполнен успешно"}


app2 = FastAPI(title="Logs target")


@app2.post("/api2/logs")
def log_parser(hostname: Annotated[str, Body()], source: Annotated[str, Body()], logs: list[str]):
    if source == "nginx":
        with open(BASE_DIR / "static" / "nginx_logs.txt", "a") as f:
            for log in logs:
                f.write(f"{hostname} {log}\n")
    else:
        with open(BASE_DIR / "static" / "ssh_logs.txt", "a") as f:
            for log in logs:
                f.write(f"{hostname} {log}\n")
    return {"message": "Логи успешно записаны"}


# скоро будем использовать для сканирования уязвимостей
app.mount("/", StaticFiles(directory=BASE_DIR /
          "static", html=True), name="static")
