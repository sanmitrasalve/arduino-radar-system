import matplotlib.pyplot as plt
import numpy as np
import serial
import time

def read_serial_data(ser):
    try:
        line = ser.readline().decode('utf-8').strip()
        if "," in line:
            angle, distance = map(int, line.split(","))
            return angle, distance
    except (ValueError, IndexError):
        pass
    return None, None

def plot_radar(serial_port):
    ser = serial.Serial(serial_port, 9600, timeout=1)
    time.sleep(2)

    fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
    fig.set_facecolor('#0f0f0f')
    ax.set_facecolor('#101820')
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)
    ax.set_thetamin(0)
    ax.set_thetamax(180)
    ax.set_ylim(0, 200)
    ax.grid(True, color='lime', linestyle='--', linewidth=0.5)
    ax.set_title("180° Radar Simulation", color='white', fontsize=14)
    ax.tick_params(colors='white')
    for label in ax.get_xticklabels() + ax.get_yticklabels():
        label.set_color('white')

    scatter = ax.scatter([], [], c='red', s=50)
    sweep_line, = ax.plot([], [], color='lime', linewidth=2)

    detected_objects = []

    while True:
        angle, distance = read_serial_data(ser)

        if angle is not None:
            theta = np.radians(angle)
            sweep_line.set_data([theta, theta], [0, 200])

            if 5 < distance <= 200:
                rad_angle = np.radians(angle)
                detected_objects.append((rad_angle, distance, time.time()))  # Add with timestamp
                print(f"Object detected at Angle: {angle}°, Distance: {distance} cm")

        # Remove old objects after 2 seconds
        current_time = time.time()
        detected_objects = [
            (a, d, t) for a, d, t in detected_objects if current_time - t < 2
        ]

        if detected_objects:
            angles, distances, _ = zip(*detected_objects)
            scatter.set_offsets(np.column_stack([angles, distances]))
        else:
            scatter.set_offsets(np.empty((0, 2)))

        plt.pause(0.05)

if __name__ == "__main__":
    serial_port = "COM6"
    plot_radar(serial_port)
