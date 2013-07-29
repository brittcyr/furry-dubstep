furry-dubstep
=============

Overview
--------
These are my solutions to the coursera cryptography class from summer of 2013

Week 1
------
Decoding when a key is reused. This takes advantage of the fact that when a space is xor'd, it leaves a one in a higher bit

Week 2
------
This is implementing CBC and CTR

Week 3
------
Read in the data and then using sha256, hash the data with the previous result

Week 4
------
Keep querying the oracle

Week 5
------
Meet in the middle attack. Create one side by using mod multiplication with g inverse. The other side uses modular multiplication with the higher order bits

Week 6
------
Define a square root function with Newton's method. For the first answer, no searching since the formula gives the answer within one.
For the second question, just search near square root of N and once it works, print the answer.
For the third question, use the hint given, but multiply through by 2 so that the fractions go away.
The last part is just RSA.
