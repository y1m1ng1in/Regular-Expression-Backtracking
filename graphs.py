import matplotlib
import matplotlib.pyplot as plt
import numpy as np


class Plotting:

  def __init__(self, title, step, exp_num):
    self.title = title
    self.step = step
    self.exp_num = exp_num
    self.axis = np.arange(0, self.exp_num, 1)
    self.data = np.array(self.step)

  def plot(self):
    fig, ax = plt.subplots()
    plt.xticks(np.arange(1, self.exp_num, 20.0))
    ax.plot(self.axis, self.data)

    ax.set(xlabel='number of xs after =', ylabel='step',
           title=self.title)
    ax.grid()

    fig.savefig(self.title + ".png")
    plt.show()
