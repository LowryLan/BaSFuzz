# Use BaSFuzz to test _readelf_

We have provided **in2**, which contains a small amount of seeds for everyone to test the environment.

2. Start a terminal in the root directory, and execute:  
`python ./basfuzz.py readelf`

3. Copy _afl-fuzz_ from **afl-basfuzz** to this directory.

4. Start a new terminal in this directory, and execute:  
`./run.sh`