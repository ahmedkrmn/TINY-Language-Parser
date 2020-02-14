### TINY Language Scanner and Parser
A Python PyQt GUI application for scanning and parsring TINY Language code (as defined in [Compiler Construction: Principles and Practice](https://www.amazon.com/Compiler-Construction-Principles-Kenneth-Louden/dp/0534939724)) and displaying the syntax tree of the given code sample. 
![Syntax Tree](/Demo1.png)

#### Running The Application
The instructions will assume that you're using a Linux distributions based on Debian due to to the dependency on [Pygraphviz](https://pygraphviz.github.io/) which fails when being built by Pip on Windows.

1. Install the OS dependencies by running `apt-get install graphviz libgraphviz-dev python3-tk`.
2. Set up a Python virtual enviroment with Pip and install the Python dependencies by running `pip install -r requirements.txt` in the project root directory.
3. Run `python __main__.py` in the project root directory.

#### An Example
Given the following TINY Language sample:
```
read x;
if 0<x then
    fact:=1;
    repeat
        fact:=fact*x;
        x:=x-1
    until x=0;
    write fact
end
```

After pasting this code snippet in the text box and clicking on **Parse**, the following sequence of steps is executed:
1. The source code is scanned to extract the tokens.
2. The extracted tokens are passed to a recursive-descent predictive parser which generates the syntax tree using a tree data structure.
3. With the help of the used graphing libraries, the syntax tree is then plotted.

![Syntax Tree](/Demo2.png)


#### Credits
The application is based on [muhakh](https://github.com/muhakh/TinyParser)'s implementation. A modified data structure is used for storing the syntax tree as well as using additional graphing libraries to provide a more precise and verbose visualization.
