import numpy as np
import pyvista as pv
from src.data.profile_dimensions import get_profile_dimensions
from src.data.util_data import Vector3D


def create_hea_beam(type_number: int, length: int) -> pv.PolyData:
    """
    Vieliecht position in ObjectManager verschieben, und dort nur translate callen
    """
    dimensions = get_profile_dimensions('HEA', type_number)
    
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
    
    ## Kombination
    beam = steg.merge([top_flansch, bottom_flansch])

    # Look
    #beam.point_data["Metallic"] = 1.0  # Full metallic
    #beam.point_data["Roughness"] = 0.3  # Slight roughness
    #beam.point_data["Colors"] = np.tile([0.8, 0.8, 0.85], (beam.n_points, 1))
   


    #beam.scale([0.0001, 0.0001, 0.0001])
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
