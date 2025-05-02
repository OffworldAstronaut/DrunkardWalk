from random import random                # For the drunkard coin toss
from time import time                    # For file R&W operations
import numpy as np                       # For general calculations
from matplotlib import pyplot as plt     # For plotting
from typing import List           # Typing hints


class Drunkard:
    def __init__(self, coin_p: float) -> None:
        """Creates a new drunkard (walker) with the given probability of stepping right.

        Args:
            coin_p (float): Probability of walking to the right.
        """
        self.pos = 0
        self.coin_p = coin_p

    def walk(self) -> int:
        """Flip a coin and move the drunkard."""
        if random() <= self.coin_p:
            self.set_pos(self.pos + 1)
        else:
            self.set_pos(self.pos - 1)
        return self.get_pos()

    # Getters and Setters

    def set_pos(self, new_pos: int) -> None:
        self.pos = new_pos

    def get_pos(self) -> int:
        return self.pos

    def set_coin_p(self, new_coin_p: float) -> None:
        self.coin_p = new_coin_p

    def get_coin_p(self) -> float:
        return self.coin_p


class Sidewalk:
    """Main class where all the single-walker simulations occur."""

    def __init__(self, size: int, coin_p: float = 0.50) -> None:
        """Creates a sidewalk (number line) for the drunkard to walk on.

        Args:
            size (int): Length of the sidewalk.
            coin_p (float, optional): Coin probability of stepping right. Defaults to 0.50.
        """
        self.drunkard = Drunkard(coin_p)
        self.size = size
        self.wandering_pos = []
        self.wandering_std = []

    def get_size(self) -> int:
        return self.size

    def wander(self, end_step: int = 1_000) -> List[int]:
        """Simulate the drunkard's walk over a number of steps."""
        for _ in range(end_step):
            self.wandering_pos.append(self.drunkard.walk())
        return self.wandering_pos

    def make_volatilty_plot(self) -> None:
        """Plots the pseudo-dispersion of a single walker's path."""
        plt.title(f"Random Walk STD (p={self.drunkard.get_coin_p()}; size={self.get_size()})")
        plt.xlabel("Time (Step)")
        plt.ylabel("STD")

        plt.plot(self.wandering_std)

        plt.savefig(
            f"RandomWalkVolatility_{time()}_"
            f"p={self.drunkard.get_coin_p()}_"
            f"size={self.get_size()}.png"
        )
        plt.close()

    def make_average_pos_plot(self) -> None:
        # TODO: This method will plot the average position of the single walker in this sidewalk
        ...

    def make_wandering_plot(self) -> None:
        """Plots the path of the walker over time."""
        plt.title(f"Random Walk (p={self.drunkard.get_coin_p()}; size={self.get_size()})")
        plt.xlabel("Time (Step)")
        plt.ylabel("Position")

        plt.plot(self.wandering_pos)

        plt.savefig(
            f"RandomWalk_{time()}_"
            f"p={self.drunkard.get_coin_p()}_"
            f"size={self.get_size()}.png"
        )
        plt.close()


class City:
    """A city containing multiple sidewalks and walkers (for ensemble simulations)."""

    def __init__(self, n_sidewalks: int, sidewalk_size: int, coin_p: float) -> None:
        self.n_sidewalks = n_sidewalks
        self.sidewalk_size = sidewalk_size
        self.coin_p = coin_p

        self.pub_positions = []
        self.pub_average = []
        self.pub_std = []

    def roam(self, end_step: int = 500) -> List[List[int]]:
        for _ in range(self.n_sidewalks):
            walker = Sidewalk(self.sidewalk_size, self.coin_p)
            self.pub_positions.append(walker.wander(end_step))
        return self.pub_positions

    def calc_pub_avg(self) -> List[float] | None:
        if not any(self.pub_positions):
            return None

        self.pub_positions = np.array(self.pub_positions, dtype=float)
        self.pub_average = []

        for i in range(self.pub_positions.shape[1]):
            self.pub_average.append(np.average(self.pub_positions[:, i]))

        return self.pub_average

    def calc_pub_std(self) -> List[float] | None:
        if not all(isinstance(row, (list, np.ndarray)) for row in self.pub_positions):
            return None

        self.pub_positions = np.array(self.pub_positions, dtype=float)
        self.pub_std = []

        for i in range(self.pub_positions.shape[1]):
            self.pub_std.append(np.std(self.pub_positions[:, i]))

        return self.pub_std

    def make_avg_graph(self) -> None:
        plt.title(f"Average Position in Time for {self.n_sidewalks} Drunkards")
        plt.xlabel("Time (Steps)")
        plt.ylabel("Average Position")

        plt.plot(self.calc_pub_avg())

        plt.savefig(
            f"AvgPos_{time()}_"
            f"nsw={self.n_sidewalks}_"
            f"sws={self.sidewalk_size}_"
            f"p={self.coin_p}.png"
        )
        plt.close()

    def make_std_graph(self) -> None:
        plt.title(f"Dispersion for {self.n_sidewalks} Drunkards")
        plt.xlabel("Time (Steps)")
        plt.ylabel("Dispersion / Standard Deviation")

        plt.plot(self.calc_pub_std())

        plt.savefig(
            f"Disp_{time()}_"
            f"nsw={self.n_sidewalks}_"
            f"sws={self.sidewalk_size}_"
            f"p={self.coin_p}.png"
        )
        plt.close()
