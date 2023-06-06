import sqlite3  # Импорт модуля для работы с базой данных SQLite
import datetime  # Импорт модуля для работы с датой и временем

def start():
    conn = sqlite3.connect('data.db')  # Установка соединения с базой данных SQLite, указывается имя файла базы данных
    cursor = conn.cursor()  # Создание объекта-курсора для выполнения SQL-запросов

    # Создание таблицы "users", если она еще не существует
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users
        (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, password TEXT, email TEXT, role TEXT, signup_date TEXT)
    ''')

    # Создание таблицы "tasks", если она еще не существует
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks
        (id INTEGER PRIMARY KEY AUTOINCREMENT, status TEXT, price REAL, adres TEXT, information TEXT,
        worker_id INTEGER, user_id INTEGER, data_create TEXT, data_deadline TEXT)
    ''')

    # Создание таблицы "comment", если она еще не существует
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS comment
        (id INTEGER PRIMARY KEY, msg TEXT, id_user INTEGER, id_task INTEGER, date TEXT)
    ''')

    conn.commit()  # Применение изменений в базе данных

def register(username, password, email):
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()

    role = "user"  # Установка роли пользователя по умолчанию
    signup_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Получение текущей даты и времени

    # Вставка данных пользователя в таблицу "users"
    cursor.execute('''
        INSERT INTO users (username, password, email, role, signup_date)
        VALUES (?, ?, ?, ?, ?)
    ''', (username, password, email, role, signup_date))

    conn.commit()

def login_info(username):
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()

    # Выполнение запроса SELECT для поиска пользователя с заданным именем
    cursor.execute('SELECT username, email, role, signup_date FROM users WHERE username = ?', (username,))

    result = cursor.fetchone()  # Извлечение результата запроса (первая строка)

    conn.close()

    if result:
        return result[1], result[2], result[3]  # Возвращение информации о пользователе (email, роль, дата регистрации)
    else:
        return None  # Если пользователь не найден, возвращается значение None

def user_exists(username):
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()

    # Выполнение запроса SELECT для поиска пользователя с заданным именем
    cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()  # Извлечение результата запроса (первая строка)

    conn.close()

    if user:
        return True  # Если пользователь существует, возвращается True
    else:
        return False  # Если пользователь не существует, возвращается False
def login(username, password):
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()

    # Выполнение запроса SELECT для поиска пользователя с заданным именем и паролем
    cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
    user = cursor.fetchone()  # Извлечение результата запроса (первая строка)

    conn.close()

    if user:
        return True  # Если пользователь существует, возвращается True
    else:
        return False  # Если пользователь не существует, возвращается False

def get_tasks_by_username_active(username):
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()

    cursor.execute('SELECT id FROM users WHERE username = ?', (username,))
    result = cursor.fetchone()

    if not result:  # Если пользователь с таким именем не найден
        return []

    user_id = result[0]

    cursor.execute('SELECT * FROM tasks WHERE user_id = ? AND status = ?', (user_id, "active"))
    rows = cursor.fetchall()

    conn.close()
    return rows

def get_tasks_by_username_archive(username):
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()

    cursor.execute('SELECT id FROM users WHERE username = ?', (username,))
    result = cursor.fetchone()

    if not result:  # Если пользователь с таким именем не найден
        return []

    user_id = result[0]

    cursor.execute('SELECT * FROM tasks WHERE user_id = ? AND status = ?', (user_id, "archive"))
    rows = cursor.fetchall()

    conn.close()
    return rows

def create_task(username, price, adres, data_deadline, information):
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()

    cursor.execute('SELECT id FROM users WHERE username = ?', (username,))
    result = cursor.fetchone()

    if not result:  # Если пользователь с таким именем не найден
        return []

    user_id = result[0]
    data_create = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute('''
        INSERT INTO tasks (status, price, adres, information, worker_id, user_id, data_create, data_deadline)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', ('active', price, adres, information, None, user_id, data_create, data_deadline))

    conn.commit()
    task_id = cursor.lastrowid
    cursor.close()
    return task_id


def show_user_case_for_user(task_id):
    # Устанавливаем соединение с базой данных
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()

    # Выполняем SQL-запрос для получения данных о задаче с указанным идентификатором
    cursor.execute('SELECT * FROM tasks WHERE id = ?', (task_id,))
    task_data = cursor.fetchone()

    # Закрываем соединение с базой данных и возвращаем полученные данные
    conn.close()
    return task_data


def show_comment(task_id):
    # Устанавливаем соединение с базой данных
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()

    # Выполняем SQL-запрос для получения комментариев, связанных с задачей с указанным идентификатором
    cursor.execute('SELECT * FROM comment WHERE id_task = ?', (task_id,))
    task_data = cursor.fetchall()

    # Закрываем соединение с базой данных и возвращаем полученные данные
    conn.close()
    return task_data


def create_comment(username, idd, text):
    # Устанавливаем соединение с базой данных
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()

    # Выполняем SQL-запрос для получения идентификатора пользователя по его имени
    cursor.execute('''SELECT id FROM users WHERE username = ? ''', (username,))
    result = cursor.fetchone()

    if not result:  # Пользователь с таким именем не найден
        return []

    user_id = result[0]
    data_create = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Вставляем новый комментарий в таблицу comment с указанными данными
    cursor.execute('''
        INSERT INTO comment(msg, id_user, id_task, date)
        VALUES(?, ?, ?, ?)''',
                   (text, user_id, idd, data_create))

    # Фиксируем изменения и закрываем соединение с базой данных
    conn.commit()
    conn.close()


def status(username):
    # Устанавливаем соединение с базой данных
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()

    # Выполняем SQL-запрос для получения роли пользователя по его имени
    cursor.execute('''SELECT role FROM users WHERE username = ? ''', (username,))
    result = cursor.fetchone()

    # Закрываем соединение с базой данных и возвращаем роль пользователя
    conn.close()
    return result[0]


def close_case(username):
    # Устанавливаем соединение с базой данных
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()

    # Выполняем SQL-запрос для получения идентификатора пользователя по его имени
    cursor.execute('''SELECT id FROM users WHERE username = ? ''', (username,))
    result = cursor.fetchone()

    if not result:  # Пользователь с таким именем не найден
        return []

    user_id = result[0]

    # Выполняем SQL-запрос для получения всех задач, связанных с указанным пользователем и статусом "archive"
    cursor.execute('''SELECT * FROM tasks WHERE worker_id = ? AND status = ?''', (user_id, "archive",))
    rows = cursor.fetchall()

    # Закрываем соединение с базой данных и возвращаем полученные задачи
    conn.close()
    return rows


def open_case(username):
    # Устанавливаем соединение с базой данных
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()

    # Выполняем SQL-запрос для получения идентификатора пользователя по его имени
    cursor.execute('''SELECT id FROM users WHERE username = ? ''', (username,))
    result = cursor.fetchone()

    if not result:  # Пользователь с таким именем не найден
        return []

    user_id = result[0]

    # Выполняем SQL-запрос для получения всех задач, связанных с указанным пользователем и статусом "active"
    cursor.execute('''SELECT * FROM tasks WHERE worker_id = ? AND status = ?''', (user_id, "active",))
    rows = cursor.fetchall()

    # Закрываем соединение с базой данных и возвращаем полученные задачи
    conn.close()
    return rows


def choise_new_case(username):
    # Устанавливаем соединение с базой данных
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()

    # Выполняем SQL-запрос для получения идентификатора пользователя по его имени
    cursor.execute('''SELECT id FROM users WHERE username = ? ''', (username,))
    result = cursor.fetchone()

    if not result:  # Пользователь с таким именем не найден
        return []

    user_id = result[0]

    # Выполняем SQL-запрос для получения всех задач, связанных с указанным пользователем или не назначенных пользователю и со статусом "active"
    cursor.execute("SELECT * FROM tasks WHERE worker_id = ? OR worker_id IS NULL AND status = ?", (None, "active",))
    rows = cursor.fetchall()

    # Закрываем соединение с базой данных и возвращаем полученные задачи
    conn.close()
    return rows


def update_task_worker(username, idd):
    # Устанавливаем соединение с базой данных
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()

    # Выполняем SQL-запрос для получения идентификатора пользователя по его имени
    cursor.execute('''SELECT id FROM users WHERE username = ? ''', (username,))
    result = cursor.fetchone()

    if not result:  # Пользователь с таким именем не найден
        return []

    user_id = result[0]

    # Выполняем SQL-запрос для обновления задачи с указанным идентификатором и установкой нового worker_id
    cursor.execute("UPDATE tasks SET worker_id = ? WHERE id = ?", (user_id, idd,))

    # Фиксируем изменения и закрываем соединение с базой данных
    conn.commit()
    conn.close()


def case_end(username, idd):
    # Устанавливаем соединение с базой данных
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()

    # Выполняем SQL-запрос для получения идентификатора пользователя по его имени
    cursor.execute('''SELECT id FROM users WHERE username = ? ''', (username,))
    result = cursor.fetchone()

    if not result:  # Пользователь с таким именем не найден
        return []

    user_id = result[0]

    # Выполняем SQL-запрос для обновления задачи с указанным идентификатором и установкой статуса "archive"
    cursor.execute("UPDATE tasks SET status = ? WHERE id = ?", ('archive', idd,))

    # Фиксируем изменения и закрываем соединение с базой данных
    conn.commit()
    conn.close()


def case_all(username):
    # Устанавливаем соединение с базой данных
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()

    # Выполняем SQL-запрос для получения всех задач
    cursor.execute("SELECT * FROM tasks")
    rows = cursor.fetchall()

    # Закрываем соединение с базой данных и возвращаем полученные задачи
    conn.close()
    return rows


def delete_case(username, idd):
    # Устанавливаем соединение с базой данных
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()

    # Выполняем SQL-запрос для удаления задачи с указанным идентификатором
    cursor.execute("DELETE FROM tasks WHERE id = ?", (idd,))

    # Фиксируем изменения и закрываем соединение с базой данных
    conn.commit()
    conn.close()


def get_users():
    # Устанавливаем соединение с базой данных
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()

    # Выполняем SQL-запрос для получения всех пользователей
    cursor.execute('''SELECT * FROM users ''')
    rows = cursor.fetchall()

    # Закрываем соединение с базой данных и возвращаем полученных пользователей
    conn.close()
    return rows


def set_worker(idd):
    # Устанавливаем соединение с базой данных
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()

    # Выполняем SQL-запрос для обновления роли пользователя с указанным идентификатором на "worker"
    cursor.execute("UPDATE users SET role = ? WHERE id = ?", ('worker', idd,))

    # Фиксируем изменения и закрываем соединение с базой данных
    conn.commit()
    conn.close()


def set_admin(idd):
    # Устанавливаем соединение с базой данных
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()

    # Выполняем SQL-запрос для обновления роли пользователя с указанным идентификатором на "admin"
    cursor.execute("UPDATE users SET role = ? WHERE id = ?", ('admin', idd,))

    # Фиксируем изменения и закрываем соединение с базой данных
    conn.commit()
    conn.close()


def delete_user(idd):
    # Устанавливаем соединение с базой данных
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()

    # Выполняем SQL-запрос для удаления пользователя с указанным идентификатором
    cursor.execute("DELETE FROM users WHERE id = ?", (idd,))

    # Фиксируем изменения и закрываем соединение с базой данных
    conn.commit()
    conn.close()


