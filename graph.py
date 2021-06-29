import numpy as np
import matplotlib.pyplot as plt

def graph(x,y,ranges,nomes, numHost, dimension, round):
    colors = np.random.rand(numHost)

    area = 1000 * np.array(ranges) * ((100/dimension)**2)

    plt.scatter(x, y, 1000*((100/dimension)**2), c="#000000", alpha=1)
    plt.scatter(x, y, s=area, c=colors, alpha=0.5)

    plt.xlim([0,dimension])
    plt.ylim([0,dimension])
    for i, txt in enumerate(nomes):
        plt.annotate(txt, (x[i], y[i]), ha='center', va='center')
        
    plt.savefig('resultados/hospedeiros no planoT=' +str(round)+ '.png')