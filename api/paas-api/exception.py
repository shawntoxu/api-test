class NodeNotFound(Exception):
    def __init__(self, node_name):
        self.node_name = node_name

class HeatException(Exception):
    pass

class BadAppTemplate(Exception):
    pass
