from pathlib import Path

from fastapi import FastAPI, Form, HTTPException, Query
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


# скоро будем использовать для сканирования уязвимостей
app.mount("/", StaticFiles(directory=BASE_DIR /
          "static", html=True), name="static")
