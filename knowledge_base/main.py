import sys 
from rdflib import Graph, URIRef, RDF, BNode

# Load the RDF data from the file
facts_graph = Graph()
file_path = sys.argv[1]
facts_graph.parse(file_path, format="turtle")

rules_graph = Graph()
file_path = sys.argv[2]
rules_graph.parse(file_path, format="turtle")


class NewRule:
    name = ""
    relationships = {}
    select = ("", "")

    def __init__(self):
        self.relationships = {}
        self.select = ("", "")
    
    def __str__(self):
        where_statements = []
        for relationship in self.relationships:
            for var in self.relationships[relationship]["vars"]:
                where_statements.append(f"{var[0]} {self.relationships[relationship]['relationship']} {var[1]} .")
        
        where_statements = " \n".join(where_statements)

        return f"PREFIX relationship: <relationship:>\nSELECT {self.select[0]} {self.select[1]} \nWHERE {{ {where_statements} }}"
 



def parse_rules(rules_graph, facts_graph):
    # init new rules
    new_rules = {}
    bnodes = {}
    for s, p, o in rules_graph:

        if isinstance(o, BNode):
            new_rules[s] = NewRule()
            new_rules[s].name = s.split(":")[1]
            bnodes[o] = new_rules[s]

            new_rules[s].relationships[o] = {
                "relationship": p,
                "vars": []
            }

    # update new rules
    for s, p, o in rules_graph:

        if isinstance(s, BNode):
            bnodes[s].relationships[s]["vars"].append(("?"+p.split(":")[1], "?"+o.split(":")[1]))
        
        if not(isinstance(o, BNode) or isinstance(s, BNode)):
            new_rules[s].select = ("?"+p.split(":")[1], "?"+o.split(":")[1])
            
        

    # apply new rules
    for x in new_rules:
        for r in facts_graph.query(str(new_rules[x])):
            facts_graph.add((r[0], URIRef(f"relationship:{new_rules[x].name}") ,r[1]))




parse_rules(rules_graph, facts_graph)



while True:
    line = input()

    if line == 'exit':
        break
    elif line == '':
        continue
    else:
        q = f"""
        PREFIX family: <family:>
        PREFIX relationship: <relationship:> 

        SELECT ?p1 ?p2
        WHERE {{
        ?p1 relationship:{line} ?p2 .
        }}
        """

        res = facts_graph.query(q)
        if len(res) == 0:
            print("There is no true statements")
        else:
            for r in facts_graph.query(q):
                print("\t", r[0], " -> ", r[1])

