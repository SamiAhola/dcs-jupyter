"""DCS aircraft types definitions."""

from typing import Literal

# Define all aircraft types as string literals
AircraftType = Literal[
    # Fighters
    'AJS37',
    'F-15C',
    'F-16C',
    'F-16C_50',
    'F-4E',
    'F/A-18C',
    'FA-18C_hornet',
    'JF-17',
    'MiG-15bis',
    'MiG-21bis',
    'MiG-29',
    'Su-25',
    'Su-25A',
    'Su-25T',
    'Su-27',
    'Su-33',
    'A-10A',
    'A-10C',
    'A-10C_2',
    # Multirole
    'AV8BNA',
    'F-14A-135-GR',
    'F-14A-95-GR',
    'F-14B',
    'F-15E',
    'F-16A',
    'F-16A MLU',
    'F-16C bl.50',
    'F-16C bl.52d',
    'F-5E',
    'F-5E-3',
    'F-5E-3_FC',
    'F-86F Sabre',
    'F-86F_FC',
    'F/A-18A',
    # Bombers/Strategic
    'B-1B',
    'B-17G',
    'B-52H',
    # Transport/Tanker
    'An-26B',
    'C-130',
    'C-17A',
    'KC-135',
    'KC135MPRS',
    'KC130',
    'S-3B',
    'S-3B Tanker',
    # AWACS/Electronic
    'E-2C',
    'E-3A',
    'F-117A',
    # Helicopters
    'Mi-8MTV2',
    'Ka-50',
    'AH-64D',
    # Trainers
    'Christen Eagle II',
    'Hawk',
    'L-39C',
    'L-39ZA',
    'Yak-52',
    # WWII Aircraft
    'MosquitoFBMkVI',
    'P-47D-30',
    'P-47D-30bl1',
    'P-47D-40',
    'P-51D',
    'P-51D-30-NA',
    'SpitfireLFMkIX',
    'SpitfireLFMkIXCW',
    'TF-51D',
    # Unmanned
    'MQ-9 Reaper',
    'RQ-1A Predator',
]
