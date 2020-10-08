# Backtracking vs. Compile-Search algorithm

Copyright (c) 2020 Yiming Lin

This repository implements catastrophic backtracking algorithm as well as compile-search algorithm which is first purposed in [Ken Thompson's paper in 1968](https://dl.acm.org/doi/pdf/10.1145/363347.363387). The purpose of current implementation is to simulate the [CloudFlare's outage in July 2, 2019](https://blog.cloudflare.com/details-of-the-cloudflare-outage-on-july-2-2019/), where the regex engine exhausted all the CPU resources. 

### Method of Measuring Algorithm
In order to keep consistency with [CloudFlare's official blog](https://blog.cloudflare.com/details-of-the-cloudflare-outage-on-july-2-2019/), we use exactly the same way to count "step" used in backtracking algorithm. Thus, our output is same as what is discussed and analyzed in [CloudFlare's official blog](https://blog.cloudflare.com/details-of-the-cloudflare-outage-on-july-2-2019/). 

However, method for counting step in backtracking algorithm cannot be easily migrated into counting step used in K.T.'s compile search algorithm. Then we decides to count steps in our own way which will be described in [Compile-Search Algorithm section](#compile-search-algorithm). 

### Backtracking Algorithm

##### The Term "Step"
According to  [CloudFlare's official blog](https://blog.cloudflare.com/details-of-the-cloudflare-outage-on-july-2-2019/),
- the regex engine matches substring against parts of regular expression counts as two step
    - Step n: Regex engine match chars against `pattern` (*pattern is some parts of a regex*)
    - Step n+1: Indice `[j, j+i)` matched successfully
- if pattern matching failed, then backtrack is needed. The entire process from matching failed to backtrack and rematch counts as two step
    - step n: Regex engine match chars against `pattern`, match failed, backtrack
    - step n+1: Indice `[j, j+i)` matched syccessfully. 
    - Notice that backtracking by adjusting matching index interval does not count as a separate step, which is consistent with [CloudFlare's official blog](https://blog.cloudflare.com/details-of-the-cloudflare-outage-on-july-2-2019/).
- drawing the conclusion (matched or failed) count as a separate step.

##### An Example: match `x=x` against `.*.*=.*` 
```sh
step 1 Greedily match chars with 1st .*
step 2 match index  [0, 3) with 1st .*   
step 3 Greedily match chars with 2nd .*  
step 4 match empty string with 2nd .*    
step 5 match index 3 E with =, backtrack 
step 6 Backtrack and rematch 1st .*      
step 6 match index  [0, 2) with 1st .*   
step 7 Greedily match chars with 2nd .*  
step 8 match index  [2, 3) with 2nd .*   
step 9 match index 3 E with =, backtrack 
step 10 Backtrack and rematch 2nd .*     
step 10 match empty string with 2nd .*   
step 11 match index 2 x with =, backtrack
step 12 Backtrack and rematch 1st .*
step 12 match index  [0, 1) with 1st .*
step 13 Greedily match chars with 2nd .*
step 14 match index  [1, 3) with 2nd .*
step 15 match index 3 E with =, backtrack
step 16 Backtrack and rematch 2nd .*
step 16 match index  [1, 2) with 2nd .*
step 17 match index 2 x with =, backtrack
step 18 Backtrack and rematch 2nd .*
step 18 match empty string with 2nd .*
step 19 attemp to match =
step 19 match index 1 = with =
step 21 Greedily match chars with 3rd .*
step 22 match index  [2, 4) with 3rd .*
step 23 done!
```
Note: E represent a space after the last character in the string

##### Run Backtracking Simulation
```sh
$ python backtracking.py
```
![alt text](https://github.com/y1m1ng1in/Regular-Expression-Backtracking/blob/master/docs/backtracking%20algorithm.png)

### Compile-Search Algorithm

##### The Term "Step"
- Each step in compile-search algorithm is each state of nfa visited when a character is consumed.
- The construction of NFA and the exploration of all reachable states by epsilon transition based on current state don't count as a step.
    - The construction of NFA for the same regular expression always requires the same number of steps. In this experiment, we are exploring matching strings with different length against the same regular expression. Thus, for each string the number of steps required for construct a NFA is same, which is not a factor that makes the number of steps used for matching different string. 
    - The NFA construction used algorithm used in this experiment can be executed in ploynormial time.
    - Since the time is really limited, the epsilon transition does not eliminated from constructed NFA. There are lots of ways to construct a NFA that does not contain epsilon transition, or employing algorithm such as traversing epsilson-closure to eliminate them. Thus, we currently just ignore the steps required for exploring all reachable states by epsilon transition. 
    - In this experiment, we perform a breadth first search (BFS) to find all reachable states by epsilon transition. 


##### Run Compile-Search Simulation
```sh
$ python kenthompson.py
```

![alt text](https://github.com/y1m1ng1in/Regular-Expression-Backtracking/blob/master/docs/ken%20thompson's%20algorithm.png)
