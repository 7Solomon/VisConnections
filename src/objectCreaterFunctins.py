import numpy as np
import pyvista as pv
from src.data.connection_dimensions import ConnectionType, LochplattenDimensions
from src.data.profile_dimensions import ProfileType, get_profile_dimensions


def create_hea_beam(type_number: int, length: int) -> pv.PolyData:
    """
    Vieliecht position in ObjectManager verschieben, und dort nur translate callen
    """
    dimensions = get_profile_dimensions(ProfileType.HEA, type_number)
    
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

def create_lochplatte(dimensions: LochplattenDimensions) -> pv.PolyData:
    """
    Create a plate with holes
    """
    # Create plate
    plate = pv.Cube(center=(0, 0, 0),
                     x_length=dimensions.length,
                     y_length=dimensions.t,
                     z_length=dimensions.height)
    
    # Create holes
    #hole_positions = [
    #    (dimensions.d/2, dimensions.h/2 - dimensions.d/2),
    #    (dimensions.b/2 - dimensions.d/2, dimensions.h/2 - dimensions.d/2),
    #    (dimensions.b/2 - dimensions.d/2, -dimensions.h/2 + dimensions.d/2),
    #    (dimensions.d/2, -dimensions.h/2 + dimensions.d/2)
    #]
    #holes = [pv.Cylinder(radius=dimensions.d/2, height=dimensions.t, center=(x, y, 0), direction=(0, 0, 1)) for x, y in hole_positions]
    #plate = plate.merge(holes)
    
    return plate


# Map profile type to function
stringToProfile = {ProfileType.HEA: create_hea_beam, ProfileType.IPE: lambda: print('Not implemented yet')}
stringToConnection ={ConnectionType.Lochplatte: create_lochplatte}