import os
import sentry_sdk
from fastapi import FastAPI
from dotenv import load_dotenv
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware
from app.item.router import router as item_router
from app.product.router import router as product_router

# Carga las variables de entorno desde el archivo .env
load_dotenv()

# Obtén el DSN de Sentry desde las variables de entorno
sentry_dsn = os.getenv("SENTRY_DSN")

app = FastAPI()

# Inicializa Sentry solo si el DSN está presente
if sentry_dsn:
    sentry_sdk.init(
        dsn=sentry_dsn,
        traces_sample_rate=1.0  # Ajusta el muestreo de trazas según tus necesidades
    )
    app.add_middleware(SentryAsgiMiddleware)

# Incluye los routers
app.include_router(item_router)
app.include_router(product_router)
