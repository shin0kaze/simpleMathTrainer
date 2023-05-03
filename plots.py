from matplotlib import pyplot as plt

def draw_scores(data):
    
    idx, *data = map(list, zip(*data))
    scores = []
    for i in range(len(idx)):
        scores.append((data[0][i], data[1][i], data[2][i]))
    #print(idx)
    #print(scores)
    plt.plot(idx, scores, label=['avg speed','fastest','slowest'])
    plt.legend(loc="upper left")
    plt.xticks([])
    plt.show()

if __name__ == "__main__":
    idx = [0, 1, 2]
    slw = [1.1, 1.2, 1.3]
    fst = [0.3, 0.4, 0.2]
    avg = [0.7, 0.8, 0.7]
    all = [(0, 1.1, 0.3, 0.7), (1, 1.2, 0.4, 0.8)]
    draw_scores(all)