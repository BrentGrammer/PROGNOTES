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
  - Have a key and a value - the value is a node in the linked list (the container class of Node)
  - Eliminates need for traversing the list - you jump right to the value if it exists.
  - This results in a hashmap that has values in it that themselves contain pointers to other items/values in the same map.
- Time complexity is O(1) due to the O(1) lookup and no need for traversal
- We are composing data structures in the LRU cache

### Implementing a LRU

```javascript
// helper
function createNode(value) {
  return value;
}

interface Node {
  value: T,
  next?: Node<T>;
  prev?: Node<T>;
}

class LRU {
  private length;
  private head; // Node<V> - the value
  private tail;

  private lookup; // Map<K, Node<V>> map with a key to the node with the value
  private reverseLookup; // we need this to determine the key of a value when we want to evict something and need to use it to clean up and prevent lookup map from growing indefinitely etc. we can then delete the key in the lookup map

// cache needs to have a capacity specified and passed in
  constructor(private capacity) {
    this.length = 0;
    this.head = this.tail = undefined; // initialize head and tail to undefined
    this.lookup = new Map();
    this.reverseLookup = new Map();
  }

  update(key, value) {
    let node = this.lookup.get(key);
    if (!node) {
      // we need to create a new node if it doesn't exist
      node = createNode(value);
      // adjust length of list
      this.length++;
      // prepend
      this.prepend(node);
      //delete if needed
      this.trimCache(); // ensures cache remains no greater than the capacity

      //update lookups
      this.lookup.set(key, node);
      this.reverseLookup.set(node, key);
    } else {
      // if exists, move it to front of list
      this.detach(node); // remove from list
      this.prepend(node); // add to front
      node.value = value; // incase value has been changed.
    }
  }


  get(key) {
    // check cache for existence
    const node = this.lookup.get(key);
    if (!node) return undefined;

    // if found, update value we've found by moving it to the front of queue (it has been most recently used now)
    this.detach(node); // remove from linked list -still in reverse lookup
    this.prepend(node); // add to front of queue

    // return val
    return node.value;
  }

  private detach(node) {
    // set the prev node next to skip the current one (removing it from list)
    if (node.prev) {
      node.prev.next = node.next;
    }
    // set the next node's prev to the current previos
    if (node.next) {
      node.next.prev = node.prev;
    }
    // with these we don't need to check for length==1 since head and tail will be undefined (??)
    if (this.head === node) {
      this.head = this.head.next; // reset head if we are currently detaching the head
    }
    if (this.tail === node) {
      this.tail = this.tail.prev;
    }
    // clear current links on our node
    node.next = undefined;
    node.prev = undefined;
  }
  private prepend(node) {
    if (!this.head) {
      this.head = this.tail = undefined;
      return;
    }

    // point to head
    node.next = this.head;
    this.head.prev = node; // set head's prev to current node

    this.head = node;
  }
  private trimCache() {
    if (this.length <= this.capacity) {
      return;
    }

    // clean/trim cache
    const tail = this.tail;
    this.detach(this.tail);

    const key = this.reverseLookup.get(tail);

    this.lookup.delete(key);
    this.reverseLookup.delete(tail);
    this.length--;
  }
}
```
