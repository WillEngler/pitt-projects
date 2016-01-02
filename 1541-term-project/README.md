1541-term-project
=================

Sample programs in C++ and Java to compare performance for a computer architecture report.

How to Compile
--------------

* C++ programs: 
 I tested and compiled CReplace and CDelete using g++ V 4.7.2 on a Debian Linux distribution. Both CDelete.cpp and CReplace.cpp rely on the helper functions in C1541.h. (Yes, I implemented functions in a header file. I'm aware of how janky that is.) I compiled with the std=c++11 flag because I make frequent use of C++ 11 language features.

* Java programs: 
 I compiled and tested JReplace and JDelete with Java version 8. JDelete.java and JReplace.java depend on the helper methods in J1541.java.

Each of the four programs expects two command line arguments: the first should be the path of a file to be modified. The second should be the path of a CSV file. For the Replace programs, the CSV file should be in the format of \<stringToFind1\>,\<replacementString1\>,\<stringToFind2\>,\<replacementString2\>... . For the Delete programs, the CSV program should be in the format \<StringToDelete1\>,\<StringToDelete2\>... .
