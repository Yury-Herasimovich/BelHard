import socket

def send_command(command, login, password):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 7772))
    
    message = f"command:{command}; login:{login}; password:{password}"
    print(f"Отправка: {message}")
    client_socket.send(message.encode('utf-8'))
    
    response = client_socket.recv(4096).decode('utf-8')
    print("Ответ сервера:", response)
    
    client_socket.close()

# Регистрация
send_command('reg', 'user1', 'password123')
send_command('reg', 'user2', 'qwerty123')

# Вход
send_command('signin', 'user1', 'password123')
send_command('signin', 'user2', 'wrongpass')  