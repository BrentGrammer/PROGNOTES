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

}

```