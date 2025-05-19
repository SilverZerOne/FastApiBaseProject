# Usa una imagen base de Python
FROM python:3.9-slim

# Establece el directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Instalar Poetry
ENV POETRY_HOME=/opt/poetry
ENV POETRY_VERSION=1.5.1
ENV PATH="/opt/poetry/bin:$PATH"
RUN curl -sSL https://install.python-poetry.org | python3 - && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

# Copia los archivos de Poetry
COPY pyproject.toml poetry.lock* ./

# Instala las dependencias con Poetry
RUN poetry install --no-interaction --no-ansi --no-root

# Copia el código de la aplicación
COPY . .

# Expone el puerto que utilizará FastAPI
EXPOSE 8000

# Comando para ejecutar la aplicación
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
