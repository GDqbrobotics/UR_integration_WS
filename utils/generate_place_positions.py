import rotation
import math

distance_between_places = 0.01
delta_alpha = 2*3.14 / 16
delta_beta = 2*3.14 / 9

def generate_places(x_center, y_center):
    points = []
    for alpha in range(-8,8):
        x = x_center - math.cos(alpha*delta_alpha)*0.025
        y = y_center - math.sin(alpha*delta_alpha)*0.025
        angles = rotation.get_rotation_for_ur(3.14,0.15,alpha*delta_alpha)
        p = (x,y,angles)
        points.append(p)
    
    for beta in range(-4,5):
        x = x_center - math.cos(beta*delta_beta)*0.01
        y = y_center - math.sin(beta*delta_beta)*0.01
        angles = rotation.get_rotation_for_ur(3.14,0.15,beta*delta_beta)
        p = (x,y,angles)
        points.append(p)

    return points

def generate_picks(x_center, y_center):
    points = []
    for delta_x in range(-2,3):
        x = x_center + delta_x*0.03
        for delta_y in range(-2,3):
            y = y_center + delta_y*0.02
            p = (x,y)
            points.append(p)
    return points

def save_points_to_file(picks,places, filename):
    with open(filename, 'w') as f:
        for i in range(25):
            x,y = picks[i]
            f.write(f"x: {x:.3f},y: {y:.3f},z: 0.0135,Rx: 2.655,Ry: 0.0,Rz: 1.76, action: Pick\n")
            x,y,angles = places[i]
            f.write(f"x: {x:.3f},y: {y:.3f},z: 0.025, Rx: {angles[0]:.3f},Ry: {angles[1]:.3f},Rz: {angles[2]:.3f}, action: Place\n")

#example of usage
places = generate_places(.08, -.50035)
picks = generate_picks(-0.1,-.5)

save_points_to_file(picks,places,"targets.txt")
