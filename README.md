# VCELDI
### Bounded verifying continuous-time Extended Linear Duration Invariants

####Basic information

It's a prototype tool to verify continuous-time ELDIs formulas againt Timed Automata (TA). We say "bounded", means that the observation interval length is bounded by $[b,e]$. It's based on [PyDBM](http://people.cs.aau.dk/~adavid/UDBM/python.html) which is a Python binding to [UPPAAL DBM Library](http://people.cs.aau.dk/~adavid/UDBM/index.html).

#### Using under Linux

It's only available on Linux.

Before using it, you need to install:

1. [UPPAAL DBM libarary](http://people.cs.aau.dk/~adavid/UDBM/index.html)
2. [SWIG](http://www.swig.org/)
3. [PyDBM](http://people.cs.aau.dk/~adavid/UDBM/python.html)


You can find the installing help on the PyDBM website.

After installing, you can use the prototype scripts.

There are nine examples (example1~example9). We can run it as:

```shell
> python exampleX.py exampleX.xml exampleX.txt
```

* "X" : 1~9.
* "exampleX.xml" is the model file of TA in UPPAAL. "exampleX.txt" is ELDIs formula file.
* Specially, for example2~example5, they share the script file "example2.py".
* After running, it will generate a file "exampleXresult.txt" which stores the Quantified Linear Real Arithmetic (QLRA) formulas. It will take long time to generate "example9result.txt".


Then we call REDLOG to solve the QLRA formulas :

```shell
> ./reduce exmapleXresult.txt
```

* "reduce" is the execution file of REDLOG.

* It will generate a file "exampleXresult" which stores the results for each QLRA formula.

* Specially, for example9, its scale is too large that "example9result.txt" will be 3.1GB. We need to splite the file. We can use the scripts in folder "splitfiles":

  ```shell
  > python splitfile.py
  ```

* After spliting, we can call REDLOG:

  ```shell
  > python run.py
  ```







