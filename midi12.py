import pygame
import pygame.midi
import math

# Initialize Pygame and the MIDI module
pygame.init()
pygame.midi.init()

# Set up MIDI input
input_device_id = pygame.midi.get_default_input_id()
midi_input = pygame.midi.Input(input_device_id)

# Set up the Pygame window and drawing surface in full-screen mode
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
window_width, window_height = screen.get_size()
clock = pygame.time.Clock()

# List to store the active points
active_points = []

# List of colors for each semitone
colors = [
    (255, 0, 0),    # Red
    (255, 128, 0),  # Orange
    (255, 255, 0),  # Yellow
    (128, 255, 0),  # Light Green
    (0, 255, 0),    # Green
    (0, 255, 255),  # Cyan
    (0, 128, 255),  # Light Blue
    (0, 0, 255),    # Blue
    (128, 0, 255),  # Purple
    (255, 0, 255),  # Magenta
    (255, 0, 128),  # Pink
    (255, 0, 64)    # Light Pink
]

# Function to calculate the angle based on the MIDI note number (semitone)
def calculate_angle(note_number):
    return note_number * (2 * math.pi / 12) - math.pi / 2

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if midi_input.poll():
        midi_events = midi_input.read(10)  # Read up to 10 MIDI events (adjust as needed)
        for midi_event in midi_events:
            event, timestamp = midi_event
            print("MIDI Event:", event, "Timestamp:", timestamp)

            # Find the note number and velocity from the MIDI event
            status, data1, data2, _ = event
            if status == 144:  # Note On event
                note_number = data1 % 12  # Map to a value between 0 and 11
                velocity = data2

                # Calculate the angle based on the MIDI note number (semitone)
                angle = calculate_angle(note_number)

                # Add a new point at the center of the screen with initial velocity and angle
                center_x, center_y = window_width // 2, window_height // 2
                # Reduce the velocity to make the dots move slower
                velocity = velocity * 0.1  # Adjust the factor (0.06) to control the speed
                lifespan = 150  # Adjust the lifespan (number of frames) here

                # Append the point to the active_points list with its corresponding color
                color = colors[note_number]
                active_points.append({"x": center_x, "y": center_y, "initial_velocity": velocity, "angle": angle, "lifespan": lifespan, "distance_traveled": 0, "color": color})

    # Clear the screen
    screen.fill((0, 0, 0))
    
    # List to store the indices of moving points
    moving_points_indices = []

    # Update the active points' positions and draw them on the screen
    for i, point in enumerate(active_points):
        x, y = point["x"], point["y"]
        velocity = point["initial_velocity"]  # Get the initial velocity instead of updating it
        angle = point["angle"]
        lifespan = point["lifespan"]
        distance_traveled = point["distance_traveled"]
        color = point["color"]

        # Calculate the new position based on the velocity and angle
        new_x = x + int(velocity * math.cos(angle))
        new_y = y + int(velocity * math.sin(angle))

        # Update the point's position and distance traveled
        point["x"], point["y"] = new_x, new_y
        point["distance_traveled"] += math.sqrt((new_x - x) ** 2 + (new_y - y) ** 2)

        # Decrease the lifespan for each point
        point["lifespan"] -= 1

        # Check if the point has traveled a certain number of pixels
        if point["distance_traveled"] >= 300:  # Adjust the threshold distance here
            point["initial_velocity"] = 0  # Set velocity to 0 to stop the point from moving

        # Calculate the radius of the dot based on its remaining lifespan
        dot_radius = 3 * (30 - point["lifespan"] / 3)  # Adjust the initial radius (25) as needed

        # Draw the point on the screen with its corresponding color
        pygame.draw.circle(screen, color, (new_x, new_y), int(dot_radius))

        # Add the index of the moving point to the list
        if velocity > 0:
            moving_points_indices.append(i)

    # Draw lines between the moving points
    for i in range(1, len(moving_points_indices)):
        prev_x, prev_y = active_points[moving_points_indices[i - 1]]["x"], active_points[moving_points_indices[i - 1]]["y"]
        current_x, current_y = active_points[moving_points_indices[i]]["x"], active_points[moving_points_indices[i]]["y"]
        line_color = active_points[moving_points_indices[i]]["color"]  # Use the color of the current point for the line
        pygame.draw.line(screen, line_color, (prev_x, prev_y), (current_x, current_y), 10)
  
    # Remove points with a lifespan of 0
    active_points = [point for point in active_points if point["lifespan"] > 0]

    # Update the display
    pygame.display.flip()
    clock.tick(30)

# Cleanup
midi_input.close()
pygame.midi.quit()
pygame.quit()
