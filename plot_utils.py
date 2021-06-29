import matplotlib.pyplot as plt
from bazooka import Bazooka


def drawPlots(objects, title, label):
    fig, ax = plt.subplots()

    for bazooka in objects:
        x, y, _, _ = bazooka.getSolution()
        ax.plot(x, y, label=label(bazooka.alpha))

    ax.set_title(title, fontsize=18)
    ax.set_aspect("equal")
    ax.grid(b=True)
    ax.legend()
    ax.set_xlabel("$x$ (m)")
    ax.set_ylabel("$y$ (m)")
    plt.show()


def drawComparisonPlots(objects, plotTitle, subplotTitle, label1, label2):
    rowCount = int(
        len(objects) // 2) if len(objects) % 2 == 0 else int(len(objects) // 2 + 1)

    fig, axes = plt.subplots(nrows=rowCount, ncols=2)

    for i, ax in enumerate(axes.flat):
        x1, y1, _, _ = objects[i][0].getSolution()
        x2, y2, _, _ = objects[i][1].getSolution()
        ax.plot(x1, y1, label=label1)
        ax.plot(x2, y2, label=label2)
        ax.grid(b=True)
        ax.set_title(subplotTitle(objects[i][0].alpha))
        ax.legend()
        ax.set_xlabel("$x$ (m)")
        ax.set_ylabel("$y$ (m)")

    fig.suptitle(plotTitle, fontsize=24)
    plt.show()
