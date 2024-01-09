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
- Runtime: O(v * E): for every vertex we visit every single edge in the graph.


