import DrunkardWalkSD as DWSD

quantity_sidewalks = 10_000
size_sidewalks = 1_500
disorder_intensity = 1.00

city = DWSD.City(quantity_sidewalks, size_sidewalks, disorder_intensity)

city.roam()

#city.make_avg_graph(plot_only=True)
city.make_std_graph(tail=125, plot_only=True, loglog=True)
#city.make_endpos_graph()