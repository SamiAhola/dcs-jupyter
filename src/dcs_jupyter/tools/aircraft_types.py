"""DCS aircraft types enumeration."""

from enum import StrEnum


class AircraftType(StrEnum):
    """DCS World aircraft types (official)."""
    
    # Fighters
    AJS37 = "AJS37"
    F_15C = "F-15C"
    F_16C = "F-16C"
    F_4E = "F-4E"
    FA_18C = "FA-18C"
    JF_17 = "JF-17"
    MIG_15BIS = "MiG-15bis"
    MIG_21BIS = "MIG-21bis"
    MIG_29 = "MiG-29"
    SU_25A = "Su-25A"
    SU_25T = "Su-25T"
    SU_27 = "Su-27"
    SU_33 = "Su-33"
    
    # Attack/Multirole
    AV8BNA = "AV8BNA"
    
    # Helicopters
    MI_8MTV2 = "Mi-8MTV2"
    
    # Trainers
    CHRISTEN_EAGLE_II = "Christen Eagle II"
    L_39C = "L-39C"
    YAK_52 = "Yak-52"
    
    # WWII Aircraft
    SPITFIRE_LF_MK_IX = "SpitfireLFMkIX"
    TF_51D = "TF-51D"
    
    # Navigation Systems
    NS430 = "NS430"
    NS430_L_39C = "NS430_L-39C"
    NS430_MI_8MT = "NS430_Mi-8MT"


# Aircraft categories
FIGHTERS = [
    AircraftType.F_15C,
    AircraftType.F_16C,
    AircraftType.F_4E,
    AircraftType.FA_18C,
    AircraftType.JF_17,
    AircraftType.MIG_15BIS,
    AircraftType.MIG_21BIS,
    AircraftType.MIG_29,
    AircraftType.SU_27,
    AircraftType.SU_33,
]

ATTACK_AIRCRAFT = [
    AircraftType.AJS37,
    AircraftType.AV8BNA,
    AircraftType.SU_25A,
    AircraftType.SU_25T,
]

HELICOPTERS = [
    AircraftType.MI_8MTV2,
]

TRAINERS = [
    AircraftType.CHRISTEN_EAGLE_II,
    AircraftType.L_39C,
    AircraftType.YAK_52,
]

WWII_AIRCRAFT = [
    AircraftType.SPITFIRE_LF_MK_IX,
    AircraftType.TF_51D,
]

NAVIGATION_SYSTEMS = [
    AircraftType.NS430,
    AircraftType.NS430_L_39C,
    AircraftType.NS430_MI_8MT,
]