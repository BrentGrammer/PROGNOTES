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
- High Availability = minimizing outages
  - i.e. think of a 4x4 that gets a flat in the desert - with a spare tire the owner can replace the flat, without it, services to come out to tow would take much longer. the spare tire allows for high availability because it minimized the time the vehicle could not proceed.
- Ensuring high levels of availability has tradeoffs and costs - higher latency or lower throughput for example.
- Need to decide whether high availability (i.e. five nines etc) is necessary for the system
- **Need to eliminate single points of failure using REDUNDANCY**
  - having duplicate functions and parts of the system to take over if failure occurs
  - Example add more servers, add more load balancers (eliminate single server or single load balancer failing bringing system down)
- Passive Redundancy: multiple duplicate components where if one dies nothing will happen, the other components will continue running. i.e. multiple servers or twin engines on an airplane
- Active Redundancy: multiple machines that work together in a way that only one or a few of them are going to be typically handling work. If one of the working machines fails the other machines will know about it and they will take over it's job for it.
  - ex leader election
- High Availability does NOT mean UX is flawless, it means that the recovery of a failure is reduced to the minumum time possible.
  - UX disruption is okay for High Availability (i.e. going to standby server means the user has to re-login)

## 9s
- 5 9s (99.999%) = ~5 minutes of downtime per year
- 3 9s (99.9%) = ~8.7 hours downtime per year

## Fault Tolerance is NOT High Availability
- Fault Tolerance happens when a system continues to work without user disruption in the case of errors in 1 or more components of the system
  - It means to Operate THROUGH failure.
- High Availability involves potential user disruption and is only about minimizing downtime.
- see [video](https://learn.cantrill.io/courses/1101194/lectures/25301529) at 9:00 timestamp
- Fault Tolerance involves additional logic to route around failures and keep the system up during faults. High Availability just involves redundant components available that maximize uptime and minimize downtime.
- Fault Tolerance is more expensive and takes longer to implement than High Availability
  - Ex: a jet with multiple engines that needs to operate if an engine fails and then land safely to effect repairs
  - A plane that has a fault in the air cannot tolerate user disruption or outage.

  ### Disaster Recovery
  - What we do when High Availability and Fault Tolerance do not work
  - We need to preserve the irreplacable parts of the system so that we can rebuild with them.
  - Off premise backups and access to them need to be in place.