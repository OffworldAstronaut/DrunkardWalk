import DrunkardWalk as DW
import numpy as np
import matplotlib.pyplot as plt

coin_disorders = np.linspace(0.1, 1, 200)
alpha_list = []

quantity_sidewalks = 10_000
size_sidewalks = 500

city = DW.City(quantity_sidewalks, size_sidewalks)

for w in coin_disorders:
    city.set_coin_W(w)
    city.roam()
    alpha = city.make_std_graph(tail=100, loglog=True, only_coef=True)
    alpha_list.append(alpha)
    city.reset_data()
    
log_coin = [np.log(x) for x in coin_disorders]    
log_alpha = [np.log(x) for x in alpha_list]

ang_coef, ind_term = np.polyfit(log_coin, log_alpha, 1)

fit_line = np.exp(ang_coef) * coin_disorders ** ang_coef

plt.title(f"W vs Alpha")
plt.xlabel("W")
plt.ylabel("Ang. Coef.")

plt.loglog(coin_disorders, fit_line, label=f"Coef. angular: {ang_coef:.5f}")
plt.loglog(coin_disorders, alpha_list)

plt.legend(loc='upper right')

plt.savefig("comparison_alpha_w.png")