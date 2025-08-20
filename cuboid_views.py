import csv

BRICK_LEN = 200
BRICK_WID = 100
BRICK_HT = 100

def place_bricks(L, W, H):
    bricks = []
    for z in range(0, H, BRICK_HT):
        for y in [0, W - BRICK_WID]:
            for x in range(0, L, BRICK_LEN):
                bricks.append((x, y, z))
        for x in [0, L - BRICK_LEN]:
            for y in range(BRICK_WID, W - BRICK_WID, BRICK_WID):
                bricks.append((x, y, z))
    for y in range(BRICK_WID, W - BRICK_WID, BRICK_WID):
        for x in range(BRICK_LEN, L - BRICK_LEN, BRICK_LEN):
            bricks.append((x, y, 0))
            bricks.append((x, y, H - BRICK_HT))
    return bricks

def find_best_cuboid(max_bricks=10000):
    bestL, bestW, bestH, max_volume = 0, 0, 0, 0
    for N in range(20, 41):
        L = N * BRICK_LEN
        W = N * BRICK_WID
        H = N * BRICK_HT
        bricks = place_bricks(L, W, H)
        if len(bricks) <= max_bricks:
            volume = L * W * H
            if volume > max_volume:
                bestL, bestW, bestH, max_volume = L, W, H, volume
    return bestL, bestW, bestH

def save_views_to_csv(bricks, bestH):
    maxZ = bestH - BRICK_HT
    
    with open('top_view.csv', 'w', newline='') as ftop, open('bottom_view.csv', 'w', newline='') as fbot:
        writer_top = csv.writer(ftop)
        writer_bottom = csv.writer(fbot)
        writer_top.writerow(['BrickID', 'X(mm)', 'Y(mm)', 'Z(mm)'])
        writer_bottom.writerow(['BrickID', 'X(mm)', 'Y(mm)', 'Z(mm)'])
        
        for i, (x, y, z) in enumerate(bricks, 1):
            if z == 0:
                writer_bottom.writerow([i, x, y, z])
            if z == maxZ:
                writer_top.writerow([i, x, y, z])

if __name__ == '__main__':
    bestL, bestW, bestH = find_best_cuboid()
    print(f"Best Cuboid: {bestL/1000:.3f} x {bestW/1000:.3f} x {bestH/1000:.3f} meters")
    
    bricks = place_bricks(bestL, bestW, bestH)
    print(f"Total bricks used: {len(bricks)}")

    save_views_to_csv(bricks, bestH)
    print("Top view saved to top_view.csv")
    print("Bottom view saved to bottom_view.csv")


