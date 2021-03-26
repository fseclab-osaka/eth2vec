## eth2vec

# Overview
Eth2Vec is an analysis tool based on a neural network for natural language processing, and it outputs the existence and kind of vulnerabilities in a target smart contract code by only taking the code as input. 
Using Eth2Vec, you can analyze code of smart contracts quickly even without expert knowledge on smart contract vulnerabilities.


# Install and Build
We implemented Eth2Vec by utilizing **Kam1n0 version 2.0.0** (https://github.com/McGill-DMaS/Kam1n0-Community) and **py-solc-x** (https://pypi.org/project/py-solc-x/). 

1. Create clones of **Kam1n0** (https://github.com/McGill-DMaS/Kam1n0-Community) and **Eth2Vec** (this) onto your local.
2. Build Kam1n0 from the source code in `kam1n0`.
3. Copy `app` of Eth2Vec to `kam1n0/kam1n0-apps/src/main/java/ca/mcgill/sis/dmas/kam1n0` of Kam1n0.
4. Copy `bin` of Eth2Vec to `kam1n0/kam1n0-resources` of Kam1n0.
5. Copy a file in `commons` of Eth2Vec to `kam1n0/kam1n0-commons/src/main/java/ca/mcgill/sis/dmas/env` of Kam1n0.
6. Copy `js` of Eth2Vec to `kam1n0/kam1n0-apps/target/classes/static` of Kam1n0.
7. Rebuild Kam1n0 with the copied files of Eth2Vec.
