# RGB COLORS

The aim is to somehow find a correlation between a rgb color and the colors relative luminance.

```sh

1> python3 main.py > colors.csv

2> mlr --csv sort -nr rel_lum colors.csv > sorted-colors.csv

# Top 1_000_000 colors
3> head -1000000 sorted-colors.csv > top-1_000_000-colors.csv

```