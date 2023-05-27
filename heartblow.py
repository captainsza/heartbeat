import numpy as np
import matplotlib.pyplot as plt
import imageio

def heart_function(t, stretch_factor, bend_factor):
    x = stretch_factor * (16 * np.sin(t)**3)
    y = bend_factor * (13 * np.cos(t) - 5 * np.cos(2 * t) - 2 * np.cos(3 * t) - np.cos(4 * t))
    return x, y

def generate_heart_animation(filename, frames, stretch_factor, bend_factor):
    images = []

    # Generate the heartbeat frames
    heartbeat_frames = np.concatenate([np.linspace(1, 1.5, int(frames/2)), np.linspace(1.5, 1, int(frames/2))])

    for i in range(frames):
        t = np.linspace(0, 2 * np.pi, 500)  # Reduced number of points
        x, y = heart_function(t, stretch_factor[i] * heartbeat_frames[i], bend_factor[i])

        fig, ax = plt.subplots(figsize=(6, 6))
        ax.scatter(x, y, c='black', s=1)  # Black particles inside the heart
        ax.plot(x, y, c='pink', linewidth=2)  # Pink heart outline

        # Add sparkling particles
        num_particles = 1500  # Reduced number of particles
        particle_t = np.random.uniform(0, 2 * np.pi, num_particles)
        particle_r = np.random.uniform(0, 1, num_particles) ** 0.5  # Adjust the distribution for particles to align around the shape
        particle_x = stretch_factor[i] * heartbeat_frames[i] * (particle_r * (16 * np.sin(particle_t)**3))
        particle_y = bend_factor[i] * (particle_r * (13 * np.cos(particle_t) - 5 * np.cos(2 * particle_t) - 2 * np.cos(3 * particle_t) - np.cos(4 * particle_t)))

        # Simulate blowing effect
        blow_factor = np.random.uniform(0.8, 1.2, num_particles)  # Random scaling factor for blowing effect
        particle_x *= blow_factor
        particle_y *= blow_factor

        ax.scatter(particle_x, particle_y, c='pink', s=1, alpha=0.6)  # Sparkling particles

        ax.axis('off')
        ax.set_xlim(-30, 30)  # Adjusted x-axis limits
        ax.set_ylim(-30, 30)  # Adjusted y-axis limits
        ax.set_facecolor('black')  # Set background color to black

        fig.set_facecolor('black')  # Set figure background color to black

        fig.canvas.draw()
        image = np.frombuffer(fig.canvas.tostring_rgb(), dtype='uint8')
        image = image.reshape(fig.canvas.get_width_height()[::-1] + (3,))
        images.append(image)

        plt.close(fig)

    imageio.mimsave(filename, images, fps=7)

if __name__ == "__main__":
    stretch_factor = np.linspace(1, 1.5, 20)
    bend_factor = np.linspace(1, 0.8, 20)
    factors = np.vstack((stretch_factor, bend_factor)).T

    generate_heart_animation("love.gif", len(factors), factors[:, 0], factors[:, 1])