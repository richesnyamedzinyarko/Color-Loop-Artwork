import colorsys
import math
import tkinter as tk


class ColorLoopArtwork:

    def __init__(self, root):
        self.root = root
        self.root.title("Python Color Loop Artwork")
        self.root.configure(bg="#111111")

        # Canvas dimensions
        self.width = 700
        self.height = 700
        self.center_x = self.width // 2
        self.center_y = self.height // 2

        # Animation state variables
        self.phase = 0.0
        self.is_running = True
        self.num_rings = 45
        self.sides = 6  # Hexagon-based spiral (change to 3, 4, 5, 8, etc.)

        # Create the Drawing Canvas
        self.canvas = tk.Canvas(
            root,
            width=self.width,
            height=self.height,
            bg="#080808",
            highlightthickness=0,
        )
        self.canvas.pack(padx=15, pady=(15, 5))

        # UI Controls Frame
        controls = tk.Frame(root, bg="#111111")
        controls.pack(fill=tk.X, padx=15, pady=(5, 15))

        self.toggle_btn = tk.Button(
            controls,
            text="Pause",
            command=self.toggle_animation,
            bg="#222222",
            fg="white",
            activebackground="#444444",
            activeforeground="white",
            relief=tk.FLAT,
            width=10,
            font=("Helvetica", 10, "bold"),
        )
        self.toggle_btn.pack(side=tk.LEFT, padx=5)

        tk.Label(
            controls,
            text="Loop Speed:",
            bg="#111111",
            fg="#cccccc",
            font=("Helvetica", 10),
        ).pack(side=tk.LEFT, padx=(15, 5))

        self.speed_slider = tk.Scale(
            controls,
            from_=1,
            to=20,
            orient=tk.HORIZONTAL,
            bg="#111111",
            fg="white",
            troughcolor="#222222",
            highlightthickness=0,
            length=200,
        )
        self.speed_slider.set(6)
        self.speed_slider.pack(side=tk.LEFT, padx=5)

        # Start the animation loop
        self.animate()

    def toggle_animation(self):
        self.is_running = not self.is_running
        self.toggle_btn.config(text="Pause" if self.is_running else "Resume")
        if self.is_running:
            self.animate()

    def hsv_to_hex(self, h, s, v):
        """Converts HSV values (0.0 - 1.0) into a Tkinter-compatible hex string."""
        r, g, b = colorsys.hsv_to_rgb(h % 1.0, s, v)
        return f"#{int(r * 255):02x}{int(g * 255):02x}{int(b * 255):02x}"

    def get_polygon_points(self, radius, rotation_angle):
        """Calculates vertex coordinates for a rotated regular polygon."""
        points = []
        for i in range(self.sides):
            angle = rotation_angle + (2 * math.pi * i / self.sides)
            x = self.center_x + radius * math.cos(angle)
            y = self.center_y + radius * math.sin(angle)
            points.extend([x, y])
        return points

    def draw_frame(self):
        self.canvas.delete("all")

        # Draw rings from outermost to innermost
        for i in range(self.num_rings, 0, -1):
            progress = i / self.num_rings

            # Pulsing radius effect
            pulse = math.sin(self.phase * 2 + progress * 6) * 12
            radius = (progress * (self.width * 0.46)) + pulse
            if radius <= 2:
                continue

            # Continuous color loop calculation
            hue = (progress * 1.2) - (self.phase * 0.4)
            saturation = 0.85
            # Fade brightness slightly near the center for depth
            brightness = 0.35 + (0.65 * progress)
            color = self.hsv_to_hex(hue, saturation, brightness)

            # Twist rotation angle per ring
            angle = (progress * math.pi * 1.5) + math.sin(self.phase) * 0.8

            points = self.get_polygon_points(radius, angle)
            self.canvas.create_polygon(
                points, outline=color, fill="", width=2.5
            )

        # Draw a glowing central core
        core_hue = -self.phase * 0.4
        core_color = self.hsv_to_hex(core_hue, 0.9, 1.0)
        self.canvas.create_oval(
            self.center_x - 8,
            self.center_y - 8,
            self.center_x + 8,
            self.center_y + 8,
            fill=core_color,
            outline="",
        )

    def animate(self):
        if not self.is_running:
            return

        self.draw_frame()

        # Advance phase based on slider value
        speed = self.speed_slider.get() * 0.004
        self.phase += speed

        # Schedule next frame (~60 FPS)
        self.root.after(16, self.animate)


if __name__ == "__main__":
    root = tk.Tk()
    app = ColorLoopArtwork(root)
    root.mainloop()