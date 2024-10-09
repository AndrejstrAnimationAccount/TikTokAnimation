from manim import *
import numpy as np

# Configure the frame size (optional, can be adjusted as needed)
config.frame_height = 12  # Reduced from 16 for a smaller frame
config.frame_width = 8    # Reduced from 9 for a smaller frame
config.pixel_width = 1080
config.pixel_height = 1920

class DijkstraAnimation(Scene):
    def construct(self):
        # Define the graph vertices and edges with weights
        vertices = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
        edges_with_weights = [
            ("A", "B", 2),
            ("A", "E", 3),
            ("B", "C", 4),
            ("B", "F", 1),
            ("C", "D", 2),
            ("C", "G", 5),
            ("D", "H", 3),
            ("E", "F", 2),
            ("F", "G", 3),
            ("G", "H", 2),
            ("H", "I", 4),
            ("I", "J", 1),
            ("E", "J", 7),
            ("D", "J", 5),  # Edge with overlapping label
        ]

        # Adjusted positions for a more complex layout and scaled down
        layout = {
            "A": [0, 3, 0],
            "B": [2, 2, 0],
            "C": [4, 2, 0],
            "D": [4, 0, 0],
            "E": [-2, 2, 0],
            "F": [0, 1, 0],
            "G": [2, 1, 0],
            "H": [4, -2, 0],
            "I": [2, -2, 0],
            "J": [0, -3, 0],
        }

        # Scaling factor to make the graph smaller
        scaling_factor = 0.8  # Adjust as needed

        # Apply scaling to layout
        scaled_layout = {v: np.array(pos) * scaling_factor for v, pos in layout.items()}

        # Create the graph without edges initially
        graph = Graph(
            vertices,
            edges=[],  # No edges initially
            layout=scaled_layout,
            labels=False,  # We'll add labels manually
            vertex_config={"radius": 0.2, "fill_color": BLUE_E},  # Smaller radius
        )

        # Add credit text at the bottom left (no animation)
        credit_text = Text("Creds: Andrejstr", font_size=14, color=WHITE)
        credit_text.to_corner(DL, buff=0.2)
        self.add(credit_text)  # Add it to the scene without animation

        # Add title text at the top
        title_text = VGroup(
            Text("Dijkstra's", font_size=40, color=WHITE),
            Text("Algorithm", font_size=40, color=WHITE)
        ).arrange(DOWN, buff=0.05)
        title_text.to_edge(UP, buff=0.3)

        # Add text above the graph
        graph_title = Text("Graph", font_size=24, color=WHITE)
        graph_title.next_to(title_text, DOWN, buff=0.2)

        # Position the graph below the graph_title
        graph.next_to(graph_title, DOWN, buff=0.3)

        # Animate writing the titles
        self.play(Write(title_text), run_time=1.5)
        self.wait(0.3)
        self.play(Write(graph_title), run_time=1)
        self.wait(0.3)

        # Create node labels integrated within nodes
        node_groups = {}
        for v in vertices:
            # Create node circle
            node = graph.vertices[v]
            node.set_z_index(2)  # Nodes above edges

            # Create label and position it at the center of the node
            label = Text(v, font_size=16, color=WHITE)
            label.move_to(node.get_center())
            label.set_z_index(3)  # Labels above nodes

            # Group node and label
            node_group = VGroup(node, label)
            node_groups[v] = node_group

        # Animate the nodes and labels appearing sequentially
        node_animations = []
        for v in vertices:
            node_group = node_groups[v]
            node_anim = GrowFromCenter(node_group, run_time=0.3)
            node_animations.append(node_anim)

        self.play(
            LaggedStart(
                *node_animations,
                lag_ratio=0.1,
            )
        )
        self.wait(0.5)

        # Create edge lines and weight labels with precise positioning
        edge_animations = []
        edge_weight_labels = []
        edge_dict = {}
        for start, end, weight in edges_with_weights:
            start_point = graph.vertices[start].get_center()
            end_point = graph.vertices[end].get_center()

            # Create edge line
            edge_line = Line(start_point, end_point, stroke_color=GRAY).set_z_index(0)
            edge_dict[(start, end)] = edge_line  # Keep track of edges

            # Calculate midpoint
            midpoint = (start_point + end_point) / 2

            # Calculate the perpendicular unit vector
            direction = end_point - start_point
            if np.linalg.norm(direction) == 0:
                # Avoid division by zero
                perpendicular = np.array([0, 1, 0])
            else:
                perpendicular = np.array([-direction[1], direction[0], 0])
                perpendicular /= np.linalg.norm(perpendicular)

            # Set offset distance
            offset_distance = 0.3  # Adjust as needed for clarity

            # Calculate label position (horizontally aligned)
            label_position = midpoint + perpendicular * offset_distance

            # Create edge weight label
            label = Text(str(weight), font_size=14, color=WHITE).set_z_index(1)
            label.move_to(label_position)  # Precisely place the label at the offset midpoint

            # Ensure label is horizontally aligned (no rotation)
            # No rotation applied to keep labels straight

            # Special handling for specific edges to prevent overlap
            if (start, end) in [("B", "E"), ("C", "F"), ("A", "E"), ("F", "G"),("B", "F"), ("D", "J")]:
                # Manually adjust label position for these edges
                # For edge D-J, move the label higher
                if (start, end) == ("A", "E") or (end, start) == ("A", "E"):
                    label_position = midpoint + perpendicular * (offset_distance - 0.5)
                    label.move_to(label_position)
                elif (start, end) == ("F", "G") or (end, start) == ("F", "G"):
                    label_position = midpoint + perpendicular * (offset_distance - 0.1)
                    label.move_to(label_position)
                elif (start, end) == ("B", "F") or (end, start) == ("B", "F"):
                    label_position = midpoint + perpendicular * (offset_distance - 0.5)
                    label.move_to(label_position)
                elif (start, end) == ("D", "J") or (end, start) == ("D", "J"):
                    # For edge D-J, move the label higher
                    label_position = midpoint + perpendicular * (offset_distance - 0.6)
                    label.move_to(label_position)
                else:
                    label.move_to(label_position + perpendicular * 0.08)  # Further offset for other edges

            edge_weight_labels.append(label)

            # Animate edge appearance using Create for smooth animation
            edge_anim = Create(edge_line, run_time=0.5, rate_func=linear)
            edge_animations.append(edge_anim)

        # Animate edges appearing in a smooth 3Blue1Brown style
        self.play(
            LaggedStart(
                *edge_animations,
                lag_ratio=0.05,
            )
        )
        self.wait(0.3)

        # Animate edge weight labels appearing after edges
        label_animations = []
        for label in edge_weight_labels:
            label_animations.append(FadeIn(label, run_time=0.3))
        self.play(
            LaggedStart(
                *label_animations,
                lag_ratio=0.05,
            )
        )
        self.wait(0.5)

        # Specify start and end points
        start_vertex = "A"
        end_vertex = "J"

        # Highlight the start and end vertices
        node_groups[start_vertex].submobjects[0].set_fill(color=GREEN, opacity=1)
        node_groups[end_vertex].submobjects[0].set_fill(color=RED, opacity=1)

        # Initialize distances and predecessors
        distances = {v: float('inf') for v in vertices}
        predecessors = {v: None for v in vertices}
        distances[start_vertex] = 0
        unvisited = set(vertices)

        # Create an array to display distances in two rows
        array_mobject = self.create_distance_array(vertices, distances, rows=2, cols=5)
        array_mobject.scale(0.9)  # Make the boxes bigger
        array_mobject.next_to(graph, DOWN, buff=0.8)  # Move it further below

        # Animate the array with smooth transitions
        self.play(
            LaggedStart(
                *[Create(group) for group in array_mobject],
                lag_ratio=0.09,
                run_time= 3,
                rate_func=smooth
            )
        )
        self.wait(0.3)

        # Dijkstra's algorithm visualization
        while unvisited:
            # Find the unvisited node with the smallest distance
            current_vertex = min(unvisited, key=lambda vertex: distances[vertex])
            if distances[current_vertex] == float('inf'):
                break
            unvisited.remove(current_vertex)

            # Highlight current vertex
            self.play(node_groups[current_vertex].submobjects[0].animate.set_fill(color=YELLOW, opacity=1), run_time=0.5)
            self.wait(0.2)

            # For all neighbors of the current vertex
            for u, v, weight in edges_with_weights:
                if u == current_vertex and v in unvisited:
                    neighbor = v
                elif v == current_vertex and u in unvisited:
                    neighbor = u
                else:
                    continue

                new_distance = distances[current_vertex] + weight
                if new_distance < distances[neighbor]:
                    distances[neighbor] = new_distance
                    predecessors[neighbor] = current_vertex

                    # Highlight the edge and update distance
                    edge_to_highlight = (current_vertex, neighbor) if (current_vertex, neighbor) in edge_dict else (neighbor, current_vertex)
                    edge = edge_dict[edge_to_highlight]
                    self.play(edge.animate.set_color(ORANGE), run_time=0.3)
                    self.wait(0.2)

                    # Update the array
                    self.update_distance_array(array_mobject, vertices, distances)
                    self.wait(0.2)

                    # Reset edge color
                    self.play(edge.animate.set_color(GRAY), run_time=0.3)

            # Mark current vertex as visited
            self.play(node_groups[current_vertex].submobjects[0].animate.set_fill(color=GREEN, opacity=1), run_time=0.5)
            self.wait(0.2)

            # Stop if we reached the end vertex
            if current_vertex == end_vertex:
                break

        # Reconstruct and highlight the shortest path
        path = self.reconstruct_path(predecessors, start_vertex, end_vertex)
        if path:
            # Display "Shortest Path" text on the right
            shortest_path_title = Text("Shortest Path", font_size=20, color=WHITE)
            shortest_path_title.to_corner(DR, buff=0.3)
            self.play(Write(shortest_path_title), run_time=1)
            self.wait(0.2)

            # Display the path sequence
            path_sequence = " ➔ ".join(path)
            path_text = Text(path_sequence, font_size=16, color=YELLOW)
            path_text.next_to(shortest_path_title, DOWN, buff=0.1)
            self.play(Write(path_text), run_time=1)
            self.wait(0.3)

            # Highlight the path edges
            path_edges = []
            for i in range(len(path)-1):
                edge_tuple = (path[i], path[i+1])
                if edge_tuple in edge_dict:
                    path_edges.append(edge_dict[edge_tuple])
                else:
                    path_edges.append(edge_dict[(path[i+1], path[i])])

            # Animate path edges
            for edge in path_edges:
                self.play(edge.animate.set_color(BLUE), run_time=0.3)
                self.wait(0.1)

            # Emphasize the path by increasing stroke width
            self.play(
                *[edge.animate.set_stroke(width=4) for edge in path_edges],
                run_time=1,
                rate_func=smooth
            )
        else:
            # If no path is found
            no_path_text = Text(f"No path from {start_vertex} to {end_vertex}", font_size=20, color=RED)
            no_path_text.to_edge(UP, buff=0.2)
            self.play(Write(no_path_text), run_time=1)
            self.wait(1)

        self.wait(2)

    def create_distance_array(self, vertices, distances, rows=2, cols=5):
        # Create a visual array to display distances in specified rows and columns
        array = VGroup()
        for i, v in enumerate(vertices):
            # Rectangle background for each vertex
            rect = Rectangle(width=1.5, height=1, stroke_color=WHITE, fill_color=BLACK, fill_opacity=0.2)

            # Vertex label
            label = Text(v, font_size=26, color=WHITE).move_to(rect.get_top()).shift(DOWN*0.3)

            # Distance value
            distance_value = distances[v] if distances[v] != float('inf') else "∞"
            distance = Text(str(distance_value), font_size=26, color=WHITE).move_to(rect.get_bottom()).shift(UP*0.3)

            # Group them
            group = VGroup(rect, label, distance)
            array.add(group)

        # Arrange the array into specified rows and columns
        array.arrange_in_grid(rows=rows, cols=cols, buff=0.3)
        return array

    def update_distance_array(self, array_mobject, vertices, distances):
        # Update the distance array with new distances
        for i, v in enumerate(vertices):
            distance_value = distances[v] if distances[v] != float('inf') else "∞"
            new_distance = Text(str(distance_value), font_size=26, color=WHITE).move_to(array_mobject[i][2].get_center())
            self.play(Transform(array_mobject[i][2], new_distance), run_time=0.2)

    def reconstruct_path(self, predecessors, start, end):
        # Reconstruct the shortest path from start to end using predecessors
        path = []
        current = end
        while current != start:
            if predecessors[current] is None:
                return None  # No path found
            path.append(current)
            current = predecessors[current]
        path.append(start)
        path.reverse()
        return path
