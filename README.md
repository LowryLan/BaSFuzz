# BaSFuzz
To mitigate the performance degradation of fuzz testing caused by repeatedly mutating similar seeds, we proposed **BaSFuzz**.

## Project Structure
 * **MOpt-basfuzz**: the main file for running BaSFuzz(on the basis of MOpt)
 * **afl-basfuzz**: the main file for running BaSFuzz(on the basis of AFL)
 * **programs**: the directory of tested programs
 * **basfuzz.py**: the main file for running BaSFuzz(in Python)
 * **selection.py**: used for Seed Selection based on byte difference analysis
 * **data.py**: used to read seed byte
 * **similarity.py**: used to compute similarity between seeds
 * **afl-gcc**: used to compile the program under test

## Environments
The experimental development and execution platform consisted of a computer equipped with 8 AMD® Ryzen 9 5900x
processors and 16GB of RAM.

| name   | version |
|--------|---------|
| Ubuntu | 20.04   |
| python | 3.7 3.8 |
| numpy  | 1.24.3  |
| tqdm   | 4.65.0  |

Install some required libraies for 32bit binaries.  
`sudo dpkg --add-architecture i386`  
`sudo apt-get update`  
`sudo apt-get install libc6:i386 libncurses5:i386 libstdc++6:i386 lib32z1`  

## Usage

### Compile
Compile **afl-basfuzz**: The compile command is the same as afl

### Running
1. Run Python in a terminal  
`python ./basfuzz.py <name of tested project>`  

2. Run AFL in _another_ terminal  
`<path of afl-fuzz> -i <input> -o <output> <PUT> <parameters> @@`


Detailed scripts in each project in **programs**

_\*NOTE*:_   
 We recommend testing the environment by testing _readelf_, because we provide **in2** for it, which contains a small number of seeds.
