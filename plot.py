import matplotlib.pyplot as plt
import csv


def read_csv(filename):
    rows = []
    with open(filename, "r") as f:
        print("Started reading from " + filename)
        reader = csv.reader(f)
        next(reader)

        for rgb, hex, rel_lum in reader:
            rows.append([
                list(map(int,
                         rgb.strip("(").strip(")").split())), hex,
                float(rel_lum)
            ])
    return rows


def get_color(color):
    rows = read_csv(f"data/{color}.csv")
    return [
        list(map(lambda list: sum(list[0]), rows)),
        list(map(lambda list: list[2], rows))
    ]


gray = get_color("gray")
red = get_color("red")
green = get_color("green")
blue = get_color("blue")
yellow = get_color("yellow")
cyan = get_color("cyan")
purple = get_color("purple")

# draw lines
fig, ax = plt.subplots()
ax.plot(gray[0], gray[1], color="gray")
ax.plot(yellow[0], yellow[1], "y")
ax.plot(cyan[0], cyan[1], "c")
ax.plot(purple[0], purple[1], color="purple")
ax.plot(red[0], red[1], "r")
ax.plot(green[0], green[1], "g")
ax.plot(blue[0], blue[1], "b")

ax.set_xlabel("Sum")
ax.set_ylabel("Luminance")

plt.show()