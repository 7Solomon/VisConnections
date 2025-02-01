from src.data.connection_dimensions import LochplattenDimensions, LochplattenType


def get_connection_dimension(object_1, connection_type, object_2):
    """
    Gets the connection Dimension between two objects
    """

    pos1 = object_1.connection_points.points[0].position
    oriantation = object_1.connection_points.points[0].oriantation

    if object_2 is not None:
        pos2 = object_2.connection_points.points[0].position
    else:
        pos2 = oriantation*100 + pos1

    origin = pos1  # maybe differ if negativ oriantation
    pos_vector = pos2 - pos1
    length = pos_vector.length_in_direction(oriantation)

    start_nx = 2
    start_ny = 2
    ## Add Function for matching type to dimesnion please Future jj
    dimensions = LochplattenDimensions(
                                        type=LochplattenType.DOUBLE, 
                                        length=abs(length),
                                        height=object_1.dimensions.h,
                                        tm=object_1.dimensions.tw, 
                                        t=10,
                                        e1=100, e2=100,p1=100, p2=100, d=10, nx=10, ny=10
                                    )
    return dimensions, origin