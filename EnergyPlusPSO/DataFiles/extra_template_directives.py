import pdb
import EnergyPlus as EP
import Merced

def calculateFourParamFromNumbers( t1, t2, t3, t4):
    # t1 is an hour 
    # return t2, t3
    # convert t4
    new_t4 = t1 + (24 - t1) * t4
    return t1, t2, t3, new_t4
    

def transformIdfFile( parsed_idf_file, parameter_substitutions ):
    Classroom_Weekday_T1 = parameter_substitutions["Classroom_Weekday_T1"]
    Classroom_Weekday_T2 = parameter_substitutions["Classroom_Weekday_T2"]
    Classroom_Weekday_T3 = parameter_substitutions["Classroom_Weekday_T3"]
    Classroom_Weekday_T4 = parameter_substitutions["Classroom_Weekday_T4"]
    Classroom_TuTh_T1 = parameter_substitutions["Classroom_Weekday_T1"]
    Classroom_TuTh_T2 = parameter_substitutions["Classroom_Weekday_T2"]
    Classroom_TuTh_T3 = parameter_substitutions["Classroom_Weekday_T3"]
    Classroom_TuTh_T4 = parameter_substitutions["Classroom_Weekday_T4"]
    Classroom_WkEndHoliday_T1 = parameter_substitutions["Classroom_WkEndHoliday_T1"]
    Classroom_WkEndHoliday_T2 = parameter_substitutions["Classroom_WkEndHoliday_T2"]
    Classroom_WkEndHoliday_T3 = parameter_substitutions["Classroom_WkEndHoliday_T3"]
    Classroom_WkEndHoliday_T4 = parameter_substitutions["Classroom_WkEndHoliday_T4"]
    Office_Weekday_T1 = parameter_substitutions["Office_Weekday_T1"]
    Office_Weekday_T2 = parameter_substitutions["Office_Weekday_T2"]
    Office_Weekday_T3 = parameter_substitutions["Office_Weekday_T3"]
    Office_Weekday_T4 = parameter_substitutions["Office_Weekday_T4"]
    Office_WkEndHoliday_T1 = parameter_substitutions["Office_WkEndHoliday_T1"]
    Office_WkEndHoliday_T2 = parameter_substitutions["Office_WkEndHoliday_T2"]
    Office_WkEndHoliday_T3 = parameter_substitutions["Office_WkEndHoliday_T3"]
    Office_WkEndHoliday_T4 = parameter_substitutions["Office_WkEndHoliday_T4"]


    ClassroomPopulationBaseLevelWeekend = parameter_substitutions["ClassroomPopulationBaseLevelWeekend"]
    ClassroomPopulationMaxLevelWeekendFrac = parameter_substitutions["ClassroomPopulationMaxLevelWeekendFrac"]
    OfficePopulationBaseLevelWeekend = parameter_substitutions["OfficePopulationBaseLevelWeekend"]
    OfficePopulationMaxLevelWeekendFrac = parameter_substitutions["OfficePopulationMaxLevelWeekendFrac"]

    ClassroomPopulationBaseLevelWeekday = parameter_substitutions["ClassroomPopulationBaseLevelWeekday"]
    ClassroomPopulationMaxLevelWeekdayFrac = parameter_substitutions["ClassroomPopulationMaxLevelWeekdayFrac"]
    OfficePopulationBaseLevelWeekday = parameter_substitutions["OfficePopulationBaseLevelWeekday"]
    OfficePopulationMaxLevelWeekdayFrac = parameter_substitutions["OfficePopulationMaxLevelWeekdayFrac"]
 
    OfficeLightingB = parameter_substitutions["OfficeLightingB"]
    OfficeLightingO = parameter_substitutions["OfficeLightingO"]
    OfficeLightingM = parameter_substitutions["OfficeLightingM"]
    ClassroomLightingB = parameter_substitutions["ClassroomLightingB"]
    ClassroomLightingO = parameter_substitutions["ClassroomLightingO"]
    ClassroomLightingM = parameter_substitutions["ClassroomLightingM"]
    WattsPerZoneFloorAreaClassroom = parameter_substitutions["WattsPerZoneFloorAreaClassroom"]
    WattsPerZoneFloorAreaUtilEEquip = parameter_substitutions["WattsPerZoneFloorAreaUtilEEquip"]
    WattsPerZoneFloorAreaOffice = parameter_substitutions["WattsPerZoneFloorAreaOffice"]
    OfficeEquipmentB = parameter_substitutions["OfficeEquipmentB"]
    OfficeEquipmentO = parameter_substitutions["OfficeEquipmentO"]
    OfficeEquipmentM = parameter_substitutions["OfficeEquipmentM"]
    ClassroomEquipmentB = parameter_substitutions["ClassroomEquipmentB"]
    ClassroomEquipmentO = parameter_substitutions["ClassroomEquipmentO"]
    ClassroomEquipmentM = parameter_substitutions["ClassroomEquipmentM"]

    # I have 6 schedules to make:
    # People schedules for all the classrooms and offices.
    # Equipment Schedules for both classrooms and offices.
    # Lighting Schedules for both classrooms and offices. 

    schedule_map = {}
    substitutions = []

    # Make the 5 classes of people schedules: Classrooms for MWF, TTh,
    # and Weekends, and offices for the week as well as for 
    all_class_schedules = Merced.classroom_schedules_people_MWF[:]
    all_class_schedules = Merced.classroom_schedules_people_TTh
    for class_sched in all_class_schedules:
        t1, t2, t3, t4 = \
            calculateFourParamFromNumbers(Classroom_Weekday_T1, \
                                              Classroom_Weekday_T2, \
                                              Classroom_Weekday_T3, \
                                              Classroom_Weekday_T4)

        min_frac = ClassroomPopulationBaseLevelWeekday
        max_frac = \
            (1.0 - ClassroomPopulationBaseLevelWeekday) * ClassroomPopulationMaxLevelWeekdayFrac + min_frac

        classroom_Weekday_schedule = \
            Merced.makeFourParameterSchedule( class_sched, \
                                                  t1, t2, t3, t4, \
                                                  min_frac, max_frac)
        substitutions.append((class_sched, classroom_Weekday_schedule ))
    else:
        schedule_map[ "class_MWF"] = classroom_Weekday_schedule
        schedule_map[ "class_TuTh" ] = classroom_TuTh_schedule

    for class_sched in Merced.classroom_schedules_people_WEH:
        t1, t2, t3, t4 = calculateFourParamFromNumbers(Classroom_WkEndHoliday_T1, Classroom_WkEndHoliday_T2, Classroom_WkEndHoliday_T3, Classroom_WkEndHoliday_T4)

        min_frac = ClassroomPopulationBaseLevelWeekend
        max_frac = (1.0 - ClassroomPopulationBaseLevelWeekday) * ClassroomPopulationMaxLevelWeekendFrac + min_frac

        classroom_WE_schedule = Merced.makeFourParameterSchedule(class_sched, t1, t2, t3, t4, min_frac, max_frac)
        substitutions.append((class_sched, classroom_WE_schedule))
    else:
        schedule_map[ "class_WE" ] = classroom_WE_schedule

    for office_sched in Merced.office_people_WD:

        min_frac = OfficePopulationBaseLevelWeekday
        max_frac = (1.0 - min_frac) * OfficePopulationMaxLevelWeekdayFrac + min_frac
        
        t1, t2, t3, t4 = calculateFourParamFromNumbers(Office_Weekday_T1, Office_Weekday_T2, Office_Weekday_T3, Office_Weekday_T4)
        office_WD = Merced.makeFourParameterSchedule( office_sched, t1, t2, t3, t4, min_frac, max_frac)
        substitutions.append((office_sched, office_WD))
    else:
        schedule_map[ "office_WD" ] = office_WD

    for sched in Merced.office_people_WEH:
        min_frac = OfficePopulationBaseLevelWeekend
        max_frac = (1.0 - min_frac) * OfficePopulationMaxLevelWeekend + min_frac

        t1, t2, t3, t4 = calculateFourParamFromNumbers( Office_WkEndHoliday_T1, Office_WkEndHoliday_T2, Office_WkEndHoliday_T3, Office_WkEndHoliday_T4)
        office_local_sched = Merced.makeFourParameterSchedule( sched, t1, t2, t3, t4, min_frac, max_frac)
        substitutions.append((sched, office_local_sched))
    else:
        schedule_map[ "office_WE" ] = office_local_sched

    # Equipment -- 5 Total
    for sched in Merced.classroom_schedules_equip_MWF:
        local_sched = Merced.makeDerivedSchedule(schedule_map["class_MWF"], sched, ClassroomEquipmentB, ClassroomEquipmentO, ClassroomEquipmentM)
        substitutions.append( (sched, local_sched))

    for sched in Merced.classroom_schedules_equip_TTh:
        local_sched = Merced.makeDerivedSchedule(schedule_map["class_TuTh"], sched, ClassroomEquipmentB, ClassroomEquipmentO, ClassroomEquipmentM)
        substitutions.append( (sched, local_sched))

    for sched in Merced.classroom_schedules_equip_WEH:
        local_sched = Merced.makeDerivedSchedule(schedule_map["class_WE"], sched, ClassroomEquipmentB, ClassroomEquipmentO, ClassroomEquipmentM)
        substitutions.append( (sched, local_sched))

    for sched in Merced.office_schedules_equip_WD:
        local_sched = Merced.makeDerivedSchedule(schedule_map["office_WD"], sched, OfficeEquipmentB, OfficeEquipmentO, OfficeEquipmentM)
        substitutions.append( (sched, local_sched))

    for sched in Merced.office_schedules_equip_WEH:
        local_sched = Merced.makeDerivedSchedule(schedule_map["office_WE"], sched, OfficeEquipmentB, OfficeEquipmentO, OfficeEquipmentM)
        substitutions.append( (sched, local_sched))

    # Lighting - 5 lighting
    for sched in Merced.office_light_WD:
        local_sched = Merced.makeDerivedSchedule(schedule_map["office_WD"], sched, OfficeLightingB, OfficeLightingO, OfficeLightingM)
        substitutions.append( (sched, local_sched))
        
    for sched in Merced.office_light_WEH:
        local_sched = Merced.makeDerivedSchedule(schedule_map["office_WE"], sched, OfficeLightingB, OfficeLightingO, OfficeLightingM)
        substitutions.append( (sched, local_sched))

    for sched in Merced.classroom_schedules_light_MWF:
        local_sched = Merced.makeDerivedSchedule(schedule_map["class_MWF"], sched, ClassroomLightingB, ClassroomLightingO, ClassroomLightingM)
        substitutions.append( (sched, local_sched))

    for sched in Merced.classroom_schedules_light_TTh:
        local_sched = Merced.makeDerivedSchedule(schedule_map["class_TuTh"], sched, ClassroomLightingB, ClassroomLightingO, ClassroomLightingM)
        substitutions.append( (sched, local_sched))

    for sched in Merced.classroom_schedules_light_WEH:
        local_sched = Merced.makeDerivedSchedule(schedule_map["class_WE"], sched, ClassroomLightingB, ClassroomLightingO, ClassroomLightingM)
        substitutions.append( (sched, local_sched))

    # Other -- 6 total

    for sched in Merced.other_schedules_people_WD:
        t1, t2, t3, t4 = \
            calculateFourParamFromNumbers(Classroom_Weekday_T1, \
                                              Classroom_Weekday_T2, \
                                              Classroom_Weekday_T3, \
                                              Classroom_Weekday_T4)

        min_frac = ClassroomPopulationBaseLevelWeekday
        max_frac = \
            (1.0 - ClassroomPopulationBaseLevelWeekday) * ClassroomPopulationMaxLevelWeekdayFrac + min_frac

        other_schedule = \
            Merced.makeFourParameterSchedule( sched, t1, t2, t3, t4, min_frac, max_frac)
        substitutions.append( (sched, other_schedule))
    else:
        schedule_map[ "other_WD" ] = other_schedule
        
    
    for sched in Merced.other_schedules_people_WEH:
        t1, t2, t3, t4 = calculateFourParamFromNumbers(Classroom_WkEndHoliday_T1, Classroom_WkEndHoliday_T2, Classroom_WkEndHoliday_T3, Classroom_WkEndHoliday_T4)

        min_frac = ClassroomPopulationBaseLevelWeekend
        max_frac = (1.0 - ClassroomPopulationBaseLevelWeekday) * ClassroomPopulationMaxLevelWeekendFrac + min_frac

        other_schedule = \
            Merced.makeFourParameterSchedule( sched, \
                                                  t1, t2, t3, t4)
        substitutions.append( (sched, other_schedule))
    else:
        schedule_map[ "other_WE" ] = other_schedule


    for sched in Merced.other_schedules_light_WD:
        other_schedule = Merced.makeDerivedSchedule(schedule_map["other_WD"], sched, OfficeLightingB, OfficeLightingO, OfficeLightingM)
        substitutions.append( (sched, other_schedule))

    for sched in Merced.other_schedules_light_WEH:
        other_schedule = Merced.makeDerivedSchedule(schedule_map["other_WE"], sched, OfficeLightingB, OfficeLightingO, OfficeLightingM)
        substitutions.append( (sched, other_schedule))

    for sched in Merced.other_schedules_equip_WD:
        other_schedule = Merced.makeDerivedSchedule(schedule_map["other_WD"], sched, ClassroomEquipmentB, ClassroomEquipmentO, ClassroomEquipmentM)
        substitutions.append( (sched, other_schedule))

    for sched in Merced.other_schedules_equip_WEH:
        other_schedule = Merced.makeDerivedSchedule(schedule_map["other_WD"], sched, ClassroomEquipmentB, ClassroomEquipmentO, ClassroomEquipmentM)
        substitutions.append( (sched, other_schedule))

    parsed_idf_file = EP.replaceMultipleNamedElementsWithNewElements( parsed_idf_file, substitutions)

    return parsed_idf_file


