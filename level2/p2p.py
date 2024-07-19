import socket
import threading
import time
from collections import defaultdict

from transaction import transaction
from checkMoney import checkMoney
from checkLog import checkLog
from checkChain import checkChain
from checkAllChains import checkAllChains
from overwrite import overwrite

class P2PNode:
    def __init__(self, port, peers, addr):
        self.port = port
        self.peers = peers
        self.addr = addr
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.addr, self.port))
        self.state = defaultdict(set)

    def start(self):
        threading.Thread(target=self._listen).start()
        threading.Thread(target=self._send_messages).start()

    def _listen(self):
        while True:
            raw_message, addr = self.sock.recvfrom(16384)
            raw_message = raw_message.decode("utf-8")

            message = raw_message.split(" ")
            if message[0] == "transaction":
                transaction(message[1: ])
            elif message[0] == "check":
                correct, sha_value, content = checkAllChains()
                self.sock.sendto(f"add {correct} {sha_value} {content}".encode("utf-8"), addr)
            elif message[0] == "add":
                correct, sha_value, content = message[1], message[2], " ".join(message[3: ])
                self.state[content].add((addr, correct, sha_value))
            elif message[0] == "overwrite":
                content = " ".join(message[1: ])
                overwrite(content)

    def _send_messages(self):
        while True:
            raw_message = input("Enter a command(checkMoney, checkLog, transaction, checkChain, checkAllChains): ")
            message = raw_message.split(" ")
            if message[0] == "transaction":
                transaction(message[1: ])
                for peer in self.peers:
                    self.sock.sendto(raw_message.encode("utf-8"), peer)
            elif message[0] == "checkMoney":
                checkMoney(message[1])
            elif message[0] == "checkLog":
                checkLog(message[1])
            elif message[0] == "checkChain":
                check, m = checkChain()
                print(m)
            elif message[0] == "checkAllChains":
                self.state = defaultdict(set)
                correct, sha_value, content = checkAllChains()
                self.state[content].add(((self.addr, self.port), str(correct), sha_value))
                for peer in self.peers:
                    self.sock.sendto("check".encode("utf-8"), peer)

                time.sleep(1)

                flag = len(self.state) == 1
                main, length = None, (len(self.peers) + 1) / 2
                for content, msg in self.state.items():
                    for m in msg:
                        addr, correct, sha_value = m[0], m[1], m[2]
                        if correct == "False":
                            flag = False
                    if len(msg) > length:
                        main = content
                        length = len(m)

                if flag:
                    transaction(["Angel", message[1], 100])
                    for peer in self.peers:
                        self.sock.sendto(f"transaction Angel {message[1]} 100".encode("utf-8"), peer)
                    print("True")
                elif main == None:
                    print("It's an untrusted system.")
                else:
                    print("False")
                    for content, m in self.state.items():
                        if content != main:
                            msg = "overwrite " + main
                            for peer in m:
                                self.sock.sendto(msg.encode("utf-8"), peer[0])

if __name__ == '__main__':
    port = 8001
    peers = [('172.17.0.3', 8001), ('172.17.0.4', 8001)]
    addr = '172.17.0.2'
    node = P2PNode(port, peers, addr)
    node.start()