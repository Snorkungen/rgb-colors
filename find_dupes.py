from generate_contrasting_colors import OUT_DIR, OUT_FILE
from os.path import join

filename = join(OUT_DIR,OUT_FILE)

vals = dict()
line_nums = dict()
with open(filename, "r") as file:
    text = file.read()
    n = 0
    for line in text.splitlines():
        n+=1
        key =  line[:7]
        if vals.get(key):
            vals[key]+=1
        else: vals[key] = 1
        
        if line_nums.get(key):
            line_nums[key] += f" {n}"
        else: line_nums[key] = str(n)
dupes = dict()

for key in vals:
    if vals[key] > 1:
        print(f"{key},{vals[key]},{line_nums[key]}")


