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
    
    def get_size(self) -> int:
        return self.size
    
    
    # Set of functions related to the single walker created in the sidewalk
    def wander(self, end_step: int=1_000) -> List:
        for _ in range (0, end_step):
            self.wandering_pos.append(self.drunkard.walk())
            
        return (self.wandering_pos)

    def make_volatilty_plot(self) -> None:
        """Plots the dispersion of the walker for each step taken. 
        ISN'T the true dispersion of the process - only measures how volatile a single walker path is. """
        
        plt.title(f"Random Walk STD (p={self.drunkard.get_coin_p()}; size={self.get_size()})")
        plt.xlabel("Time (Step)")
        plt.ylabel("STD")
        
        plt.plot(self.wandering_std)
        
        plt.savefig(f"""RandomWalkVolatility_
                    {time()}_
                    p={self.drunkard.get_coin_p()}_
                    size={self.get_size()}.png""")
        
    def make_average_pos_plot(self) -> None:
        # TODO: This method will plot the average position of the single walker in this sidewalk
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

class City:
    def __init__(self, n_sidewalks: int, sidewalk_size: int, coin_p: float) -> None:
        self.n_sidewalks = n_sidewalks
        self.sidewalk_size = sidewalk_size
        self.coin_p = coin_p
        
        self.pub_positions = []
        self.pub_average = []
        self.pub_std = []
        
    def roam(self, end_step: int=500) -> List[List]:
        for _ in range(0, self.n_sidewalks):
            walker = Sidewalk(self.sidewalk_size, self.coin_p)
            self.pub_positions.append(walker.wander(end_step))
            
        return self.pub_positions
    
    def calc_pub_avg(self) -> List[float] | None:
        if not any(self.pub_positions):
            return None
        
        else:
            self.pub_positions = np.array(self.pub_positions)
            for i in range(0, self.pub_positions.shape[1]):
                self.pub_average.append(np.average(self.pub_positions[:, i]))
                
            return self.pub_average
        
    def calc_pub_std(self) -> List[float] | None: 
        if not all(isinstance(row, (list, np.ndarray)) for row in self.pub_positions):
            return None
        
        else:
            self.pub_positions = np.array(self.pub_positions, dtype=float)
            for i in range(0, self.pub_positions.shape[1]):
                self.pub_std.append(np.std(self.pub_positions[:, i]))
                
            return self.pub_std
    
    def make_avg_graph(self):
        plt.title(f"Average position in time for {self.n_sidewalks} drunkards")
        plt.xlabel(f"Time (Steps)")
        plt.ylabel(f"Average Position")
        plt.plot(self.calc_pub_avg())
        
        plt.savefig(f"""AvgPos_{time()}_nsw={self.n_sidewalks}_sws={self.sidewalk_size}_p={self.coin_p}.png""")
        
        plt.close()
        
    def make_std_graph(self):
        plt.title(f"Dispersion for {self.n_sidewalks} drunkards")
        plt.xlabel(f"Time (Steps)")
        plt.ylabel(f"Dispersion / Standard Deviation")
        plt.plot(self.calc_pub_std())
        
        plt.savefig(f"""Disp_{time()}_nsw={self.n_sidewalks}_sws={self.sidewalk_size}_p={self.coin_p}.png""")
        
        plt.close()    
    