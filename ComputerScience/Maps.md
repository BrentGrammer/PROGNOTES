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
