# 1. Сборка Docker image

Сборка Docker-образа:

```bash
docker build -t credit-default-api:v1 .
```

Проверка:

```bash
docker images | grep credit-default-api
```

---

# 2. Запуск Docker-контейнера

```bash
docker run --rm -p 5000:5000 credit-default-api:v1
```

После запуска сервис доступен:

```text
http://localhost:5000
```

Проверка:

```bash
curl http://localhost:5000/health
```

И затем можно выполнить запрос:

```bash
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{ ... }'
```

---

# 3. Docker Compose

Проект также содержит:

```text
docker-compose.yml
```

Compose запускает ML-сервис и NGINX.

Запуск:

```bash
docker compose up --build
```

Архитектура:

```text
Client
  |
  v
NGINX :8080
  |
  v
ML Service :5000
  |
  v
LogisticRegression
```

После запуска API доступно через:

```text
http://localhost:8080
```

Проверка:

```bash
curl http://localhost:8080/health
```

Остановка:

```bash
docker compose down
```

Просмотр логов:

```bash
docker compose logs
```

Логи ML-сервиса:

```bash
docker compose logs ml-service
```

Логи NGINX:

```bash
docker compose logs nginx
```

---

# 4. Docker Hub

После сборки образ можно загрузить в Docker Hub.

Авторизация:

```bash
docker login
```

Добавление Docker Hub tag:

```bash
docker tag credit-default-api:v1 <DOCKERHUB_USERNAME>/credit-default-api:v1
```

Загрузка:

```bash
docker push <DOCKERHUB_USERNAME>/credit-default-api:v1
```

После публикации образ можно получить командой:

```bash
docker pull <DOCKERHUB_USERNAME>/credit-default-api:v1
```

Docker Hub:

```text
https://hub.docker.com/r/<DOCKERHUB_USERNAME>/credit-default-api
```

---

