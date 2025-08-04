/**
 * @file main.cpp
 * @author Rafael Amorim (rafael.science.amorim@gmail.com)
 * @brief Simulation and statistical analysis of Random Walk in Random Environments (RWRE)
 * @version 0.1
 * @date 2025-08-02
 * 
 * @copyright Copyright (c) 2025
 */

#include <iostream>     // basic I/O 
#include <fstream>      // files I/O 
#include <string>       // string manipulation
#include <format>       // easy string formatting 
#include <vector>       // vectors 
#include <cmath>        // numerical necessities 
#include <random>       // probabilistic necessities 
#include <ctime>        // time functions 

using namespace std;

/**
 * @brief Represents a random walker
 */
class Drunkard
{
    private:
        int position;   // position of the walker in the number line
        mt19937 rd; 
        uniform_real_distribution<> distCoin; 
    public:
        /**
         * @brief Construct a new Drunkard object
         *
         * @param sidewalkSize size of the associated sidewalk; the walker starts in the middle
         */
        Drunkard(int sidewalkSize) :    position(sidewalkSize / 2.0),
                                        rd(random_device{}()),
                                        distCoin(0.0, 1.0) {}; 


        /**
         * @brief Moves the drunkard one step according to it's coin toss
         * 
         * @param site_coin coin associated with the current walker's position in the sidewalk
         * @return int walker's current position
         */
        int walk(double site_coin)
        {
            if (distCoin(rd) <= site_coin) { this->position += 1; }
            else { this -> position -= 1; };

            getPos();
        };

        int getPos()
        {
            return this->position; 
        }
};

/**
 * @brief Environment of a single walker -- can be interpreted as the original number line
 * 
 */
class Sidewalk
{
    private:
        Drunkard drunkard;                      // drunkard associated with the sidewalk
        mt19937 rd;                             // random number generator 
        uniform_real_distribution<> distCoins;  // uniform real distribution for the coins
        vector<double> vectorCoins;             // vector to store the sidewalk's coins
        int maxStep;                            // max number of steps of the random walk
    public:
        /**
         * @brief Creates a new Sidewalk
         * 
         * @param size size of the sidewalk 
         * @param W the coins' disorder intensity, originates from the City
         */
        Sidewalk(int size, double W) :  // seeds the RNG
                                        rd(random_device{}()),
                                        // initializes the prob distribution
                                        distCoins(-1.0 * W / 2.0, W / 2.0), 
                                        // initializes the Drunkard   
                                        drunkard(Drunkard(size)),
                                        // stores the max step for wandering              
                                        maxStep(size / 2.0)                    
                                        {

                                            // populates the coins vector
                                            for (size_t i = 0; i < size; i++)
                                            {
                                                vectorCoins.push_back(distCoins(rd));
                                            }
                                        }; 

    /**
     * @brief Simulates a random walk over a certain number of steps
     * 
     * @return vector<int> vector with all the positions over time
     */
    vector<int> wander()
    {
        // vector to store all walker's position over time
        vector<int> positions; 

        // executes the drunkard's wandering
        for (size_t step = 1; step <= maxStep; step++)
        {
            // gets the coin associated with the current walker's position 
            double currentCoin = vectorCoins[drunkard.getPos()];
            // walk the drunkard one step and stores the position
            positions.push_back(drunkard.walk(currentCoin));
        }

        // returns the vector with the random walk
        return positions;
    }
};

class City 
{ 
    public:
};

int main()
{
    printf("Hello world");
    return 0; 
}