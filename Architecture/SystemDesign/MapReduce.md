# MapReduce
- Used for processing large data sets in a distributed system.

- Original challenge was dealing with large datasets and processing them.
- Vertical scaling for processing large datasets has a limit
- You eventually need horizontal scaling to deal with processing lots of data
  - need to add machines etc.

### Main idea

- The majority of data processing tasks can be split up into two main steps
  - Map: apply a map function to the data (stored across different machines in a distributed system)
    - transforms data into key value pairs (intermediate form)
      - This is important as you are looking for commonalities between the pieces/chunks of data
      - i.e. some keys will be common or related, so you can aggregate those etc. in the reduce step
    - these pairs are shuffled/sorted
  - Reduce
    - The key value pairs from the map step and reduced to some final output (i.e. a file etc)
- Assumes a central control plane exists that is aware of everything going on in the mapreduce process.
  - knows where all chunks of data reside and how to communicate with all the machines in the distributed system and workers doing the map and reduce work.
- Avoids moving data: The data remains unmoved wherever they reside. The map programs move to the data and operate on it locally. (we don't grab data and aggregate it moving it elsewhere).
- Fault Tolerance: Assumes the Map and Reduce functions are idempotent. Multiple repititions of them will result in the same outcome.
- 
