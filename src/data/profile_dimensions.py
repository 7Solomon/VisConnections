from dataclasses import dataclass
from typing import List

@dataclass
class ProfileDimensions:
    h: float    # höhe
    b: float    # breite
    tw: float    # stegdicke
    tf: float    # flanschdicke
    r: float    # radius Schweissnaht

#HEA_CONNECTION_POINTS = {}

# Dimensions in mm
HEA_DIMENSIONS = {
    100: ProfileDimensions(h=96, b=100, tw=5, tf=8, r=12),
    200: ProfileDimensions(h=190, b=200, tw=6.5, tf=10, r=18),
    300: ProfileDimensions(h=290, b=300, tw=8.5, tf=14, r=27),
}

IPE_DIMENSIONS = {
    100: ProfileDimensions(h=100, b=55, tw=4.1, tf=5.7, r=7),
    200: ProfileDimensions(h=200, b=100, tw=5.6, tf=8.5, r=12),
    300: ProfileDimensions(h=300, b=150, tw=7.1, tf=10.7, r=15),
}

DIMENSION_MAP = {
    'HEA': HEA_DIMENSIONS,
    'IPE': IPE_DIMENSIONS
}
    

def get_profile_dimensions(profile_type: str, size: int) -> ProfileDimensions:
    if profile_type not in DIMENSION_MAP:
        raise ValueError(f"Unknown profile type: {profile_type}")
    if size not in DIMENSION_MAP[profile_type]:
        raise ValueError(f"Unknown size {size} for profile type {profile_type}")
        
    return DIMENSION_MAP[profile_type][size]

