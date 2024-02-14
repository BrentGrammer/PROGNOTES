# Availability

- How resistant to failure a system is - how fault tolerant is the system
- The percentage of a given period of time where the system is operational

### Measuring Availability

$$\text{Number of non-error Responses} \over \text{Number of total requests}$$

- The percentage of time that a system is operational and up during a given year.
- measured in '9s' (percentages with the number 9). Ex: 99% availability = two nines of availability, 99.9% availability means it has three nines availability (number of 9s in the metric). 90% = one nine
  - 4 nines and up availability is target (five nines is gold standard and considered **Highly Available**)
- SLA - service level agreement. Agreement between provider and customers on the system's availability (amongst other things)
  - SLO - service level objective - a SLA is made up of SLOs, more granular gaurantees

### High Availability - use REDUNDANCY to eliminate single points of failure

- Ensuring high levels of availability has tradeoffs and costs - higher latency or lower throughput for example.
- Need to decide whether high availability (i.e. five nines etc) is necessary for the system
- **Need to eliminate single points of failure using REDUNDANCY**
  - having duplicate functions and parts of the system to take over if failure occurs
  - Example add more servers, add more load balancers (eliminate single server or single load balancer failing bringing system down)
- Passive Redundancy: multiple duplicate components where if one dies nothing will happen, the other components will continue running. i.e. multiple servers or twin engines on an airplane
- Active Redundancy: multiple machines that work together in a way that only one or a few of them are going to be typically handling work. If one of the working machines fails the other machines will know about it and they will take over it's job for it.
  - ex leader election
