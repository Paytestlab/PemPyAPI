from PinRobot import PinRobot

def main():
    global robot
    robot = PinRobot()
    robot.InitializeTerminal("Yoximo.xml")
    robot.InitializeConnection("192.168.1.102", 23)
    #robot.SendCommand("Stop")
    #robot.SendCommand("Sleep")
    robot.SendCommand("Sleep")
    robot.SendCommand("Home")
    robot.SendCommand("Stop")
    robot.SendCommand("Sleep")
    robot.SendCommand("0")
    robot.SendCommand("1")
    robot.SendCommand("2")
    robot.SendCommand("3")
    robot.SendCommand("4")
    #robot.SendCommand("5")
    #robot.SendCommand("6")
    #robot.SendCommand("7")
    #robot.SendCommand("8")
    #robot.SendCommand("9")
    #robot.SendCommand(".")
    #robot.SendCommand("Menu")
    #robot.SendCommand("Stop")
    #robot.SendCommand("OK")

    for index in range(1000):
        robot.SendCommand("9")
    #robot.CloseConnection()


def sendSequence():
    robot.sendCommand("2")
    robot.sendCommand("2")
    robot.sendCommand("6")
    robot.sendCommand("Menu")


main()