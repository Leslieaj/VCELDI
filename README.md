# VCELDI
### Bounded Model Checking Continuous-time Extended Linear Duration Invariants

#### Basic information

It's a prototype tool to verify continuous-time ELDIs formulas againt Timed Automata (TA). We say "bounded", means that the observation interval length is bounded by [b, e]. It's based on [PyDBM](http://people.cs.aau.dk/~adavid/UDBM/python.html) which is a Python binding to [UPPAAL DBM Library](http://people.cs.aau.dk/~adavid/UDBM/index.html).

#### Using under Linux

It's only available on Linux. (We test it on Ubuntu 16.04 64bit.)

Before using it, you need to install:

1. [UPPAAL DBM libarary](http://people.cs.aau.dk/~adavid/UDBM/index.html)
2. [PyDBM](http://people.cs.aau.dk/~adavid/UDBM/python.html)


The source codes of the UPPAAL DBM libarary and PyDBM are included in this package. You can install them or you can download by yourself.

You can find the installing help on the UPPAAL DBM and PyDBM website. (There may be some errors in some environments during installation process. Pls follow the help in their website.)

After installing, you can use the prototype scripts.

There are nine examples (example1~example9). We can run it as:

```shell
> python exampleX.py exampleX.xml exampleX.txt
```

* python version is 2.7, 64bit.
* "X" : 1~9.
* __"exampleX.xml"__ is the model file of TA in UPPAAL. __"exampleX.txt"__ is ELDIs formula file.
* After running, it will generate a file __"exampleXresult.txt"__ which stores the Quantified Linear Real Arithmetic (QLRA) formulas. _It will take long time to generate "example9result.txt"_.
* __"example7" and "example9" is the two experiments shown in the paper.__


Then we call REDLOG to solve the QLRA formulas :

```shell
> ./reduce exampleXresult.txt
```

* "reduce" is the execution file of REDLOG.

* It will generate a file __"exampleXresult"__ which stores the results(true or false) for each QLRA formula.

* The final result is the conjunction of the results of QLRA formula. We don't do the final step in this version because we want to see the result of every QLRA formula when we do some experiments. The final step is easy to get.

* The QE time will show in the end of the file "exampleXresult".

* You can also use the commad "time ./reduce exampleXresult.txt" to get the QE time.

* Specially, for example9, its scale is too large that "example9result.txt" will be 3.1GB. We can solve the formulas directly like above. We can also splite the file. We can use the scripts in folder __"splitfiles"__:

  ```shell
  > python splitfile.py
  ```
  After spliting, we can call REDLOG:

  ```shell
  > python run.py
  ```

* We don't upload the "example9result.txt" and "example9result", because they are too large.






