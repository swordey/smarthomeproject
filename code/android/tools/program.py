import sys
sys.path.append(r'./tools/')
from condition import *

class Program:
    def __init__(self,f_name = None):
        self.name = f_name
        self.running = False
        self.actuator = None
        self.conditions = []
        self.conditionOrder = ''

    def setupConnection(self):
        if self.actuator.connect():
            for condition in self.conditions:
                if not condition.connect():
                    return False
        else:
            return False
        return True

    def setActuator(self, f_actuator):
        self.actuator = f_actuator

    def isRunning(self):
        return self.running

    def start(self):
        self.running = True

    def stop(self):
        self.running = False

    def addCondition(self, f_condition):
        self.conditions.append(f_condition)

    def execute(self):
        for condition in self.conditions:
            if condition.checkCondition():
                self.actuator.changeState(condition.getValue())
                break

    def evaluate(self):
        evaluatedConditions = []
        for condition in self.conditions:
            evaluatedConditions.append(condition.checkCondition())
        condOrder = self.conditionOrder
        for condNumber in xrange(1,len(self.conditions)+1):
            condOrder = condOrder.replace("#c"+str(condNumber),evaluatedConditions[condNumber-1])
        return eval(condOrder)

    def toArray(self):
        data = {}
        data["programname"] = self.name
        data["running"] = self.running
        data["actuatorid"] = self.actuator.id
        data["conditions"] = [condition.toArray() for condition in self.conditions]
        return data

    def fromArray(self, f_array, f_sensors, f_actuators):
        for actuator in f_actuators:
            if f_array["actuatorid"] == actuator.id:
                self.actuator = actuator
                break
        self.name = f_array["programname"]
        self.running = f_array["running"]
        for condition in f_array["conditions"]:
            cond = Condition()
            cond.fromArray(condition, f_sensors)
            self.conditions.append(cond)

