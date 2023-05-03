from matplotlib import pyplot as plt

def draw_scores(slw, fst, avg):

    indexes = []
    scores = []
    for i in range(len(slw)):
        scores.append((slw[i], fst[i], avg[i]))
        indexes.append(i)

    plt.plot(indexes, scores, label=['avg speed','fastest','slowest'])
    plt.legend(loc="upper left")
    plt.xticks([])
    plt.show()

if __name__ == "__main__":
    slw = [1.1, 1.2, 1.3]
    fst = [0.3, 0.4, 0.2]
    avg = [0.7, 0.8, 0.7]
    draw_scores(slw, fst, avg)