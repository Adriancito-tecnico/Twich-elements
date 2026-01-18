import asyncio
import sys
import random
import time

print (" ")
print ("--- SORTEO TWITCH V.1.2.0 ---")
print ("--- Adriancitotecnico ---")
print (" ")
while True:
    command1 = input ("Presione Enter para configurar el sorteo, escriba 'S' para salir o \"redes\": ")
    if command1.lower() == "S":
        sys.exit()
    if command1.lower() == "redes":
        print (" ")
        print ("Redes:")
        print ("    Youtube: @Adriancito_tecnico")
        print ("    Twich: Adriancitotecnico")
        print ("    Github: Adriancito-tecnico")
        print (" ")
    if not command1:
        break
    else:
        if not command1.lower() == "redes" or not command1.lower() == "S":
            print ("Comando no reconocido.")
        pass

print (" ")
print ("--- Configuración del sorteo ---")
print (" ")
time.sleep(1)

Bucle_1 = True
Bucle_2 = True
while Bucle_1:
    canal = input("Ingrese el nombre del canal de Twitch : ")
    channel= f"#{canal}"
    if not canal:
        print("El canal no es valido.")
        
    else:
        break
while Bucle_2:
    Palabra_Clave = input("Ingrese la palabra clave para el sorteo: ")
    if not Palabra_Clave:
        print ("La palabra clave no es valida.")
    else:
        if not Palabra_Clave.startswith("!"):
            Palabra_Clave = f"!{Palabra_Clave}"
        break

Administrador = input("Ingrese el nombre del administrador del sorteo o dele a enter para que sea el streamer (todo en minusculas): ")
if not Administrador:
    Administrador = canal

Palabra_finalizadora = input ("Ingrese la palabra clave para finalizar el sorteo (por defecto '!fin'): ")
if not Palabra_finalizadora:                 
    Palabra_finalizadora = "!fin"
if not Palabra_finalizadora.startswith("!"):
    Palabra_finalizadora = f"!{Palabra_finalizadora}"

print (" ")
print (f"Canal de twich: {canal} - {channel}")
print (f"Palabra de entrada al sorteo: {Palabra_Clave}")
print (f"Palbra de finalización: {Palabra_finalizadora}")
print (f"Adrministrador del sorteo: {Administrador}")
print (" ")

Participantes = []
print (" ")
print (f"--- Leyendo el chat de {canal} ---")
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

        finalizado = False
        while not finalizado:
            line = await reader.readline()
            decoded_line = line.decode('utf-8').strip()
            
            if decoded_line.startswith('PING'):
                writer.write("PONG :tmi.twitch.tv\r\n".encode('utf-8'))
                await writer.drain()
                continue

            if 'PRIVMSG' in decoded_line:
                user = decoded_line.split('!', 1)[0][1:].lower()
                message = decoded_line.split('PRIVMSG', 1)[1].split(':', 1)[1].strip()
                print(f"[{user}]: {message}")

                if message == Palabra_Clave:
                    if user not in Participantes:
                        Participantes.append(user)
                        print (f"   >>>{user} ANOTADO ✅")
                    else:
                        print (f"   >>>{user} YA ESTABA ANOTADO ❌")

                if message == Palabra_finalizadora and user == Administrador:
                    print ("\n--- El registro ha sido finalizado ---\n")
                    finalizado = True
        if Participantes:
            command2 = input("Presione Enter para ver los participantes o 'Saltar' para elegir ganador: ")
            if not command2:
                print (f"Participantes: {Participantes}")
                print (f"\nTotal de participantes: {len(Participantes)}\n")
                print (" ")
                command3 = input("Presione Enter para elegir al ganador: ")
            else:
                pass
            while True:
                print ("Eligiendo ganador...")
                ganador = random.choice(Participantes)
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
                reroll = input("Escriba 'R' para REROLL o Enter para finalizar: ").lower()
                if reroll == 'r':
                    continue
                else:
                    break
        else:
            print("No hubo participantes.")
            command4 = input("Presione Enter para finalizar: ")

    except Exception:
        pass
    finally:
        writer.close()
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
for i in range (25):
    print (" ")
print ("Redes:")
print ("    Youtube: @Adriancito_tecnico")
print ("    Twich: Adriancitotecnico")
print ("    Github: Adriancito-tecnico")
for i in range (25):
    print (" ")
time.sleep (1)
command5 = input ("Presione enter para cerrar el programa:")