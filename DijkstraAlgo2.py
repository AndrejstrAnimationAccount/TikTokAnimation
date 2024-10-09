from manim import *
import numpy as np

# Configure the frame size (optional, can be adjusted as needed)
config.frame_height = 16
config.frame_width = 9
config.pixel_width = 1080
config.pixel_height = 1920

class DijkstraAnimation(Scene):
    def construct(self):
        # Define the graph vertices and edges with weights
        vertices = ["A", "B", "C", "D", "E", "F"]
        edges_with_weights = [
            ("A", "B", 2),
            ("A", "E", 1),
            ("B", "C", 2),
            ("B", "E", 3),
            ("C", "D", 1),
            ("C", "F", 4),
            ("D", "F", 1),
            ("E", "F", 5),
        ]

        # Adjusted positions for vertical layout
        layout = {
            "A": [0, 4, 0],
            "B": [2.5, 1.5, 0],
            "C": [2.5, -1, 0],
            "D": [0, -4, 0],
            "E": [-2.5, 1.5, 0],
            "F": [-2.5, -1, 0],
        }

        # Create the graph without edges initially
        graph = Graph(
            vertices,
            edges=[],  # No edges initially
            layout=layout,
            labels=False,  # We'll add labels manually
            vertex_config={"radius": 0.3, "fill_color": BLUE_E},
        )

        # Add credit text at the bottom left (no animation)
        credit_text = Text("Creds: Andrejstr", font_size=14, color=WHITE)
        credit_text.to_corner(DL, buff=0.2)
        self.add(credit_text)  # Add it to the scene without animation

        # Add title text at the top
        title_text = VGroup(
            Text("Dijkstra's", font_size=60, color=WHITE),
            Text("Algorithm", font_size=60, color=WHITE)
        ).arrange(DOWN, buff=0.1)
        title_text.to_edge(UP, buff=0.5)

        # Add text above the graph
        graph_title = Text("Graph", font_size=40, color=WHITE)
        graph_title.next_to(title_text, DOWN, buff=0.3)

        # Position the graph below the graph_title
        graph.next_to(graph_title, DOWN, buff=0.5)

        # Animate writing the titles
        self.play(Write(title_text), run_time=2)
        self.wait(0.5)
        self.play(Write(graph_title), run_time=1)
        self.wait(0.5)

        # Create node labels integrated within nodes
        node_groups = {}
        for v in vertices:
            # Create node circle
            node = graph.vertices[v]
            node.set_z_index(2)  # Nodes above edges

            # Create label and position it at the center of the node
            label = Text(v, font_size=24, color=WHITE)
            label.move_to(node.get_center())
            label.set_z_index(3)  # Labels above nodes

            # Group node and label
            node_group = VGroup(node, label)
            node_groups[v] = node_group

        # Animate the nodes and labels appearing sequentially
        node_animations = []
        for v in vertices:
            node_group = node_groups[v]
            node_anim = GrowFromCenter(node_group, run_time=0.5)
            node_animations.append(node_anim)

        self.play(
            LaggedStart(
                *node_animations,
                lag_ratio=0.2,
            )
        )
        self.wait(1)

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
            offset_distance = 0.4  # Adjust as needed for clarity

            # Calculate label position (horizontally aligned)
            label_position = midpoint + perpendicular * offset_distance

            # Create edge weight label
            label = Text(str(weight), font_size=24, color=WHITE).set_z_index(1)
            label.move_to(label_position)  # Precisely place the label at the offset midpoint

            # Ensure label is horizontally aligned (no rotation)
            # Remove any rotation to keep labels straight
            # label.rotate(angle + PI / 2)  # This line is removed to keep labels horizontal

            # Optional: Reduce font size slightly if overlapping persists
            # label.scale(0.9)

            # Special handling for specific edges to prevent overlap
            if (start, end) in [("B", "E"), ("C", "F")]:
                # Manually adjust label position for these edges
                label.move_to(label_position + perpendicular * 0.1)  # Further offset

            edge_weight_labels.append(label)

            # Animate edge appearance using Create for smooth animation
            edge_anim = Create(edge_line, run_time=1, rate_func=smooth)
            edge_animations.append(edge_anim)

        # Animate edges appearing in a smooth 3Blue1Brown style
        self.play(
            LaggedStart(
                *edge_animations,
                lag_ratio=0.1,
            )
        )
        self.wait(0.5)

        # Animate edge weight labels appearing after edges
        self.play(
            LaggedStart(
                *[FadeIn(label, run_time=0.5) for label in edge_weight_labels],
                lag_ratio=0.1,
            )
        )
        self.wait(1)

        # Specify start and end points
        start_vertex = "A"
        end_vertex = "D"

        # Highlight the start and end vertices
        node_groups[start_vertex].submobjects[0].set_fill(color=GREEN, opacity=1)
        node_groups[end_vertex].submobjects[0].set_fill(color=RED, opacity=1)

        # Initialize distances
        distances = {v: float('inf') for v in vertices}
        distances[start_vertex] = 0
        unvisited = set(vertices)

        # Create an array to display distances
        array_mobject = self.create_distance_array(vertices, distances)
        array_mobject.scale(0.8)
        array_mobject.next_to(graph, DOWN, buff=0.5)

        # Animate the array with smooth transitions
        self.play(
            LaggedStart(
                *[Create(group) for group in array_mobject],
                lag_ratio=0.1,
                run_time=3,
                rate_func=smooth
            )
        )
        self.wait(1)

        # Dijkstra's algorithm visualization
        while unvisited:
            # Find the unvisited node with the smallest distance
            current_vertex = min(unvisited, key=lambda vertex: distances[vertex])
            if distances[current_vertex] == float('inf'):
                break
            unvisited.remove(current_vertex)

            # Highlight current vertex
            node_groups[current_vertex].submobjects[0].set_fill(color=YELLOW, opacity=1)
            self.wait(0.5)

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

                    # Highlight the edge and update distance
                    edge_to_highlight = (current_vertex, neighbor) if (current_vertex, neighbor) in edge_dict else (neighbor, current_vertex)
                    edge = edge_dict[edge_to_highlight]
                    self.play(
                        edge.animate.set_color(ORANGE),
                        run_time=1,
                        rate_func=smooth
                    )
                    self.wait(0.5)

                    # Update the array
                    self.update_distance_array(array_mobject, vertices, distances)
                    self.wait(0.5)

                    # Reset edge color
                    self.play(edge.animate.set_color(GRAY), run_time=0.5)

            # Mark current vertex as visited
            node_groups[current_vertex].submobjects[0].set_fill(color=GREEN, opacity=1)
            self.wait(0.5)

            # Stop if we reached the end vertex
            if current_vertex == end_vertex:
                break

        # Reconstruct and highlight the shortest path
        path = self.reconstruct_path(start_vertex, end_vertex, distances, edges_with_weights)
        if path:
            # Display "Shortest Path" text on the right
            shortest_path_title = Text("Shortest Path", font_size=30, color=WHITE)
            shortest_path_title.to_corner(DR, buff=1)
            self.play(Write(shortest_path_title), run_time=2)
            self.wait(1)

            # Display the path sequence
            path_sequence = [start_vertex] + [end for _, end in path]
            path_text = Text(" ➔ ".join(path_sequence), font_size=24, color=YELLOW)
            path_text.next_to(shortest_path_title, DOWN, buff=0.3)
            self.play(Write(path_text), run_time=2)
            self.wait(1)

            for start, end in path:
                edge_to_highlight = (start, end) if (start, end) in edge_dict else (end, start)
                edge = edge_dict[edge_to_highlight]
                self.play(
                    edge.animate.set_color(BLUE),
                    run_time=1.5,
                    rate_func=smooth
                )
                self.wait(0.5)
            # Emphasize the path
            self.play(
                *[edge_dict[(start, end) if (start, end) in edge_dict else (end, start)].animate.set_stroke(width=6) for start, end in path],
                run_time=2,
                rate_func=smooth
            )
        else:
            # If no path is found
            no_path_text = Text(f"No path from {start_vertex} to {end_vertex}", font_size=36, color=RED)
            no_path_text.to_edge(UP)
            self.play(Write(no_path_text), run_time=2)
            self.wait(2)

        self.wait(2)

    def create_distance_array(self, vertices, distances):
        array = VGroup()
        for i, v in enumerate(vertices):
            rect = Rectangle(width=1.2, height=1.2, stroke_color=WHITE)
            label = Text(v, font_size=24, color=WHITE).set_z_index(3)
            distance_value = distances[v] if distances[v] != float('inf') else "∞"
            distance = Text(str(distance_value), font_size=24, color=WHITE).set_z_index(3)
            # Increased buff for better spacing between letter and number
            column = VGroup(label, distance).arrange(DOWN, buff=0.3)
            group = VGroup(rect, column)
            array.add(group)
        array.arrange(RIGHT, buff=0.5)
        return array

    def update_distance_array(self, array_mobject, vertices, distances):
        for i, v in enumerate(vertices):
            distance_value = distances[v] if distances[v] != float('inf') else "∞"
            distance_text = Text(str(distance_value), font_size=24, color=WHITE).set_z_index(3)
            distance_text.move_to(array_mobject[i][1][1])
            self.play(Transform(array_mobject[i][1][1], distance_text), run_time=0.5)

    def reconstruct_path(self, start_vertex, end_vertex, distances, edges_with_weights):
        # Create a graph representation for traversal
        graph_dict = {v: [] for v in distances.keys()}
        for u, v, w in edges_with_weights:
            graph_dict[u].append((v, w))
            graph_dict[v].append((u, w))

        # Backtrack from end_vertex to start_vertex
        path = []
        current = end_vertex
        while current != start_vertex:
            found = False
            for neighbor, weight in graph_dict[current]:
                if distances.get(neighbor, float('inf')) + weight == distances[current]:
                    path.append((neighbor, current))
                    current = neighbor
                    found = True
                    break
            if not found:
                return None  # No path found
        path.reverse()
        return path
