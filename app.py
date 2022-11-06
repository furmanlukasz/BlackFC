import streamlit as st
import streamlit.components.v1 as components
from graph_utils import get_graph
from streamlit_agraph import agraph, Node, Edge, Config
import networkx as nx

st.set_page_config(layout="wide")
st.title("Black Friday Sales Cookie3 DataLab")
st.markdown("Demo for graph query for Black Friday Sales Data 2019")

sidebar = st.sidebar


def compute_graph():
    graph = get_graph(st.session_state.degree)
    nx.write_gpickle(graph, "test.gpickle")


degree = sidebar.slider('Minimum number of interactions', 2, 20, 10, on_change=compute_graph, key='degree')

categories = ['Exchanges', 'Marketplaces',
              'Finance', 'Games',
              'Gambling', 'Governance',
              'Development', 'Social',
              'Storage', 'High risk',
              'Security', 'Wallet',
              'Identity', 'Property',
              'Media', 'Insurance',
              'Energy']

options = st.multiselect('Select categories:', categories, ['Exchanges', 'Marketplaces',
                                                            'Finance', 'Games',
                                                            'Gambling'])

G = nx.read_gpickle("test.gpickle")

for node,edge in zip(G.nodes(), G.edges()):
    # G.nodes[node]['hidden'] = True
    # if node == G.nodes[node]:
    #     G.nodes[node]['hidden'] = False
    # if edge[0] == node:
    #     G.nodes[node]['hidden'] = False
    try:
        # print(G.nodes[node]['category'])
        if G.nodes[node]['category'] in options:
            G.nodes[node]['hidden'] = False
    except:
        pass

# print(G.nodes(data=True))
nodes = [Node(id=i[0], label=i[0], **i[1]) for i in G.nodes(data=True)]

edges = [Edge(source=i, target=j, color=color, dashes=True, smooth=True, width=5) for (i, j, color) in G.edges(data=True)] #, type="CURVE_SMOOTH"

# for node in nodes:
#     print(node)
    # if node['category'] not in options:
    #     node['hidden'] = True

config = Config(width='100%',
                height=800,
                directed=True,
                nodeHighlightBehavior=True,
                highlightColor="#f700ff",
                collapsible=True,
                node={'labelProperty': 'label'},
                link={'labelProperty': 'label', 'renderLabel': True},
                layout={"hierarchical":False},
                physics={"enabled":True, "stabilization":False,
                         "forceAtlas2Based":{"theta":0.5, "gravitationalConstant":-50.0, "centralGravity":0.01, "springLength":100, "springConstant":0.08, "damping":0.4, "avoidOverlap":0},
                         "solver":"forceAtlas2Based"}, #"iterations":10000,

                )

return_value = agraph(nodes=nodes,
                      edges=edges,
                      config=config)

print(return_value)
sidebar.info("Click on a node to see its details: {}".format(return_value))
