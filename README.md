# BenchMe
The major drawback of utilizing and enforcing SELinux in any system is the performance hit that it can make on the system. Therefore, it is important to point out that enforcing SELinux is not only about how it can be administrated and configured for best level of system security, but analyzing and possibly manipulating the SELinux policy for performance analysis and tuning while maintaining the same level of security is another important area of focus that should be a priority in some cases.

With that being said, BenchMe is a simple benchmark tool that could be used to measure various performance characteristics of Linux-based system with SELinux enabled. The goal is find out if enabling SELinux could introduce overhead to system response time.

### BenchMe Under the Hood: 
BenchMe is implemented in Python 2.7, and it utilizes various Linux commands including but limited to: DD, CPIPE, and PV, and also python libraries including but not limited to: OS, Subprocess, Multiprocessing, Time, and many others. 

### BenchMe in Action: 
BecnhMe runs multiple system performance tests listed below:

1. File Copy Test: measures the rate at which data can be transferred from one file to another, using various file sizes: 256Byte, 1KB, 4KB. Those tests ran for 10 seconds each, and each time the Bandwidth Rate and Copy Completion Time were captured in addition to the number of completed files that were successfully completed.

2. PIPE Throughput: measures the time a process can write 512 bytes file to a pipe.

3. PIPE Switching: this is similar to the previous test although the piping is between two processes in bi-directional way. 

4. Process Creation: measures the time a process can fork and reap a child that immediately exits.

5. EXECL: measures the number of execl calls that can be performed per minute.

6. Shell Scripts: measures the number of shell script that can be ran per minute.

##### Screenshots: 
![alt tag](https://i.imgur.com/fRRkXpw.jpg)
![alt tag](https://i.imgur.com/T8es8nv.jpg)
![alt tag](https://i.imgur.com/D4Ojfcv.jpg)
![alt tag](https://i.imgur.com/MrKwIwI.jpg)

### References: 
1. [UnixBench](https://github.com/kdlucas/byte-unixbench) 
2. [CPIPE](https://melbournegenomics.github.io/)
3. [PV](http://linux.die.net/man/1/pv)
