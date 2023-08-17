
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

            status, data1, data2, _ = event
            note_number = data1  # MIDI note value

            if status == 144 and data2 != 0:  # Note On event
                # Calculate the y-coordinate and x-coordinate
                y_coordinate = window_height - int((note_number - 36) / (46) * window_height)
                x_coordinate = int((timestamp / 100000) * window_width)

                # Add a new point to active_points list
                color = colors[note_number % 12]
                active_points.append({"x": x_coordinate, "y": y_coordinate, "color": color})


    # Clear the screen
    screen.fill((0, 0, 0))
    
    # Draw the active points on the screen
    for point in active_points:
        x, y = point["x"], point["y"]
        color = point["color"]
        pygame.draw.circle(screen, color, (x, y), 5)

    # Update the display
    pygame.display.flip()
    clock.tick(30)

# Cleanup
midi_input.close()
pygame.midi.quit()
pygame.quit()

