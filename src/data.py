from dataclasses import dataclass

@dataclass
class ProfileDimensions:
    h: float    # höhe
    b: float    # breite
    tw: float    # stegdicke
    tf: float    # flanschdicke
    r: float    # radius Schweissnaht

# Dimensions in mm
HEA_DIMENSIONS = {
    100: ProfileDimensions(h=96, b=100, tw=5, tf=8, r=12),
    200: ProfileDimensions(h=190, b=200, tw=6.5, tf=10, r=18),
    300: ProfileDimensions(h=290, b=300, tw=8.5, tf=14, r=27),
    # Add more sizes as needed
}

IPE_DIMENSIONS = {
    100: ProfileDimensions(h=100, b=55, tw=4.1, tf=5.7, r=7),
    200: ProfileDimensions(h=200, b=100, tw=5.6, tf=8.5, r=12),
    300: ProfileDimensions(h=300, b=150, tw=7.1, tf=10.7, r=15),
    # Add more sizes as needed
}

def get_profile_dimensions(profile_type: str, size: int) -> ProfileDimensions:
    dimension_map = {
        'HEA': HEA_DIMENSIONS,
        'IPE': IPE_DIMENSIONS
    }
    
    if profile_type not in dimension_map:
        raise ValueError(f"Unknown profile type: {profile_type}")
    if size not in dimension_map[profile_type]:
        raise ValueError(f"Unknown size {size} for profile type {profile_type}")
        
    return dimension_map[profile_type][size]


@dataclass(frozen=True)
class Vector3D:
    x: int
    y: int
    z: int
    
    def asTuple(self):
        return self.x, self.y, self.z