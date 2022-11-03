import socket
import random

HOST = ''                
PORT = 4444
client1=0
client2=0
client1_wins=0
client1_lose=0
client2_wins=0
client2_lose=0 
draw=0
card_deck=[]
card_deck1=[]
card_deck2=[]
k=1
suit=["C","D","H","S"]
rank=["1","2","3","4","5","6","7","8","9","10","11","12","13"]
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(5)
conn1, addr1 = s.accept()
conn2, addr2 = s.accept()
print ('Connected by', addr1)
print ('Connected by', addr2)

#card shuffle
for i in range(4):
    for j in range(13):
        card_deck.append(rank[j]+suit[i])
random.shuffle(card_deck)
for i in range(26):
    card_deck[i]=(card_deck[i][:len(card_deck[i])-1])
    card_deck1.append(int(card_deck[i]))
for i in range(26,52):
    card_deck[i]=(card_deck[i][:len(card_deck[i])-1])
    card_deck2.append(int(card_deck[i]))
print("card_deck1:",card_deck1)
print("card_deck2:",card_deck2)

#start sending to client
while 1:
    data1 = conn1.recv(1024).decode()
    data2 = conn2.recv(1024).decode()
    if not data1: break
    if data1=="WANTGAME":
        print("Recieved from client1: ",data1)
        conn1.send(b"GAME START")
        conn1.send(bytes(str(card_deck1),"utf-8"))
    if data2=="WANTGAME":
        print("Recieved from client2: ",data2)
        conn2.send(b"GAME START")
        conn2.send(bytes(str(card_deck2),"utf-8"))

#recieving cards from client
        while 1:
            #client1
            recieved_card1=conn1.recv(8).decode()
            if recieved_card1!="PLAYCARD": break
            if recieved_card1=="PLAYCARD":
                print("client1:",recieved_card1)
                cardone=conn1.recv(3).decode()
            recieved_card2=conn2.recv(8).decode()
            if recieved_card2=="PLAYCARD":
                print("client2:",recieved_card1)
                cardtwo=conn2.recv(3).decode()
                print("client1card:",cardone) 
                print("client2card:",cardtwo)
#sending results to client
                if(int(cardone)>int(cardtwo)):
                    client1+=1
                    if k<10:
                        client1_wins+=1
                        client2_lose+=1
                        # conn1.send(b"YOU WON FOR CARD "+bytes(str(k),"utf-8")+b" ")
                    elif k>9:
                        client1_wins+=1
                        client2_lose+=1
                        # conn1.send(b"YOU WON FOR CARD "+bytes(str(k),"utf-8"))
                    if k==26:
                        if client1>client2:
                            print("client1 wins")
                            conn1.send(b"WIN : "+bytes(str(client1_wins),"utf-8")+b"  ")
                            conn1.send(b"DRAW: "+bytes(str(draw),"utf-8")+b"  ")
                            conn1.send(b"LOSE: "+bytes(str(client1_lose),"utf-8")+b"  ")
                            conn2.send(b"WIN : "+bytes(str(client2_wins),"utf-8")+b"  ")
                            conn2.send(b"DRAW: "+bytes(str(draw),"utf-8")+b"  ")
                            conn2.send(b"LOSE: "+bytes(str(client2_lose),"utf-8")+b"  ")
                            conn1.send(b"YOU WON THE GAME!")
                            conn2.send(b"YOU LOST THE GAME!")
                elif(int(cardone)<int(cardtwo)):
                    client2+=1
                    if k<10:
                        client2_wins+=1
                        client1_lose+=1
                        # conn2.send(b"YOU WON FOR CARD "+bytes(str(k),"utf-8")+b" ")
                    elif k>9:
                        client2_wins+=1
                        client1_lose+=1
                        # conn2.send(b"YOU WON FOR CARD "+bytes(str(k),"utf-8"))
                    if k==26:
                        if client1<client2:
                            print("client2 wins")
                            conn1.send(b"WIN : "+bytes(str(client1_wins),"utf-8")+b"  ")
                            conn1.send(b"DRAW: "+bytes(str(draw),"utf-8")+b"  ")
                            conn1.send(b"LOSE: "+bytes(str(client1_lose),"utf-8")+b"  ")
                            conn2.send(b"WIN : "+bytes(str(client2_wins),"utf-8")+b"  ")
                            conn2.send(b"DRAW: "+bytes(str(draw),"utf-8")+b"  ")
                            conn2.send(b"LOSE: "+bytes(str(client2_lose),"utf-8")+b"  ")
                            conn1.send(b"YOU LOST THE GAME!")
                            conn2.send(b"YOU WON THE GAME!")
                else:
                    draw+=1
                    if k==26:
                        conn1.send(b"WIN : "+bytes(str(client1_wins),"utf-8")+b"  ")
                        conn1.send(b"DRAW: "+bytes(str(draw),"utf-8")+b"  ")
                        conn1.send(b"LOSE: "+bytes(str(client1_lose),"utf-8")+b"  ")
                        conn2.send(b"WIN : "+bytes(str(client2_wins),"utf-8")+b"  ")
                        conn2.send(b"DRAW: "+bytes(str(draw),"utf-8")+b"  ")
                        conn2.send(b"LOSE: "+bytes(str(client2_lose),"utf-8")+b"  ")
                        if client1>client2:
                            print("client1 wins")
                            conn1.send(b"YOU WON THE GAME!")
                            conn2.send(b"YOU LOST THE GAME!")
                        elif client1<client2:
                            print("client2 wins")
                            conn1.send(b"YOU LOST THE GAME!")
                            conn2.send(b"YOU WON THE GAME!")
                k+=1
print("ENDED!")
conn1.close()
conn2.close()
