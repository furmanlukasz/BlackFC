import streamlit as st
import streamlit.components.v1 as components
from graph_utils import get_graph, get_data, word_cloud
from streamlit_agraph import agraph, Node, Edge, Config
import networkx as nx
import matplotlib.pyplot as plt
plt.rcParams.update({'text.color': "red",
                     'axes.labelcolor': "red"})

st.set_page_config(layout="wide")
st.title("Black Friday Sales Cookie3 DataLab")
st.markdown("Demo for graph query for Black Friday Sales Data 2019")

sidebar = st.sidebar

data, dapps = get_data()

def compute_graph():

    graph = get_graph(data, st.session_state.degree)
    nx.write_gpickle(graph, "test.gpickle")

# ______________________________________________________________________________________________________________________
# Slider

degree = sidebar.slider('Minimum number of interactions (higher value will show most active daaps and users)', 2, 20, 3, on_change=compute_graph, key='degree')


# ______________________________________________________________________________________________________________________
# Checkbox categories

categories = ['Exchanges', 'Marketplaces',
              'Finance', 'Games',
              'Gambling', 'Governance',
              'Development', 'Social',
              'Storage', 'High risk',
              'Security', 'Wallet',
              'Identity', 'Property',
              'Media', 'Insurance',
              'Energy']

options = sidebar.multiselect('Select categories:', categories, categories)

# ______________________________________________________________________________________________________________________
# Categories Pie Chart

fig, ax = plt.subplots(1,1,figsize=[8,8],frameon=False)
# ax = fig.add_subplot(111)
# ax = dapps[dapps['platform'] == 'Ethereum']['category'].value_counts().plot(kind='pie',  figsize=(8, 8), fontsize=16)

dapps[(dapps['platform'] == 'Ethereum') & (dapps['category'].isin(options))]['category'].value_counts().plot(kind='pie',  figsize=(8, 8), fontsize=16, ax=ax)
sidebar.write(ax.get_figure())

# ______________________________________________________________________________________________________________________
# Word Cloud

sidebar.markdown("Tag's Word Cloud")
# sidebar.write(word_cloud(data.tag))
df_tag = dapps[(dapps['platform'] == 'Ethereum') & (dapps['category'].isin(options))].tag
sidebar.write(word_cloud(df_tag))

# ______________________________________________________________________________________________________________________
# Graph


G = nx.read_gpickle("test.gpickle")
# list_nodes_to_remove = []
for node,edge in zip(G.nodes(), G.edges()):
    try:
        if G.nodes[node]['category'] not in options:
            G.nodes[node]['hidden'] = False
            # list_nodes_to_remove.append(node)
    except:
        pass

# G.remove_nodes_from(list_nodes_to_remove)
G.remove_nodes_from(list(nx.isolates(G)))

nodes = [Node(id=i[0], label=i[0], **i[1]) for i in G.nodes(data=True)]

edges = [Edge(source=i, target=j, color=color, dashes=True, smooth=True, width=5) for (i, j, color) in G.edges(data=True)] #, type="CURVE_SMOOTH"

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
st.info("Click on a node")
if return_value is not None:
    # sidebar.info("Click on a node to see its details: {}".format(return_value))
    url = 'https://etherscan.io/address/' + return_value
    link = '[{}]({})'.format(return_value,url)
    st.markdown('Follow the link to see the contract or address on Etherscan: {}'.format(link), unsafe_allow_html=True)

    # st.markdown(link, unsafe_allow_html=True)


