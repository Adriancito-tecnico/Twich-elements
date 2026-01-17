import asyncio
import sys
import random
import time

print (" ")
print ("--- SORTEO TWITCH V.1.0.0 ---")
print ("--- Por: Adriancitotecnico ---")
print (" ")

command = input ("Presione Enter para configurar el sorteo o 'S' para salir: ")
if command.lower() == "S":
    print ("Saliendo del programa...")
    sys.exit()
else:
    print(" ")
    print ("--- Configuracion del sorteo ---")
    print(" ")
canal = input ("Intrduzca el canal de Twich:")
channel = f"#{canal}"
Palabra_sorteo = input ("Introduzca la palabra cave para participar en el sorteo:")
Palabra_Finalización = input ("Introduzca la palabra clave para finalizar el sorteo:")
Administrador = input ("Introduzca un Administrador que inicie y finalize sorteo o solo dele a enter para que sea el streamer. (el nombre debe ir todo en minusculas):")
if not Administrador:
    Administrador = canal
print (" ")
print (f"Calan de twich: {canal}-{channel}")
print (f"Palabra de entrada al sorteo: {Palabra_sorteo}")
print (f"Palbra de finalización: {Palabra_Finalización}")
print (f"Adrministrador del sorteo: {Administrador}")
print (" ")
command = input ("Preseione enter para comenzar el sorteo o escriba \"S\" para salir:")
if command == "S":
    ("Saliendo del Programa...")
    time.sleep(1)
    sys.exit()
else:
    Participantes = []
    print ("Se ha creado la variable \"Participantes\".")

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

                if message == Palabra_sorteo:
                    if not user in Participantes:
                        Participantes.append(user)
                        print (f"   >>>{user} ANOTADO ✅")
                    else:
                        print (f"   >>>{user} YA ESTABA ANOTADO ❌")
                    
                if message == Palabra_Finalización and user == Administrador:
                    print (" ")
                    print ("---El registro ha sido finalizado---")
                    print (" ")
                    command = input ("Dele al enter para ver a los participantes o escriba \"Saltar\" para elegir directamente al ganador:")
                    if not command:
                        print ("Participantes:")
                        print (Participantes)

                    command = input ("Presione el enter para elegir al ganador:")
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
commmand = input ("Presione enter para cerrar el programa:")
