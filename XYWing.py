import math

def xyWing(domains, row, col, inferenceCtr):
    if sum(domains[row][col]) != 2:
        return inferenceCtr
    rows = len(domains)
    rn = int(math.sqrt(rows))
    x=[]    # pivot cell
    # get the 2 candidates for this cell
    for i in range(9):
        if domains[row][col][i]:
            x.append(i)
    zx = None
    zxrow = None
    zxcol = None
    # checking for a bivalued cell with one different element in same row
    for c in range(rows):
        if c!=col and sum(domains[row][c]) == 2:
            pincer = [] 
            for i in range(9):
                if domains[row][c][i]:
                    pincer.append(i)
            if pincer[0] == x[0] and pincer[1]!=x[1]:
                zx=pincer[1]
                zxrow = row
                zxcol = c
            elif pincer[1] == x[0] and pincer[0]!=x[1]:
                zx=pincer[0]
                zxrow = row
                zxcol = c
    if zx is None: # cell was not found in the same row
        # checking for a bivalued cell with one different element in same column
        for r in range(rows):
            if r!=row and sum(domains[r][col]) == 2:
                pincer = []
                for i in range(9):
                    if domains[r][col][i]:
                        pincer.append(i)
                if pincer[0] == x[0] and pincer[1]!=x[1]:
                    zx=pincer[1]
                    zxrow = r
                    zxcol = col
                elif pincer[1] == x[0] and pincer[0]!=x[1]:
                    zx=pincer[0]
                    zxrow = r
                    zxcol = col

    if zx is None: # cell was not found in the same row or column
        # checking for a bivalued cell with one different element in same square
        row_start = (row // rn) * rn
        col_start = (col // rn) * rn
        for r in range(row_start, row_start + rn):
            for c in range(col_start, col_start + rn):
                if (r!=row or c!=col) and sum(domains[r][c])==2:
                    pincer = []
                    for i in range(9):
                        if domains[r][c][i]:
                            pincer.append(i)
                    if pincer[0] == x[0] and pincer[1]!=x[1]:
                        zx=pincer[1]
                        zxrow = r
                        zxcol = c
                    elif pincer[1] == x[0] and pincer[0]!=x[1]:
                        zx=pincer[0]
                        zxrow = r
                        zxcol = c
    if zx is None:
        return inferenceCtr # no other bivalued cell found in same row, column or square
    # repeating the above matching for x[1]
    zy = None
    zyrow = None
    zycol = None
    # checking for a bivalued cell (x[1], zx) in same row
    for c in range(rows):
        if c!=col and sum(domains[row][c]) == 2:
            pincer = []
            for i in range(9):
                if domains[row][c][i]:
                    pincer.append(i)
            if pincer[0] == x[1] and pincer[1] == zx:
                zy=pincer[1]
                zyrow = row
                zycol = c
            elif pincer[1] == x[1] and pincer[0] == zx:
                zy=pincer[0]
                zyrow = row
                zycol = c
    if zy is None: # cell was not found in the same row
        # checking for a bivalued cell (x[1], zx) in same column 
        for r in range(rows):
            if r!=row and sum(domains[r][col]) == 2:
                pincer = []
                for i in range(9):
                    if domains[r][col][i]:
                        pincer.append(i)
                if pincer[0] == x[1] and pincer[1] == zx:
                    zy=pincer[1]
                    zyrow = r
                    zycol = col
                elif pincer[1] == x[1] and pincer[0] == zx:
                    zy=pincer[0]
                    zyrow = r
                    zycol = col

    if zy is None: # cell was not found in the same row or column
        # checking for a bivalued cell (x[1], zx) in same square
        row_start = (row // rn) * rn
        col_start = (col // rn) * rn
        for r in range(row_start, row_start + rn):
            for c in range(col_start, col_start + rn):
                if (r!=row or c!=col) and sum(domains[r][c])==2:
                    pincer = []
                    for i in range(9):
                        if domains[r][c][i]:
                            pincer.append(i)
                    if pincer[0] == x[1] and pincer[1]==zx:
                        zy=pincer[1]
                        zyrow = r
                        zycol = c
                    elif pincer[1] == x[1] and pincer[0]==zx:
                        zy=pincer[0]
                        zyrow = r
                        zycol = c
    if zy is None:
        return inferenceCtr # no other bivalued cell found in same row, column or square
    zxrow_start = (zxrow // rn) * rn 
    zxcol_start = (zxcol // rn) * rn 
    zyrow_start = (zyrow // rn) * rn 
    zycol_start = (zycol // rn) * rn 
    # check if cell in sqaure of (x[0],zx) pincer cell can see (x[1],zx) pincer cell
    # remove zx from cells that can see both pincer cells
    for r in range(zxrow_start, zxrow_start+rn):
        for c in range(zxcol_start, zxcol_start+rn):
            if (r!=zxrow or c!=zxcol) and (r!=zyrow or c!=zycol) and (r!=row or c!=col):
                if r==zyrow or c==zycol or (r>=zyrow_start and r<zyrow_start+rn and c>=zycol_start and c<zycol_start+rn):
                    domains[r][c][zx] = False
    # check if cell in sqaure of (x[1],zx) pincer cell can see (x[0],zx) pincer cell
    # remove zx from cells that can see both pincer cells
    for r in range(zyrow_start, zyrow_start+rn):
        for c in range(zycol_start, zycol_start+rn):
            if (r!=zyrow or c!=zycol) and (r!=zxrow or c!=zxcol) and (r!=row or c!=col):
                if r==zxrow or c==zxcol or (r>=zxrow_start and r<zxrow_start+rn and c>=zxcol_start and c<zxcol_start+rn):
                    domains[r][c][zx] = False
    return inferenceCtr