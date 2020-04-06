import time


class Condition:
    def __init__(self,f_id = None,f_type = None, f_value = None, f_condition = None):
        self.id = f_id
        self.type = f_type
        self.value = f_value
        self.isfired = False
        if f_type == "Sensor":
            self.sensor = f_condition["sensor"]
            self.condition = f_condition["condition"]
        elif f_type == "Date":
            self.time = f_condition

    def connect(self):
        if self.type == "Sensor":
            return self.sensor.connect()
        else:
            return True

    def close(self):
        if self.type == "Sensor":
            self.sensor.close()

    def getValue(self):
        return self.value

    def checkCondition(self):
        if self.type == "Sensor":
            if not self.sensor.updated:
                return False
            return bool(eval(str(self.sensor.data) + self.condition))
        elif self.type == "Date":
            isittime = time.strptime(time.strftime("%H:%M"), "%H:%M") == time.strptime(self.time, "%H:%M")
            if self.isfired:
                if not isittime:
                    self.isfired = False
                return False
            else:
                if isittime:
                    self.isfired = True
                return isittime
        return False

    def toArray(self):
        data = {}
        data["type"] = self.type
        data["value"] = self.value
        data["id"] = self.id
        if self.type == "Sensor":
            data["sensorid"] = self.sensor.id
            data["sensorcond"] = self.condition
        elif self.type == "Date":
            data["timecond"] = self.time
        return data

    def fromArray(self, f_array, f_sensors):
        self.type = f_array["type"]
        self.value = f_array["value"]
        self.id = f_array["id"]
        if self.type == "Sensor":
            for sensor in f_sensors:
                if f_array["sensorid"] == sensor.id:
                    self.sensor = sensor
                    break
            self.condition = f_array["sensorcond"]
        elif self.type == "Date":
            self.time = f_array["timecond"]

