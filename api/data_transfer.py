import json

def initialize_matrix(matrix):
    nodes = []
    edges = []
    n = matrix.shape
    print(matrix.shape[0])
    for i in range(matrix.shape[0]):
        id_entry = {"id" : i}
        nodes.append({"data" : id_entry})
        for j in range(matrix.shape[1]):
            if matrix[i][j] == 1:
                edge_entry = {}
                edge_entry["id"] = str(i) + str(j)
                edge_entry["source"] = str(i)
                edge_entry["target"] = str(j)
                edges.append({"data" : edge_entry})
    return json.dumps(nodes), json.dumps(edges)


"""
If the value is 1, then the color will be changed to red. If the value is -1, the color will be changed to blue
"""
def send_data_for_tick(matrix):
    new_path = []
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            if matrix[i][j] == 1:
                key = str(i) + str(j)
                new_path.append({key : "red"})
            elif matrix[i][j] == -1:
                key = str(i) + str(j)
                new_path.append([key, "blue"])
    return json.dumps(new_path)

def process_list_tick_matrices(list):
    all_paths = [send_data_for_tick(matrix) for matrix in list]
    return json.dumps(all_paths)

def send_node_change_data(nodes):
    node_colors = []
    for node in nodes:
        if node == 1:
            node_colors.append("red")
        elif node == 1:
            node_colors.append("blue")
        else:
            node_colors.append("black")
    return node_colors
