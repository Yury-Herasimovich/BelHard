import socket
from datetime import datetime
import re

users = {}

def parse_http_request(data):
    if data.startswith(('GET', 'POST')):
        lines = data.split('\r\n')
        method, path, _ = lines[0].split(' ', 2)
        
        # Главная страница
        if path == '/':
            return "HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8\r\n\r\n<h1>Главная страница</h1>"
        
        # Тест/номер
        elif re.match(r'/test/(\d+)/', path):
            test_num = re.search(r'/test/(\d+)/', path).group(1)
            return f"HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8\r\n\r\nТест {test_num} запущен"
        
        # Сообщение от пользователя
        elif re.match(r'/message/([^/]+)/([^/]+)/', path):
            login = re.search(r'/message/([^/]+)/', path).group(1)
            text = re.search(r'/message/[^/]+/([^/]+)/', path).group(1)
            print(f"{datetime.now()} - Сообщение от {login}: {text}")
            return f"HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8\r\n\r\nСообщение получено"
        
        # Запрос файла
        elif '.' in path:  # Если есть расширение (например, /file.txt)
            try:
                with open(path[1:], 'r') as file:
                    content = file.read()
                return f"HTTP/1.1 200 OK\r\nContent-Type: text/plain; charset=utf-8\r\n\r\n{content}"
            except FileNotFoundError:
                return "HTTP/1.1 404 Not Found\r\n\r\nФайл не найден"
        
        # Неизвестный HTTP-запрос
        else:
            return f"HTTP/1.1 400 Bad Request\r\n\Content-Type: text/html; charset=utf-8\r\n\r\nНеизвестные данные по HTTP: {path}"
    
    # Если это не HTTP, обрабатываем команды
    else:
        return process_command(data)

def process_command(data):
    try:
        # Извлекаем команду, логин и пароль
        command = re.search(r'command:(\w+);', data).group(1)
        login = re.search(r'login:([^;]+);', data).group(1).strip()
        password = re.search(r'password:([^;]+)', data).group(1).strip()
        
        if command == 'reg':
            # Проверка логина (только латиница + цифры, мин 6 символов)
            if not (re.match(r'^[a-zA-Z0-9]{6,}$', login)):
                return f"{datetime.now()} - Ошибка регистрации {login}: неверный логин"
            
            # Проверка пароля (мин 8 символов, хотя бы 1 цифра)
            if not (len(password) >= 8 and re.search(r'\d', password)):
                return f"{datetime.now()} - Ошибка регистрации {login}: неверный пароль"
            
            # Пользователь уже существует
            if login in users:
                return f"{datetime.now()} - Ошибка регистрации {login}: пользователь уже существует"
            
            # Регистрация
            users[login] = password
            return f"{datetime.now()} - Пользователь {login} зарегистрирован"
        
        elif command == 'signin':
            # Проверка входа
            if login in users and users[login] == password:
                return f"{datetime.now()} - Пользователь {login} выполнил вход"
            else:
                return f"{datetime.now()} - Ошибка входа {login}: неверный логин/пароль"
        
        else:
            return f"{datetime.now()} - Неизвестная команда: {command}"
    
    except (AttributeError, IndexError):
        return f"{datetime.now()} - Ошибка формата данных: {data}"

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('127.0.0.1', 7772))  # Принимаем со всех интерфейсов
    server_socket.listen(5)
    print("Сервер запущен. Ожидание подключений...")
        
    while True:
        client_socket, addr = server_socket.accept()
        print(f"Подключён клиент: {addr}")
            
        data = client_socket.recv(4096).decode('utf-8')
        if not data:
            continue
            
            
        response = parse_http_request(data)
        client_socket.send(response.encode('utf-8'))
        client_socket.close()

if __name__ == "__main__":
    start_server()