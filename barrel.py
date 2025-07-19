import requests as rq
import argparse
import sys
import fitz # PyMuPDF

# Fluff
logo = r'''
  ____ __ _ _
 /=//==//=/  \
|=||==||=|    |
|=||==||=|~-, |
|=||==||=|^.`;|
 \=\\==\\=\`=.:
  `"""""""`^-,`.
           `.~,'
          ',~^:,
          `.^;`.
           ^-.~=;.
              `.^.:`.
'''

# Not fluff
usage_fluff = """Barrel: A Semi-All-In-One SANS Index Tool
Things barrel CAN do: 
- Convert a PDF to text
- Generate an index from said text file
- Combine multiple index files into one
Things barrel CANNOT do:
- Generate an index from a PDF directly
- Get an index perfectly (you will need to tailor the output. Some garbage slips through the cracks)
- Cook you breakfast
- Do your homework
"""

how_to = """How to use:
1. Download your PDFs from here: https://www.sans.org/account/download-materials
2. Decrypt your PDFs using a tool like qpdf or StirlingPDF
3. Convert your PDF to text using the `convert` argument: python barrel.py convert -i <input.pdf> -o <output.pdf>
4. Generate an index from the text file using the `index` argument: python barrel.py index -i <input.txt> -o <output.txt> -n <"your name">
5. Tidy up the output file as needed, removing any unwanted entries or formatting issues. This cannot be automated.
6. If you have multiple index files, combine them using the `combine` argument: python barrel.py combine <input1.txt> <input2.txt> <...> -o <output.txt>
"""

# Set up parser
parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input-file", help="text file of SANS book")
parser.add_argument("-o", "--output-file", help="output file of index")
parser.add_argument("-n", "--student-name", help="full name of student")
parser.add_argument("convert", action='store_true', help="convert PDF to text")
parser.add_argument("combine", nargs='+', help="combine multiple index files into one")
options = parser.parse_args(sys.argv[1:])

# Check if the user wants to convert a PDF to text
if sys.argv[1] == 'convert':
    if not options.input_file or not options.output_file:
        print("""Please provide both input and output files for conversion.\n
              Usage: python barrel.py convert -i input.pdf -o output.txt""")
        sys.exit(1)
    
    try:
        doc = fitz.open(options.input_file)
        with open(options.output_file, "w", encoding="utf-8") as f:
            for page in doc:
                f.write(page.get_text())
        doc.close()
        print(f"Converted {options.input_file} to {options.output_file}")
    except Exception as e:
        print(f"Error converting {options.input_file} to {options.output_file}: {e}")
    sys.exit(0)

# Check if the user wants to combine index files
'''if options.combine:
    if not options.input_file or not options.output_file:
        print("Please provide both input files (comma separated) and an output file for combining.")
        sys.exit(1)
    
    input_files = options.input_file.split(',')
    combined_index = set()
    
    for input_file in input_files:
        try:
            with open(input_file.strip(), "r", encoding='utf-8') as f:
                for line in f:
                    combined_index.add(line.strip())
            print(f"Added entries from {input_file.strip()}")
        except Exception as e:
            print(f"Error reading {input_file.strip()}: {e}")
    
    with open(options.output_file, "w", encoding='utf-8') as f:
        for entry in sorted(combined_index):
            f.write(entry + "\n")
    
    print(f"Combined index written to {options.output_file}")
    sys.exit(0)
'''
#if options.combine:
args = sys.argv[2:]
if sys.argv[1] == 'combine':
    if len(args) == 0:
        print("""Please provide input files (space separated)\n
              Usage: python barrel.py combine -i file1.txt,file2.txt,file3.txt""")
        sys.exit(1)

    index = {}
    for count, filename in enumerate(args):
        with open(filename, "r", encoding='utf-8') as f:
            for line in f.read().split("\n"):
                if ": " not in line:
                    continue
                index_key, pages = line.split(": ")
                if index_key not in index:
                    index[index_key] = ""
                index[index_key] += f"{count +1}({pages}) | "

    # Trim tailing " | "
    for key in index.keys():
        index[key] = index[key].rstrip(" | ")

    # Turn index into lines
    lines = []
    for key in index.keys():
        lines.append(f"{key}: {index[key]}")
    lines.sort()

    for line in lines:
        with open("combined.txt", "a", encoding='utf-8') as f:
            f.write(line + "\n")
    print(f"Combined index written to {f.name}")
    sys.exit(0)


if '__main__' not in __name__:
    print(logo)
    print(usage_fluff)
    print(how_to)
