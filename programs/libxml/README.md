# Use BaSFuzz to test _libxml_

1. Start a terminal in the root directory, and execute:  
`python ./basfuzz.py libxml`

2. Copy _afl-fuzz_ from **afl-basfuzz** to this directory.

3. Start a new terminal in this directory, and execute:  
`./run.sh`