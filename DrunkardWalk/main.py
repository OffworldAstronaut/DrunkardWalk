from time import time                       # For file R&W operations
import numpy as np                          # General numerical necessities
from matplotlib import pyplot as plt        # For plotting
from matplotlib.ticker import FormatStrFormatter  # For formatting axes in plots
from typing import List                     # Typing hints
from scipy.stats import norm                # Normalization library

class Drunkard: 
    def __init__(self, sidewalk_size: int) -> None:
        """Creates a new drunkard (walker) with a given probability of stepping right.

        Args:
            sidewalk_size (int): Size of the sidewalk that the walker is placed.
        """
        # Position of the walker -- the walker starts at the middle of the sidewalk
        self.pos = int(sidewalk_size / 2.0)

    def walk(self) -> int:
        """Flips a coin and moves the drunkard one step."""
    
        if np.random.uniform() <= self.coin_p:
            self.set_pos(self.pos + 1)
            
        else: 
            self.set_pos(self.pos - 1)
            
        return self.get_pos()
    
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

    def __init__(self, size: int, coins: List) -> None:
        """Creates a sidewalk (number line) for the drunkard to walk on.

        Args:
            size (int): Length of the sidewalk.
            coin_p (float, optional): Coin probability of stepping right. Defaults to 0.50 (fair coin).
        """
        # Each sidewalk automatically has a drunkard attached to it
        self.drunkard = Drunkard(size)
        # Stores the sidewalk's size 
        self.size = size
        # Stores each position of the drunkard over time
        self.wandering_pos = []
        # Stores the arrays of coins for each slot of the sidewalk
        self.coins = coins
        # Stores the average position of the drunkard over time
        self.avg_pos = []
        # Stores the dispersion (STD) of the drunkard's position over time
        self.std_pos = []

    def wander(self, end_step: int = 1_000) -> List[int]:
        """Simulate the drunkard's walk over a number of steps."""
        
        # Walks the drunkard for as many steps as specified in the method call
        for _ in range(end_step):
            # Selects the coin assigned to the current position occupied by the walker
            new_coin = self.coins[self.drunkard.get_pos()]
            # Updates the walker's coin 
            self.drunkard.set_coin_p(new_coin)
            # Each step is recorded in the "wandering_pos" attribute
            self.wandering_pos.append(self.drunkard.walk())
            # Calculates the average and standard deviation of the drunkard's position
            # and appends them to their respective lists
            self.avg_pos.append(self.calc_avg())
            self.std_pos.append(self.calc_std())
            
        # The positions traveled by the walker are returned for statistical analysis
        return self.wandering_pos
    
    def calc_avg(self) -> float:
        """Calculates the average position of the drunkard over time.

        Returns:
            float: Average position of the drunkard.
        """
        
        # Prevents user shenanigans: trying to calc average of nothing
        if not self.wandering_pos:
            return 0.0
        
        # Calculates and returns the average position
        return np.mean(self.wandering_pos)
    
    # TODO: method to calculate the dispersion (STD) over time
    def calc_std(self) -> float:
        """Calculates the dispersion (STD) of the drunkard's position over time.

        Returns:
            float: Dispersion (STD) of the drunkard's position.
        """
        
        # Prevents user shenanigans: trying to calc STD of nothing
        if not self.wandering_pos:
            return 0.0
        
        # Calculates and returns the dispersion
        return np.std(self.wandering_pos)
    
    # TODO: method to plot the average position over time
    def plot_avgpos(self) -> None:
        """Plots the average position of the drunkard over time."""
    
        # Title -- Changes automatically with the sidewalk's size
        plt.title(f"Average Position in Time for Drunkard on Sidewalk of Size {self.size}")
        plt.xlabel("Time (Steps)")
        plt.ylabel("Average Position")
        
        # Plots the average position over time
        self.avg_pos = [x - int(self.size / 2) for x in self.avg_pos]
        plt.plot(self.avg_pos)
        
        # Saves the plot -- filename automatically configured for timestamp and sidewalk size
        plt.savefig(
            f"AvgPos_{time()}_sws={self.size}.png"
        )
        plt.close()
        
    # TODO: method to plot the dispersion (STD) over time
    def plot_stdpos(self, tail: int, loglog: bool=False) -> None:
        """Plots the dispersion (STD) of the drunkard's position over time.

        Args:
            tail (int): Number of last steps to consider for the plot.
            loglog (bool, optional): If True, plots in log-log scale. Defaults to False.
        """
        
        # Prepares data for plotting
        xpoints = np.arange(len(self.std_pos))[-tail:]
        pubstd = self.std_pos[-tail:]
        sqrt_t = np.sqrt(xpoints)
        
        coef_ang, _ = np.polyfit(np.log(xpoints), np.log(pubstd), 1)
        
        # Title and labels
        plt.title(f"Dispersion for Drunkard on Sidewalk of Size {self.size}")
        plt.xlabel("Time (Steps)")
        plt.ylabel("Dispersion")
        
        # Plots
        if loglog:
            plt.loglog(xpoints, pubstd, label=f"Dispersion, Alpha={coef_ang:.4f}")
            plt.loglog(xpoints, sqrt_t, label=r"$\sqrt{t}$", linestyle='--')
        else:
            plt.plot(xpoints, pubstd, label=f"Dispersion, Alpha={coef_ang:.4f}")
            plt.plot(xpoints, sqrt_t, label=r"$\sqrt{t}$", linestyle='--')
        
        plt.legend(loc='upper right')
        
        # Saves the plot
        plt.savefig(
            f"Disp_{time()}_sws={self.size}.png"
        )
        
        plt.close()
    
    # TODO: method to plot the histogram of all the positions of the drunkard
    def plot_endpos(self, sturges: bool=True, nbins: int=50) -> None:
        """Plots the end positions of the drunkard's walk.

        Args:
            sturges (bool): If True, uses Sturges' Law for the histogram bin count. Defaults to True
            nbins (int, optional): Number of bins to use if not using Sturges' Law. Defaults to 50.
        """
        
        # Changes the referential for the plot
        self.wandering_pos = [x - int(self.size / 2) for x in self.wandering_pos]
        
        # Fits a gaussian curve to the positions
        mu, sigma = norm.fit(self.wandering_pos)

        # Title changes automatically with the sidewalk's size
        plt.title(f"Final positions for Drunkard on Sidewalk of Size {self.size}")
        plt.suptitle(f"Mu: {mu:.4f}, Sigma: {sigma:.4f}")
        plt.xlabel("Final position")
        plt.ylabel("Frequency")
        
        if sturges:
            # Using Sturges' rule: bins = 1 + log2(n)
            nbins = int(np.ceil(1 + np.log2(len(self.wandering_pos))))

        # Plots the histogram
        count, bins, _ = plt.hist(self.wandering_pos, bins=nbins, density=True, alpha=0.6, color='b')

        # Plots the gaussian fit
        x = np.linspace(min(bins), max(bins), 1000)
        y = norm.pdf(x, mu, sigma)
        plt.plot(x, y, 'r--', linewidth=2)

        # Save plot
        plt.savefig(
            f"Endpos_{time():.0f}_sws={self.size}_sigma={sigma}.png"
        )

        plt.close()
        
    # Auxiliar method -- returns the sidewalk's size
    def get_size(self) -> int:
        return self.size
    
class City:
    """Environment for multiple sidewalks -- runs many simulations for statistical analysis."""

    def __init__(self, n_sidewalks: int, sidewalk_size: int, coin_W: float=0.5) -> None:
        # Number of sidewalks in the city
        self.n_sidewalks = n_sidewalks
        # Size of the city's sidewalks 
        self.sidewalk_size = sidewalk_size
        # Amplitude of possible coins prob. value -- the higher the amplitude the wider 
        # the interval between the lowest and highest possible walk-right-probability values.
        self.coin_W = coin_W    # ranges from 0 to 1

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

    def reset_data(self):
        self.pub_positions = []
        self.pub_end_positions = []
        self.pub_average = []
        self.pub_std = []
        
    def set_coin_W(self, new_coin_W: float) -> None:
        self.coin_W = new_coin_W
    
    def generate_coins(self) -> List[float]:
        # Lower bound of the possible coin values
        low_b = ((-1.0 * self.coin_W) / 2.0) + 0.5
        # Upper bound of the possible coin values
        high_b = (self.coin_W / 2.0) + 0.5    
        # List of coins assigned to each sidewalk position -- Populated by a uniform prob. dist. via Numpy
        coins = np.random.uniform(low_b, high_b, self.sidewalk_size).tolist()
            
        # Returns the generated coins
        return coins
        
    def roam(self) -> List[List[int]]:
        """Executes each sidewalk simulation in succession and stores the positions for 
        statistical analysis. 
        
        Returns:
            List[List[int]]: List containing lists of the positions of each walker over time.
        """
        
        # Defines the maximum steps in function of the size of the sidewalks
        end_step = int(self.sidewalk_size / 2.0) + 1
        
        # Executes the random walk for each sidewalk specified in the City's initialization
        for _ in range(self.n_sidewalks):
            # Creates a new sidewalk with a given size and generates the necessary coins
            sidewalk = Sidewalk(self.sidewalk_size, self.generate_coins())
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
            
        # Changes the referential for the average calculation -- useful for the plotting
        self.pub_average = [x - int(self.sidewalk_size / 2) for x in self.pub_average]
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

    def make_avg_graph(self, plot_only: bool=True) -> None:
        """Plots the averages over time of the random walks. 
        """
        # Title -- Changes automatically with the number of sidewalks
        plt.title(f"Average Position in Time for {self.n_sidewalks} Drunkards, W={self.coin_W}")
        plt.xlabel("Time (Steps)")
        plt.ylabel("Average Position")
        
        # Calculates and stores the average over time 
        pubavg = self.calc_pub_avg()
        
        # Writes the data to a file for posterior storage 
        if not plot_only:
            with open(
                    f"AvgPos_{time()}"
                    f"_nsw={self.n_sidewalks}"
                    f"_sws={self.sidewalk_size}"
                    f"_w={self.coin_W}.dat""", "w") as f:
                
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
            w={self.coin_W}.png"""
        )
        plt.close()

    def make_std_graph(self, tail: int, plot_only: bool=True, loglog: bool=False, only_coef: bool=False) -> float:
        """Plots the dispersion over time of random walks

        Args:
            plot_only (bool, optional): If this option is true, no .dat will be written. Defaults to True.
            loglog (bool, optional): Option to plot linear or log-log. Defaults to False (linear).

        Returns:
            float: angular coefficient of the polyfit line
        """
        
        # Calculates and stores the dispersion over time 
        pubstd = self.calc_pub_std()
        xpoints = np.arange(len(pubstd))

        if not plot_only:
            # Writes the data to a file for posterior storage 
            with open(
                f"Disp_{time()}_"
                f"nsw={self.n_sidewalks}_"
                f"sws={self.sidewalk_size}_"
                f"w={self.coin_W}.dat", "w") as f:
                
                for i, val in enumerate(pubstd, start=1):
                    f.write(f"{i} {val:.4f}\n")

        # Prepare data for plotting
        pubstd = pubstd[-tail:]
        xpoints = xpoints[-tail:]
        
        #sqrt_t = np.sqrt(xpoints)
        coef_ang, independent_term = np.polyfit(np.log(xpoints), np.log(pubstd), 1)
        
        reference = np.exp(independent_term) * np.power(xpoints, coef_ang)
        
        if only_coef:
            ...

        else:    
            fig, ax = plt.subplots()
            
            # Title and labels
            ax.set_title(f"Dispersion for {self.n_sidewalks} Drunkards, W={self.coin_W}")
            ax.set_xlabel("Time (Steps)")
            ax.set_ylabel("Dispersion")

            # Plots
            if loglog:
                ax.loglog(xpoints, pubstd, label=f"Dispersion, Alpha={coef_ang:.4f}")
                ax.loglog(xpoints, reference, label=f"t ~ {coef_ang:.4f}", linestyle='--')
            else:
                ax.plot(xpoints, pubstd, label=f"Dispersion, Alpha={coef_ang:.4f}")
                ax.plot(xpoints, reference, label=f"t ~ {coef_ang:.4f}", linestyle='--')

            # Add legend
            ax.yaxis.set_minor_formatter(FormatStrFormatter('%.2f'))
            ax.xaxis.set_minor_formatter(FormatStrFormatter('%.2f'))
            ax.tick_params(axis='both', which='minor', labelsize=10)
            ax.legend(loc='upper right')

            # Saves the plot
            plt.savefig(
                f"Disp_{time()}_"
                f"nsw={self.n_sidewalks}_"
                f"sws={self.sidewalk_size}_"
                f"w={self.coin_W}.png"
            )

            plt.close()
        
        return coef_ang
        
    def make_endpos_graph(self, sturges: bool=True, nbins: int=50) -> None:
        """Plots the end positions of every random walk simulated.

        Args:
            sturges (bool): If True, uses Sturges' Law for the histogram bin count. Defaults to True
            nbins (int, optional): Number of bins to use if not using Sturges' Law. Defaults to 50.
        """

        # Changes the referential for the plot
        self.pub_end_positions = [x - int(self.sidewalk_size / 2) for x in self.pub_end_positions]

        # Fits a gaussian curve to the positions
        mu, sigma = norm.fit(self.pub_end_positions)

        # Title changes automatically with the number of sidewalks
        plt.title(f"Final positions for {self.n_sidewalks} Drunkards")
        plt.suptitle(f"Mu: {mu:.4f}, Sigma: {sigma:.4f}, W: {self.coin_W}")
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
            f"w={self.coin_W}.png"
        )

        plt.close()