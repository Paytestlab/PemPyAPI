from PinRobot import PinRobot

def main():
    robot = PinRobot()
    robot.InitializeTerminal("Yomani.xml")
    robot.InitializeConnection("localhost", 3000)
    robot.SendCommand("1")




main()