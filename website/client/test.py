from client import Client
import time
from threading import Thread

c1 = Client("Satoshi")
c2 = Client("Ruri")

def update_messages():
    """
     Updates the local list of messages
    """
    msgs = []
    run = True
    while run:
        time.sleep(0.1)#Updates every 0.1 seconds
        new_messages = c1.get_messages() #Get new messages
        msgs.extend(new_messages)

        for msg in msgs:
            print(msg) #Display messages

            if msg == "{quit}":
                run = False
                break

Thread(target= update_messages).start()

c1.send_message("Konnichiva")
time.sleep(5)
c2.send_message("Ah! konnichiva")
time.sleep(5)
c1.send_message("Funde kudasai!")
time.sleep(5)
c2.send_message("Hai Yorokonde...")
time.sleep(5)

c1.disconnect()
time.sleep(2)
c2.disconnect()

