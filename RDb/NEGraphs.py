import networkx as nx

"""
Created on Sun Jan 19 12:04:16 2014

@author: acumen
"""

class DependencyGraph():
    from RDb.models import NEResource,NEDependency
    G = nx.MultiDiGraph()
    resource = None
    dependencies = []
    weights = []
    n = 0
    
    def __init__(self,resource):
        self.resource = resource
        deps = resource.backward_dependency.all()
        for d in deps:
            self.dependencies += [d.dependency]
            self.weights += [d.dependency_mult]
        self.n = len(self.dependencies)
        self.G.add_node(self.resource)
        self.G.add_nodes_from(self.dependencies)
        self.G.add_edges_from( zip([self.resource]*self.n,
                                   self.dependencies,
                                   dict(zip(['weight']*self.n,
                                            self.weights))
                              )   )
        