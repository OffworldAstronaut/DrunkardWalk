import DrunkardWalk as DW

# Dummy variables -- we only need the size of the sidewalks and the coins 
quantity_sidewalks = 10_000
size_sidewalks = 1_500
disorder_intensity = 0.00

city = DW.City(quantity_sidewalks, size_sidewalks, disorder_intensity)

# generate the coins 
coins = city.generate_coins()

# create a sidewalk with the generated coins

sidewalk = DW.Sidewalk(size_sidewalks, coins)

sidewalk.wander(end_step=20_000)

sidewalk.plot_avgpos()
sidewalk.plot_stdpos(1000, loglog=True)
sidewalk.plot_endpos()