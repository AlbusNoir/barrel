import requests as rq
import argparse
import sys
import fitz # PyMuPDF


# Set up parser
parser = argparse.ArgumentParser(description="Barrel: A Semi-All-In-One SANS Index Tool", formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument("-i", "--input-file", help="Use: -i <inputfile>. Required for: convert")
parser.add_argument("-o", "--output-file", help="Use: -o <outputfile>. Required for: convert")
parser.add_argument("-n", "--student-name", help="Your full name, as it appears in the index. Used as a delimiter for parsing index.")
parser.add_argument("index", action='store_true', help="User: index -i <input.txt> -o <output.txt> -n 'Your Name'")
parser.add_argument("convert", action='store_true', help="Use: convert -i <input.pdf> -o <output.txt>")
parser.add_argument("combine", nargs='*', help="Use: combine <input1.txt> <input2.txt> <input3.txt> ...")
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


# Check if the user wants to combine index files:
if sys.argv[1] == 'combine':
    args = sys.argv[2:]
    if len(args) == 0:
        print("""Please provide input files (space separated)\n
              Usage: python barrel.py combine file1.txt file2.txt file3.txt""")
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

# Index
if sys.argv[1] == 'index':
# The meat of the code: Generate an index from a text file
    if not options.input_file or not options.output_file or not options.student_name:
        print("Please enter the required options.\nUsage: python barrel.py -i input.txt -o output.txt -n 'Your Name'")
        sys.exit(1)

    delimiter = f"Licensed To: {options.student_name}"

    # Get common English words. Using https://github.com/dwyl/english-words
    common_words = rq.get("https://raw.githubusercontent.com/dwyl/english-words/master/words.txt").text.split("\n")

    # Doubling up a little bit by using a file for some additional common words.
    common_words_file = 'common_words_large.txt'

    # Function to recursively strip given characters in a word. We're stripping most common symbols
    characters_to_strip = "+=|©$#*.@%^&{}<>()'\":,”“‘?;-•’—…[]!"
    phrases_to_strip = ["'s", "'re", "'ve", "'t", "[0]", "[1]", "[2]", "[3]", "[4]", "[5]", "[6]"]
    def strip_characters(word):
        word_length = len(word)
        word = word.replace("’", "'")
        while True:
            for phrase in phrases_to_strip:
                if word.endswith(phrase):
                    word = word[:len(phrase)]
            word = word.strip(characters_to_strip).rstrip(".")
            if len(word) == word_length:
                return word
            else:
                word_length = len(word)

    # Driver function to check if a word should be added to the index
    def word_is_eligible(word):
        # Length check
        if len(word) < 3:
            return False
        # Starts with number
        if word[0].isdigit():
            return False
        # Not common English word, or a plural of a common word
        if word.lower() in common_words or word.lower() + "s" in common_words:
            return False
        # same check but on file
        with open(common_words_file, "r") as f:
            if word.lower() in f or word.lower() + "s" in common_words:
                return False
        # Not URL
        if word.startswith("http://") or word.startswith("https://"):
            return False
        # If we reach this point, the word is eligible
        return True

    # Get pages in text file
    with open(options.input_file, "r", encoding='utf-8') as f:
        data = f.read()
        pages = data.split(delimiter)[1:]

    # Get words per page
    index = {}        # store page number and words on page
    total_words = []  # Stores all words
    for page_idx, page in enumerate(pages):
        # Recursively strip whitespace from newline and tabs and replace with singular space
        page = page.replace("\n", " ").replace("\t", " ")
        page_len = len(page)
        while True:
            page = page.replace("  ", " ")
            if len(page) == page_len:
                break
            else:
                page_len = len(page)
        # Trim whitespace
        page = page.strip()
        # Get words
        words = page.split(" ")
        long_words = []
        for word in words:
            # Strip out some punctuation
            word = strip_characters(word).lower()
            # If the word made it past the checks, append to index
            if word_is_eligible(word):
                total_words.append(word)
                long_words.append(word)
        index[page_idx] = long_words

    # Get results
    results = []
    for word in set(total_words):
        # Get pages where the word appears
        pages_word_is_in = []
        for page in index.keys():
            if word in index[page]:
                pages_word_is_in.append(str(page))
        
        if len(pages_word_is_in) < 15:
            joined_pages = ', '.join(pages_word_is_in)
            # Only append if not page number
            if word != joined_pages:
                results.append(f"{word}: {', '.join(pages_word_is_in)}")

    # Finally, sort output and write to file
    results.sort(key=str.casefold)

    with open(options.output_file, "w", encoding='utf-8') as f:
        for result in results:
            f.write(result + "\n")

    print(f"Written index to {options.output_file}")
