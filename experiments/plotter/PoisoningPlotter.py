from .Plotter import Plotter
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from queue import Queue

class PoisoningPlotter(Plotter):

    def __init__(self, app, *argv):
        self.name = 'LabelPlotter'
        self.app = app
        self.argv = argv
        self.colormap = {'TMC-Shapley': 'blue', 'G-Shapley': 'orange', 'Leave-One-Out': 'olive', 'KNN-LOO': 'violet', 'KNN-Shapley': 'purple'}
        self.colors = Queue()
        self.colors.put('green')
        self.colors.put('deeppink')
        self.colors.put('skyblue')
        self.colors.put('navy')
        self.colors.put('darkturquoise')

    def getColor(self, name):
        if self.colormap.__contains__(name):
            return self.colormap[name]
        else:
            self.colormap[name] = self.colors.get()
            return self.colormap[name]

    def plot(self, save_path=None, forks=True):

        data_num = self.app.X.shape[0]
        forksets = self.app.forksets

        for (name, result) in self.argv:
            res_v = result
            if forks:
                # sum of shapleys of all forksets
                res_v = np.array([res_v[forksets[fork_id]].sum() for fork_id in forksets])
            res_i = np.argsort(-res_v)[::-1]
            cnt = 0
            f = []
            total = 0
            cnt = 0
            total = self.app.watermarked.sum()
             # plot a different plot when doing forksets
            if forks:
                for i in range(len(forksets)):
                    # count how many detected flips
                    cnt += self.app.watermarked[forksets[res_i[i]]].sum() 
                    f.append(1.0 * cnt / total)
            else:
                for i in range(data_num):
                    if self.app.watermarked[int(res_i[i])] == 1:
                        cnt += 1
                        f.append(1.0 * cnt / total)
            if forks:
                x = np.array(range(1, len(forksets) + 1)) / len(forksets) * 100
                plot_length = len(forksets) // 10
                x = np.append(x[0:-1:plot_length], x[-1])
                f = np.append(f[0:-1:plot_length], f[-1])
            else:
                x = np.array(range(1, data_num + 1)) / data_num * 100
                x = np.append(x[0:-1:100], x[-1])
                f = np.append(f[0:-1:100], f[-1])
            plt.plot(x, np.array(f) * 100, 'o-', color = self.getColor(name), label = name)


        if forks:
            ran_v = np.random.rand(len(forksets))
        else:
            ran_v = np.random.rand(data_num)

        ran_i = np.argsort(-ran_v)[::-1]
        cnt = 0
        f = []
        total = 0
        cnt = 0
        # for i in range(data_num):
        #     if self.app.watermarked[int(ran_i[i])] == 1:
        #         total += 1
        total = self.app.watermarked.sum()
        if len(forksets) == data_num:
            x = np.array(range(1, len(forksets) + 1)) / len(forksets) * 100
            f = x / 100
        else:
            for i in range(len(forksets)):
                # count how many detected flips
                cnt += self.app.watermarked[forksets[ran_i[i]]].sum()
                f.append(1.0 * cnt / total)
            x = np.array(range(1, len(forksets) + 1))
            plot_length = len(forksets) // 10
            x = np.append(x[0:-1:plot_length], x[-1])
            f = np.append(f[0:-1:plot_length], f[-1])
        plt.plot(x, np.array(f) * 100, '--', color='red', label = "Random", zorder=7)

        if forks:
            plt.xlabel('Forks inspected (%)', fontsize=15)
        else:
            plt.xlabel('Fraction of data inspected (%)', fontsize=15)        
        plt.ylabel('Fraction of backdoors detected (%)', fontsize=15)
        plt.legend(loc='lower right', prop={'size': 15})
        plt.tight_layout()
        if save_path is not None:
            plt.savefig(save_path + '.pdf')
        plt.show()
        plt.clf()
