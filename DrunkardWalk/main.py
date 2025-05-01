from random import random               # for the drunkard coin toss
from time import time                   # for file R&W operations
import numpy as np                      # for general calculations
from matplotlib import pyplot as plt    # for plotting
from typing import Tuple, List          # typing

# Drunkard class, composition with Sidewalk 
class Drunkard:
    def __init__(self, coin_p : float) -> None:
        """Creates a new "drunkard" (walker) with some parameters

        Args:
            coin_p (float): his probability of walking to the right
        """
        self.pos = 0
        self.coin_p = coin_p
        
    def walk(self) -> None:
        """Flip a coin and moves the Drunkard
        """
        if random() <= self.coin_p:
            self.set_pos(self.pos + 1)
            
        else: 
            self.set_pos(self.pos - 1)
            
        return self.get_pos()
        
    # Getters and Setters 
    
    def set_pos(self, new_pos) -> None:
        self.pos = new_pos
        
    def get_pos(self) -> int:
        return self.pos
    
    def set_coin_p(self, new_coin_p) -> None:
        self.coin_p = new_coin_p
        
    def get_coin_p(self) -> float:
        return self.coin_p

# Main class - all the simulations occur here
class Sidewalk:
    def __init__(self, size: int, coin_p: float=0.50):
        """Creates a sidewalk (number line) for the Drunkard to walk on

        Args:
            size (int): size of the sidewalk
            coin_p (float, optional): Coin probability of walking to the right. Defaults to 0.50.
        """
        self.drunkard = Drunkard(coin_p)
        self.size = size
        self.wandering_pos = []
        self.wandering_std = []
    
    def get_size(self) -> int:
        return self.size
    
    def wander(self, end_step: int=1_000) -> Tuple[List]:
        for _ in range (0, end_step):
            self.wandering_pos.append(self.drunkard.walk())
            self.wandering_std.append(np.std(self.wandering_pos))
            
        return (self.wandering_pos, self.wandering_std)

    def make_dispersion_plot(self) -> None:
        """Plots the dispersion of the walker for each step taken"""
        
        plt.title(f"Random Walk STD (p={self.drunkard.get_coin_p()}; size={self.get_size()})")
        plt.xlabel("Time (Step)")
        plt.ylabel("STD")
        
    def make_average_pos_plot(self) -> None:
        # TODO: this method plots the average position of the wandering for each step
        ...

    def make_wandering_plot(self) -> None:
        """Plots the wandering of the walker from beggining until the end."""
        
        plt.title(f"Random Walk (p={self.drunkard.get_coin_p()}; size={self.get_size()})")
        plt.xlabel("Time (Step)")
        plt.ylabel("Position")
        
        plt.plot(self.wandering_pos)
        plt.savefig(f"""RandomWalk_{time()}
                    _p={self.drunkard.get_coin_p()}
                    _size={self.get_size()}.png""")