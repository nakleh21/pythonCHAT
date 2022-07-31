import socket
import threading

print('''
  ______ _         _____  ____ _______       _   _  ____  
 |  ____| |       / ____|/ __ \__   __|/\   | \ | |/ __ \ 
 | |__  | |      | (___ | |  | | | |  /  \  |  \| | |  | |
 |  __| | |       \___ \| |  | | | | / /\ \ | . ` | |  | | CHAT
 | |____| |____   ____) | |__| | | |/ ____ \| |\  | |__| |
 |______|______| |_____/ \____/  |_/_/    \_\_| \_|\____/ 
                                                          
-------------------------REGLAS del chat------------------------
 1.- NO HAGAS SPAM, seras expulsado!
 ---------------------------------------------------------------
''')


# Choosing Nickname
nickname = input("Ingresa tu nombre de Usuario: ")
if nickname == 'admin':
    password = input ("Ingresa la clave de admin: ")

# Connecting To Server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 55555))

stop_thread = False

# Listening to Server and Sending Nickname
def receive():
    while True:
        global stop_thread
        if stop_thread:
            break
        try:
            # Receive Message From Server
            # If 'NICK' Send Nickname
            message = client.recv(1024).decode('ascii')
            if message == 'NICK':
                client.send(nickname.encode('ascii'))
                next_message= client.recv(1024).decode('ascii')
                if next_message == 'PASS':
                    client.send(password.encode('ascii'))
                    if client.recv(1024).decode('ascii') == 'REFUSE':
                        print("Password incorrecto")
                        stop_thread = True


            else:
                print(message)
        except:
            # Close Connection When Error
            print("Error")
            client.close()
            break

# Sending Messages To Server
def write():
    while True:
        if stop_thread:
            break
        message = '{}: {}'.format(nickname, input(''))
        if not message[len(nickname) + 2:].startswith('/'):
            client.send(message.encode('ascii'))
        else:
            if nickname == 'admin':
                if message[len(nickname)+2:].startswith('/kick'):
                    client.send(f'KICK {message[len(nickname)+2+6:]}'.encode('ascii'))
            else:
                print('Solo el admin puede ejecutar estos comandos')


# Starting Threads For Listening And Writing
receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()