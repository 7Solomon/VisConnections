import numpy as np
import pyvista as pv
from src.data.connection_dimensions import ConnectionType, LochplattenDimensions, LochplattenType
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

def create_standard_plate(dimensions: LochplattenDimensions)-> pv.PolyData:
    # Create plate
    plate = pv.Cube(center=(0, 0, dimensions.tm/2),
                    x_length=abs(dimensions.length),
                    y_length=dimensions.height,
                    z_length=dimensions.t)
    
    # Create holes
    print('P1, p2, e1 and e2 are direction less, please implement du kek')
    hole = pv.Cylinder(radius=dimensions.d/2, height=dimensions.t)
    holes = hole.copy()
    for i in range(dimensions.nx):
        for j in range(dimensions.ny):
            hole_position = (dimensions.e1 + i*dimensions.p1, dimensions.e2 + j*dimensions.p2, 0)
            holes = holes.merge(hole.copy().translate(hole_position))
    
    # Combine plate and holes
    plate_with_holes = plate.merge(holes)
    return plate_with_holes

def create_double_plate(dimensions: LochplattenDimensions) -> pv.PolyData:
    # Create plate
    plate_1 = pv.Cube(center=(0, dimensions.tm/2, 0),
                    x_length=abs(dimensions.length),
                    y_length=dimensions.t,
                    z_length=dimensions.height)
    # Create holes
    hole = pv.Cylinder(radius=dimensions.d/2, height=dimensions.t)
    holes = hole.copy()
    for i in range(dimensions.nx):
        for j in range(dimensions.ny):
            hole_position = (dimensions.e1 + i*dimensions.p1, dimensions.e2 + j*dimensions.p2, 0)
            holes = holes.merge(hole.copy().translate(hole_position))
    
    plate_1_with_holes = plate_1.merge(holes)
    plate_2 = plate_1.copy().translate((0, -dimensions.tm - dimensions.t, 0))
    plate_2.rotate_y(180)

    plate_with_holes = plate_1_with_holes.merge(plate_2)
    return plate_with_holes

def create_lochplatte(dimensions: LochplattenDimensions) -> pv.PolyData:
    if dimensions.type == LochplattenType.STANDART:
        return create_standard_plate(dimensions)
    elif dimensions.type == LochplattenType.DOUBLE:
        return create_double_plate(dimensions)
    else:
        raise NotImplementedError(f"LochplattenType {dimensions.type} not implemented yet")



# Map profile type to function
stringToProfile = {ProfileType.HEA: create_hea_beam, ProfileType.IPE: lambda: print('Not implemented yet')}
stringToConnection ={ConnectionType.Lochplatte: create_lochplatte}