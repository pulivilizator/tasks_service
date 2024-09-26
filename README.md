## Проект бота для управления задачами.


#### Запуск проекта:
Для запуска клонируйте репозиторий и укажите в `docker compose` файле свой токен бота в переменной окружения,
так же измените в сервисе `todos` переменную окружения TG_ID на свой телеграм id(узнать его можно например [тут](https://t.me/getmyid_bot)).
Там же можете изменить пароль суперпользователя для доступа в админку джанго.

После запуска документацию api вы сможете найти на http://127.0.0.1:8000/docs и http://127.0.0.1:8001/docs 
для DRF и FastAPI соответственно

---

#### Реализация:

Реализовано три основных сервиса работающих независимо друг от друга и связанных через API:
- Сервис комментариев на FastAPI для хранения, управления, кэширования комментариев.
- Сервис на Django/DRF для управления задачами и авторизации запросов.
- Сервис бота для предоставления клиента пользователю с использованием aiogram, aiogram-dialog минимизирующий запросы к бэкенду и управляющий диалоговыми окнами.

Есть возможность взаимодействия как через http api, так и через бота.
При первом запросе бот создает пользователю профиль в БД без пароля, такой пользователь не может пользоваться api вне бота.
При запросах через http необходимо зарегистрироваться и использовать access токен для запросов.
Для регистрации необходимо уже быть пользователем бота,
после указания id и пароля при регистрации бот отправит подтверждение вам в телеграм.
Для передачи данных от джанги к боту я не стал тащить брокер, а решил использовать pubsub редиса, т.к там всего одна задача.

Сервис комментариев и сам бот так же авторизуются на бэкенде джанги, но использую для этого связку ключей private и public key.

---

#### Основные трудности:

Основные проблемы у меня были связаны с реализацией авторизации пользователя на стороне Джанги и минимизацией запросов со стороны бота.

Первую проблему я решил созданием модели пользователя с необязательным паролем и реализацией своей системы аутентификации и авторизации запросов с использованием связки ключей для своих сервисов и jwt токенов для стороних запросов.

Вторую проблему решил использованием пайдантика в боте, храня и изменяя списки данных в виде json в dialog_data бота, что позволило не делать повторные запросы для их получения с сервера.