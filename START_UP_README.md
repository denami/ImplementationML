# START_UP — запуск проекта

## 1. Требования

Для запуска проекта необходимо установить:

* Python 3.12+
* Git
* Docker
* Docker Compose

Проверка:

```bash
python --version
git --version
docker --version
docker compose version
```

---

# 2. Клонирование проекта

```bash
git clone <GITHUB_REPOSITORY_URL>
cd <PROJECT_DIRECTORY>
```

---

# 3. Создание виртуального окружения

Создаём виртуальное окружение:

```bash
python -m venv .venv
```

Активируем его.

### Linux / macOS

```bash
source .venv/bin/activate
```

### Windows

```powershell
.venv\Scripts\activate
```

После активации в терминале должно отображаться:

```text
(.venv)
```

---

# 4. Установка зависимостей

Устанавливаем зависимости проекта:

```bash
pip install -r requirements.txt
```

При необходимости обновить `pip`:

```bash
python -m pip install --upgrade pip
```

---

# 5. Получение датасета

Для обучения используется:

**Default of Credit Card Clients Dataset**

Источник:

https://www.kaggle.com/datasets/uciml/default-of-credit-card-clients-dataset

Данные могут загружаться программно через Kaggle API.

Для этого необходимо настроить Kaggle credentials в переменных окружения.

Пример:

```bash
export KAGGLE_USERNAME="your_username"
export KAGGLE_KEY="your_api_key"
```

В Windows PowerShell:

```powershell
$env:KAGGLE_USERNAME="your_username"
$env:KAGGLE_KEY="your_api_key"
```

Загрузка Dataset

```bash
python -m models.download_data
```

Dataset будет сохранен в директории `data/raw`

---

# 6. Обучение модели

После установки зависимостей и получения датасета запускается обучение:

```bash
python -m models.train_model
```

В результате выполняется обучение `LogisticRegression` и выводятся основные метрики:

```text
Accuracy:  0.8077
Precision: 0.6868
Recall:    0.2396
F1:        0.3553
ROC-AUC:   0.7076
```

Обученная модель сохраняется в:

```text
models/model_v1.joblib
```

---

# 7. Проверка загрузки модели

Для проверки функции загрузки модели:

```bash
python -m models.test_inference
```

Пример результата:

```text
Prediction: 1
Default probability: 0.5112
```

---

# 8. Запуск Flask API локально

Запуск сервиса:

```bash
python -m app.api
```

После запуска API доступно по адресу:

```text
http://localhost:5000
```

---

# 9. Проверка Health endpoint

В отдельном терминале:

```bash
curl http://localhost:5000/health
```

Ожидаемый ответ:

```json
{
  "status": "ok",
  "model": "v1"
}
```

---

# 10. Проверка Prediction API

Endpoint:

```text
POST /predict
```

Пример запроса:

```bash
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "LIMIT_BAL": 20000,
    "SEX": 2,
    "EDUCATION": 2,
    "MARRIAGE": 2,
    "AGE": 24,
    "PAY_0": 2,
    "PAY_2": 2,
    "PAY_3": -1,
    "PAY_4": -1,
    "PAY_5": -2,
    "PAY_6": -2,
    "BILL_AMT1": 3913,
    "BILL_AMT2": 3102,
    "BILL_AMT3": 689,
    "BILL_AMT4": 0,
    "BILL_AMT5": 0,
    "BILL_AMT6": 0,
    "PAY_AMT1": 0,
    "PAY_AMT2": 689,
    "PAY_AMT3": 0,
    "PAY_AMT4": 0,
    "PAY_AMT5": 0,
    "PAY_AMT6": 0
  }'
```

Пример ответа:

```json
{
  "default_probability": 0.4765,
  "model_version": "v1",
  "prediction": 0
}
```

Где:

* `default_probability` — вероятность дефолта;
* `prediction` — итоговый прогноз модели (`0` или `1`);
* `model_version` — версия используемой модели.

---

# 15. Структура проекта

```text
credit-default-ml/
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── README.md
├── START_UP_README.md
├── ARCHITECTURE.md
│
├── docker/
│   └── nginx.conf
│
├── models/
│   ├── model_v1.joblib
│   ├── model_loader.py
│   ├── train_model.py
│   └── test_inference.py
│
├── src/
│   ├── __init__.py
│   └── app.py
│
├── tests/
│
├── notebooks/
│
└── data/
```

---

# 16. Быстрый запуск

Если модель уже обучена и `model_v1.joblib` присутствует в репозитории:

```bash
git clone <GITHUB_REPOSITORY_URL>
cd <PROJECT_DIRECTORY>

python -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt

python -m src.app
```

Для запуска через Docker:

```bash
docker build -t credit-default-api:v1 .
docker run --rm -p 5000:5000 credit-default-api:v1
```

Для запуска через Docker Compose:

```bash
docker compose up --build
```

После этого сервис доступен через:

```text
http://localhost:8080
```

---

# 17. Проверка проекта

Минимальная последовательность проверки:

```bash
# 1. Проверить Python
python --version

# 2. Установить зависимости
pip install -r requirements.txt

# 3. Проверить модель
python -m models.test_inference

# 4. Запустить API
python -m src.app

# 5. Проверить health
curl http://localhost:5000/health

# 6. Проверить prediction
curl -X POST http://localhost:5000/predict ...
```

После этого проект готов к контейнеризации и дальнейшему A/B-тестированию моделей.
