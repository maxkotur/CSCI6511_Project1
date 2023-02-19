from queue import PriorityQueue
import copy


class Bucket:
    def __init__(self, size, target):
        self.size = size
        self.filled = 0
        self.target = target

    def drain(self):
        if self.filled == 0:
            return False

        self.filled = 0
        return True

    def fill(self):
        if self.filled == self.size:
            return False

        self.filled = self.size
        return True

    def pour(self, other_bucket):
        if self.size < other_bucket.size:
            return False, other_bucket.filled
        unit_to_full = other_bucket.size - other_bucket.filled

        if self.filled == 0:
            return False, other_bucket.filled
        elif unit_to_full == 0:
            return False, other_bucket.filled
        else:
            if unit_to_full >= self.filled:
                other_bucket.filled = other_bucket.filled + self.filled
                self.filled = 0
            elif unit_to_full < self.filled:
                other_bucket.filled = other_bucket.size
                self.filled = self.filled - unit_to_full
            return True, other_bucket

    def pour_capacitor(self, cap):
        if self.filled == 0:
            return -1
        elif cap + self.filled > self.target:
            return -1
        cap = cap + self.filled
        self.filled = 0
        return cap


class Node:
    def __init__(self, bucket_array, children, parent_node, state_capacitor, target):
        self.bucket_array = bucket_array
        self.children = children
        self.parent_node = parent_node
        self.state_capacitor = state_capacitor
        self.heuristic = float('inf')
        self.target = target
        self.consec_pours = 0

    def update_heuristic(self, cost):
        self.heuristic = cost

    def update_consec_pours(self, cost):
        self.consec_pours = cost

    def update_state_capacitor(self, cost):
        self.state_capacitor = cost

    def __gt__(self, other):
        if isinstance(other, Node):
            if self.heuristic > other.heuristic:
                return True
            if self.heuristic < other.heuristic:
                return False
            return self.state_capacitor > other.state_capacitor

    def perform_action_and_return_buckets(self, bucket_array, selected_index, action, target_index, cap):
        action_performed = False
        temp_bucket_array = copy.deepcopy(bucket_array)

        if target_index is None:
            if action == "Fill":
                action_performed = temp_bucket_array[selected_index].fill()

            elif action == "Drain":
                action_performed = temp_bucket_array[selected_index].drain()

            elif action == "Capacitor":
                action_performed = temp_bucket_array[selected_index].pour_capacitor(cap)
        else:
            if action == "Pour":
                action_performed, other = temp_bucket_array[selected_index].pour(
                    other_bucket=temp_bucket_array[target_index])
                if action_performed:
                    temp_bucket_array[target_index] = Bucket(size=other.size, target=self.target)
                    temp_bucket_array[target_index].filled = other.filled

        return temp_bucket_array, action_performed

    def get_children(self, node):
        children = []
        bucket_array = node.bucket_array
        # print("Start of get children")
        # for bucket in bucket_array:
        #     print(f"bucket: {bucket.filled}")

        max_bucket = bucket_array[len(bucket_array) - 1].size
        if max_bucket < self.target - node.state_capacitor:
            new_bucket_array, action = node.perform_action_and_return_buckets(bucket_array, len(bucket_array) - 1,
                                                                              "Fill", None, 0)
            if action:
                # print("Fill")
                children.append(self.create_Node(node, new_bucket_array, node.state_capacitor))
            new_bucket_array, action = node.perform_action_and_return_buckets(bucket_array, len(bucket_array) - 1,
                                                                              "Capacitor", None,
                                                                              node.state_capacitor)
            if action != -1:
                # print("Cap")
                children.append(self.create_Node(node, new_bucket_array, action))
            return children

        for i, bucket in enumerate(bucket_array):

            new_bucket_array, action = node.perform_action_and_return_buckets(bucket_array, i, "Fill", None, 0)
            if action:
                # print("Fill")
                children.append(self.create_Node(node, new_bucket_array, node.state_capacitor))

            new_bucket_array, action = node.perform_action_and_return_buckets(bucket_array, i, "Drain", None, 0)
            if action:
                # print("Drain")
                children.append(self.create_Node(node, new_bucket_array, node.state_capacitor))

            new_bucket_array, action = node.perform_action_and_return_buckets(bucket_array, i, "Capacitor", None,
                                                                              node.state_capacitor)
            if action != -1:
                # print("Cap")
                children.append(self.create_Node(node, new_bucket_array, action))

            if len(bucket_array) > 1:
                rem_size = bucket_array[-1].size - bucket_array[-2].size - 2
                if (rem_size <= self.target - node.state_capacitor) or (len(bucket_array) < 4):
                    # print(f"Size: {rem_size} and State to targ: {self.target - node.state_capacitor}")
                    for j, bucket_j in enumerate(bucket_array):
                        if i <= j:
                            break
                        new_bucket_array, action = node.perform_action_and_return_buckets(bucket_array, i, "Pour", j, 0)
                        if action:
                            # print("Pour")
                            children.append(self.create_Node(node, new_bucket_array, node.state_capacitor))
                            cost = node.consec_pours
                            if cost < len(bucket_array):
                                children[-1].update_consec_pours(cost + 1)
                            else:
                                children.pop()
        return children

    def create_Node(self, parent_node, bucket_array, state_capacitor):
        # for bucket in bucket_array:
        #     print(f"bucket: {bucket.filled}")
        node = Node(bucket_array=bucket_array, children=[], parent_node=parent_node, state_capacitor=state_capacitor, target=self.target)
        return node


class Player:

    # def __init__(self):

    def run(self, problem):
        # this function should return the path and the search_tree
        bucket_array = []

        i = 0
        while i < len(problem["size"]):
            bucket = Bucket(size=problem["size"][i], target=problem["target"])
            bucket_array.append(bucket)
            i = i + 1

        # Instantiate the root of the node
        parent_node = Node(bucket_array=bucket_array, children=[], parent_node=None, state_capacitor=0, target=problem["target"])

        # Goal test in case initial state is the goal
        if problem['target'] == 0:
            return 0

        steps = self.informed_search(node=parent_node, problem=problem)
        return steps

    def check_Visited(self, neighbour, visited):
        for node in visited:
            if neighbour.state_capacitor == node.state_capacitor:
                neigh_buckets = neighbour.bucket_array
                visit = True
                for i, bucket in enumerate(node.bucket_array):
                    # print(f"{bucket.filled} and {neigh_buckets[i].filled}")
                    if bucket.filled != neigh_buckets[i].filled:
                        visit = False
                if visit:
                    return True
        return False

    def construct_graph(self, node, target):
        visited = []  # List for visited nodes.
        queue = []  # Initialize a queue
        visited.append(node)
        queue.append(node)
        goal = False

        while queue:  # Creating loop to visit each node
            m = queue.pop(0)
            children = m.get_children(m)
            m.children = children

            for neighbour in children:
                if not self.check_Visited(neighbour, visited):
                    visited.append(neighbour)
                    queue.append(neighbour)

            # print(f"Cap level: {m.state_capacitor}")
            if m.state_capacitor == target:
                goal = True
                return goal, visited

        return goal, visited

    def compare_Nodes(self, node_A, node_B):
        if node_A.state_capacitor == node_B.state_capacitor:
            neigh_buckets = node_A.bucket_array
            for i, bucket in enumerate(node_B.bucket_array):
                if bucket.filled != neigh_buckets[i].filled:
                    return False
            return True
        return False

    def apply_heuristic(self, start_node, end_node):
        end_node.update_heuristic(0)
        cost = 1
        node = end_node
        while not self.compare_Nodes(node, start_node):
            node = node.parent_node
            node.update_heuristic(cost)
            for child in node.children:
                if child.heuristic == float('inf'):
                    child.update_heuristic(cost)
                cost += 1
        return start_node

    def a_star(self, start, goal_state):
        # Create a priority queue to store the nodes to be explored
        pq = PriorityQueue()
        pq.put((0, start))
        visited = []

        while not pq.empty():
            # Get the node with the lowest cost
            cost, current_node = pq.get()

            # Check if we have reached the goal state
            if current_node.state_capacitor == goal_state.state_capacitor:
                return current_node

            # Mark the node as visited
            visited.append(current_node)

            # Add the children of the current node to the priority queue
            for child in current_node.children:
                if not self.check_Visited(child, visited):
                    pq.put((child.heuristic + 1, child))

        return -1

    def informed_search(self, node, problem):

        goal, visited = self.construct_graph(node, problem["target"])

        if not goal:
            return -1

        start_node = visited[0]
        end_node = visited[len(visited) - 1]
        self.apply_heuristic(start_node, end_node)
        end_node = self.a_star(start_node, end_node)
        path = []
        while not self.compare_Nodes(start_node, end_node):
            bucket_array = end_node.bucket_array
            buckets = []
            for bucket in bucket_array:
                buckets.append(bucket.filled)
            buckets.append(end_node.state_capacitor)
            path.append(buckets)
            end_node = end_node.parent_node
        path.reverse()
        i = 0
        for p in path:
            i += 1
            print(f"Step {i}")
            print(p)
        steps = len(path)
        return steps


if __name__ == '__main__':
    f = open("test_cases", "r")
    string = f.readline()
    targ = f.readline()
    targ = int(targ)
    li = list(string.split(","))
    li = [int(i) for i in li]
    li.sort()
    problem = {
        "size": li,
        "target": targ
    }
    player = Player()
    steps = player.run(problem)
    print(f"Min number of steps are: {steps}")
