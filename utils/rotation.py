import math

# Convert Euler angles (ZXY) to Quaternion
def euler_to_quaternion_zxy(heading, attitude, bank):
    # Half angles
    c1 = math.cos(heading / 2)
    s1 = math.sin(heading / 2)
    c2 = math.cos(attitude / 2)
    s2 = math.sin(attitude / 2)
    c3 = math.cos(bank / 2)
    s3 = math.sin(bank / 2)

    # Compute quaternion components
    w = c1 * c2 * c3 + s1 * s2 * s3
    x = s1 * c2 * c3 - c1 * s2 * s3
    y = c1 * s2 * c3 + s1 * c2 * s3
    z = c1 * c2 * s3 - s1 * s2 * c3

    return w, x, y, z

# Convert Quaternion to Axis-Angle
def quaternion_to_axis_angle(w, x, y, z):
    # Compute the angle
    angle = 2 * math.acos(w)
    angles = (x*angle, y*angle, z*angle)

    return angles

def get_rotation_for_ur(heading, attitude, bank):
    # Convert Euler angles (ZXY) to quaternion
    w, x, y, z = euler_to_quaternion_zxy(heading, attitude, bank)

    # Convert quaternion to axis-angle
    angles = quaternion_to_axis_angle(w, x, y, z)

    return angles