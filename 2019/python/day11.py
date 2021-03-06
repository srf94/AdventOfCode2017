import numpy as np
from utils import read_data
from intcode.vm import IntcodeVM


raw = read_data(11)[0].split(",")


def paint_spaceship(panel_colours):
    left_rotation = np.array([[0, -1], [1, 0]])

    direction = np.array([0, 1])
    location = np.array([0, 0])
    vm = IntcodeVM(raw)

    while True:
        # 0 is black, 1 is white
        intcode_input = panel_colours.get(tuple(location), 0)

        colour = vm.run(intcode_input)
        if colour is None:
            break

        panel_colours[tuple(location)] = colour

        rotation = vm.run()
        if rotation == 0:
            direction = left_rotation.dot(direction)
        else:
            direction = left_rotation.T.dot(direction)
        location = location + direction
    return panel_colours


print("Part 1:")
print(len(paint_spaceship({})))


colours = paint_spaceship({(0, 0): 1})

# Shift grid so every point is in top-right quadrant
min_x = abs(min(x for x, y in colours))
min_y = abs(min(y for x, y in colours))
shifted_colours = {(x + min_x, y + min_y): v for (x, y), v in colours.items()}

max_x = abs(max(x for x, y in shifted_colours))
max_y = abs(max(y for x, y in shifted_colours))
array = [[" "] * (max_x + 1) for _ in range(max_y + 1)]
for (x, y), v in shifted_colours.items():
    array[y][x] = "0" if v else " "


print("Part 2:")
print("\n".join("".join(i) for i in reversed(array)))
