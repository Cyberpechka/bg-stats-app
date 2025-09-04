<!-- Название проекта -->
# 🎲 BoardGame Stats

<!-- Краткое описание - что это и для кого -->
Веб-приложение для учета результатов и статистики в настольных играх. Создано для того, чтобы папа и его друзья могли отслеживать свои победы и составлять рейтинги.

<!-- Иконки стека технологий - это визуально выделяет проект. Можно сгенерировать на shields.io -->
## 🛠 Технологии

**Клиент (Фронтенд):** ![HTML5](https://img.icons8.com/?size=100&id=20909&format=png&color=000000) ![CSS3](https://img.icons8.com/?size=100&id=21278&format=png&color=000000) ![JavaScript](https://img.icons8.com/?size=100&id=108784&format=png&color=000000)

**Сервер (Бэкенд):** ![Python](https://img.icons8.com/?size=100&id=l75OEUJkPAk4&format=png&color=000000) [<img src="https://icon.icepanel.io/Technology/svg/FastAPI.svg" width="90" height="130" alt="FastAPI" style="filter: invert(0%)" />](https://fastapi.tiangolo.com/)
 [![PostgreSQL](https://img.icons8.com/?size=100&id=JRnxU7ZWP4mi&format=png&color=000000)](https://www.postgresql.org/)

**Тестирование:** [<img src="https://icon.icepanel.io/Technology/svg/pytest.svg" width="90" height="130" alt="FastAPI" style="filter: invert(0%)" />](https://fastapi.tiangolo.com/)

---

<!-- Самая важная часть - как всё запустить. Расписано по шагам. -->
## 🚀 Быстрый старт (Для разработчиков)

Это руководство поможет вам запустить полную копию проекта на вашем локальном компьютере для разработки и тестирования.

### Предварительные требования

Убедитесь, что на вашем компьютере установлены:
*   Python 3.10+
*   `pip` (менеджер пакетов Python)
*   Git

### 1. Клонирование репозитория

```bash
# Клонируйте репозиторий к себе на компьютер
git clone https://github.com/BoardGameStats/bg-stats-app.git

# Перейдите в созданную папку проекта
cd bg-stats-app
```

### 2. Запуск бэкенда (FastAPI сервер)
```bash
Откройте первый терминал и выполните:

bash
cd backend

# Создаем виртуальное окружение
python -m venv venv

# Активируем виртуальное окружение
# Для Linux/macOS:
source venv/bin/activate
# Для Windows:
venv\Scripts\activate

# Устанавливаем зависимости
pip install -r requirements.txt

# Запускаем сервер
uvicorn app.main:app --reload
```

Бэкенд запущен! Доступен по адресу: http://localhost:8000
Документация API (Swagger): http://localhost:8000/docs

### 3. Запуск фронтенда
```bash
Откройте второй терминал (не закрывая первый) и выполните:

bash
cd frontend

# Запускаем встроенный HTTP-сервер
python -m http.server 3000
```
Фронтенд запущен! Доступен по адресу: http://localhost:3000

### 📁 Структура проекта
```bash
text
bg-stats-app/
├── backend/                 # Исходный код бэкенда (FastAPI)
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py         # Главный файл, создание приложения и эндпоинтов
│   │   ├── models.py       # Модели SQLAlchemy для работы с БД
│   │   └── database.py     # Настройка подключения к базе данных
│   ├── requirements.txt    # Список зависимостей Python
│   └── tests/              # Папка для тестов (Pytest)
├── frontend/               # Исходный код фронтенда
│   ├── index.html          # Главная страница
│   ├── styles.css          # Стили
│   ├── script.js           # Логика (JavaScript с fetch-запросами к API)
│   └── assets/             # Папка для изображений
└── README.md               # Этот файл
```

### 🧪 Тестирование
```bash
Для запуска тестов бэкенда:
bash
cd backend
pytest
```

### 🤝 Как внести свой вклад?
```bash
Создайте форк (Fork) репозитория

Создайте feature-ветку (git checkout -b feature/AmazingFeature)

Сделайте коммит изменений (git commit -m 'feat: Add AmazingFeature')

Запушьте ветку (git push origin feature/AmazingFeature)

Откройте Pull Request

Используем Conventional Commits
```

### 👨‍💻 Участники проекта
```bash
Клочко Тимофей - Backend Developer (FastAPI, ML)

Рыженко Егор - Frontend Developer (JavaScript, HTML, CSS)

Кузнецов Александр - Team Lead, Testing & DevOps
```

### 📄 Лицензия
```bash
Этот проект распространяется под лицензией MIT. См. файл LICENSE для подробностей.
```

### 🙏 Благодарности
```bash
Особая благодарность нашему главному тестировщику и вдохновителю — папе! 🎯
```