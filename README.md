# BaSFuzz
To mitigate the performance degradation of fuzz testing caused by repeatedly mutating similar seeds, we proposed **BaSFuzz**.

## Project Structure
 * **afl-basfuzz**: the main file for running BaSFuzz(in AFL)
 * **programs**: the directory of tested programs
 * **basfuzz.py**: the main file for running BaSFuzz(in Python)
 * **selection.py**: used for Seed Selection based on byte difference analysis
 * **data.py**: used to read seed byte
 * **similarity.py**: used to compute similarity between seeds

## Environments
| name   | version |
|--------|---------|
| python | 3.7     |
| numpy  | 1.24.3  |
| tqdm   | 4.65.0  |


## Usage

### Compile
Compile **afl-basfuzz**: The compile command is the same as afl

### Running
1. Run Python in a terminal  
`python ./basfuzz.py <name of tested project> <absolute path of output>`  

2. Run AFL in _another_ terminal  
`<path of afl-fuzz> -i <input> -o <output> <PUT> <parameters> @@`


Detailed scripts in each project in **programs**