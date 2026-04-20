# -----------------------------
# GRAPHS (same GF + F1)
# -----------------------------
graph_GF = {
    "Entrance": ["P3"],
    "P1": ["P2", "Esc1"],
    "P2": ["P1", "P3", "P9","Esc1"],
    "P3": ["P2", "P4", "Entrance"],
    "P4": ["P3", "P5","Esc2"],
    "P5": ["P4", "P6", "Esc2"],
    "P6": ["P5", "P7","Esc2"],
    "P7": ["P6", "P8"],
    "P8": ["P7", "P9"],
    "P9": ["P8", "P10", "P2","Esc1"],
    "P10": ["P9","Esc1"],
    "Esc1": ["P1","P2","P9"],
    "Esc2": ["P5","P4","P6"],
}

graph_F1 = {
    "P1": ["P2", "P16", "P15"],
    "P2": ["P1", "P3", "P15","Esc1"],
    "P3": ["P2", "P4","Esc1"],
    "P4": ["P3", "P5"],
    "P5": ["P4", "P6","Esc2"],
    "P6": ["P5", "P7","Esc2"],
    "P7": ["P6", "P8"],
    "P8": ["P7", "P9"],
    "P9": ["P8", "P10"],
    "P10": ["P9", "P11"],
    "P11": ["P10", "P12"],
    "P12": ["P11", "P13"],
    "P13": ["P12", "P14","Esc1"],
    "P14": ["P13", "P15","Esc1"],
    "P15": ["P14", "P16", "P2", "P1","Esc1"],
    "P16": ["P15", "P1"],
    "Esc1": ["P1","P2","P3","P13","P14","P15"],
    "Esc2": ["P5","P6"],
}

graph_F2 = {
    "P1": ["P2", "P16", "P15"],
    "P2": ["P1", "P3", "P15", "Esc1"],
    "P3": ["P2", "P4", "Esc1"],
    "P4": ["P3", "P5"],
    "P5": ["P4", "P6", "Esc2"],
    "P6": ["P5", "P7", "Esc2"],
    "P7": ["P6", "P8"],
    "P8": ["P7", "P9"],
    "P9": ["P8", "P10"],
    "P10": ["P9", "P11"],
    "P11": ["P10", "P12"],
    "P12": ["P11", "P13"],
    "P13": ["P12", "P14", "Esc1"],
    "P14": ["P13", "P15", "Esc1"],
    "P15": ["P14", "P16", "P2", "P1", "Esc1"],
    "P16": ["P15", "P1"],
    "Esc1": ["P1", "P2", "P3", "P13", "P14", "P15"],
    "Esc2": ["P5", "P6"],
}

graph_F3 = {
    "P1": ["P2", "P16" ,"Esc1"],
    "P2": ["P1", "P3"],
    "P3": ["P2", "P4"],
    "P4": ["P3", "P5"],
    "P5": ["P4", "P6", "Esc2"],
    "P6": ["P5", "P7", "Esc2"],
    "P7": ["P6", "P8"],
    "P8": ["P7", "P9"],
    "P9": ["P8", "P10"],
    "P10": ["P9", "P11"],
    "P11": ["P10", "P12","Esc1"],
    "P12": ["P11", "P13"],
    "P13": ["P12", "P14"],
    "P14": ["P13", "P15"],
    "P15": ["P14", "P16"],
    "P16": ["P15", "P1", "Esc1"],

    "Esc1": ["P16","P1","P11"],
    "Esc2": ["P5", "P6"],
}


def make_bidirectional(graph):
    for node in list(graph.keys()):
        for neighbor in graph[node]:
            if neighbor not in graph:
                graph[neighbor] = []
            if node not in graph[neighbor]:
                graph[neighbor].append(node)
    return graph


graph_GF = make_bidirectional(graph_GF)
graph_F1 = make_bidirectional(graph_F1)
graph_F2 = make_bidirectional(graph_F2)
graph_F3 = make_bidirectional(graph_F3)
