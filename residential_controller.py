import time

class Column:
    def __init__(self, _id, _amountOfFloors, _amountOfElevators):
        self.ID = _id
        self.status = 'online'
        self.elevatorList = []
        self.callButtonList = []
        self.createElevators(_amountOfFloors, _amountOfElevators)
        self.createCallButtons(_amountOfFloors)
    
    def createCallButtons(self, _amountOfFloors):
        buttonFloor = 1
        callButtonID = 1
        for i in range (_amountOfFloors):
            if buttonFloor < _amountOfFloors:
                callButton = CallButton(callButtonID, buttonFloor, "Up")
                self.callButtonList.append(callButton)
                callButtonID += 1
            if buttonFloor > 1:
                callButton = CallButton(callButtonID, buttonFloor, "Down")
                self.callButtonList.append(callButton)
                callButtonID += 1
            buttonFloor += 1

    def createElevators(self, _amountOfFloors, _amountOfElevators):
        elevatorID = 1
        for i in range (_amountOfElevators):
            elevator = Elevator(elevatorID, _amountOfFloors)
            self.elevatorList.append(elevator)
            elevatorID += 1
    
    def requestElevator(self, floor, direction):
        elevator = self.findElevator(floor, direction)
        elevator.floorRequestList.append(floor)
        elevator.move()
        elevator.operateDoors()
        elevator.floorReauestList = []
        return elevator

    def findElevator(self, requestedFloor, requestedDirection):
        bestElevator = None
        bestScore = 5
        referenceGap = 10000000

        for elevator in self.elevatorList:
            #The elevator is at my floor and going in the direction I want
            if requestedFloor == elevator.currentFloor and elevator.status == "stopped" and requestedDirection == elevator.direction:
                bestElevator, bestScore, referenceGap = self.checkIfElevatorIsBetter(1, elevator, bestScore, referenceGap, bestElevator, requestedFloor)
            #The elevator is lower than me, is coming up and I want to go up
            elif requestedFloor > elevator.currentFloor and elevator.status == "Up" and requestedDirection == elevator.direction:
                bestElevator, bestScore, referenceGap = self.checkIfElevatorIsBetter(2, elevator, bestScore, referenceGap, bestElevator, requestedFloor)
            #The elevator is higher than me, is coming down and I want to go down
            elif requestedFloor < elevator.currentFloor and elevator.status == "Down" and requestedDirection == elevator.direction:
                bestElevator, bestScore, referenceGap = self.checkIfElevatorIsBetter(2, elevator, bestScore, referenceGap, bestElevator, requestedFloor)
            #The elevator is idle
            elif elevator.status == "idle":
                bestElevator, bestScore, referenceGap = self.checkIfElevatorIsBetter(3, elevator, bestScore, referenceGap, bestElevator, requestedFloor)
            #The elevator is not available, but still could take the call if nothing better is found
            else:
                bestElevator, bestScore, referenceGap = self.checkIfElevatorIsBetter(4, elevator, bestScore, referenceGap, bestElevator, requestedFloor)
        return bestElevator

    def checkIfElevatorIsBetter(self, scoreToCheck, newElevator, bestScore, referenceGap, bestElevator, floor):
        if scoreToCheck < bestScore:
            bestScore = scoreToCheck
            bestElevator = newElevator
            referenceGap = abs(newElevator.currentFloor - floor)
        elif bestScore == scoreToCheck:
            gap = abs(newElevator.currentFloor - floor)
            if referenceGap > gap:
                bestElevator = newElevator
                referenceGap = gap
        return bestElevator, bestScore, referenceGap

class Elevator:
    def __init__(self, _id, _amountOfFloors):
        self.ID = _id
        self.status = ''
        self.currentFloor = 1
        self.direction = None
        self.door = Door(_id)
        self.floorRequestButtonList = []
        self.floorRequestList = []
        self.screenDisplay = []
        self.createFloorRequestButtons(_amountOfFloors)

    def createFloorRequestButtons(self, _amountOfFloors):
        buttonFloor = 1
        floorRequestButtonID = 1 
        for i in range (_amountOfFloors):
            floorRequestButton = FloorRequestButton( floorRequestButtonID, buttonFloor)
            self.floorRequestButtonList.append(floorRequestButton)
            buttonFloor += 1
            floorRequestButtonID += 1
    
    def requestFloor(self, floor):
        self.floorRequestList.append(floor)
        self.move()
        self.operateDoors()

    def move(self):
        while len(self.floorRequestList) != 0:
            destination = self.floorRequestList[0]
            self.status = "moving"
            if self.currentFloor < destination:
                self.direction = "Up"
                self.sortFloorList()
                while self.currentFloor < destination:
                    self.currentFloor += 1
                    self.screenDisplay.append(self.currentFloor)
            elif self.currentFloor > destination:
                self.direction = "Down"
                self.sortFloorList()
                while self.currentFloor > destination:
                    self.currentFloor -= 1
                    self.screenDisplay.append(self.currentFloor)
            self.status = "stopped"
            self.floorRequestList.pop()
        self.status = "idle"
        self.floorRequestList = []

    def sortFloorList(self):
        if self.direction == "Up":
            self.floorRequestList.sort()
        else:
            self.floorRequestList.sort(reverse=True)

    def operateDoors(self):
        self.door.status = "opened"
        overweight = 350 #kg chosen at random
        obstruction = False #by default there is obstruction
        #time.sleep(5) wait five seconds --> not working
        if overweight < 600:
            self.door.status = "closing"
            if obstruction == False:
                self.door.status = "closed"
            else:
                self.operateDoors()
        else:
            while overweight == True:
                print("Activate overweight alarm")
            self.operateDoors()

        
class CallButton:
    def __init__(self, _id, _floor, _direction):
        self.ID = _id
        self.status = "OFF"
        self.floor = _floor
        self.direction = _direction

class FloorRequestButton:
    def __init__(self, _id, _floor):
        self.ID = _id
        self.status = "OFF"
        self.floor = _floor

class Door:
    def __init__(self, _id):
        self.ID = _id
        self.status = "closed"

# column = Column(1, 10, 2)
# column.elevatorList[0].currentFloor = 10
# column.elevatorList[1].currentFloor = 3
# column.elevatorList[0].status = 'idle'
# column.elevatorList[1].status = 'moving'
# column.elevatorList[1].direction = 'Up'
# elevator = column.requestElevator(3, 'Down')
# elevator.requestFloor(2)