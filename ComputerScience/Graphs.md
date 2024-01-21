# Graphs

- A series of nodes with some amount of connections to other nodes.
  - no rules, just none, some or alot of connections
- All trees are Graphs

### Terms

- see [video](https://frontendmasters.com/courses/algorithms/graphs-overview/)
- Cycle: if you visit at least 3 nodes and return to the original node, you have a cycle
  - Visiting A,B,C,A is a cycle
- Acyclic graph: has no cycles
- Connected graph: Every node can reach every other node.
- Directed graph: Connections to nodes are one way or asymmetric.
  - asymmetric means that though two nodes are connected bidirectionally, one way is more expensive than the other way or has a greater weight than the other.
- Undirected graph: no direction between links, can go both ways between nodes.
- Weighted graph: There is some sort of value associated with the direction
  - in undirected graph, the weights are same - symmetric
  - in directed graph, you can have asymmetric weights between two connected nodes.
- dag graph: directed acyclic graph. every path has a terminus and you can't quite make it to every other node
- Vertex: Node can be referred to as a vertex or a point
- Edge: the connection between two nodes.
- Runtime: O(v \* E): for every vertex we visit every single edge in the graph.

### Representing Graphs

- Adjacency List (most common)
  - A list of edges: Each element in the list is a edge that says where it goes to and the weight associated with the connection.
  - it's a list showing what the node is adjacent to
  ```python
  [
    [{to: 1, weight: 10}, {to: 3, weight: 7}], # index 0 is the first node or node with value of 0 and points to nodes 1 and 3
    [], # this is for node 1 - it is a terminus for example and so would be an empty list (no edges it goes to)
    [{to: 0, weight: 5}] # node 2 points to node 0 and has a connection weight of 5
  ]
  ```
- Adjacency matrix (less common to see - takes more memory of O(V^2))

  - Each node is a row and the columns represent the other nodes it can connect to. The values in each row are the weights from node to node
  - Note how this takes up a lot of memory to represent all possible connections explicitly - it grows exponentially as you get more nodes.

  ```python
  [
    [0,10,0,5], # node 0 is not connected to 0, is to 1 with weight 10, is not connection to 2, and is to 3 with weight 5
    [0,0,0,0,0] # node 1 has a assymetric relationship - 1 has connections to it, but does not connect to any other node itself
  ]
  ```

### Searching

- Breadth first search and depth first search are available since all trees are graphs.
- We don't pop and pull off a stack, we call a function and use recursion for searching.
- In a graph, we often want the path associated with a search

```javascript
// Breadth First Search

// we need to know where we're starting from and what we're looking for, and want to return the path we took.
// because we don't use recursion with breadth first, we need to maintain the path ourselves as we search.
// common approach for this is filling an array of `prev` = [-1. ...] (no node has a -1 val).
// The previous array is who I came from (need a seen or visited array as well of Falses)
function bfs(graph, source, needle) {
  // since graph is adjacency matrix there are as many rows as cols, the length rows will = cols
  const seen = new Array(graph.length).fill(false);
  // setup previous array:
  const prev = new Array(graph.length).fill(-1); // fill with default -1s, nothing has parents right now

  // setup the source as seen as the first one
  seen[source] = true;
  const q = [source]; // put source as first in queue, note: source is a number
  // we don't revisit the first source as it would be a waste

  // while queue has length grab the item out of the queue
  do {
    const curr = q.shift();

    if (curr === needle) {
      break; // we found the needle, so exit loop
    }

    // adjacencies:
    // anything we select we grab out the row, by grabbing the row it represents connections to other nodes - i.e. the element in the row says what connection is to the column (node)
    const adjs = graph[curr]; // will have the elements in a row matching to cols to get the connection/edge
    // walk thru and grab each one of the edges
    for (let i = 0; i < adjs.length; i++) {
      // if no edge, then just continue
      if (adjs[i] === 0) {
        continue;
      }
      if (seen[i]) {
        // if we've seen this, then move on
        continue;
      }
      // if not seen, push it into queue, mark as seen and add where it came from
      seen[i] = true;
      // the previous where i came from is the current (the row)
      prev[i] = curr; // the thing we popped from the queue has our i as a child
      // now add i to the queue
      q.push(i);
    }

    // if we haven't found target, then we need to do some book keeping:
    seen[curr] = true;
  } while (q.length);

  // build backwards, walk previouses until we get to a -1
  let curr = needle; // start where are target to find is
  const out = []; // represents our path through the graph starting at the needle back to the source

  // loop until we've found a point that has no parent (if we never found the needle it will be -1 to begin with and we'll immediately stop and return empty path - there is no path from source to target)
  while (prev[curr] !== -1) {
    out.push(curr);
    curr = prev[curr]; // set this to who added me to this search/set it to parent
  }

  // if we did have a path then return and reverse the path
  if (out.length) {
    // we didn't add source because source has a parent of -1, so we need to concat it
    return [source].concat(out.reverse());
  } else {
    // or return nothing if no path
    return null;
  }
}
```
