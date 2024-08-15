import pymem
import time
import tkinter as tk

# Configurar pymem para leer la memoria del proceso del juego
process_name = "SonicDash_R_Ring.exe"  # Reemplaza con el nombre del proceso correcto
address = 0x0BC7C8E8  # Dirección de memoria obtenida

# Iniciar pymem y conectar al proceso
try:
    pm = pymem.Pymem(process_name)
    print(f"Conectado al proceso {process_name}")
except pymem.exception.ProcessNotFound:
    print(f"No se pudo encontrar el proceso {process_name}")
    exit(1)

# Dirección de memoria completa
ticket_address = address

# Función para actualizar el número de tickets en la interfaz gráfica
def update_tickets(ticket_count):
    ticket_label.config(text=f'Tickets dispensados: {ticket_count}')
    root.update()

# Función para simular el pago de tickets con cuenta atrás
def simulate_ticket_payment(initial_tickets):
    for ticket_count in range(initial_tickets, -1, -1):
        update_tickets(ticket_count)
        time.sleep(0.1)  # Ajusta este valor para controlar la velocidad de la cuenta atrás
    # Después de la cuenta atrás, resetea el valor de tickets en la memoria
    pm.write_int(ticket_address, 0)

# Configurar la interfaz gráfica
root = tk.Tk()
root.title("Simulador de Dispensador de Tickets")

ticket_label = tk.Label(root, text="Tickets dispensados: 0", font=("Helvetica", 16))
ticket_label.pack(pady=20)

# Bucle para leer la memoria y actualizar la interfaz gráfica
def monitor_tickets():
    ticket_count_prev = 0
    while True:
        try:
            ticket_count = pm.read_int(ticket_address)
            if ticket_count != ticket_count_prev:
                ticket_count_prev = ticket_count

                # Si hay tickets dispensados, simula el pago de tickets
                if ticket_count > 0:
                    simulate_ticket_payment(ticket_count)

            time.sleep(1)  # Leer la memoria cada segundo
        except Exception as e:
            print(f"Error: {e}")
            break

# Iniciar el monitoreo de tickets en un hilo separado
import threading
threading.Thread(target=monitor_tickets, daemon=True).start()

root.mainloop()
