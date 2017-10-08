from PinRobot import PinRobot
from Utilities import Utilities
import socket
import argparse
import sys
import time


def main():
    parser = argparse.ArgumentParser(description='PIN Robot API')
    parser.add_argument('--auto', action='store_true', help='Flag to indicate automated TCP test mode')
    parser.add_argument('-config','-configfile", help="path to configuration xml',required=False)
    parser.add_argument('-ip','-robot_ip", help="ip address to the robot',type = str,required=False)
    parser.add_argument('-port','-port_ip", help="port to the robot',type = int,required=False)

    args = (parser.parse_args())
    mode = ""
    
    if ((args.auto) and (args.config is None) and (args.ip is None) and (args.port is None)):
        parser.error('-auto requires -config,-ip,port')

    if args.auto:
        mode = 'auto'
    else:
        mode = 'manual'

    configfile = args.config
    robot_ip = args.ip
    robot_port = args.port
    
    global robot
    robot = PinRobot()
    result = False
    _path = "Configuration"
    if (mode == 'manual'):
        try:
            files = Utilities.get_and_print_conf_list(_path)
            while result is False:
                index = int(input())
                if(index > len(files) or index <= 0):
                    print("Wrong input, retry")
                    continue

                config = Utilities.select_conf(_path, index);

                result = robot.InitializeTerminal(config)
            
                if(False is result):
                    print("Could not initialize the terminal, please try again")

            IP = input("Enter IP: ")
            Port = input("Enter Port: ")
            if(False is robot.InitializeConnection(IP, int(Port))):
                raise ConnectionError("InitializeConnection", "Could not connect")


            Keypress = input("Enter key[0-9][Ok][Menu][Stop][.]: ")
            while('x' not in Keypress):
                if(False is robot.SendCommand(Keypress)):
                    raise InputError(Keypress, "No command found")
                Keypress = input("Enter key: ") 
        except (InputError,ConnectionError,ParseError):
            pass

    elif (mode == 'auto'):
        try:
            if(False is robot.InitializeTerminal(configfile)):
                    raise ParseError("InitializeTerminal", "Parsing Error")
        
            if(False is robot.InitializeConnection(robot_ip, int(robot_port))):
                    raise ConnectionError("InitializeConnection", "Could not connect")

            time.sleep(5)
        

            #Symbolic name, meaning all available interfaces
            HOST = '127.0.0.1'
            #Arbitrary non-privileged port
            PORT = 8888
             
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)            
            
            try:
                s.bind((HOST, PORT))
            except socket.error as msg:
                print ('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
                sys.exit()
                         
            #Start listening on socket
            s.listen(10)
            print ("PEM listening for incoming commands")
            
            #wait to accept a connection - blocking call
            conn, addr = s.accept()
            print ('Connected with ' + addr[0] + ':' + str(addr[1]))
                
             
            #keep talking with the client
            while 1:
                
                #command to robot
                command = ""
                
                data = conn.recv(1024)            
                if data:
                    command += data.decode()
                    print ('received: ',command)
                    if('x' not in command):
                        robot.SendCommand(command)
                        if(False is robot.SendCommand(command)):
                            raise InputError(Keypress, "No command found")
                    else:
                        break
            s.close()

        except (InputError,ConnectionError,ParseError):
            pass
    
class Error(Exception):
    pass

class InputError(Error):
    def __init__(self, expression, message):
        self.expression = expression
        self.message = message

class ParseError(Error):
      def __init__(self, expression, message):
        self.expression = expression
        self.message = message


class ConnectionError(Error):
      def __init__(self, expression, message):
        self.expression = expression
        self.message = message

main()
