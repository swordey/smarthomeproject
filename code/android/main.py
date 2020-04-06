from kivy.app import App
from kivy.uix.settings import SettingsWithSidebar
from kivy.uix.label import Label
from kivy.uix.dropdown import DropDown
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.switch import Switch
from kivy.uix.popup import Popup
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.checkbox import CheckBox
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager, NoTransition
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.carousel import Carousel
from kivy.core.window import Window

import json
import sys
import time
android = False

sys.path.append(r'./tools/')
from settingbutton import *
from scrolloptions import *
from sensor import *
from actuator import *
from condition import *
from serverclass import *
from program import *

Builder.load_string('''
<ProgramScreen>:
<ModulScreen>:
	FloatLayout:
		size_hint: 1, 1
		pos_hint: {'center_x': .5, 'center_y': .5}
		Button:
			pos_hint: {"x": 0.90, "y": 0.95}
			on_release: app.open_settings()
			size_hint: 0.1, 0.05
			background_normal: "./pictures/settings_orig.png"
			background_down: "./pictures/settings.png"
			border: 0,0,0,0
        Label:
            id: programname
            size_hint: 0.5, 0.025
			pos_hint: {"x": 0, "y": 0.975}
        Label:
            id: actuatorname
            size_hint: 0.5, 0.025
			pos_hint: {"x": 0, "y": 0.95}
        Button:
            text: 'Add'
            id: addbtn
			size_hint: (0.45, 0.17)
			pos_hint: {'x': 0.5, 'y': 0.05}
			on_release: root.myparent.addCondition(self)
        Button:
            text: 'Back'
            id: savebtn
			size_hint: (0.45, 0.17)
			pos_hint: {'x': 0.05, 'y': 0.05}
			on_release: root.myparent.openProgramPage(self)

		
''')

class ProgramScreen(Screen):
    def __init__(self, f_parent, *args, **kargs):
        super(ProgramScreen, self).__init__(*args, **kargs)
        self.myparent = f_parent
        self.carousel = Carousel(direction='right', size_hint=(1,1), pos_hint={'x':0,'y':0})
        self.floatLayoutPrograms = FloatLayout(id='program',size_hint=(1, 1))

        self.scrollLayoutSensors = ScrollView(id='sensor', size_hint=(1,1))
        self.gridLayoutSensors = GridLayout(cols=1,spacing=10, size_hint=(1,1))
        # self.gridLayoutSensors.bind(minimum_height=self.gridLayoutSensors.setter('height'))
        self.scrollLayoutSensors.add_widget(self.gridLayoutSensors)

        self.floatLayoutSensors = FloatLayout(id='sensor',size_hint=(1, 1))

        self.floatLayoutActuators = FloatLayout(id='actuator',size_hint=(1, 1))

        # self.carousel.add_widget(self.floatLayoutSensors)
        self.carousel.add_widget(self.scrollLayoutSensors)
        self.carousel.add_widget(self.floatLayoutActuators)
        self.carousel.add_widget(self.floatLayoutPrograms)
        self.gridLayoutConditions = GridLayout(cols=1,size_hint=(1, 0.92),pos_hint={"x": 0, "y": 0})
        self.floatLayoutPrograms.add_widget(self.gridLayoutConditions)
        self.add_widget(self.carousel)
        self.buttonP = []
        self.buttonS = []
        self.labelsP = []
        self.buttonA = []
        self.tbuttonsP = []
        self.labelsS = []
        self.labelsA = []
        self.tbuttonsA = []
        self.lastSensorCount = 0

        self.selectedProgramName = ''

    def changeProgram(self, data, instance):
        self.selectedProgramName = instance

    def updateProgramScreen(self):
        for x in self.labelsP:
            self.gridLayoutConditions.remove_widget(x)
        for x in self.buttonP:
            self.floatLayoutPrograms.remove_widget(x)
        for x in self.tbuttonsP:
            self.floatLayoutPrograms.remove_widget(x)

        settingsButton = Button(background_normal="./pictures/settings_orig.png", background_down="./pictures/settings.png",
                                border=(0,0,0,0), size_hint=(0.16,0.08), pos_hint={"x": 0.84, "y": 0.92},
                                on_release=self.myparent.open_settings)

        self.floatLayoutPrograms.add_widget(settingsButton)
        self.buttonP.append(settingsButton)

        programName = "Programs" if self.selectedProgramName == '' else self.selectedProgramName

        programButton = Button(text=programName, size_hint=(0.26, 0.08), pos_hint={'x': 0, 'y': 0.92})
        drop = DropDown()
        for program in self.myparent.programs:
            btnn = Button(text=program.name, size_hint_y=None, height=44)
            btnn.bind(on_release=lambda btnn: drop.select(btnn.text))
            drop.add_widget(btnn)

        programButton.bind(on_release=drop.open)
        drop.bind(on_select=self.changeProgram)



        addButton = Button(background_normal="./pictures/add.png", size_hint=(0.16,0.08),border=(0,0,0,0),
                           pos_hint={"x": 0.36, "y": 0.92})
        addButton.bind(on_release=self.myparent.addProgram)

        self.floatLayoutPrograms.add_widget(programButton)
        self.floatLayoutPrograms.add_widget(addButton)
        self.buttonP.append(programButton)
        self.buttonP.append(addButton)

        if programName is not "Programs":

            delbutton = Button(background_normal="./pictures/x.png",
                               pos_hint={'x': 0.68, 'y': 0.92},border=(0,0,0,0),
                               size_hint=(0.16, 0.08))
            delbutton.bind(on_release=self.myparent.delProgram)
            delbutton.id = programName
            editbutton = Button(background_normal="./pictures/edit.png",
                                pos_hint={'x': 0.52, 'y': 0.92},border=(0,0,0,0),
                                size_hint=(0.16, 0.08))
            editbutton.bind(on_release=self.myparent.editProgram)
            editbutton.id = programName

            self.floatLayoutPrograms.add_widget(delbutton)
            self.floatLayoutPrograms.add_widget(editbutton)
            self.buttonP.append(delbutton)
            self.buttonP.append(editbutton)

            selectedProgram = None
            for program in self.myparent.programs:
                if program.name is self.selectedProgramName:
                    selectedProgram = program
                    break


            if selectedProgram is not None:
                runTButton = ToggleButton(text="Run", size_hint=(0.1, 0.08), pos_hint={'x': 0.26, 'y': 0.92})
                runTButton.state = 'down' if selectedProgram.running else 'normal'
                runTButton.text = 'Stop' if selectedProgram.running else 'Run'
                runTButton.bind(on_release=self.myparent.changeProgramState)
                runTButton.id = selectedProgram.name
                self.tbuttonsP.append(runTButton)
                self.floatLayoutPrograms.add_widget(runTButton)

                for condition in selectedProgram.conditions:
                    if condition.type == "Sensor":
                        label = Label(text=condition.sensor.name + " ( " + condition.condition + " )\n"+condition.sensor.getData())
                        label.font_size = '40sp'
                        label.texture_update()
                        self.labelsP.append(label)
                        self.gridLayoutConditions.add_widget(label)

                        # label = Label(text=condition.sensor.name + " ( " + condition.condition + " )",
                        #                pos_hint={'x': 0, 'y': 0.95 - counter * blockHeight - blockHeight},
                        #                size_hint=(0.5, blockHeight))
                        # label.font_size = '20sp'
                        # label.texture_update()
                        # label1 = Label(text=condition.sensor.getData(),
                        #                pos_hint={'x': 0.50, 'y': 0.95 - counter * blockHeight - blockHeight},
                        #                size_hint=(0.5, blockHeight))
                        # label1.font_size = '20sp'
                        # label1.texture_update()
                        # self.floatLayoutPrograms.add_widget(label)
                        # self.floatLayoutPrograms.add_widget(label1)
                        # self.labelsP.append(label)
                        # self.labelsP.append(label1)
                    elif condition.type == "Date":

                        label = Label(text='Time ( ' + condition.time + ' )\n'+time.strftime("%H:%M:%S"))
                        label.font_size = '40sp'
                        label.texture_update()
                        self.labelsP.append(label)
                        self.gridLayoutConditions.add_widget(label)

    def updateSensorScreen(self):
        if not len(self.myparent.sensors) == self.lastSensorCount:
            self.lastSensorCount = len(self.myparent.sensors)
            for x in self.labelsS:
                self.gridLayoutSensors.remove_widget(x)

            for sensorNr in xrange(len(self.myparent.sensors)):
                label = Label(text=self.myparent.sensors[sensorNr].toString(), size_hint_y=None, height=50)
                              # pos_hint={'x': 0, 'y': 0.95 - (sensorNr + 1) * 0.2},
                label.id = self.myparent.sensors[sensorNr].id
                label.font_size = '30sp'
                label.texture_update()
                self.labelsS.append(label)
                self.gridLayoutSensors.add_widget(label)
        else:
            for sensorNr in xrange(len(self.myparent.sensors)):
                if not self.myparent.sensors[sensorNr].updated:
                    continue

                for label in self.labelsS:
                    if label.id == self.myparent.sensors[sensorNr].id:
                        label.text = self.myparent.sensors[sensorNr].toString()

    def updateActuatorScreen(self):
        for x in self.labelsA:
            self.floatLayoutActuators.remove_widget(x)
        for x in self.tbuttonsA:
            self.floatLayoutActuators.remove_widget(x)
        for x in self.buttonA:
            self.floatLayoutActuators.remove_widget(x)

        settingsButton = Button(background_normal="./pictures/settings_orig.png",
                                background_down="./pictures/settings.png",
                                border=(0, 0, 0, 0), size_hint=(0.1, 0.05), pos_hint={"x": 0.90, "y": 0.95},
                                on_release=self.myparent.open_settings)

        self.floatLayoutActuators.add_widget(settingsButton)
        self.buttonA.append(settingsButton)

        for actuatorNr in xrange(len(self.myparent.actuators)):
            label = Label(text=self.myparent.actuators[actuatorNr].name,
                          pos_hint={'x': 0, 'y': 0.95 - (actuatorNr + 1) * 0.2},
                          size_hint=(0.5, 0.2))
            label.font_size = '30sp'
            label.texture_update()
            button = ToggleButton(text='On' if self.myparent.actuators[actuatorNr].state == 'on' else 'Off',
                                  pos_hint={'x': 0.5, 'y': 0.95 - (actuatorNr + 1) * 0.2},
                                  size_hint=(0.5, 0.2))
            button.state = 'down' if self.myparent.actuators[actuatorNr].state == 'on' else 'normal'
            button.id = self.myparent.actuators[actuatorNr].id
            button.bind(on_release=self.changeActuatorState)
            self.tbuttonsA.append(button)
            self.labelsA.append(label)
            self.floatLayoutActuators.add_widget(label)
            self.floatLayoutActuators.add_widget(button)

    def updateScreen(self):
        if self.carousel.current_slide.id == 'program':
            self.updateProgramScreen()
        elif self.carousel.current_slide.id == 'sensor':
            self.updateSensorScreen()
        elif self.carousel.current_slide.id == 'actuator':
            self.updateActuatorScreen()

    def changeActuatorState(self, instance):
        for actuatorIndex in xrange(len(self.myparent.actuators)):
            if self.myparent.actuators[actuatorIndex].id == instance.id:
                if instance.state == "down":
                    if self.myparent.actuators[actuatorIndex].connect():
                        if self.myparent.actuators[actuatorIndex].changeState('on'):
                            instance.text = 'On'
                    else:
                        instance.state = "normal"
                else:
                    if self.myparent.actuators[actuatorIndex].connect():
                        if self.myparent.actuators[actuatorIndex].changeState('off'):
                            instance.text = 'Off'
                    else:
                        instance.state = "down"


class ModulScreen(Screen):
    def __init__(self, f_parent, *args, **kargs):
        super(ModulScreen, self).__init__(*args, **kargs)
        self.myparent = f_parent
        self.labels = []
        self.tbutton = []
        self.button = []
        self.floatLayout = FloatLayout(size_hint=(1, 1))
        self.add_widget(self.floatLayout)
        self.currentProgram = ''
        self.currentActuator = 'AsdAsd'
        self.currentProgramNr = None
        # self.ids["'tab2'"].add_widget(self.floatLayout)

    def updateScreen(self):
        for x in self.labels:
            self.floatLayout.remove_widget(x)
        for x in self.tbutton:
            self.floatLayout.remove_widget(x)
        for x in self.button:
            self.floatLayout.remove_widget(x)

        self.ids["programname"].text = self.currentProgram
        self.ids["actuatorname"].text = self.currentActuator

        if self.currentProgramNr is not None:
            for x in xrange(len(self.myparent.programs[self.currentProgramNr].conditions)):
                height = 0.15
                stateLabel = Label(text = self.myparent.programs[self.currentProgramNr].conditions[x].value,
                              pos_hint={'x':0.05,'y':0.95 - (x + 1) * height},
                              size_hint = (0.1,height))

                self.floatLayout.add_widget(stateLabel)
                self.labels.append(stateLabel)

                if self.myparent.programs[self.currentProgramNr].conditions[x].type == "Sensor":
                    sensorLabel = Label(text = self.myparent.programs[self.currentProgramNr].conditions[x].sensor.name,
                              pos_hint={'x':0.15,'y':0.95 - (x + 1) * height},
                              size_hint = (0.325,height))
                    sensorConditionLabel = Label(text=self.myparent.programs[self.currentProgramNr].conditions[x].condition,
                                        pos_hint={'x': 0.475, 'y': 0.95 - (x + 1) * height},
                                        size_hint=(0.325, height))
                    self.floatLayout.add_widget(sensorLabel)
                    self.floatLayout.add_widget(sensorConditionLabel)
                    self.labels.append(sensorLabel)
                    self.labels.append(sensorConditionLabel)
                elif self.myparent.programs[self.currentProgramNr].conditions[x].type == "Date":
                    timeLabel = Label(text = "Time",
                              pos_hint={'x':0.15,'y':0.95 - (x + 1) * height},
                              size_hint = (0.325,height))
                    timeConditionLabel = Label(text=self.myparent.programs[self.currentProgramNr].conditions[x].time,
                                        pos_hint={'x': 0.475, 'y': 0.95 - (x + 1) * height},
                                        size_hint=(0.325, height))
                    self.floatLayout.add_widget(timeLabel)
                    self.floatLayout.add_widget(timeConditionLabel)
                    self.labels.append(timeLabel)
                    self.labels.append(timeConditionLabel)
                elif self.myparent.programs[self.currentProgramNr].conditions[x].type == "Button":
                    buttonLabel = Label(text="Button",
                                      pos_hint={'x': 0.15, 'y': 0.95 - (x + 1) * height},
                                      size_hint=(0.325, height))
                    self.floatLayout.add_widget(buttonLabel)
                    self.labels.append(buttonLabel)

                editbutton = Button(background_normal="./pictures/edit.png",
                                   pos_hint={'x': 0.80, 'y': 0.95 - (x + 1) * height + height/2},
                                   size_hint=(0.20, height/2))
                editbutton.bind(on_release=self.myparent.editCondition)
                editbutton.id = self.myparent.programs[self.currentProgramNr].conditions[x].id

                delbutton = Button(background_normal="./pictures/x.png",
                                   pos_hint={'x': 0.80, 'y': 0.95 - (x + 1) * height},
                                   size_hint=(0.20, height/2))
                delbutton.bind(on_release=self.myparent.delCondition)
                delbutton.id = self.myparent.programs[self.currentProgramNr].conditions[x].id

                self.floatLayout.add_widget(editbutton)
                self.floatLayout.add_widget(delbutton)
                self.button.append(editbutton)
                self.button.append(delbutton)

class AddModulScreen(Screen):
    def __init__(self, f_parent, *args, **kargs):
        super(AddModulScreen, self).__init__(*args, **kargs)
        self.myparent = f_parent
        self.floatLayout = FloatLayout(size_hint=(1, 1))
        self.add_widget(self.floatLayout)
        self.currentCondition = None
        self.widgets = []

        self.typelabel = Label(text='Type:', size_hint=(0.45, 0.17), pos_hint={'x':0.05,'y':0.73})
        self.sensorlabel = Label(text='Sensor name:', size_hint=(0.45, 0.17), pos_hint={'x':-1,'y':0.56})
        self.sensorcondlabel = Label(text='Condition:', size_hint=(0.45, 0.17), pos_hint={'x':-1,'y':0.39})
        self.timecondlabel = Label(text='Condition (hh:mm):', size_hint=(0.45, 0.34), pos_hint={'x':0.05,'y':0.22})

        self.floatLayout.add_widget(self.typelabel)
        self.floatLayout.add_widget(self.sensorlabel)
        self.floatLayout.add_widget(self.sensorcondlabel)
        self.floatLayout.add_widget(self.timecondlabel)

        self.condbtn = Button(text="Select", size_hint=(0.45, 0.17), pos_hint={'x': 0.5, 'y': 0.73})
        self.typedd = DropDown()
        choosableTypes = ["Sensor", "Date", "Button"]
        for type in choosableTypes:
            btnn = Button(text=type, size_hint_y=None, height='48dp')
            btnn.bind(on_release=lambda btnn: self.typedd.select(btnn.text))
            self.typedd.add_widget(btnn)

        # self.typedd.bind(on_select=lambda instance, x: setattr(self.condbtn, 'text', x))
        self.typedd.bind(on_select=self.updateScreen)
        self.condbtn.bind(on_release=self.typedd.open)

        self.sensorbtn = Button(text="Select", size_hint=(0.45, 0.17), pos_hint={'x': -1, 'y': 0.56})
        self.actuatorcomm = Button(text="Select", size_hint= (0.45, 0.17),pos_hint= {'x': 0.5, 'y': 0.22})
        self.backbtn = Button(text="Back", size_hint= (0.45, 0.17),pos_hint= {'x': 0.05, 'y': 0.05})
        self.backbtn.bind(on_release=self.myparent.openModulPage)
        self.savebtn = Button(text="Save", size_hint= (0.45, 0.17),pos_hint= {'x': 0.5, 'y': 0.05})
        self.savebtn.bind(on_release=self.myparent.saveCondition)

        self.floatLayout.add_widget(self.sensorbtn)
        self.floatLayout.add_widget(self.actuatorcomm)
        self.floatLayout.add_widget(self.condbtn)
        self.floatLayout.add_widget(self.backbtn)
        self.floatLayout.add_widget(self.savebtn)

        self.timecond = TextInput(text="Type",  size_hint=(0.45,  0.34), pos_hint= {'x': -1, 'y': 0.39})
        self.sensorcond = TextInput(text="Type", size_hint=(0.45, 0.17), pos_hint={'x': -1, 'y': 0.39})
        self.floatLayout.add_widget(self.timecond)
        self.floatLayout.add_widget(self.sensorcond)

    def updateScreen(self, instance="Select condition", condition = None):
        # Set text of dropdown button
        if condition is None:
            self.condbtn.text = instance
            conditionType = instance
        elif isinstance(condition, basestring):
            self.condbtn.text = condition
            conditionType = condition
        else:
            self.condbtn.text = condition.type
            conditionType = condition.type


        # Move every widget out
        self.timecond.pos_hint = {'x': -1, 'y': 0.39}
        self.timecondlabel.pos_hint = {'x': -1, 'y': 0.39}
        self.sensorbtn.pos_hint = {'x': -1, 'y': 0.56}
        self.sensorlabel.pos_hint = {'x': -1, 'y': 0.56}
        self.sensorcondlabel.pos_hint = {'x': -1, 'y': 0.39}
        self.sensorcond.pos_hint = {'x': -1, 'y': 0.39}

        if conditionType == "Select condition":
            pass
        elif conditionType == "Sensor":
            # Sensor
            drop1 = DropDown()
            for sensor in self.myparent.sensors:
                btnn = Button(text=str(sensor.id), size_hint_y=None, height=44)
                btnn.bind(on_release=lambda btnn: drop1.select(btnn.text))
                drop1.add_widget(btnn)

            self.sensorbtn.bind(on_release=drop1.open)
            self.sensorbtn.pos_hint = {'x':0.5,'y':0.56}
            self.sensorbtn.text = 'Select'
            self.sensorlabel.pos_hint = {'x':0.05,'y':0.56}
            drop1.bind(on_select=lambda instance, x: setattr(self.sensorbtn, 'text', x))
            # Condition
            self.sensorcond.pos_hint = {'x': 0.5, 'y': 0.39}
            self.sensorcond.text = 'Type'
            self.sensorcondlabel.pos_hint = {'x': 0.05, 'y': 0.39}

            # Set if condition exists
            if not isinstance(condition, basestring) and condition is not None:
                self.sensorbtn.text = condition.sensor.id
                self.sensorcond.text = condition.condition
        elif conditionType == "Date":
            self.timecondlabel.pos_hint = {'x': 0.05, 'y': 0.39}
            self.timecond.pos_hint = {'x': 0.5, 'y': 0.39}
            self.timecond.text = 'Type'

            # Set if condition exists
            if not isinstance(condition, basestring) and condition is not None:
                self.timecond.text = condition.time
        elif conditionType == "button":
            pass

        drop2 = DropDown()
        for actuator in self.myparent.actuators:
            for comm in actuator.commands:
                btnn = Button(text=comm, size_hint_y=None, height=44)
                btnn.bind(on_release=lambda btnn: drop2.select(btnn.text))
                drop2.add_widget(btnn)

        self.actuatorcomm.bind(on_release=drop2.open)
        drop2.bind(on_select=lambda instance, x: setattr(self.actuatorcomm, 'text', x))
        self.actuatorcomm.text = 'Select'
        if not isinstance(condition, basestring) and condition is not None:
            self.actuatorcomm.text = condition.value

class SmartHomeApp(App):
    def __init__(self,*args, **kargs):
        super(SmartHomeApp, self).__init__(*args, **kargs)
        self.sensorCount = 0
        self.actuatorCount = 0
        self.conditionCount = 0
        self.programCount = 0
        self.buttonInitialized = False
        self.settings = []
        self.settingsFileName = "./smarthome.ini"
        self.sensorDataFileName = "./config/sensordata.txt"
        self.actuatorDataFileName = "./config/actuatordata.txt"
        self.modulDataFileName = "./config/moduldata.txt"
        self.programDataFileName = "./config/programdata.txt"
        self.settingsJson = "./config/settings.json"
        self.sensors = []
        self.actuators = []
        self.moduls = []
        self.programs = []
        self.currentSensorOption = ''
        self.currentActuatorOption = ''
        self.use_kivy_settings = False
        self.smarthomegui = []
        self.config = None
        self.incomingData = []
        self.firstRun = True

        # Receiving server
        self.server = Server(self)
        self.server.startThread()
        self.dataReadingEvent = None
        self.modulScreen = ModulScreen(self, name='ModulPage')
        self.addModulScreen = AddModulScreen(self, name='AddModulPage')
        self.programScreen = ProgramScreen(self, name = "ProgramPage")

        self.sm = ScreenManager()
        # progScreen = Screen("ProgramPage")
        # sm.add_widget(progScreen)
        self.sm.add_widget(self.modulScreen)
        self.sm.add_widget(self.addModulScreen)
        self.sm.add_widget(self.programScreen)
        self.sm.current = "ProgramPage"

    # Builds
    def build(self):
        self.settings_cls = SettingsWithSidebar
        self.loadSensorData()
        self.loadActuatorData()
        self.loadProgramData()
        self.modulScreen.updateScreen()
        self.addModulScreen.updateScreen()
        self.programScreen.updateProgramScreen()
        self.programScreen.updateSensorScreen()
        self.programScreen.updateActuatorScreen()
        self.startReading()
        return self.sm

    def build_config(self,config):
        config.read(self.settingsFileName)
        self.currentSensorOption = config.getdefault("default","options",-1)
        self.currentActuatorOption = config.getdefault("default","options1",-1)
        self.config = config

    def build_settings(self,settings):
        self.settings = settings
        self.settings.register_type('buttons', SettingButtons)
        self.settings.register_type('scrolloptions', SettingScrollOptions)
        self.settings.add_json_panel('SmartHome',
                                self.config,
                                self.settingsJson)

    def notify(self,f_title, f_msg):
        if android:
            droid.makeToast(f_msg)
            droid.notify(f_title, f_msg)
        else:
            self.showMsg(f_title,f_msg)

    def showMsg(self, f_title, f_msg):
        content = BoxLayout(orientation='vertical')
        label = Label(text=f_msg)
        content.add_widget(label)
        buttonOk = Button(text="Ok", size_hint_y=None, height=50)
        content.add_widget(buttonOk)
        popup = Popup(content=content, title=f_title,
                      size_hint=(None, None), size=(500, 500),
                      auto_dismiss=False)
        buttonOk.bind(on_release=popup.dismiss)
        popup.open()

    # Settings changing
    def on_config_change(self, config, section, key, value):
        print config, section, key, value
        if 'add_sensor' in value:
            self.addSensor()
        elif 'del_sensor' in value:
            self.delSensor()
        elif 'add_actuator' in value:
            self.addActuator()
        elif 'del_actuator' in value:
            self.delActuator()
        elif 'get_command_actuator' in value:
            for actuator in self.actuators:
                if self.currentActuatorOption in actuator.id:
                    actuator.getCommandFromModul()
                    config.set('actuator', 'commands','|'.join(actuator.commands))
                    config.write()
                    interface = self.settings.interface
                    interface.children[0].children[0].children[0].children[1].value = '|'.join(actuator.commands)
                    self.saveActuatorData()
        elif 'options1' in key:
            self.currentActuatorOption = value.replace('\n','')
            for actuator in self.actuators:
                if self.currentActuatorOption in actuator.id:
                    config.set('actuator', 'name', actuator.name)
                    config.set('actuator', 'ip', actuator.sock.getip())
                    config.write()
                    interface = self.settings.interface
                    interface.children[0].children[0].children[0].children[2].value = actuator.sock.getip()
                    interface.children[0].children[0].children[0].children[3].value = actuator.name
                    break
        elif 'options' in key:
            self.currentSensorOption = value.replace('\n','')
            for sensor in self.sensors:
                if self.currentSensorOption in sensor.id:
                    config.set('sensor', 'name', sensor.name)
                    config.set('sensor', 'ip', sensor.sock.getip())
                    config.set('sensor', 'unit', sensor.unit)
                    config.set('sensor', 'receiving', str(int(sensor.receiving)))
                    config.write()
                    interface = self.settings.interface
                    interface.children[0].children[0].children[0].children[8].value = sensor.unit
                    interface.children[0].children[0].children[0].children[9].value = sensor.sock.getip()
                    interface.children[0].children[0].children[0].children[10].value = sensor.name
                    interface.children[0].children[0].children[0].children[7].value = str(int(sensor.receiving))
                    break
        else:
            if 'default' != value:
                if "sensor" in section:
                    for x in xrange(len(self.sensors)):
                        if self.currentSensorOption in self.sensors[x].id:
                            if "receiving" in key:
                                value = int(value)
                                if 1 == value:
                                    if self.sensors[x].connect():
                                        config.set(section, key, str(value))
                                        config.write()
                                        self.sensors[x].start_receiving()
                                    else:
                                        interface = self.settings.interface
                                        interface.children[0].children[0].children[0].children[3].value = str(
                                            0)
                                else:
                                    config.set(section, key, str(value))
                                    config.write()
                                    self.sensors[x].close()
                                    self.sensors[x].stop_receiving()
                            elif "ip" in key:
                                self.sensors[x].setip(value)
                            else:
                                setattr(self.sensors[x], key, value)
                                config.set(section, key, str(value))
                                config.write()
                            break
                    self.saveSensorData()
                elif "actuator" in section:
                    for x in xrange(len(self.actuators)):
                        if self.currentActuatorOption in self.actuators[x].id:
                            if "ip" in key:
                                self.actuators[x].setip(value)
                            else:
                                setattr(self.actuators[x], key, value)
                            config.set(section, key, str(value))
                            config.write()
                    self.saveActuatorData()
                # self.updateEventStatus()

    def updateEventStatus(self):
        receivingSensors = [sensor for sensor in self.sensors if sensor.receiving]
        receivingSensorNumber = len(receivingSensors)
        if self.dataReadingEvent is None and receivingSensorNumber > 0:
            self.startReading()
        elif self.dataReadingEvent is not None and receivingSensorNumber == 0:
            self.stopReading()

    def close_settings(self, settings):
        super(SmartHomeApp, self).close_settings(settings)
        self.modulScreen.updateScreen()
        # self.smarthomegui.updateGUI()

    def refresh(self, dt):
        self.programScreen.updateScreen()

    # Data processing
    def startReading(self):
        self.dataReadingEvent = Clock.schedule_interval(self.readData, 0.5)

    def stopReading(self):
        self.dataReadingEvent.cancel()
        self.dataReadingEvent = None

    def readData(self, dt):
        runningPrograms = [program for program in self.programs if program.running == True]
        if len(self.incomingData) > 0:
            print '\r Buffer count:',len(self.incomingData),
            inputJson = self.incomingData[0]
            self.decodeData(inputJson)
            self.incomingData.pop(0)

        if len(runningPrograms) > 0:
            self.checkConditions()
        self.programScreen.updateScreen()
        # self.processData()
        # self.smarthomegui.updateGUI()
        # self.modulScreen.updateScreen()


    def checkConditions(self):
        for program in self.programs:
            if program.isRunning():
                program.execute()

    def processData(self):
        pass

    def decodeData(self, f_dataString):
        try:
            output = json.loads(f_dataString)
            output = output[0]
            for x in xrange(len(self.sensors)):
                if output["deviceid"] == self.sensors[x].id:
                    self.sensors[x].data = output["data"]
                    self.sensors[x].unit = output["unit"]
                    self.sensors[x].updated = 1
        except Exception as e:
            print e,

    def loadSensorData(self):
        with open(self.sensorDataFileName, 'r') as file:
            jsonInput = json.load(file)
            for data in jsonInput:
                sensor = Sensor(self)
                sensor.fromArray(data)
                self.sensors.append(sensor)
                self.sensorCount += 1

    def loadActuatorData(self):
        with open(self.actuatorDataFileName, 'r') as file:
            jsonInput = json.load(file)
            for data in jsonInput:
                actuator = Actuator(self)
                actuator.fromArray(data)
                self.actuators.append(actuator)
                self.actuatorCount += 1

    def loadProgramData(self):
        with open(self.programDataFileName, 'r') as file:
            jsonInput = json.load(file)
            for data in jsonInput:
                program = Program(self)
                program.fromArray(data, self.sensors, self.actuators)
                self.programs.append(program)
                self.programCount += 1

    # def loadModulData(self):
    #     with open(self.modulDataFileName, 'r') as file:
    #         jsonInput = json.load(file)
    #         for data in jsonInput:
    #             modul = Modul(self)
    #             modul.fromArray(data, self.sensors, self.actuators)
    #             self.moduls.append(modul)
    #             self.modulCount += 1

    def connectOnStartUp(self):
        receivingSensors = [sensor for sensor in self.sensors if sensor.receiving]
        for sensor in receivingSensors:
            if not sensor.connect():
                sensor.stop_receiving()
                if sensor.id == self.config.getdefault('default', 'options', ''):
                    self.config.set('sensor', 'receiving', str(0))
        self.saveSensorData()
        self.smarthomegui.updateGUI()

    # Operation with sensors
    def addSensor(self):
        self.sensorCount += 1
        self.sensors.append(Sensor(self,'sensor'+str(self.sensorCount),'localhost','-'))
        self.saveSensorData()

    def delSensor(self):
        for sensorIndex in xrange(len(self.sensors)):
            if self.sensors[sensorIndex].id == self.currentSensorOption:
                self.sensors.pop(sensorIndex)
                break
        self.saveSensorData()

    def saveSensorData(self):
        with open(self.sensorDataFileName,'w') as file:
            jsonOut = []
            for sensor in self.sensors:
                jsonOut.append(sensor.toArray())
            json.dump(jsonOut, file)

    # Operation with actuators
    def addActuator(self):
        self.actuatorCount += 1
        self.actuators.append(Actuator(self,'actuator'+str(self.actuatorCount),'localhost'))
        self.saveActuatorData()

    def delActuator(self):
        for actuatorIndex in xrange(len(self.actuators)):
            if self.actuators[actuatorIndex].id == self.currentActuatorOption:
                self.actuators.pop(actuatorIndex)
                break
        self.saveActuatorData()

    def saveActuatorData(self):
        with open(self.actuatorDataFileName,'w') as file:
            jsonOut = []
            for actuator in self.actuators:
                jsonOut.append(actuator.toArray())
            json.dump(jsonOut, file)

    def saveCondition(self, instance):
        # Get condition name
        if self.addModulScreen.currentCondition is None:
            conditionName = 'Cond'+str(self.conditionCount)
            self.conditionCount += 1
        else:
            conditionName = self.addModulScreen.currentCondition


        # Get condition type
        conditionType = self.addModulScreen.condbtn.text
        command = self.addModulScreen.actuatorcomm.text

        # Check if it is changed
        if conditionType == "Select" or command == "Select":
            return

        if conditionType == "Sensor":
            sensorName = self.addModulScreen.sensorbtn.text
            sensorCond = self.addModulScreen.sensorcond.text

            choosenSensor = None
            for sensor in self.sensors:
                if sensor.id in sensorName:
                    choosenSensor = sensor
                    break
            if choosenSensor is None or sensorCond == "Condition":
                return

            condition = Condition(conditionName,conditionType, command, {"sensor" : choosenSensor, "condition" : sensorCond})

        elif conditionType == "Date":
            datecond = self.addModulScreen.timecond.text
            if datecond == "Time":
                return
            condition = Condition(conditionName,conditionType, command, datecond)
        elif conditionType == "Button":
            condition = Condition(conditionName,conditionType, command)
        self.conditionCount += 1
        self.programs = self.saveConditionData(self.programs,self.modulScreen.currentProgramNr,condition)
        # self.programs[instance.parent.parent.myparent.modulScreen.currentProgramNr].addCondition(condition)
        self.saveProgramData()
        self.openModulPage()

    def saveConditionData(self, f_programs, f_programNr, f_condition):
        for conditionNr in xrange(len(f_programs[f_programNr].conditions)):
            if f_programs[f_programNr].conditions[conditionNr].id == f_condition.id:
                f_programs[f_programNr].conditions[conditionNr] = f_condition
                return f_programs
        f_programs[f_programNr].addCondition(f_condition)
        return f_programs

    # def saveModul(self, instance):
    #     # Get condition type
    #     conditionType = instance.parent.parent.ids["condbtn"].text
    #
    #     # Check if it is changed
    #     if conditionType == "Condition":
    #         return
    #
    #     actuatorName = instance.parent.parent.ids["actuatorbtn"].text
    #     choosenActuator = None
    #     for actuator in self.actuators:
    #         if actuator.id in actuatorName:
    #             choosenActuator = actuator
    #             break
    #
    #     command = instance.parent.parent.ids["actuatorcomm"].text
    #
    #     if choosenActuator is None or command == "Condition":
    #         return
    #
    #     if conditionType == "Sensor":
    #         sensorName = instance.parent.parent.ids["sensorbtn"].text
    #         sensorCond = instance.parent.parent.ids["sensorcond"].text
    #
    #         choosenSensor = None
    #         for sensor in self.sensors:
    #             if sensor.id in sensorName:
    #                 choosenSensor = sensor
    #                 break
    #         if choosenSensor is None or sensorCond == "Condition":
    #             return
    #
    #         modul = Modul('Module' + str(self.modulCount),conditionType, {"sensor" : choosenSensor, "condition" : sensorCond}, choosenActuator, command)
    #
    #     elif conditionType == "Date":
    #         datecond = instance.parent.parent.ids["timecond"].text
    #         if datecond == "Time (hh:mm)":
    #             return
    #         modul = Modul('Module' + str(self.modulCount), conditionType,datecond, choosenActuator, command)
    #     elif conditionType == "Button":
    #         modul = Modul('Module' + str(self.modulCount), conditionType, [], choosenActuator, command)
    #     self.modulCount += 1
    #     self.programs[instance.parent.parent.myparent.modulScreen.currentProgramNr].addModul(modul)
    #     self.saveProgramData()
    #     self.modulScreen.updateScreen()
    #     self.sm.current = 'ModulPage'
    #     self.sm.do_layout()

    # def saveModul2(self, instance):
    #     sensorName = instance.children[0].children[0].children[0].children[4].text
    #     condition = instance.children[0].children[0].children[0].children[3].text
    #     actuatorName = instance.children[0].children[0].children[0].children[2].text
    #     command = instance.children[0].children[0].children[0].children[1].text
    #
    #     choosenSensor = None
    #     for sensor in self.sensors:
    #         if sensor.id in sensorName:
    #             choosenSensor = sensor
    #             break
    #     choosenActuator = None
    #     for actuator in self.actuators:
    #         if actuator.name in actuatorName:
    #             choosenActuator = actuator
    #             break
    #     if choosenActuator is None or choosenSensor is None or condition in "Condition" or command in "Command":
    #         return
    #     modul = Modul('Module'+str(self.modulCount),choosenSensor,condition,choosenActuator,command)
    #     self.modulCount += 1
    #     self.moduls.append(modul)
    #     self.saveModulData()
    #     self.modulScreen.updateScreen()





    # def addModul(self, instance):
    #     content = FloatLayout(size_hint=(1,1))
    #     drop = DropDown()
    #     btnn = Button(text="sensor", size_hint_y=None, height=44)
    #     btnn.bind(on_release=lambda btnn: drop.select(btnn.text))
    #     drop.add_widget(btnn)
    #     btnn = Button(text="data", size_hint_y=None, height=44)
    #     btnn.bind(on_release=lambda btnn: drop.select(btnn.text))
    #     drop.add_widget(btnn)
    #     btnn = Button(text="button", size_hint_y=None, height=44)
    #     btnn.bind(on_release=lambda btnn: drop.select(btnn.text))
    #     drop.add_widget(btnn)
    #     dropOpener = Button(text="Select Sensor", size_hint=(1,0.2), pos_hint={'x':0,'top':1})
    #     dropOpener.bind(on_release=drop.open)
    #     drop.bind(on_select=lambda instance, x: setattr(dropOpener1, 'text', x))
    #     content.add_widget(dropOpener)
    #
    #
    #
    #     drop1 = DropDown()
    #     for sensor in self.sensors:
    #         btnn = Button(text=str(sensor.id), size_hint_y=None, height=44)
    #         btnn.bind(on_release=lambda btnn: drop1.select(btnn.text))
    #         drop1.add_widget(btnn)
    #     dropOpener1 = Button(text="Select Sensor", size_hint=(1,0.2), pos_hint={'x':0,'top':1})
    #     dropOpener1.bind(on_release=drop1.open)
    #     drop1.bind(on_select=lambda instance, x: setattr(dropOpener1, 'text', x))
    #     content.add_widget(dropOpener1)
    #     text = TextInput(text = "Condition", size_hint=(1,0.2), pos_hint={'x':0,'top':0.8})
    #     content.add_widget(text)
    #     drop2 = DropDown()
    #     for actuator in self.actuators:
    #         btnn = Button(text=str(actuator.name), size_hint_y=None, height=44)
    #         btnn.bind(on_release=lambda btnn: drop2.select(btnn.text))
    #         drop2.add_widget(btnn)
    #     dropOpener2 = Button(text="Select Actuator", size_hint=(1,0.2), pos_hint={'x':0,'top':0.6})
    #     dropOpener2.bind(on_release=drop2.open)
    #     drop2.bind(on_select=lambda instance, x: setattr(dropOpener2, 'text', x))
    #     content.add_widget(dropOpener2)
    #     text1 = TextInput(text="Command", size_hint=(1, 0.2), pos_hint={'x': 0, 'top': 0.4})
    #     content.add_widget(text1)
    #
    #     buttonSave = Button(text="Save", size_hint=(1, 0.2), pos_hint={'x': 0, 'top': 0.2})
    #     content.add_widget(buttonSave)
    #     popup = Popup(content=content, title="Add modul",
    #                   size_hint=(None, None), size=(500,500),
    #                   auto_dismiss=False)
    #     buttonSave.bind(on_release=popup.dismiss)
    #     popup.bind(on_dismiss=self.saveModul)
    #     popup.open()

    # def saveModulData(self):
    #     with open(self.modulDataFileName,'w') as file:
    #         jsonOut = []
    #         for modul in self.moduls:
    #             jsonOut.append(modul.toArray())
    #         json.dump(jsonOut, file)

    def saveProgramData(self):
        with open(self.programDataFileName,'w') as file:
            jsonOut = []
            for program in self.programs:
                jsonOut.append(program.toArray())
            json.dump(jsonOut, file)

    # def commandActuator(self, instance):
    #     for modul in self.moduls:
    #         if modul.name == instance.id:
    #             if not modul.setupModul():
    #                 instance.state = "normal"
    #                 return
    #             if instance.state is "down":
    #                 modul.actuator.changeState(1)
    #                 print "Turn ", instance.text, " actuator On"
    #                 self.startReading()
    #             else:
    #                 modul.actuator.changeState(0)
    #                 time.sleep(1)
    #                 print "Turn ", instance.text, " actuator Off"

    # def delModul(self,instance):
    #     for modulIndex in xrange(len(self.moduls)):
    #         if self.moduls[modulIndex].name == instance.id:
    #             self.moduls.pop(modulIndex)
    #             break

    def getActuator(self):
        content = FloatLayout(size_hint=(1,1))
        drop = DropDown()
        for actuator in self.actuators:
            btnn = Button(text=str(actuator.id), size_hint_y=None, height=44)
            btnn.bind(on_release=lambda btnn: drop.select(btnn.text))
            drop.add_widget(btnn)
        dropOpener = Button(text="Select", size_hint=(0.8,0.4), pos_hint={'center_x':0.5,'y':0.5})
        dropOpener.bind(on_release=drop.open)
        drop.bind(on_select=lambda instance, x: setattr(dropOpener, 'text', x))
        content.add_widget(dropOpener)
        buttonOk = Button(text="Save", size_hint=(0.4,0.4), pos_hint={'x':0.1,'y':0.1})
        buttonBack = Button(text="Back", size_hint=(0.4,0.4), pos_hint={'x':0.5,'y':0.1})
        content.add_widget(buttonOk)
        content.add_widget(buttonBack)
        popup = Popup(content=content, title='Choose actuator',
                      size_hint=(None, None), size=(500, 500),
                      auto_dismiss=False)
        buttonOk.bind(on_release=popup.dismiss)
        buttonBack.bind(on_release=popup.dismiss)
        popup.open()
        popup.bind(on_dismiss=self.saveActuatorForProgram)

    def saveActuatorForProgram(self, instance):
        choosenActuator = None
        for actuator in self.actuators:
            if actuator.id == instance.content.children[2].text:
                choosenActuator = actuator
                break

        if choosenActuator is not None:
            self.programs[-1].setActuator(choosenActuator)
            self.modulScreen.currentActuator = self.programs[-1].actuator.name
            self.saveProgramData()
            self.openModulPage()
        elif instance.content.children[2].text is not "Select":
            self.notify("Error","Can't find actuator.")

    # Program functions
    def addProgram(self, instance):
        programName = "Program" + str(self.programCount)
        self.modulScreen.currentProgram = programName
        self.modulScreen.currentProgramNr = self.programCount
        self.programCount += 1
        program = Program(programName)
        self.programs.append(program)
        self.getActuator()

    def delProgram(self,instance):
        self.programCount -= 1
        for programIndex in xrange(len(self.programs)):
            if self.programs[programIndex].name == instance.id:
                self.programs.pop(programIndex)
                break
        self.saveProgramData()
        self.programScreen.selectedProgramName = ''
        self.programScreen.updateScreen()

    def editProgram(self, instance):
        programName = instance.id
        self.modulScreen.currentProgram = programName
        for programNr in xrange(len(self.programs)):
            if programName == self.programs[programNr].name:
                self.modulScreen.currentProgramNr = programNr
                self.modulScreen.currentActuator = self.programs[programNr].actuator.name
                self.openModulPage()

    def changeProgramState(self, instance):
        for programIndex in xrange(len(self.programs)):
            if self.programs[programIndex].name == instance.id:
                if instance.state == "down":
                    if self.programs[programIndex].setupConnection():
                        self.programs[programIndex].running = True
                        instance.text = 'Stop'
                    else:
                        instance.state = "normal"
                else:
                    self.programs[programIndex].running = False
                    instance.text = 'Run'

    def changeActuatorStateOfProgram(self, instance):
        for programIndex in xrange(len(self.programs)):
            if self.programs[programIndex].name == instance.id:
                if instance.state == "down":
                    self.programs[programIndex].actuator.changeState('on')
                    instance.text = 'On'
                else:
                    self.programs[programIndex].actuator.changeState('off')
                    instance.text = 'Off'
                self.programScreen.updateScreen()

    # Condition functions
    def addCondition(self, instance):
        self.openAddModulPage()

    def editCondition(self, instance):
        choosenCond = None
        for condition in self.programs[self.modulScreen.currentProgramNr].conditions:
            if condition.id == instance.id:
                choosenCond = condition
        if choosenCond is not None:
            self.openAddModulPage(None, choosenCond)

    def delCondition(self, instance):
        for conditionIndex in xrange(len(self.programs[self.modulScreen.currentProgramNr].conditions)):
            if self.programs[self.modulScreen.currentProgramNr].conditions[conditionIndex].id == instance.id:
                self.programs[self.modulScreen.currentProgramNr].conditions.pop(conditionIndex)
                self.saveProgramData()
                self.modulScreen.updateScreen()
                break

    # Open page functions
    def openModulPage(self, instance = None):
        self.modulScreen.updateScreen()
        self.sm.current = 'ModulPage'
        self.sm.do_layout()

    def openAddModulPage(self, instance=None, condition=None):
        if instance == None and condition == None:
            self.addModulScreen.currentCondition = None
            self.addModulScreen.updateScreen()
        else:
            self.addModulScreen.currentCondition = condition.id
            self.addModulScreen.updateScreen(None, condition)
        self.sm.current = 'AddModulPage'
        self.sm.do_layout()

    def openProgramPage(self, instance=None):
        self.programScreen.updateScreen()
        self.sm.current = 'ProgramPage'
        self.sm.do_layout()

if __name__ == "__main__":
    SmartHomeApp().run()