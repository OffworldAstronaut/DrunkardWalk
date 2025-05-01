from random import random
import numpy as np
from matplotlib import pyplot as plt


class Drunkard:
    def __init__(self, pos : int, coin_p : float) -> None:
        """Creates a new "drunkard" (walker) with some parameters

        Args:
            pos (int): his position in the number line
            coin_p (float): his probability of walking to the right
        """
        self.pos = pos 
        self.coin_p = coin_p
        
    def walk(self) -> None:
        """Flip a coin and moves the Drunkard
        """
        if random() <= self.coin_p:
            self.pos += 1 
            
        else: 
            self.pos -= 1
            
        self.get_pos()
        
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
    def __init__(self, size: int, coin_p : float=0.50, start_pos: int=0):
        self.drunkard = Drunkard(start_pos, coin_p)
        self.size = size
        self.wandering_pos = []
    
    def wander(self, end_step : int=1_000):
        for i in range (0, end_step):
            self.wandering_pos.append(self.drunkard.walk())
            
        return self.wandering_pos