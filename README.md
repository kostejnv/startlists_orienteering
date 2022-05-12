# Creating startlists for orienteering events

This project is used for testing methods for the problem Creating orienteering startlists for orienteering events described in my bachelor thesis "Algorithms for timetabling in sports".

## Requirements

+ pandas==1.3.4
+ minizinc==0.6.0

## Usage

The results of the experiments can be shown if you run:

```
python3 show_results.py
```

If you want to test methods, run:

```
python3 tests.py
```
You can also run only specific method if you run one of the function included in script *tests.py*

Let us note that although most of the data you can find [Czech orienteering database (ORIS)](https://oris.orientacnisporty.cz/) - used startlists, entries and event info, the information about courses are not public. For illustration how the platform works, we add these information for one of event to the project. It was with the allowance of organizers.