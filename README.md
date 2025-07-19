```
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
```

### Barrel: A Semi-All-In-One SANS Index Tool  
---

#### Things barrel CAN do: 
- Convert a PDF to text
- Generate an index from said text file
- Combine multiple index files into one  
- Generate errors, helpful and unhelpful

#### Things barrel CANNOT do:
- Generate an index from a PDF directly
- Get an index perfectly (You will likely need to tailor the output. This is an unfortunate limitation of the tool in its current state)
- Cook you breakfast
- Your homework  
- Guarantee a passing grade on whatever exam you use this to prepare for  
- Explain why this project is named `barrel`  
---

#### Setup and Installation:  
1. Clone this repo.
2. Install Python if you don't have it. I developed this on 3.12.0, but anything 3.6 or newer is fine. 3.6 is the minimum as this file uses f-strings.  
3. If you want to mimic the environment it was developed in, install pipenv by running `pip install pipenv` (or the equivalent for your OS).  
   1. I suggest creating and activating a virtual environment and installing the packages into that env, rather than system-wide pip. You can run `pipenv install` and it should install all of the files from the pipfile. To activate the env, run `pipenv shell`. If you don't want to use pipenv, and you'd rather just use the system-wide pip, I have included a requirements.txt file as well.
4. Once in your virtual env (or not, depending on what you chose to do), you can proceed to the 'How to use' section.
---

#### How to use:
1. Download your PDFs from here: https://www.sans.org/account/download-materials
2. Decrypt your PDFs using a tool like [qpdf](https://github.com/qpdf/qpdf) or [StirlingPDF](https://www.stirlingpdf.com/) (or Adobe if you have that)
3. Convert your PDF to text using the `convert` argument: `python barrel.py convert -i <input.pdf> -o <output.txt>`
4. Generate an index using the `index` argument: `python barrel.py index -i <input.txt> -o <output.txt> -n <"your name">`
5. Tidy up the output file as needed, removing any unwanted entries. I tried to account for most common words and such, but some garbage may still slip through.
6. If you have multiple index files, combine them using the `combine` argument: `python barrel.py combine <input1.txt> <input2.txt> <input3.txt> ...` No need to specify output file, it will be written to combined.txt  

---

#### Future state and possible TODOs:  
[ ] - Probably not a clean way to do this, but can the decryption part be done in file?? Idk  
[ ] - Maybe allow for doing bulk conversion via an input file??  
[ ] - Maybe allow for bulk indexing too??  
[ ] - Probably some other janitorial cleaning needed as well

---  

*Special thanks to [George O](https://github.com/Ge0rg3) for the original inspiration for this. This is largely based on their work and is really just an expansion of it. You can view their original project [here](https://github.com/Ge0rg3/sans-index-creator).*



