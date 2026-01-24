import threading
import socket
import random
import sys
import customtkinter as ctk

class MiAppGrande(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("1280x720")
        self.title("Sorteo Twitch V.1.2.0")
        
        self.participantes = []
        self.canal_nombre = ""
        self.palabra_clave = ""
        self.corriendo = False
        self.ganador_actual = None
        self.ventana_ganador = None

        self.pantalla_inicio()

    def limpiar_pantalla(self):
        for widget in self.winfo_children():
            widget.destroy()

    def pantalla_inicio(self):
        self.limpiar_pantalla()
        ctk.CTkLabel(self, text="CONFIGURACIÓN", font=("Arial", 35, "bold")).pack(pady=40)
        self.ent_canal = ctk.CTkEntry(self, placeholder_text="Nombre del Canal", width=500, height=60, font=("Arial", 20))
        self.ent_canal.pack(pady=15)
        self.ent_palabra = ctk.CTkEntry(self, placeholder_text="Palabra Clave", width=500, height=60, font=("Arial", 20))
        self.ent_palabra.pack(pady=15)
        ctk.CTkButton(self, text="INICIAR", width=400, height=80, font=("Arial", 22, "bold"), fg_color="#56ADFF", command=self.preparar_sorteo).pack(pady=40)

    def preparar_sorteo(self):
        self.canal_nombre = self.ent_canal.get().lower().replace("#", "")
        self.palabra_clave = self.ent_palabra.get()
        if self.canal_nombre and self.palabra_clave:
            self.limpiar_pantalla()
            self.interfaz_sorteo()
            self.corriendo = True
            threading.Thread(target=self.conexion_twitch, daemon=True).start()

    def interfaz_sorteo(self):
        self.contenedor_principal = ctk.CTkFrame(self, fg_color="transparent")
        self.contenedor_principal.pack(expand=True, fill="both", padx=20, pady=20)

        self.col_izq = ctk.CTkFrame(self.contenedor_principal, fg_color="transparent")
        self.col_izq.pack(side="left", padx=20, fill="y")

        self.lista_scroll = ctk.CTkScrollableFrame(self.col_izq, width=300, height=500, label_text="PARTICIPANTES", fg_color="#F0F4F8", label_fg_color="#56ADFF", label_text_color="white", border_color="#56ADFF", border_width=2)
        self.lista_scroll.pack(pady=(0, 20))

        self.btn_ganador = ctk.CTkButton(self.col_izq, text="ELEGIR GANADOR", width=300, height=60, font=("Arial", 16, "bold"), fg_color="#56ADFF", command=self.obtener_ganador)
        self.btn_ganador.pack()

        self.col_centro = ctk.CTkFrame(self.contenedor_principal, fg_color="transparent")
        self.col_centro.pack(side="left", expand=True, fill="both")

        ctk.CTkLabel(self.col_centro, text=f"CANAL: \n{self.canal_nombre.upper()}", font=("Arial", 18, "bold")).pack(pady=10)
        ctk.CTkLabel(self.col_centro, text=f"PALABRA CLAVE: \n{self.palabra_clave.upper()}", font=("Arial", 18, "bold")).pack(pady=10)
        self.label_estado = ctk.CTkLabel(self.col_centro, text="ESPERANDO...", font=("Arial", 30, "bold"), text_color="#56ADFF")
        self.label_estado.pack(expand=True)

        self.chat_scroll = ctk.CTkScrollableFrame(self.contenedor_principal, width=300, height=500, label_text="CHAT EN VIVO", fg_color="#F0F4F8", label_fg_color="#56ADFF", label_text_color="white", border_color="#56ADFF", border_width=2)
        self.chat_scroll.pack(side="right", padx=20)

        ctk.CTkButton(self, text="SALIR", fg_color="#FF4B4B", command=sys.exit).pack(side="bottom", pady=20)

    def abrir_ventana_ganador(self, nombre):
        if self.ventana_ganador:
            self.ventana_ganador.destroy()
        
        self.ganador_actual = nombre
        self.ventana_ganador = ctk.CTkToplevel(self)
        self.ventana_ganador.geometry("500x600")
        self.ventana_ganador.title("GANADOR SELECCIONADO")
        self.ventana_ganador.attributes("-topmost", True)

        ctk.CTkLabel(self.ventana_ganador, text="¡GANADOR!", font=("Arial", 25, "bold")).pack(pady=10)
        ctk.CTkLabel(self.ventana_ganador, text=nombre.upper(), font=("Arial", 45, "bold"), text_color="#56ADFF").pack(pady=10)
        
        ctk.CTkLabel(self.ventana_ganador, text="MENSAJES DEL GANADOR:", font=("Arial", 14, "bold")).pack(pady=5)
        self.chat_ganador = ctk.CTkScrollableFrame(self.ventana_ganador, width=400, height=300, fg_color="#F0F4F8", border_color="#56ADFF", border_width=2)
        self.chat_ganador.pack(pady=10)

        ctk.CTkButton(self.ventana_ganador, text="REROLL", fg_color="#56ADFF", height=50, width=200, font=("Arial", 16, "bold"), command=self.obtener_ganador).pack(pady=10)

    def conexion_twitch(self):
        sock = socket.socket()
        try:
            sock.connect(('irc.chat.twitch.tv', 6667))
            sock.send(f"PASS oauth:anypass\r\n".encode('utf-8'))
            sock.send(f"NICK justinfan{random.randint(1000,9999)}\r\n".encode('utf-8'))
            sock.send(f"JOIN #{self.canal_nombre}\r\n".encode('utf-8'))

            while self.corriendo:
                data = sock.recv(2048).decode('utf-8')
                if data.startswith('PING'):
                    sock.send("PONG :tmi.twitch.tv\r\n".encode('utf-8'))
                elif 'PRIVMSG' in data:
                    user = data.split('!')[0][1:].lower()
                    msg = data.split('PRIVMSG')[1].split(':', 1)[1].strip()
                    
                    self.after(0, self.dibujar_chat_general, user, msg)
                    
                    if self.ganador_actual and user == self.ganador_actual:
                        self.after(0, self.dibujar_chat_ganador, msg)

                    if msg == self.palabra_clave and user not in self.participantes:
                        self.participantes.append(user)
                        self.after(0, self.dibujar_nombre, user)
        except:
            pass

    def dibujar_nombre(self, user):
        ctk.CTkLabel(self.lista_scroll, text=f"• {user}", text_color="#1A1A1A", font=("Arial", 16, "bold")).pack(pady=2, anchor="w")

    def dibujar_chat_general(self, user, msg):
        ctk.CTkLabel(self.chat_scroll, text=f"{user}: {msg}", text_color="#1A1A1A", font=("Arial", 12), wraplength=250, justify="left").pack(pady=1, anchor="w")

    def dibujar_chat_ganador(self, msg):
        if self.ventana_ganador and self.ventana_ganador.winfo_exists():
            ctk.CTkLabel(self.chat_ganador, text=f"» {msg}", text_color="#1A1A1A", font=("Arial", 14, "bold"), wraplength=350, justify="left").pack(pady=2, anchor="w")

    def obtener_ganador(self):
        if self.participantes:
            ganador = random.choice(self.participantes)
            self.abrir_ventana_ganador(ganador)

if __name__ == "__main__":
    ctk.set_appearance_mode("light")
    app = MiAppGrande()
    app.mainloop()
