import asyncio
import sys
import random
import time

print (" ")
print ("--- SORTEO TWITCH V.1.0.0 ---")
print ("--- Adriancitotecnico ---")
print (" ")

command = input ("Presione Enter para configurar el sorteo o 'S' para salir: ")
if command.lower() == "S":
    print ("Saliendo del programa...")
    sys.exit()

print (" ")
print ("--- Configuración del sorteo ---")
print (" ")
time.sleep(1)

canal = input("Ingrese el nombre del canal de Twitch : ")
if not canal:
    print("Debe ingresar un nombre de canal válido.")
    sys.exit()
channel= f"#{canal}"

time.sleep(1)
print (" ")
print ("Canal establecido en:", canal,"-", channel)
print (" ")
time.sleep(1)

Bot = input ("Ingrese el nombre del bot que hara el sorteo:")
if not Bot:
    print ("Ingrese un nombre valido.")
    sys.exit()
print ("El bot establecido es:", Bot)
time.sleep(1)

Participantes = []
Palabra_Clave = input("Ingrese la palabra clave para el sorteo: ")
if not Palabra_Clave.startswith("!"):
    Palabra_Clave = f"!{Palabra_Clave}"

time.sleep(1)           
Administrador = input("Ingrese el nombre del administrador del sorteo o dele a enter para que sea el streamer: ")
if not Administrador:
    Administrador = "Canal"
time.sleep(1)
print (" ")
print ("Se ha establecido como administrador del sorteo a:", Administrador)
print (" ")

time.sleep(1)
print (" ")
input(f"Pulse Enter para iniciar en el canal {canal} con: {Palabra_Clave}")
print (" ")

Palabra_finalizadora = input ("Ingrese la palabra clave para finalizar el sorteo (por defecto '!finalizar'): ")
if not Palabra_finalizadora:                 
    Palabra_finalizadora = "!finalizar"
if not Palabra_finalizadora.startswith("!"):
    Palabra_finalizadora = f"!{Palabra_finalizadora}"

time.sleep(1)
print (" ")
print (f"Palabra clave para finalizar el sorteo establecida en: {Palabra_finalizadora}")
print (" ")
time.sleep(1)

print (" ")
print (f"---Leyendo el chat de {canal}---")
print (" ")

async def main():
    server = 'irc.chat.twitch.tv'
    port = 6667
    nickname = 'justinfan12345' 

    try:
        reader, writer = await asyncio.open_connection(server, port)

        writer.write(f"PASS oauth:anypass\r\n".encode('utf-8'))
        writer.write(f"NICK {nickname}\r\n".encode('utf-8'))
        writer.write(f"JOIN {channel}\r\n".encode('utf-8'))
        await writer.drain()

        while True:
            line = await reader.readline()
            if not line:
                break
            
            decoded_line = line.decode('utf-8').strip()
            
            if decoded_line.startswith('PING'):
                writer.write("PONG :tmi.twitch.tv\r\n".encode('utf-8'))
                await writer.drain()
                continue

            if 'PRIVMSG' in decoded_line:
                user = decoded_line.split('!', 1)[0][1:]
                message = decoded_line.split('PRIVMSG', 1)[1].split(':', 1)[1]
                print(f"[{user}]: {message}")

                if message == Palabra_Clave:
                    if not user in Participantes:
                        Participantes.append(user)
                        print (f"   >>>{user} ANOTADO ✅")
                    else:
                        print (f"   >>>{user} YA ESTABA ANOTADO ❌")
                    
                if message == Palabra_finalizadora and user == Administrador:
                    print (" ")
                    print ("---El registro ha sido finalizado---")
                    print (" ")
                    command = input ("Dele al enter para ver a los participantes o escriba \"Saltar\" para elegir directamente al ganador:")
                    if not command:
                        print ("Participantes:")
                        print (Participantes)
                

                    command = input ("Escriba \"Elegir\" para elegir al ganador:")
                    if command == "Saltar" or command == "Elegir":
                        ganador = random.choice(Participantes)
                        time.sleep(5)
                        print ("3")
                        time.sleep(1)
                        print ("2")
                        time.sleep(1)
                        print ("1")
                        time.sleep(1)
                        for i in range (25):
                            print (" ")
                        print (f"--- El ganador es: {ganador} ---")
                        for i in range (25):
                            print (" ")
                        break

    except Exception:
        pass
    finally:
        writer.close()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
