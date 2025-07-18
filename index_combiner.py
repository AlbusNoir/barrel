import sys

# Parse CLI flags
args = sys.argv[1:]
if len(args) == 0:
<<<<<<< HEAD
    print("Usage: 'python index_combiner.py index1.txt index2.txt index3.txt ... > output_file'")
=======
    print("Usage: 'python index_combiner.py index1.txt index2.txt index3.txt' etc.")
>>>>>>> 8acc4f77112e907fd3b4345eee7e7736c1773a7a

# Get file data
index = {}
for count, filename in enumerate(args):
    with open(filename, "r") as f:
        for line in f.read().split("\n"):
            if ": " not in line:
                continue
            index_key, pages = line.split(": ")
            if index_key not in index:
                index[index_key] = ""
            index[index_key] += f"{count + 1}({pages}) | "

# Trim trialing " | "s
for key in index.keys():
    index[key] = index[key].rstrip(" | ")

# Turn index -> lines
lines = []
for key in index.keys():
    lines.append(f"{key}: {index[key]}")
lines.sort()

for line in lines:
    print(line)