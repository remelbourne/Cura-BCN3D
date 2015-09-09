__copyright__ = "Copyright (C) 2013 David Braam - Released under terms of the AGPLv3 License"

import wx
import ConfigParser as configparser
import os.path
import math

from Cura.util import profile
from Cura.util import resources

class simpleModePanel(wx.Panel):
    "Main user interface window for Quickprint mode"
    def __init__(self, parent, callback):
        super(simpleModePanel, self).__init__(parent)
        self._callback = callback

        if profile.getMachineSetting('machine_type') == 'BCN3DSigma':
            self._print_extruder_options = []
            self._print_profile_options = []
            self._print_material_options = []


            printExtruderPanel = wx.Panel(self)
            for filename in resources.getSimpleModeExtruders():
                cp = configparser.ConfigParser()
                cp.read(filename)
                base_filename = os.path.splitext(os.path.basename(filename))[0]
                name = base_filename
                if cp.has_option('info', 'name'):
                    name = cp.get('info', 'name')
                button = wx.RadioButton(printExtruderPanel, -1, name, style=wx.RB_GROUP if len(self._print_extruder_options) == 0 else 0)
                button.base_filename = base_filename
                button.filename = filename
                self._print_extruder_options.append(button)
                if profile.getPreference('simpleModeExtruder') == base_filename:
                    button.SetValue(True)

            printTypePanel = wx.Panel(self)
            for filename in resources.getSimpleModeProfiles():
                cp = configparser.ConfigParser()
                cp.read(filename)
                base_filename = os.path.splitext(os.path.basename(filename))[0]
                name = base_filename
                if cp.has_option('info', 'name'):
                    name = cp.get('info', 'name')
                button = wx.RadioButton(printTypePanel, -1, name, style=wx.RB_GROUP if len(self._print_profile_options) == 0 else 0)
                button.base_filename = base_filename
                button.filename = filename
                self._print_profile_options.append(button)
                if profile.getPreference('simpleModeProfile') == base_filename:
                    button.SetValue(True)

            printMaterialPanel = wx.Panel(self)
            for filename in resources.getSimpleModeMaterials():
                cp = configparser.ConfigParser()
                cp.read(filename)
                base_filename = os.path.splitext(os.path.basename(filename))[0]
                name = base_filename
                if cp.has_option('info', 'name'):
                    name = cp.get('info', 'name')
                button = wx.RadioButton(printMaterialPanel, -1, name, style=wx.RB_GROUP if len(self._print_material_options) == 0 else 0)
                button.base_filename = base_filename
                button.filename = filename
                self._print_material_options.append(button)
                if profile.getPreference('simpleModeMaterial') == base_filename:
                    button.SetValue(True)

            if profile.getMachineSetting('gcode_flavor') == 'UltiGCode':
                printMaterialPanel.Show(False)

            self.wipeTower = wx.CheckBox(self, -1, 'Wipe tower')
            self.printSupport = wx.CheckBox(self, -1, 'Print support structure')
            self.space1 = wx.StaticText(self, -1, '')
            self.text1 = wx.StaticText(self, -1, 'Select support extruder:')
            self.leftSupport = wx.CheckBox(self, -1, 'Left')
            self.rightSupport = wx.CheckBox(self, -1, 'Right')
            self.bothSupport = wx.CheckBox(self, -1, 'Both')
            self.space2 = wx.StaticText(self, -1, '')
            self.text2 = wx.StaticText(self, -1, 'Select support material:')
            self.plaSupport = wx.CheckBox(self, -1, 'PLA')
            self.absSupport = wx.CheckBox(self, -1, 'ABS')
            self.filaSupport = wx.CheckBox(self, -1, 'Filaflex')
            self.pvaSupport = wx.CheckBox(self, -1, 'PVA')

            sizer = wx.GridBagSizer()
            self.SetSizer(sizer)

            sb = wx.StaticBox(printExtruderPanel, label=_("Select object extruder:"))
            boxsizer = wx.StaticBoxSizer(sb, wx.VERTICAL)
            for button in self._print_extruder_options:
                boxsizer.Add(button)
            printExtruderPanel.SetSizer(wx.BoxSizer(wx.VERTICAL))
            printExtruderPanel.GetSizer().Add(boxsizer, 1, flag = wx.EXPAND)
            sizer.Add(printExtruderPanel, (0,0), flag = wx.EXPAND)

            sb = wx.StaticBox(printMaterialPanel, label=_("Select object material:"))
            boxsizer = wx.StaticBoxSizer(sb, wx.VERTICAL)
            for button in self._print_material_options:
                boxsizer.Add(button)
            printMaterialPanel.SetSizer(wx.BoxSizer(wx.VERTICAL))
            printMaterialPanel.GetSizer().Add(boxsizer, flag = wx.EXPAND)
            sizer.Add(printMaterialPanel, (1,0), flag = wx.EXPAND)

            sb = wx.StaticBox(printTypePanel, label=_("Select quickprint profile:"))
            boxsizer = wx.StaticBoxSizer(sb, wx.VERTICAL)
            for button in self._print_profile_options:
                boxsizer.Add(button)
            printTypePanel.SetSizer(wx.BoxSizer(wx.VERTICAL))
            printTypePanel.GetSizer().Add(boxsizer, flag = wx.EXPAND)
            sizer.Add(printTypePanel, (2,0), flag = wx.EXPAND)

            sb = wx.StaticBox(self, label=_("Other:"))
            boxsizer = wx.StaticBoxSizer(sb, wx.VERTICAL)
            boxsizer.Add(self.wipeTower)
            boxsizer.Add(self.printSupport)
            boxsizer.Add(self.space1)
            boxsizer.Add(self.text1)
            boxsizer.Add(self.leftSupport)
            boxsizer.Add(self.rightSupport)
            boxsizer.Add(self.bothSupport)
            boxsizer.Add(self.space2)
            boxsizer.Add(self.text2)
            boxsizer.Add(self.plaSupport)
            boxsizer.Add(self.absSupport)
            boxsizer.Add(self.filaSupport)
            boxsizer.Add(self.pvaSupport)
            sizer.Add(boxsizer, (3,0), flag=wx.EXPAND)

            for button in self._print_profile_options:
                button.Bind(wx.EVT_RADIOBUTTON, self._update)
            for button in self._print_material_options:
                button.Bind(wx.EVT_RADIOBUTTON, self._update)
            for button in self._print_extruder_options:
                button.Bind(wx.EVT_RADIOBUTTON, self._update)

            self.wipeTower.Bind(wx.EVT_CHECKBOX, self._update)
            self.printSupport.Bind(wx.EVT_CHECKBOX, self._update)
            self.leftSupport.Bind(wx.EVT_CHECKBOX, self._update)
            self.rightSupport.Bind(wx.EVT_CHECKBOX, self._update)
            self.bothSupport.Bind(wx.EVT_CHECKBOX, self._update)
            self.plaSupport.Bind(wx.EVT_CHECKBOX, self._update)
            self.absSupport.Bind(wx.EVT_CHECKBOX, self._update)
            self.filaSupport.Bind(wx.EVT_CHECKBOX, self._update)
            self.pvaSupport.Bind(wx.EVT_CHECKBOX, self._update)

        else:
            self._print_material_options = []
            self._print_profile_options = []

            printTypePanel = wx.Panel(self)
            for filename in resources.getSimpleModeProfiles():
                cp = configparser.ConfigParser()
                cp.read(filename)
                base_filename = os.path.splitext(os.path.basename(filename))[0]
                name = base_filename
                if cp.has_option('info', 'name'):
                    name = cp.get('info', 'name')
                button = wx.RadioButton(printTypePanel, -1, name, style=wx.RB_GROUP if len(self._print_profile_options) == 0 else 0)
                button.base_filename = base_filename
                button.filename = filename
                self._print_profile_options.append(button)
                if profile.getPreference('simpleModeProfile') == base_filename:
                    button.SetValue(True)

            printMaterialPanel = wx.Panel(self)
            for filename in resources.getSimpleModeMaterials():
                cp = configparser.ConfigParser()
                cp.read(filename)
                base_filename = os.path.splitext(os.path.basename(filename))[0]
                name = base_filename
                if cp.has_option('info', 'name'):
                    name = cp.get('info', 'name')
                button = wx.RadioButton(printMaterialPanel, -1, name, style=wx.RB_GROUP if len(self._print_material_options) == 0 else 0)
                button.base_filename = base_filename
                button.filename = filename
                self._print_material_options.append(button)
                if profile.getPreference('simpleModeMaterial') == base_filename:
                    button.SetValue(True)

            if profile.getMachineSetting('gcode_flavor') == 'UltiGCode':
                printMaterialPanel.Show(False)

            self.printSupport = wx.CheckBox(self, -1, _("Print support structure"))

            sizer = wx.GridBagSizer()
            self.SetSizer(sizer)

            sb = wx.StaticBox(printMaterialPanel, label=_("Select material for printing:"))
            boxsizer = wx.StaticBoxSizer(sb, wx.VERTICAL)
            for button in self._print_material_options:
                boxsizer.Add(button)
            printMaterialPanel.SetSizer(wx.BoxSizer(wx.VERTICAL))
            printMaterialPanel.GetSizer().Add(boxsizer, flag=wx.EXPAND)
            sizer.Add(printMaterialPanel, (0,0), flag=wx.EXPAND)

            sb = wx.StaticBox(printTypePanel, label=_("Select a quickprint profile:"))
            boxsizer = wx.StaticBoxSizer(sb, wx.VERTICAL)
            for button in self._print_profile_options:
                boxsizer.Add(button)
            printTypePanel.SetSizer(wx.BoxSizer(wx.VERTICAL))
            printTypePanel.GetSizer().Add(boxsizer, flag=wx.EXPAND)
            sizer.Add(printTypePanel, (1,0), flag=wx.EXPAND)

            sb = wx.StaticBox(self, label=_("Other:"))
            boxsizer = wx.StaticBoxSizer(sb, wx.VERTICAL)
            boxsizer.Add(self.printSupport)
            sizer.Add(boxsizer, (2,0), flag=wx.EXPAND)

            for button in self._print_profile_options:
                button.Bind(wx.EVT_RADIOBUTTON, self._update)
            for button in self._print_material_options:
                button.Bind(wx.EVT_RADIOBUTTON, self._update)

            self.printSupport.Bind(wx.EVT_CHECKBOX, self._update)

    def _update(self, e):
        if profile.getMachineSetting('machine_type') == 'BCN3DSigma':
            for button in self._print_extruder_options:
                if button.GetValue():
                    profile.putPreference('simpleModeExtruder', button.base_filename)
        for button in self._print_profile_options:
            if button.GetValue():
                profile.putPreference('simpleModeProfile', button.base_filename)
        for button in self._print_material_options:
            if button.GetValue():
                profile.putPreference('simpleModeMaterial', button.base_filename)
        self._callback()

    def getSettingOverrides(self):
        settings = {}
        for setting in profile.settingsList:
            if not setting.isProfile():
                continue
            settings[setting.getName()] = setting.getDefault()

        for button in self._print_profile_options:
            if button.GetValue():
                cp = configparser.ConfigParser()
                cp.read(button.filename)
                for setting in profile.settingsList:
                    if setting.isProfile():
                        if cp.has_option('profile', setting.getName()):
                            settings[setting.getName()] = cp.get('profile', setting.getName())

        if profile.getMachineSetting('gcode_flavor') != 'UltiGCode':
            for button in self._print_material_options:
                if button.GetValue():
                    cp = configparser.ConfigParser()
                    cp.read(button.filename)
                    for setting in profile.settingsList:
                        if setting.isProfile():
                            if cp.has_option('profile', setting.getName()):
                                settings[setting.getName()] = cp.get('profile', setting.getName())


        #Options when we decide to print the wipe tower
        if self.wipeTower.GetValue():
            settings['wipe_tower'] = True
            layer_thickness = (profile.getProfileSettingFloat('layer_height')) * 1000
            settings['wipeTowerSize'] = int(math.sqrt(profile.getProfileSettingFloat('wipe_tower_volume') * 1000 * 1000 * 1000 / layer_thickness))
        #The information that gets sent to settings depending on the material and the extruder that we choose
        #PLA
        if self.printSupport.GetValue() and self.leftSupport.GetValue() and self.plaSupport.GetValue():
            settings['support'] = 'Touching buildplate'
            settings['support_dual_extrusion'] = 'First extruder'
            settings['print_temperature'] = 220
            settings['print_bed_temperature'] = 45
        elif self.printSupport.GetValue() and self.rightSupport.GetValue() and self.plaSupport.GetValue():
            settings['support'] = 'Touching buildplate'
            #Opcion rara que cuando poniamos supportExtruder = 1, lo demas dejaba de funcionar asi que he puesto un if para remediarlo
            if profile.getPreference('simpleModeExtruder') == '2_Right Extruder':
                settings['supportExtruder'] = 1
            else:
                settings['support_dual_extrusion'] = 'Second extruder'
            settings['print_temperature2'] = 220
            settings['print_bed_temperature'] = 45
        elif self.printSupport.GetValue() and self.bothSupport.GetValue() and self.plaSupport.GetValue():
            settings['support'] = 'Touching buildplate'
            settings['support_dual_extrusion'] = 'Both'
            settings['print_temperature'] = 220
        #ABS
        elif self.printSupport.GetValue() and self.leftSupport.GetValue() and self.absSupport.GetValue():
            settings['support'] = 'Touching buildplate'
            settings['supportExtruder'] = 0
            settings['support_dual_extrusion'] = 'First extruder'
            settings['print_temperature'] = 250
            settings['print_bed_temperature'] = 70
        elif self.printSupport.GetValue() and self.rightSupport.GetValue() and self.absSupport.GetValue():
            settings['support'] = 'Touching buildplate'
            settings['supportExtruder'] = 1
            settings['support_dual_extrusion'] = 'Second extruder'
            settings['print_temperature2'] = 250
            settings['print_bed_temperature'] = 70
        elif self.printSupport.GetValue() and self.bothSupport.GetValue() and self.absSupport.GetValue():
            settings['support'] = 'Touching buildplate'
            settings['support_dual_extrusion'] = 'Both'
            settings['print_temperature'] = 250
        #Filaflex
        elif self.printSupport.GetValue() and self.leftSupport.GetValue() and self.filaSupport.GetValue():
            settings['support'] = 'Touching buildplate'
            settings['supportExtruder'] = 0
            settings['support_dual_extrusion'] = 'First extruder'
            settings['print_temperature'] = 250
            settings['print_bed_temperature'] = 100
        elif self.printSupport.GetValue() and self.rightSupport.GetValue() and self.filaSupport.GetValue():
            settings['support'] = 'Touching buildplate'
            settings['supportExtruder'] = 1
            settings['support_dual_extrusion'] = 'Second extruder'
            settings['print_temperature2'] = 250
            settings['print_bed_temperature'] = 100
        elif self.printSupport.GetValue() and self.bothSupport.GetValue() and self.filaSupport.GetValue():
            settings['support'] = 'Touching buildplate'
            settings['support_dual_extrusion'] = 'Both'
            settings['print_temperature'] = 250
        #PVA
        elif self.printSupport.GetValue() and self.leftSupport.GetValue() and self.pvaSupport.GetValue():
            settings['support'] = 'Touching buildplate'
            settings['supportExtruder'] = 0
            settings['support_dual_extrusion'] = 'First extruder'
            settings['print_temperature'] = 190
            settings['print_bed_temperature'] = 55
        elif self.printSupport.GetValue() and self.rightSupport.GetValue() and self.pvaSupport.GetValue():
            settings['support'] = 'Touching buildplate'
            settings['supportExtruder'] = 1
            settings['support_dual_extrusion'] = 'Second extruder'
            settings['print_temperature2'] = 190
            settings['print_bed_temperature'] = 55
        elif self.printSupport.GetValue() and self.bothSupport.GetValue() and self.pvaSupport.GetValue():
            settings['support'] = 'Touching buildplate'
            settings['support_dual_extrusion'] = 'Both'
            settings['print_temperature'] = 190
        #return the settings in order to be added in the gcode
        return settings

    def updateProfileToControls(self):
            pass

