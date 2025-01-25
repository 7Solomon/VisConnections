import pyvista as pv
from src.data import Vector3D, get_profile_dimensions

def create_hea_beam(size: int) -> pv.PolyData:
    """
    Vieliecht position in ObjectManager verschieben, und dort nur translate callen
    """
    dimensions = get_profile_dimensions('HEA', size)
    length = 1000  # Length of the beam in mm
    
    # Create components
    steg = pv.Cube(center=(length/2, 0, 0),
                  x_length=length,
                  y_length=dimensions.tw,
                  z_length=dimensions.h-2*dimensions.tw)
    
    top_flansch = pv.Cube(center=(length/2, 0, (dimensions.h/2 - dimensions.tf/2)),
                         x_length=length,
                         y_length=dimensions.b,
                         z_length=dimensions.tf)
    
    bottom_flansch= pv.Cube(center=(length/2, 0, (-dimensions.h/2 + dimensions.tf/2)),
                           x_length=length,
                           y_length=dimensions.b,
                           z_length=dimensions.tf)
    
    # Combine and scale to meters
    beam = steg.merge([top_flansch, bottom_flansch])
    beam.scale([0.0001, 0.0001, 0.0001])
    return beam


#def create_ipe_beam(size: int) -> pv.PolyData:
#    dimensions = get_profile_dimensions('IPE', size)
#    length = 1000  # Length of the beam in mm
#    # Create components
#    web = pv.Cube(center=(0, 0, 0),
#                  x_length=dimensions.s,
#                  y_length=dimensions.h-2*dimensions.t,
#                  z_length=dimensions.b)
#    
#    top_flange = pv.Cube(center=(0, dimensions.h/2 - dimensions.t/2, 0),
#                         x_length=dimensions.b,
#                         y_length=dimensions.t,
#                         z_length=dimensions.b)
#    
#    bottom_flange = pv.Cube(center=(0, -dimensions.h/2 + dimensions.t/2, 0),
#                           x_length=dimensions.b,
#                           y_length=dimensions.t,
#                           z_length=dimensions.b)
#    
#    # Combine and scale to meters
#    beam = web.merge([top_flange, bottom_flange])
#    beam.scale([0.001, 0.001, 0.001])
#    return beam

# Map profile type to function
stringToProfile = {'HEA': create_hea_beam,'IPE': lambda: print('Not implemented yet')}
