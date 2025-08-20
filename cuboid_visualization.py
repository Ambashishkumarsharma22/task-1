import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

BRICK_LEN = 200
BRICK_WID = 100
BRICK_HT = 100

def place_bricks(L, W, H):
    bricks = []
    # Walls: front, back, left, right
    for z in range(0, H, BRICK_HT):
        for y in [0, W - BRICK_WID]:
            for x in range(0, L, BRICK_LEN):
                bricks.append((x, y, z, 0, 1, 2))
        for x in [0, L - BRICK_LEN]:
            for y in range(BRICK_WID, W - BRICK_WID, BRICK_WID):
                bricks.append((x, y, z, 0, 1, 2))
    # Floor and ceiling layers
    for y in range(BRICK_WID, W - BRICK_WID, BRICK_WID):
        for x in range(BRICK_LEN, L - BRICK_LEN, BRICK_LEN):
            bricks.append((x, y, 0, 0, 1, 2))
            bricks.append((x, y, H - BRICK_HT, 0, 1, 2))
    return bricks

def find_best_cuboid(max_bricks=10000):
    bestL, bestW, bestH, bestN, max_volume = 0, 0, 0, 0, 0
    for N in range(20, 41):
        L = N * BRICK_LEN
        W = N * BRICK_WID
        H = N * BRICK_HT
        bricks = place_bricks(L, W, H)
        if len(bricks) <= max_bricks:
            volume = L * W * H
            if volume > max_volume:
                bestL, bestW, bestH, bestN, max_volume = L, W, H, len(bricks), volume
    return bestL, bestW, bestH, bestN

def draw_brick(ax, x, y, z, dx, dy, dz, color='red'):
    verts = [
        [(x, y, z), (x+dx, y, z), (x+dx, y+dy, z), (x, y+dy, z)],
        [(x, y, z+dz), (x+dx, y, z+dz), (x+dx, y+dy, z+dz), (x, y+dy, z+dz)],
        [(x, y, z), (x+dx, y, z), (x+dx, y, z+dz), (x, y, z+dz)],
        [(x, y+dy, z), (x+dx, y+dy, z), (x+dx, y+dy, z+dz), (x, y+dy, z+dz)],
        [(x, y, z), (x, y+dy, z), (x, y+dy, z+dz), (x, y, z+dz)],
        [(x+dx, y, z), (x+dx, y+dy, z), (x+dx, y+dy, z+dz), (x+dx, y, z+dz)]
    ]
    ax.add_collection3d(Poly3DCollection(verts, facecolors=color, edgecolors='k', linewidths=0.5, alpha=0.7))

def visualize(bricks):
    fig = plt.figure(figsize=(12,8))
    ax = fig.add_subplot(111, projection='3d')
    for (x, y, z, _, _, _) in bricks:
        draw_brick(ax, x, y, z, BRICK_LEN, BRICK_WID, BRICK_HT)
    ax.set_xlabel('X (mm)')
    ax.set_ylabel('Y (mm)')
    ax.set_zlabel('Z (mm)')
    ax.set_title('3D Hollow Cuboid Visualization')
    plt.show()

if __name__ == '__main__':
    bestL, bestW, bestH, bestN = find_best_cuboid()
    print(f"Best Cuboid: {bestL/1000:.2f} x {bestW/1000:.2f} x {bestH/1000:.2f} meters, using {bestN} bricks.")
    bricks = place_bricks(bestL, bestW, bestH)
    visualize(bricks)

