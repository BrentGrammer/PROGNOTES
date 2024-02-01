# Storage

## Databases
- Database is just a server. A computer/machine.

### Persistence
- Persistence through a power outage etc. is not gauranteed with a database.
- If data is written to Disk, then the data will persist even if the database server goes down. (barring catastrophic machine failure
- If data is just in memory when server goes down, then the data is lost (i.e. when data is being put in a hash table or array etc. before written to disk.)  