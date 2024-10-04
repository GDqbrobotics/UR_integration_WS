from PIL import Image
import numpy as np

def extract_points_from_image(image_path):
    img = Image.open(image_path).convert('L')  # Convert to grayscale
    img_array = np.array(img)

    points = []
    for y in range(img_array.shape[0]):
        for x in range(img_array.shape[1]):
            if img_array[y, x] < 128:  # Assuming black is less than 128
                points.append((x, y))

    return points, img_array.shape

def order_points(points):
    if not points:
        return []

    ordered_points = [points.pop(0)]

    while points:
        last_point = ordered_points[-1]
        closest_point = min(points, key=lambda p: np.linalg.norm(np.array(last_point) - np.array(p)))
        ordered_points.append(closest_point)
        points.remove(closest_point)

    return ordered_points

def convert_pixels_to_meters(points, img_size):
    width, height = img_size
    max_side = max(width, height)
    scale = 0.4 / max_side  # Scale to 40 cm
    offset_x = 0
    offset_y = -0.6

    # Centering coordinates
    center_x = width / 2 * scale + offset_x
    center_y = height / 2 * scale + offset_y

    converted_points = []
    for i, (x, y) in enumerate(points):
        if i % 5 == 0:  # Save every 5th point
            x_m = (x * scale) - center_x
            y_m = -(y * scale) + center_y  # Invert y for proper orientation
            converted_points.append((x_m, y_m))

    return converted_points

def save_points_to_file(points, filename):
    with open(filename, 'w') as f:
        for x, y in points:
            f.write(f"p[{x:.3f}, {y:.3f}, 0.01, 2.1, 2.25, 0]\n")
        f.write("p[0, -0.6, 0.1, 2.1, 2.25, 0]\n")

def main():
    image_path = 'image.png'  # Update this to your image path
    points, img_size = extract_points_from_image(image_path)
    ordered_points = order_points(points)
    converted_points = convert_pixels_to_meters(ordered_points, img_size)
    
    save_points_to_file(converted_points, 'traj.txt')

    # Output the converted points (optional)
    for point in converted_points:
        print(point)

if __name__ == '__main__':
    main()