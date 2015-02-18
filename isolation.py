#isolation
from pprint import pprint

points_list = [
    [0.0, 1.28, 0.64],
    [1.28, 1.28, 0.64],
    [1.28, 0.0, 0.64],
    [0.0, 0.0, 0.0]
]
point = points_list[3]
plane = (0, 1, 2)


product_left = [a - b for a, b in zip(point, points_list[plane[0]])]
dot_product = sum([i*j for i, j in zip(product_left, point)])

pprint(dot_product)
