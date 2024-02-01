# Maps

### Terms
- Load Factor: amount of data points vs amount of storage
  - 0.7 considered a good load factor (data / memory space)
- key - hashable val to look up data. must be consistent
- value - associated with key
- collision: two keys map to same cell

### Structure
- underlying structure is an ArrayList
- A consistent hashing function takes in the key and produces a number
  - You can take this number and modulo it (%) by the length of the data (num items in the map)
  - This modulo result uniquely maps to a slot in the underlying array structure - you store the key and the value in that slot
  - if there is a collision an extra sublist is in the slot and you just add the keyvalue pair to the sub-arraylist

- O(1) access as long as collisions do not build up.
  - If a lot of keys are in the same bucket for ex., then that degrades the performance.


## LRU (Least Recently Used)
- Caching mechanism that evicts the oldest item
- An LRU Cache has nodes containing cached values that are arranged in a linked list.
- The LRU must be arranged in a way that allows for lookup of a value and moving that node/value to the head of the Queue when it is looked up and used.
- Most recently used val is at the head of the queue, the least recently used val is at the end of the queue.

### Data Structures in a LRU cache
- Doubly linked list (each node points forwards and backwards)
- HashMap (use a key for each value stored in the cache for lookups)
  - Have a key and a value - the value is a node in the linked list  (the container class of Node)
  - Eliminates need for traversing the list - you jump right to the value if it exists.
  - This results in a hashmap that has values in it that themselves contain pointers to other items/values in the same map.
- Time complexity is O(1) due to the O(1) lookup and no need for traversal
- We are composing data structures in the LRU cache