
# 223_Rectangle_Area

def compute_area(A, B, C, D, E, F, G, H):
    # sum of areas of two rectangles
    result = (C - A) * (D - B) + (G - E) * (H - F)
    # no overlap
    if (C <= E or G <= A or H <= B or D <= F):
        return result
    # overlap length on x
    dx = min(C, G) - max(A, E)
    # overlap length on y
    dy = min(D, H) - max(B, F)
    return result - dx * dy

print(compute_area(-3, 0, 3, 4, 0, -1, 9, 2))   # pragma: no cover
