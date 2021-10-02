from os import listdir
from os.path import isfile, join
from sudoku import getDifficulty, getboard, sudokuByBacktrackingWithMRVAndInference, initDomains, getTotalCost

def trainThreshold():
    l2 = []
    l3 = []
    l4 = []
    thresh = []
    relDir = "./data"
    allFiles = [f for f in listdir(relDir) if isfile(join(relDir, f))]
    for fileName in allFiles:
        f = open(join(relDir, fileName), "r")
        txt = f.read()
        board = getboard(txt)
        domains = initDomains(board)
        [isSolvable, g, inferenceCtr] = sudokuByBacktrackingWithMRVAndInference(board, 0, domains, True, 0)
        if isSolvable:
            if fileName.find("-l2")!=-1:
                l2.append(getTotalCost(g, inferenceCtr))
            elif fileName.find("-l3")!=-1:
                l3.append(getTotalCost(g, inferenceCtr))
            elif fileName.find("-l4")!=-1:
                l4.append(getTotalCost(g, inferenceCtr))
    thresh.append(min(l2))
    thresh.append(min(l3))
    thresh.append(min(l4))
    with open('thresholds.txt', 'w') as f:
        f.write('\n'.join(str(e) for e in thresh))

if __name__=="__main__":
    trainThreshold()
    print("Training complete")