from time import time                       # For file R&W operations
import numpy as np                          # General numerical necessities
from matplotlib import pyplot as plt        # For plotting
from typing import List                     # Typing hints
from scipy.stats import norm

class Drunkard:
    def __init__(self, coin_p: float) -> None:
        """Creates a new drunkard (walker) with a given probability of stepping right.

        Args:
            coin_p (float): Probability of walking one step to the right.
        """
        # Position of the walker
        self.pos = 0
        # Probability of walking one step to the right
        self.coin_p = coin_p

    def walk(self) -> int:
        """Flips a coin and moves the drunkard one step."""
    
        if np.random.uniform() <= self.coin_p:
            self.set_pos(self.pos + 1)
            
        else: 
            self.set_pos(self.pos - 1)
            
        return self.get_pos()

    # Getters and Setters

    # Position 
    def set_pos(self, new_pos: int) -> None:
        self.pos = new_pos

    def get_pos(self) -> int:
        return self.pos

    # Coin
    def set_coin_p(self, new_coin_p: float) -> None:
        self.coin_p = new_coin_p

    def get_coin_p(self) -> float:
        return self.coin_p


class Sidewalk:
    """Environment of a single drunkard -- can be interpreted as the original number line."""

    def __init__(self, size: int, coin_p: float = 0.50) -> None:
        """Creates a sidewalk (number line) for the drunkard to walk on.

        Args:
            size (int): Length of the sidewalk.
            coin_p (float, optional): Coin probability of stepping right. Defaults to 0.50 (fair coin).
        """
        # Each sidewalk automatically has a drunkard attached to it
        self.drunkard = Drunkard(coin_p)
        self.size = size
        # Stores each position of the drunkard over time
        self.wandering_pos = []

    def wander(self, end_step: int = 1_000) -> List[int]:
        """Simulate the drunkard's walk over a number of steps."""
        
        # Walks the drunkard for as many steps as specified in the method call
        for _ in range(end_step):
            # Each step is recorded in the "wandering_pos" attribute
            self.wandering_pos.append(self.drunkard.walk())
            
        # The positions traveled by the walker are returned for statistical analysis
        return self.wandering_pos

    def make_wandering_plot(self) -> None:
        """Plots the path of the walker over time (position in function of step)."""
        
        # Plot title -- automatically varies with the coin chosen and the size of the sidewalk
        plt.title(f"Random Walk (p={self.drunkard.get_coin_p()}; size={self.get_size()})")
        plt.xlabel("Time (Step)")
        plt.ylabel("Position")

        plt.plot(self.wandering_pos)

        # Saves the figure with custom filename -- varies with timestamp, coin and sidewalk size
        plt.savefig(
            f"RandomWalk_{time()}_"
            f"p={self.drunkard.get_coin_p()}_"
            f"size={self.get_size()}.png"
        )
        # Closes the plot at hand to prevent memory inefficiency and inaccurate plotting
        plt.close()
        
    # Auxiliar method -- gets the sidewalk's size
    def get_size(self) -> int:
        return self.size


class City:
    """Environment for multiple sidewalks -- runs many simulations for statistical analysis."""

    def __init__(self, n_sidewalks: int, sidewalk_size: int, coin_p: float) -> None:
        # Number of sidewalks in the city
        self.n_sidewalks = n_sidewalks
        # Size of the city's sidewalks 
        self.sidewalk_size = sidewalk_size
        # Coin probability of the sidewalks' walkers
        self.coin_p = coin_p

        # DISCLAIMER: a set of sidewalks is called a "pub" (yes, like the ones in Britain); 
        # The following lists are "lists of lists": they contain data from each sidewalk simulated in
        # the city, or derived from them; 
        
        # Stores the lists of positions from each sidewalk simulated
        self.pub_positions = []
        # Stores the end positions from each sidewalk simulated
        self.pub_end_positions = []
        # Stores the average of every walker's position in a given time (ie. record every walker's position 
        # at step 1, 2, ... and average them, then store in this list)
        self.pub_average = []
        # Stores the dispersion (STD) of every walker in a given time -- same logic as above
        self.pub_std = []

    def roam(self, end_step: int = 500) -> List[List[int]]:
        """Executes each sidewalk simulation in succession and stores the positions for 
        statistical analysis. 

        Args:
            end_step (int, optional): The maximum number of steps that the walkers
            are going to traverse. Defaults to 500.

        Returns:
            List[List[int]]: List containing lists of the positions of each walker over time.
        """
        
        # Executes the random walk for each sidewalk specified in the City's initialization
        for _ in range(self.n_sidewalks):
            # Creates a new sidewalk with a given size and coin probability
            sidewalk = Sidewalk(self.sidewalk_size, self.coin_p)
            # Executes the random walk for as many steps as needed
            positions = sidewalk.wander(end_step)
            # Slices the last position and stores it
            self.pub_end_positions.append(positions[-1])
            # Stores the generated array
            self.pub_positions.append(positions)
            
        # Returns the list of lists
        return self.pub_positions

    def calc_pub_avg(self) -> List[float] | None:
        """Calculates and returns the average position over time across all sidewalks.

        Returns:
            List[float] | None: List of average positions over time
        """
        
        # Prevents user shenanigans: trying to calc average of nothing
        if not all(isinstance(row, (list, np.ndarray)) for row in self.pub_positions):
            return None

        # Transforms the pub_positions array into a numpy one (a matrix if you will) 
        # for ease of manipulation
        self.pub_positions = np.array(self.pub_positions, dtype=float)
        # Empties the pub_average array to prevent computational error if the method
        # has been run previously
        self.pub_average = []

        # Traverses each column to calculate its average -- each column of the matrix
        # is a given step: the ith column is the ith step.
        for step in range(self.pub_positions.shape[1]):
            # Selects the desired column from the matrix
            column = self.pub_positions[:, step]
            # Calculates its average and stores in the array
            self.pub_average.append(np.average(column))

        # Returns the list of averages
        return self.pub_average

    def calc_pub_std(self) -> List[float] | None:
        """Calculates and returns the dispersion (STD) over time across all sidewalks.

        Returns:
            List[float] | None: List of dispersions over time
        """
        
        # Prevents user shenanigans: trying to calc STD of nothing
        if not all(isinstance(row, (list, np.ndarray)) for row in self.pub_positions):
            return None

        # Transforms the pub_positions array into a numpy one (a matrix if you will) 
        # for ease of manipulation
        self.pub_positions = np.array(self.pub_positions, dtype=float)
        # Empties the pub_std array to prevent computational error if the method
        # has been run previously
        self.pub_std = []

        # Traverses each column to calculate its dispersion -- each column of the matrix
        # is a given step: the ith column is the ith step.
        for step in range(self.pub_positions.shape[1]):
            self.pub_std.append(np.std(self.pub_positions[:, step]))

        # Returns the list of dispersions
        return self.pub_std

    def make_avg_graph(self) -> None:
        """Plots the averages over time of the random walks. 
        """
        # Title -- Changes automatically with the number of sidewalks
        plt.title(f"Average Position in Time for {self.n_sidewalks} Drunkards")
        plt.xlabel("Time (Steps)")
        plt.ylabel("Average Position")
        
        # Calculates and stores the average over time 
        pubavg = self.calc_pub_avg()
        
        # Writes the data to a file for posterior storage 
        with open(f"AvgPos_{time()}"
                  f"_nsw={self.n_sidewalks}"
                  f"_sws={self.sidewalk_size}"
                  f"_p={self.coin_p}.dat""", "w") as f:
            
            for i, val in enumerate(pubavg, start=1):
                f.write(f"{i} {val:.4f}\n")
        
        # Plots the data in a matplotlib plot
        plt.plot(pubavg)
        
        # Saves the plot -- filename automatically configured for timestamp, coin, number of
        # sidewalks and their size
        plt.savefig(
            f"""AvgPos_{time()}_
            nsw={self.n_sidewalks}_
            sws={self.sidewalk_size}_
            p={self.coin_p}.png"""
        )
        plt.close()

    def make_std_graph(self) -> None:
        """Plots the dispersion over time of the random walks."""
        
        # Calculates and stores the dispersion over time 
        pubstd = self.calc_pub_std()

        # Writes the data to a file for posterior storage 
        with open(
            f"Disp_{time()}_"
            f"nsw={self.n_sidewalks}_"
            f"sws={self.sidewalk_size}_"
            f"p={self.coin_p}.dat", "w") as f:
            
            for i, val in enumerate(pubstd, start=1):
                f.write(f"{i} {val:.4f}\n")

        # Prepare data for plotting
        xpoints = np.arange(len(pubstd))
        sqrt_t = np.sqrt(xpoints)

        fig, ax = plt.subplots()
        
        # Title and labels
        ax.set_title(f"Dispersion for {self.n_sidewalks} Drunkards")
        ax.set_xlabel("Time (Steps)")
        ax.set_ylabel("Dispersion")

        # Plots
        ax.plot(pubstd, label="Dispersion")
        ax.plot(sqrt_t, label=r"$\sqrt{t}$", linestyle='--')

        # Add legend
        ax.legend(loc='upper right')

        # Saves the plot
        plt.savefig(
            f"Disp_{time()}_"
            f"nsw={self.n_sidewalks}_"
            f"sws={self.sidewalk_size}_"
            f"p={self.coin_p}.png"
        )

        plt.close()
        
    def make_endpos_graph(self, sturges: bool=True, nbins: int=50) -> None:
        """Plots the end positions of every random walk simulated.

        Args:
            sturges (bool): If True, uses Sturges' Law for the histogram bin count. Defaults to True
            nbins (int, optional): Number of bins to use if not using Sturges' Law. Defaults to 50.
        """

        # Fits a gaussian curve to the positions
        mu, sigma = norm.fit(self.pub_end_positions)

        # Title changes automatically with the number of sidewalks
        plt.title(f"Final positions for {self.n_sidewalks} Drunkards")
        plt.suptitle(f"Mu: {mu:.4f}, Sigma: {sigma:.4f}")
        plt.xlabel("Final position")
        plt.ylabel("Frequency")
        
        if sturges:
            # Using Sturges' rule: bins = 1 + log2(n)
            nbins = int(np.ceil(1 + np.log2(len(self.pub_end_positions))))

        # Plots the histogram
        count, bins, _ = plt.hist(self.pub_end_positions, bins=nbins, density=True, alpha=0.6, color='b')

        # Plots the gaussian fit
        x = np.linspace(min(bins), max(bins), 1000)
        y = norm.pdf(x, mu, sigma)
        plt.plot(x, y, 'r--', linewidth=2)

        # Save plot
        plt.savefig(
            f"Endpos_{time():.0f}_"
            f"nsw={self.n_sidewalks}_"
            f"sws={self.sidewalk_size}_"
            f"sigma={sigma}"
            f"p={self.coin_p}.png"
        )

        plt.close()
        
