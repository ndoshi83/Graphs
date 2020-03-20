"""
Simple graph implementation
"""
from util import Stack, Queue  # These may come in handy

class Graph:

    """Represent a graph as a dictionary of vertices mapping labels to edges."""
    def __init__(self):
        self.vertices = {}

    def add_vertex(self, vertex_id):
        """
        Add a vertex to the graph.
        """
        self.vertices[vertex_id] = set()

    def add_edge(self, v1, v2):
        """
        Add a directed edge to the graph.
        """
        if v1 in self.vertices and v2 in self.vertices:
            self.vertices[v1].add(v2)
        else:
            raise ValueError('Vertex does not exist')

    def add_undirected_edge(self, v1, v2):
        """
        Add a undirected edge to the graph.
        """
        if v1 in self.vertices and v2 in self.vertices:
            self.vertices[v1].add(v2)
            self.vertices[v2].add(v1)
        else:
            raise ValueError('Vertex does not exist')

    def get_neighbors(self, vertex_id):
        """
        Get all neighbors (edges) of a vertex.
        """
        if vertex_id in self.vertices:
            return self.vertices[vertex_id]
        else:
            raise ValueError('Vertex does not exist')

    def bft(self, starting_vertex):
        """
        Print each vertex in breadth-first order
        beginning from starting_vertex.
        """
        # Create queue
        q = Queue()
        # Enqueue starting vertex
        q.enqueue(starting_vertex)
        # Create a set to store visited vertices
        visited = set()
        # While the queue is not empty
        while q.size() > 0:
            # Dequeue first vertex
            v = q.dequeue()
            # Check if vertex is visited
            # If not visited
            if v not in visited:
                # Mark it as visited
                print(v)
                visited.add(v)
                # Enqueue all neighbors into queue
                for neighbor in self.get_neighbors(v):
                    q.enqueue(neighbor)

    def dft(self, starting_vertex):
        """
        Print each vertex in depth-first order
        beginning from starting_vertex.
        """
        # Create stack
        s = Stack()
        # Push starting vertex
        s.push(starting_vertex)
        # Create a set to store visited vertices
        visited = set()
        while s.size() > 0:
            # Pop first vertex
            v = s.pop()
            # Check if vertex is visited
            # If not visited
            if v not in visited:
                print(v)
                visited.add(v)
                # Push all neighbors into stack
                for neighbor in self.get_neighbors(v):
                    s.push(neighbor)

    def dft_recursive(self, starting_vertex, visited = None):
        """
        Print each vertex in depth-first order
        beginning from starting_vertex.

        This should be done using recursion.
        """
        if visited is None:
            visited = set()

        print(visited)
        # Check if node has been visited
        if starting_vertex in visited:
            return visited
        # If not
        else:
            # Mark as visited
            visited.add(starting_vertex)
            # Call dft_recursive on each neighbor
            for neighbor in self.get_neighbors(starting_vertex):
                print(neighbor)
                self.dft_recursive(neighbor)

    def bfs(self, starting_vertex, destination_vertex):
        """
        Return a list containing the shortest path from
        starting_vertex to destination_vertex in
        breath-first order.
        """
        # Create queue
        q = Queue()
        # Enqueue a path to the starting vertex
        q.enqueue( [starting_vertex] )
        # Create set to store visited vertices
        visited = set()
        # While queue is not empty
        while q.size() > 0:
            # Dequeue first PATH
            path = q.dequeue()
            # Grab vertex from end of the path
            v = path[-1]
            # Check if vertex is visited
            # If not visited
            if v not in visited:
                # Mark as visited
                visited.add(v)
                # Check if vertex is target
                if v == destination_vertex:
                    # If positive, return Path
                    return path
                # Enqueue path to neighbors
                for neighbor in self.get_neighbors(v):
                    # Copy of path
                    path_c = path.copy()
                    path_c.append(neighbor)
                    # Enqueue copy
                    q.enqueue(path_c)

    def dfs(self, starting_vertex, destination_vertex):
        """
        Return a list containing a path from
        starting_vertex to destination_vertex in
        depth-first order.
        """
        # Create stack
        s = Stack()
        # Enqueue a path to the starting vertex
        s.push([starting_vertex])
        # Create set to store visited vertices
        visited = set()
        # While stack is not empty
        while s.size() > 0:
            # Pop first PATH
            path = s.pop()
            # Grab vertex from end of the path
            v = path[-1]
            # Check if vertex is visited
            # If not visited
            if v not in visited:
                # Mark as visited
                visited.add(v)
                # Check if vertex is target
                if v == destination_vertex:
                    # If positive, return Path
                    return path
                # Push path to neighbors
                for neighbor in self.get_neighbors(v):
                    # Copy of path
                    path_c = path.copy()
                    path_c.append(neighbor)
                    # Enqueue copy
                    s.push(path_c)


    def dfs_recursive(self, starting_vertex, destination_vertex, 
    path = None, visited = None):
        """
        Return a list containing a path from
        starting_vertex to destination_vertex in
        depth-first order.

        This should be done using recursion.
        """
        # Initialize path and visited
        if path is None:
            path = []
        if visited is None:
            visited = set()

        # Check if destination vertex is in visited
        if starting_vertex not in visited:
            visited.add(starting_vertex)
            path_c = path.copy()
            path_c.append(starting_vertex)
            if starting_vertex == destination_vertex:
                return path_c
            for neighbor in self.get_neighbors(starting_vertex):
                new_path = self.dfs_recursive(neighbor, destination_vertex, 
                path_c, visited)
                if new_path is not None:
                    return new_path
        return None

if __name__ == '__main__':
    graph = Graph()  # Instantiate your graph
    # https://github.com/LambdaSchool/Graphs/blob/master/objectives/breadth-first-search/img/bfs-visit-order.png
    graph.add_vertex(1)
    graph.add_vertex(2)
    graph.add_vertex(3)
    graph.add_vertex(4)
    graph.add_vertex(5)
    graph.add_vertex(6)
    graph.add_vertex(7)
    graph.add_edge(5, 3)
    graph.add_edge(6, 3)
    graph.add_edge(7, 1)
    graph.add_edge(4, 7)
    graph.add_edge(1, 2)
    graph.add_edge(7, 6)
    graph.add_edge(2, 4)
    graph.add_edge(3, 5)
    graph.add_edge(2, 3)
    graph.add_edge(4, 6)

    '''
    Should print:
        {1: {2}, 2: {3, 4}, 3: {5}, 4: {6, 7}, 5: {3}, 6: {3}, 7: {1, 6}}
    '''
    print(graph.vertices)

    # '''
    # Valid BFT paths:
    #     1, 2, 3, 4, 5, 6, 7
    #     1, 2, 3, 4, 5, 7, 6
    #     1, 2, 3, 4, 6, 7, 5
    #     1, 2, 3, 4, 6, 5, 7
    #     1, 2, 3, 4, 7, 6, 5
    #     1, 2, 3, 4, 7, 5, 6
    #     1, 2, 4, 3, 5, 6, 7
    #     1, 2, 4, 3, 5, 7, 6
    #     1, 2, 4, 3, 6, 7, 5
    #     1, 2, 4, 3, 6, 5, 7
    #     1, 2, 4, 3, 7, 6, 5
    #     1, 2, 4, 3, 7, 5, 6
    # '''
    # graph.bft(1)

    # '''
    # Valid DFT paths:
    #     1, 2, 3, 5, 4, 6, 7
    #     1, 2, 3, 5, 4, 7, 6
    #     1, 2, 4, 7, 6, 3, 5
    #     1, 2, 4, 6, 3, 5, 7
    # '''
    # graph.dft(1)
    graph.dft_recursive(1)

    # '''
    # Valid BFS path:
    #     [1, 2, 4, 6]
    # '''
    # print(graph.bfs(1, 6))

    # '''
    # Valid DFS paths:
    #     [1, 2, 4, 6]
    #     [1, 2, 4, 7, 6]
    # '''
    # print(graph.dfs(1, 6))
    # print(graph.dfs_recursive(1, 6))
