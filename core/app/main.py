import time

from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

from api import menu, submenu, dishe

app = FastAPI()
app.include_router(menu.router)
app.include_router(submenu.router)
app.include_router(dishe.router)

time.sleep(10)

register_tortoise(
    app,
    db_url="postgres://dz1user:pgdz1pswrd@postgres_container:5432/dz1",
    # db_url="sqlite://db.sqlite",
    modules={'models': ['models']},
    generate_schemas=True,
    add_exception_handlers=True
)
