import DrunkardWalk as DW 

quantity_sidewalks = 10_000
size_sidewalks = 1_000
coin_p = 0.5

city = DW.City(quantity_sidewalks, size_sidewalks, coin_p)

city.roam()

city.make_avg_graph()
city.make_std_graph(loglog=True)
city.make_endpos_graph(sturges=False, nbins=50)