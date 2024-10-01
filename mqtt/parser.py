def parse_message_to_vector(input_string):
    # Initialize the output vector and the success flag
    vector = []
    is_valid = False
    
    # Define the expected keys and their order
    expected_keys = {
        'x': 0,
        'y': 1,
        'z': 2,
        'Rx': 3,
        'Ry': 4,
        'Rz': 5
    }
    
    # Initialize the vector with None values
    vector = [None] * 6

    # Split the string by commas and strip whitespace
    elements = [e.strip() for e in input_string.split(',')]
    
    # Process each element
    for e in elements:
        try:
            # Split each element by ':' to get key and value
            key, value = e.split(':')
            key = key.strip()
            value = value.strip()
            
            if key in expected_keys:
                # Store the float value in the correct position
                vector[expected_keys[key]] = float(value)
            else:
                print(f"Error: '{key}' is not a valid coordinate name.")
                return [], False
            
        except (ValueError, IndexError):
            print(f"Error: '{e}' is not a valid entry. It should be in the format 'x: value_x, y: value_y, z: value_z, Rx: value_Rx, Ry: value_Ry, Rz: value_Rz'.")
            return [], False
            
    # Check if all required coordinates were provided
    if all(v is not None for v in vector):
        is_valid = True
    else:
        print("Error: Not all coordinates were provided.")
    
    return is_valid, vector