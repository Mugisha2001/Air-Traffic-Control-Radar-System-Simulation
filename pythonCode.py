import matplotlib.pyplot as plt
import numpy as np
import random
import time

# Aircraft class to simulate an aircraft with position, speed, heading, and altitude
class Aircraft:
    def __init__(self, id, x, y, speed, heading, altitude):
        self.id = id
        self.x = x
        self.y = y
        self.speed = speed
        self.heading = heading
        self.altitude = altitude

    def move(self):
        # Convert heading to radians
        radians = np.radians(self.heading)
        # Update the aircraft's position based on speed and heading
        self.x += self.speed * np.cos(radians)
        self.y += self.speed * np.sin(radians)

    def get_position(self):
        return self.x, self.y

    def get_altitude(self):
        return self.altitude

    def check_collision(self, other_aircraft):
        # Simple collision detection based on proximity of aircrafts
        distance = np.sqrt((self.x - other_aircraft.x)**2 + (self.y - other_aircraft.y)**2)
        return distance < 50  # If the aircrafts are within 50 nautical miles

# Radar system that simulates radar coverage and visualizes aircraft
class RadarSystem:
    def __init__(self, radar_range, radar_center=(0, 0)):
        self.radar_range = radar_range
        self.radar_center = radar_center
        self.aircrafts = []
        self.airspace_zones = []  # List of defined airspace zones

    def add_aircraft(self, aircraft):
        self.aircrafts.append(aircraft)

    def add_airspace_zone(self, x1, y1, x2, y2, name="Zone"):
        # Adding an airspace zone defined by two corner points (x1, y1) and (x2, y2)
        self.airspace_zones.append((x1, y1, x2, y2, name))

    def visualize(self):
        # Create the radar plot
        fig, ax = plt.subplots(figsize=(10, 10))
        ax.set_xlim(-self.radar_range, self.radar_range)
        ax.set_ylim(-self.radar_range, self.radar_range)
        ax.set_title('Air Traffic Control Radar Simulation')

        # Draw radar coverage (circular region of visibility)
        radar_circle = plt.Circle(self.radar_center, self.radar_range, color='blue', fill=False, linestyle='--')
        ax.add_artist(radar_circle)

        # Draw airspace zones
        for zone in self.airspace_zones:
            x1, y1, x2, y2, name = zone
            ax.plot([x1, x2], [y1, y2], 'r--', label=name)
            ax.fill_between([x1, x2], y1, y2, color='yellow', alpha=0.2)

        # Visualize each aircraft on the radar
        for aircraft in self.aircrafts:
            x, y = aircraft.get_position()
            altitude = aircraft.get_altitude()
            ax.plot(x, y, 'bo', markersize=10)  # Plot aircraft as blue dots
            ax.text(x + 2, y + 2, f'ID: {aircraft.id} Alt: {altitude}ft', fontsize=8)

        # Labels for axis
        ax.set_xlabel('X Position (nautical miles)')
        ax.set_ylabel('Y Position (nautical miles)')

        # Display the radar plot
        plt.legend()
        plt.show()

    def update(self):
        # Update positions of all aircrafts
        for aircraft in self.aircrafts:
            aircraft.move()

    def check_aircraft_within_range(self, aircraft):
        x, y = aircraft.get_position()
        # Calculate the distance from the radar center
        distance = np.sqrt(x**2 + y**2)
        return distance <= self.radar_range

    def detect_collisions(self):
        for i, aircraft in enumerate(self.aircrafts):
            for j, other_aircraft in enumerate(self.aircrafts):
                if i != j and aircraft.check_collision(other_aircraft):
                    print(f"Collision detected between Aircraft {aircraft.id} and Aircraft {other_aircraft.id}")

# Function to generate random aircraft data
def generate_random_aircraft(id):
    x = random.randint(-500, 500)
    y = random.randint(-500, 500)
    speed = random.uniform(100, 400)  # Speed in knots
    heading = random.randint(0, 360)  # Heading in degrees
    altitude = random.randint(1000, 35000)  # Altitude in feet
    return Aircraft(id, x, y, speed, heading, altitude)

# Main function to run the simulation
def run_simulation():
    radar_range = 1000  # Radar range in nautical miles
    radar = RadarSystem(radar_range)

    # Generate 10 random aircraft
    for i in range(10):
        aircraft = generate_random_aircraft(i)
        radar.add_aircraft(aircraft)

    # Define airspace zones (example)
    radar.add_airspace_zone(-200, -200, 200, 200, name="Main Zone")

    # Run simulation loop
    while True:
        radar.visualize()  # Visualize the radar screen
        radar.update()  # Update aircraft positions
        radar.detect_collisions()  # Check for any collisions
        time.sleep(1)  # Pause to simulate real-time
        print("Simulation running...")

if __name__ == "__main__":
    run_simulation()
