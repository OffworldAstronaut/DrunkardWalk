from random import random
import numpy as np
from matplotlib import pyplot as plt
from typing import List
from time import time


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
    
class Sidewalk:
    def __init__(self, size: int, coin_p : float=0.50):
        self.drunkard = Drunkard(coin_p)
        self.size = size
        self.wandering_pos = []
    
    def get_size(self) -> int:
        return self.size
    
    def wander(self, end_step: int=1_000) -> List[int]:
        for _ in range (0, end_step):
            self.wandering_pos.append(self.drunkard.walk())
            
        return self.wandering_pos

    def make_dispersion_plot(self) -> None:
        ...
        
    def make_average_pos_plot(self) -> None:
        ...

    def make_wandering_plot(self) -> None:
        plt.title(f"Random Walk (p={self.drunkard.get_coin_p()}; size={self.get_size()})")
        plt.xlabel("Time (Step)")
        plt.ylabel("Position")
        
        plt.plot(self.wandering_pos)
        plt.savefig(f"""RandomWalk_{time()}
                    _p={self.drunkard.get_coin_p()}
                    _size={self.get_size()}.png""")