from PinRobot import PinRobot

def main():
    global robot
    robot = PinRobot()
    robot.InitializeTerminal("Yomani.xml")
    robot.InitializeConnection("localhost", 3000)
    robot.SendCommand("0")
    robot.SendCommand("1")
    robot.SendCommand("2")
    robot.SendCommand("3")
    robot.SendCommand("4")
    robot.SendCommand("5")
    robot.SendCommand("6")
    robot.SendCommand("7")
    robot.SendCommand("8")
    robot.SendCommand("9")
 

def sendSequence():
    robot.sendCommand("2")
    robot.sendCommand("2")
    robot.sendCommand("6")
    robot.sendCommand("Menu")


main()