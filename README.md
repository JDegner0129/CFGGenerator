# Context-Free Grammars for Python #

A Python module for CSCE 428 (Automata, Computation, and Formal Languages) that, given a
newline-delimited file of the form:

> number of rules
>
> rule 1
>
> ...
>
> rule n
>
> expression 1
>
> ...
>
> expression m

Will evaluate all of the provide strings for a match against the provided context-free
grammar.

## Running the Program ##
To run this program, execute the command `python grammar.py < <inputfile>` from the command line.
Or, if you prefer, simply provide a pattern and expressions from stdin.

## Input ##
This module takes one input file from the command line and parses its first line as the number
of rules in the context-free grammars, the next n lines as the grammar's rules, and the remaining
lines as the expressions to be matched against the grammar.

## Output ##
This module will print 'YES' or 'NO' for each expression in the input file to denote its membership
in the context-free grammar's language.

## The Grammar Rules ##
TODO.

## How It Works ##
TODO.

## Technologies Used ##
- Python 2.7.5