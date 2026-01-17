import asyncio

async def main():
    server = 'irc.chat.twitch.tv'
    port = 6667
    nickname = 'justinfan12345'
    
    canal_input = "TrikiVals_" 
    channel = f"#{canal_input.lower().replace('#', '')}"

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

    except Exception:
        pass
    finally:
        writer.close()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass