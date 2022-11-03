import socket

HOST = 'localhost'
PORT = 4444
final_cards=[]       
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
s.send(b"WANTGAME")

#recieving from server
data = s.recv(10).decode()
cards= s.recv(1024).decode()
deck=cards[1:len(cards)-1]
cards=deck.split(",")
for i in range(len(cards)):
	final_cards.append(int(cards[i]))

#sending cards back to server
for i in range(26):
	if i==0:
		s.send(b"PLAYCARD")
		if len(cards[i])==1:
			s.send(bytes(cards[i]+"  ","utf-8"))
		elif len(cards[i])==2:
			s.send(bytes(cards[i]+" ","utf-8"))
	else:
		s.send(b"PLAYCARD")
		if len(cards[i])==2:
			s.send(bytes(cards[i]+" ","utf-8"))
		else:
			s.send(bytes(cards[i],"utf-8"))
# result=s.recv(10)

print('Received', data)
print('Cards are::', final_cards)

#recieving results from server
while 1:
	result=s.recv(4096).decode()
	print("",result)
	if not result: break

s.close()