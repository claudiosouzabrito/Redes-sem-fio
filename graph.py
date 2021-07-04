import numpy as np
import matplotlib
from matplotlib.patches import Circle, Wedge, Polygon, Ellipse
from matplotlib.collections import PatchCollection
import matplotlib.pyplot as plt
import matplotlib.patches as matpatches


def graph(x, y, ranges, nomes, numHost, dimension):
    fig, ax = plt.subplots(figsize=(8, 8))
    patches = []

    for i in range(numHost):
        circle = Circle((x[i], y[i]), ranges[i])
        patches.append(circle)

    for i, txt in enumerate(nomes):
        plt.annotate('o', (x[i], y[i]), ha='center', va='center')
    for i, txt in enumerate(nomes):
        plt.annotate(txt, (x[i], y[i]+3), ha='center', va='center')

    colors = 2 * np.random.rand(len(patches))
    p = PatchCollection(patches, cmap=matplotlib.cm.jet, alpha=0.5)

    p.set_array(np.array(colors))
    ax.add_collection(p)

    plt.axis([0, dimension, 0, dimension])
    plt.axis('square')
    plt.savefig('resultados/hospedeiros no plano.png')
    # plt.show()
