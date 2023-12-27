import sys
from tqdm import tqdm as original_tqdm
import shutil
import random

PI = 3.141592653589793

def generate_gradient(start_rgb, end_rgb, steps):
    gradient = []
    for i in range(steps):
        intermediate_rgb = [
            int(start_rgb[j] + (i / (steps - 1)) * (end_rgb[j] - start_rgb[j]))
            for j in range(3)
        ]
        gradient.append(f"\033[38;2;{intermediate_rgb[0]};{intermediate_rgb[1]};{intermediate_rgb[2]}m")
    return gradient

def factorial(n):
    return 1 if n == 0 else [1, *[i for i in range(2, n + 1)]][0]

def approximate_sin(x, terms=10):
    two_pi = 2 * PI
    x, sin_x, fact, power_of_x = x % two_pi, 0, 1, x
    
    for n in range(terms):
        if n > 0: fact *= (2 * n) * (2 * n + 1); power_of_x *= x * x
        term = power_of_x / fact if n % 2 == 0 else -power_of_x / fact
        sin_x += term
        if abs(term) < 1e-15: break
    return sin_x

def smooth_color(progress, colors, frequency, phase_shift):
    angle = 2.0 * PI * frequency * progress + phase_shift
    sine_value = approximate_sin(angle)
    index = int((sine_value + 1) / 2 * (len(colors) - 1))
    return colors[index % len(colors)]

color_transitions = [
    ((255, 255, 0), (154, 205, 50)),   # Yellow to Yellow-Green
    ((154, 205, 50), (0, 255, 0)),     # Yellow-Green to Green
    ((0, 255, 0), (0, 127, 255)),      # Green to Blue-Green (Cyan)
    ((0, 127, 255), (0, 0, 255)),      # Blue-Green (Cyan) to Blue
    ((0, 0, 255), (39, 0, 51)),        # Blue to Dark Blue (towards Indigo)
    ((39, 0, 51), (139, 0, 139)),      # Dark Blue (towards Indigo) to Dark Magenta
    ((139, 0, 139), (199, 21, 133)),   # Dark Magenta to Medium Violet Red (towards Pink)
    ((199, 21, 133), (255, 105, 180)), # Medium Violet Red (towards Pink) to Light Pink
    ((255, 105, 180), (255, 20, 147)), # Light Pink to Deep Pink
    ((255, 20, 147), (255, 69, 0)),    # Deep Pink to Red-Orange
    ((255, 69, 0), (255, 140, 0)),     # Red-Orange to Dark Orange
    ((255, 140, 0), (255, 255, 0)),    # Dark Orange to Yellow
]

steps_per_transition = 15

def generate_rainbow_colors():
    RAINBOW_COLORS = []
    for start_rgb, end_rgb in color_transitions:
        RAINBOW_COLORS.extend(generate_gradient(start_rgb, end_rgb, steps_per_transition))
    return RAINBOW_COLORS

class RainbowTQDM(original_tqdm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bar_width = max(shutil.get_terminal_size().columns - 20, 10)
        self.RAINBOW_COLORS = generate_rainbow_colors()
        self.frequency = 0.3  # Use with caution. High values may cause seizures!
        self.phase_shift = random.uniform(0, 2 * PI)

    def update(self, n=1):
        progress_ratio = self.n / self.total if self.total else 0
        color_code = smooth_color(progress_ratio, self.RAINBOW_COLORS, self.frequency, self.phase_shift)
        self.bar_format = "{l_bar}" + color_code + "{bar}\033[0m" + "|{n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}{postfix}]"
        super().update(n)

# byebye boring grey tqdm :)
def apply_override_tqdm():
    #sys.modules['tqdm']._instances.clear()
    sys.modules['tqdm'].tqdm = RainbowTQDM

apply_override_tqdm()