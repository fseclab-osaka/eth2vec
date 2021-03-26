## eth2vec

# Overview
Eth2Vec is an analysis tool based on a neural network for natural language processing, and it outputs the existence and kind of vulnerabilities in a target smart contract code by only taking the code as input. 
Using Eth2Vec, you can analyze code of smart contracts quickly even without expert knowledge on smart contract vulnerabilities.


# Install
We implemented Eth2Vec by utilizing **Kam1n0 version 2.0.0** (https://github.com/McGill-DMaS/Kam1n0-Community) and **py-solc-x** (https://pypi.org/project/py-solc-x/). 

1. Create clone of **Kam1n0** (https://github.com/McGill-DMaS/Kam1n0-Community) and **Eth2Vec** (this) onto your local.
2. 

First, the main module, PV-DM model, was implemented by \texttt{Kam1n0}, 
which is a server system~\cite{Ding2016Kam1n0} utilized for binary analysis~\cite{asm2vec}. 
We mainly modified the source codes in \texttt{DisassemblyFactoryIDA.ja\\va} and \texttt{ExtractBinaryViaIDA.py}. 
In particular, \texttt{ExtractBinaryVi\\aIDA.py} initially generates a JSON file extracted from IDA by disassembling binary codes, and then \texttt{DisassemblyFactoryIDA.java} takes the file to store the binary codes within \texttt{Kam1n0}. 
However, IDA cannot use EVM bytecodes for implementing Eth2Vec. 
Therefore, we changed \texttt{ExtractBinaryViaIDA.py}: For instance, the code information is obtained by compiling a Solidity file with \texttt{py-solc-x} without IDA, and then its resultant assembly codes, abstract syntax tree (AST), and binary codes are extracted. 

ドメイン名の全文字数を*d*としたとき、
その頻度*p<sub>i</sub>=c<sub>i</sub> / d*を用いて、エントロピー*E*は
以下のように表すことができる  
    <img src="https://latex.codecogs.com/gif.latex?\begin{align*}&space;E&space;=&space;-&space;\sum_{i=1}^{n}&space;p_{i}&space;\times&space;\log_{2}p_{i}&space;\end{align*}" />  
例: 3.180832987205441 (osaka-u.ac.jp)
4. ドメインに紐づけられたIPアドレス数  
5種類のDNSサーバ `1.1.1.1`, `8.8.8.8`, `208.67.222.123`, `176.103.130.130`, `64.6.64.6`
に介してドメインに紐づけられたIPアドレスを探し、その種類を数える  
例: 3 (github.com)
5. IPアドレスの所属する国数  
上記IPアドレスが割り振られた国を検索し、その種類を数える  
例: 1 (github.com)
6. Time To Live (TTL) の平均値  
上記DNSサーバへの問い合わせ時に取得したTTL値の平均  
例: 53667 (osaka-u.ac.jp)
7. TTLの標準偏差  
上記DNSサーバへの問い合わせ時に取得したTTL値の標準偏差  
例: 102768.95645475826 (osaka-u.ac.jp)
8. ドメインの有効日数  
whoisサーバに登録されたドメインの情報から、ドメインの作成日から有効期限までの日数を計算する  
例: 2268 (osaka-u.ac.jp)
9. ドメインのアクティブ日数  
whoisサーバに登録されたドメインの情報から、ドメインの作成日から直近の更新日までの日数を計算する  
例: 1904 (osaka-u.ac.jp)

- Amazon Linux AMI release 2018.03
- Node.js v12.18.3
- npm 6.14.6
