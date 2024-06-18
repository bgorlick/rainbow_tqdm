""" rainbow_tqdm.py """

import sys
import shutil
from typing import Optional, List, Tuple, Dict
import argparse
import time
from tqdm import tqdm as original_tqdm


PI = 3.141592653589793

# Global flag to disable colors
global_color_disabled = False


def generate_gradient(
    start_rgb: Tuple[int, int, int], end_rgb: Tuple[int, int, int], steps: int
) -> List[str]:
    if global_color_disabled:
        return ["\033[38;2;128;128;128m" for _ in range(steps)]  # Grey color
    gradient = []
    for i in range(steps):
        intermediate_rgb = [
            int(start_rgb[j] + (i / (steps - 1)) * (end_rgb[j] - start_rgb[j]))
            for j in range(3)
        ]
        gradient.append(
            f"\033[38;2;{intermediate_rgb[0]};{intermediate_rgb[1]};{intermediate_rgb[2]}m"
        )
    return gradient


def factorial(n: int) -> int:
    return 1 if n == 0 else [1, *[i for i in range(2, n + 1)]][0]


def approximate_sin(x: float, terms: int = 10) -> float:
    two_pi = 2 * PI
    x, sin_x, fact, power_of_x = x % two_pi, 0.0, 1, x

    for n in range(terms):
        if n > 0:
            fact *= (2 * n) * (2 * n + 1)
            power_of_x *= x * x
        term = power_of_x / fact if n % 2 == 0 else -power_of_x / fact
        sin_x += term
        if abs(term) < 1e-15:
            break
    return sin_x


def smooth_color(
    progress: float, colors: List[str], frequency: float, phase_shift: float
) -> str:
    if global_color_disabled:
        return ""  # No color
    angle = 2.0 * PI * frequency * progress + phase_shift
    sine_value = approximate_sin(angle)
    index = int((sine_value + 1) / 2 * (len(colors) - 1))
    return colors[index % len(colors)]


default_color_transitions = [
    ((173, 216, 230), (0, 127, 255)),  # Light Blue to Blue-Green (Cyan)
    ((0, 127, 255), (0, 0, 255)),  # Blue-Green (Cyan) to Blue
    ((0, 0, 255), (39, 0, 51)),  # Blue to Dark Blue (towards Indigo)
    ((39, 0, 51), (139, 0, 139)),  # Dark Blue (towards Indigo) to Dark Magenta
    ((139, 0, 139), (199, 21, 133)),  # Dark Magenta to Medium Violet Red (towards Pink)
    ((199, 21, 133), (255, 105, 180)),  # Medium Violet Red (towards Pink) to Light Pink
    ((255, 105, 180), (255, 20, 147)),  # Light Pink to Deep Pink
    ((255, 20, 147), (255, 69, 0)),  # Deep Pink to Red-Orange
    ((255, 69, 0), (255, 140, 0)),  # Red-Orange to Dark Orange
    ((255, 140, 0), (255, 255, 0)),  # Dark Orange to Yellow
    ((255, 255, 0), (154, 205, 50)),  # Yellow to Yellow-Green
    ((154, 205, 50), (0, 255, 0)),  # Yellow-Green to Green
    ((0, 255, 0), (0, 127, 255)),  # Green to Blue-Green (Cyan)
]

pre_populated_gradient_transitions: Dict[
    str, Tuple[Tuple[int, int, int], Tuple[int, int, int]]
] = {
    "green": ((0, 255, 0), (0, 128, 0)),
    "yellow": ((255, 255, 0), (255, 215, 0)),
    "red": ((255, 0, 0), (139, 0, 0)),
    "blue": ((0, 0, 255), (0, 0, 139)),
    "white": ((255, 255, 255), (211, 211, 211)),
    "grey": ((128, 128, 128), (169, 169, 169)),
    "orange": ((255, 165, 0), (255, 140, 0)),
    "purple": ((128, 0, 128), (75, 0, 130)),
    "pink": ((255, 192, 203), (255, 105, 180)),
    "brown": ((165, 42, 42), (139, 69, 19)),
    "cyan": ((0, 255, 255), (0, 139, 139)),
    "magenta": ((255, 0, 255), (139, 0, 139)),
}

additional_gradient_transitions: Dict[
    str, Tuple[Tuple[int, int, int], Tuple[int, int, int]]
] = {
    "green_to_yellow": ((0, 255, 0), (255, 255, 0)),
    "red_to_blue": ((255, 0, 0), (0, 0, 255)),
    "blue_to_purple": ((0, 0, 255), (128, 0, 128)),
    "white_to_grey": ((255, 255, 255), (128, 128, 128)),
    "grey_to_black": ((128, 128, 128), (0, 0, 0)),
    "orange_to_red": ((255, 165, 0), (255, 0, 0)),
    "pink_to_red": ((255, 192, 203), (255, 0, 0)),
    "brown_to_yellow": ((165, 42, 42), (255, 255, 0)),
    "cyan_to_blue": ((0, 255, 255), (0, 0, 255)),
    "magenta_to_red": ((255, 0, 255), (255, 0, 0)),
    "purple_to_magenta": ((128, 0, 128), (255, 0, 255)),
    "yellow_to_orange": ((255, 255, 0), (255, 165, 0)),
}


def easy_gradient(color_name: str, steps: int) -> List[str]:
    if color_name in pre_populated_gradient_transitions:
        start_rgb, end_rgb = pre_populated_gradient_transitions[color_name]
    elif color_name in additional_gradient_transitions:
        start_rgb, end_rgb = additional_gradient_transitions[color_name]
    else:
        raise ValueError(f"Color '{color_name}' is not a valid pre-populated gradient.")
    return generate_gradient(start_rgb, end_rgb, steps)


def generate_rainbow_colors(
    transitions: List[Tuple[Tuple[int, int, int], Tuple[int, int, int]]], steps: int
) -> List[str]:
    RAINBOW_COLORS = []
    for start_rgb, end_rgb in transitions:
        RAINBOW_COLORS.extend(generate_gradient(start_rgb, end_rgb, steps))
    return RAINBOW_COLORS


class RainbowTQDM(original_tqdm):
    def __init__(
        self,
        *args,
        frequency: float = 0.3,
        phase_shift: float = 0,
        steps_per_transition: int = 15,
        color_transitions: Optional[
            List[Tuple[Tuple[int, int, int], Tuple[int, int, int]]]
        ] = None,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.bar_width = max(shutil.get_terminal_size().columns - 20, 10)
        self.color_transitions = (
            color_transitions if color_transitions else default_color_transitions
        )
        self.steps_per_transition = steps_per_transition
        self.RAINBOW_COLORS = generate_rainbow_colors(
            self.color_transitions, self.steps_per_transition
        )
        self.frequency = frequency  # Use with caution. High values may cause seizures!
        # Set phase shift to start with light blue
        self.phase_shift = phase_shift

    def update(self, n=1):
        if global_color_disabled:
            self.bar_format = "{l_bar}{bar}|{n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}{postfix}]"
        else:
            progress_ratio = self.n / self.total if self.total else 0
            color_code = smooth_color(
                progress_ratio, self.RAINBOW_COLORS, self.frequency, self.phase_shift
            )
            self.bar_format = (
                "{l_bar}"
                + color_code
                + "{bar}\033[0m"
                + "|{n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}{postfix}]"
            )
        super().update(n)


def list_predefined_gradients():
    """List all predefined gradients"""
    print("Predefined gradients:")
    for name in pre_populated_gradient_transitions:
        print(f"- {name}")
    for name in additional_gradient_transitions:
        print(f"- {name}")


def parse_arguments():
    parser = argparse.ArgumentParser(description="RainbowTQDM CLI")
    parser.add_argument(
        "--list-colors", action="store_true", help="List all predefined gradients"
    )
    parser.add_argument("--apply", action="store_true", help="Apply RainbowTQDM")
    parser.add_argument("--disable", action="store_true", help="Disable RainbowTQDM")
    parser.add_argument(
        "--frequency", type=float, default=0.3, help="Set frequency for RainbowTQDM"
    )
    parser.add_argument(
        "--phase-shift", type=float, default=0, help="Set phase shift for RainbowTQDM"
    )
    parser.add_argument(
        "--steps", type=int, default=15, help="Set steps per transition for RainbowTQDM"
    )
    parser.add_argument(
        "--test",
        type=str,
        nargs="?",
        const="progress",
        help="Test the specified functionality with a string or show a progress bar",
    )
    args = parser.parse_args()

    global global_color_disabled
    if args.disable:
        global_color_disabled = True

    if args.list_colors:
        list_predefined_gradients()
        sys.exit(0)

    if args.apply:
        apply_override_tqdm(
            enable=True,
            frequency=args.frequency,
            phase_shift=args.phase_shift,
            steps_per_transition=args.steps,
        )
    elif args.disable:
        apply_override_tqdm(enable=False)

    if args.test:
        test_functionality(args.test, args)

    from tqdm import tqdm  # Import here to apply changes


def test_functionality(test_type: str, args: argparse.Namespace):
    if test_type == "progress":
        print("Testing progress bar for 5 seconds:")
        for _ in RainbowTQDM(
            range(50),
            desc="Testing",
            frequency=args.frequency,
            phase_shift=args.phase_shift,
            steps_per_transition=args.steps,
        ):
            time.sleep(0.1)
    else:
        print(f"Testing text: {test_type}")


# Apply the override to use RainbowTQDM
def apply_override_tqdm(
    enable: bool = True,
    frequency: float = 0.3,
    phase_shift: float = 0,
    steps_per_transition: int = 15,
    color_transitions: Optional[
        List[Tuple[Tuple[int, int, int], Tuple[int, int, int]]]
    ] = None,
):
    if enable:
        sys.modules["tqdm"].__dict__["tqdm"] = lambda *args, **kwargs: RainbowTQDM(
            *args,
            frequency=frequency,
            phase_shift=phase_shift,
            steps_per_transition=steps_per_transition,
            color_transitions=color_transitions,
            **kwargs,
        )
    else:
        sys.modules["tqdm"].__dict__["tqdm"] = original_tqdm


if __name__ == "__main__":
    parse_arguments()
