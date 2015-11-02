__author__ = 'Rebeca'
 #If we are in simple mode and want to use the left extruder
        if getPreference('startMode') == 'Simple' and getMachineSetting('machine_type') == 'BCN3DSigma' and getPreference('simpleModeExtruder') == '1_Left Extruder':
            if getProfileSetting('support') == 'Touching buildplate' and getProfileSetting('support_dual_extrusion') == 'Second extruder':
                extruderCount = 2
                gcode_parameter_key = 'S'
                if getMachineSetting('gcode_flavor') == 'Mach3/LinuxCNC':
                    gcode_parameter_key = 'P'
                if extruderCount > 1:
                    alterationContents = getAlterationFile("start%d.gcode" % (extruderCount))
                eSteps = getMachineSettingFloat('steps_per_e')
                if eSteps > 0:
                    prefix += 'M92 E%f\n' % (eSteps)
                temp = getProfileSettingFloat('print_temperature')
                bedTemp = 0
                if getMachineSetting('has_heated_bed') == 'True':
                    bedTemp = getProfileSettingFloat('print_bed_temperature')
                if bedTemp > 0 and not isTagIn('{print_bed_temperature}', alterationContents):
                    prefix += 'M190 %s%f\n' % (gcode_parameter_key, bedTemp)
                if temp > 0 and not isTagIn('{print_temperature}', alterationContents):
                    if extruderCount > 1:
                        for n in xrange(1, extruderCount):
                            t = temp
                            if n > 0 and getProfileSettingFloat('print_temperature%d' % (n+1)) > 0:
                                t = getProfileSettingFloat('print_temperature%d' % (n+1))
                            prefix += 'M104 T%d %s%f\n' % (n, gcode_parameter_key, t)
                        for n in xrange(0, extruderCount):
                            t = temp
                            if n > 0 and getProfileSettingFloat('print_temperature%d' % (n+1)) > 0:
                                t = getProfileSettingFloat('print_temperature%d' % (n+1))
                            prefix += 'M109 T%d %s%f\n' % (n, gcode_parameter_key, t)
                        prefix += 'T0\n'
                    else:
                        prefix += 'M109 %s%f\n' % (gcode_parameter_key, temp)
            else:
                alterationContents = getAlterationFile("startleft.gcode")
        #If we are in simple mode and want to use the right extruder
        elif getPreference('startMode') == 'Simple' and getMachineSetting('machine_type') == 'BCN3DSigma' and getPreference('simpleModeExtruder') == '2_Right Extruder':
            if getProfileSetting('support') == 'Touching buildplate' and getProfileSetting('support_dual_extrusion') == 'First extruder':
                extruderCount = 2
                gcode_parameter_key = 'S'
                if getMachineSetting('gcode_flavor') == 'Mach3/LinuxCNC':
                    gcode_parameter_key = 'P'
                if extruderCount > 1:
                    alterationContents = getAlterationFile("startrightdouble.gcode")
                eSteps = getMachineSettingFloat('steps_per_e')
                if eSteps > 0:
                    prefix += 'M92 E%f\n' % (eSteps)
                temp = getProfileSettingFloat('print_temperature')
                bedTemp = 0
                if getMachineSetting('has_heated_bed') == 'True':
                    bedTemp = getProfileSettingFloat('print_bed_temperature')
                if bedTemp > 0 and not isTagIn('{print_bed_temperature}', alterationContents):
                    prefix += 'M190 %s%f\n' % (gcode_parameter_key, bedTemp)
                if temp > 0 and not isTagIn('{print_temperature}', alterationContents):
                    if extruderCount > 1:
                        for n in xrange(0, 1):
                            t = temp
                            if n > 0 and getProfileSettingFloat('print_temperature%d' % (n+1)) > 0:
                                t = getProfileSettingFloat('print_temperature%d' % (n+1))
                            prefix += 'M104 T%d %s%f\n' % (n, gcode_parameter_key, t)
                        for n in reversed(xrange(0, extruderCount)):
                            t = temp
                            if n > 0 and getProfileSettingFloat('print_temperature%d' % (n+1)) > 0:
                                t = getProfileSettingFloat('print_temperature%d' % (n+1))
                            prefix += 'M109 T%d %s%f\n' % (n, gcode_parameter_key, t)
                        prefix += 'T1\n'
                    else:
                        prefix += 'M109 %s%f\n' % (gcode_parameter_key, temp)
            else:
                alterationContents = getAlterationFile("startright.gcode")
        #If we are not on simple mode or if we want to use both extruders
        else:
            gcode_parameter_key = 'S'
            if getMachineSetting('gcode_flavor') == 'Mach3/LinuxCNC':
                gcode_parameter_key = 'P'
            if extruderCount > 1:
                alterationContents = getAlterationFile("start%d.gcode" % (extruderCount))
            eSteps = getMachineSettingFloat('steps_per_e')
            if eSteps > 0:
                prefix += 'M92 E%f\n' % (eSteps)
            temp = getProfileSettingFloat('print_temperature')
            bedTemp = 0
            if getMachineSetting('has_heated_bed') == 'True':
                bedTemp = getProfileSettingFloat('print_bed_temperature')
            if bedTemp > 0 and not isTagIn('{print_bed_temperature}', alterationContents):
                prefix += 'M190 %s%f\n' % (gcode_parameter_key, bedTemp)
            if temp > 0 and not isTagIn('{print_temperature}', alterationContents):
                if extruderCount > 1:
                    for n in xrange(1, extruderCount):
                        t = temp
                        if n > 0 and getProfileSettingFloat('print_temperature%d' % (n+1)) > 0:
                            t = getProfileSettingFloat('print_temperature%d' % (n+1))
                        prefix += 'M104 T%d %s%f\n' % (n, gcode_parameter_key, t)
                    for n in xrange(0, extruderCount):
                        t = temp
                        if n > 0 and getProfileSettingFloat('print_temperature%d' % (n+1)) > 0:
                            t = getProfileSettingFloat('print_temperature%d' % (n+1))
                        prefix += 'M109 T%d %s%f\n' % (n, gcode_parameter_key, t)
                    prefix += 'T0\n'
                else:
                    prefix += 'M109 %s%f\n' % (gcode_parameter_key, temp)