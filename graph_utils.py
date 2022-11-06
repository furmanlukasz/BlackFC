import pandas as pd
import networkx as nx
from tqdm import tqdm
import numpy as np
import seaborn as sns
from sklearn.preprocessing import PowerTransformer


def new_color_pallete(n):
    new_cl = []
    for i in range(len(n)):
        new_cl.append(list((np.random.random(size=3).tolist() +[1])))

    return sns.color_palette(new_cl).as_hex()


def get_graph(degree = 5):
    df_blackfriday_CA = pd.read_csv('blackfriday_CA_with_categories_and_tags.csv').drop(columns=['Unnamed: 0'])

    category_list = df_blackfriday_CA['category'].unique().tolist()

    unique_colors = new_color_pallete(category_list)

    df_blackfriday_CA['value'] = df_blackfriday_CA['value'].apply(lambda x: int(str(x))/10)
    min = df_blackfriday_CA['value'].min()
    max = df_blackfriday_CA['value'].max()
    df_blackfriday_CA['value'] = df_blackfriday_CA['value'].apply(lambda x: (x - min)/(max-min))



    G = nx.MultiDiGraph()

    for i,row in tqdm(df_blackfriday_CA.iterrows()):
        kk = category_list[0]
        for k in category_list:
            if row['category'] == k:
                G.add_node(row['to'], color=unique_colors[category_list.index(k)], size=2, title=row['category'], category=row['category'], hidden=True)
                G.add_edge(row['to'], row['from'], relation=row['callingFunction'], arrows='to', value=row['value']+0.6, color=unique_colors[category_list.index(k)])
        # G.add_edge(row['to'], row['from'], relation=row['callingFunction'], arrows='to', value=row['value']+0.6, color=unique_colors[category_list.index(kk)]) #, color=unique_colors[category_list.index(kk)]


    trh_degree = degree
    core = [node for node, deg in dict(G.degree()).items() if deg >= trh_degree]
    nG = nx.subgraph(G, core)

    for node in nG.nodes():
        nG.nodes[node]['size'] = nG.degree[node]

    noG = nx.Graph(nG)

    degree = list(dict(noG.degree).values())
    transformer = PowerTransformer().fit(np.array(degree).reshape(-1, 1))
    normalized_degree = transformer.transform(np.array(degree).reshape(-1, 1))
    normalized_degree_list = np.abs(normalized_degree.flatten().tolist())

    # images = ['icons/{}.png'.format(i) for i in category_list]
    images = ['https://i.ibb.co/kqfLj6F/Exchanges.png',
              'https://i.ibb.co/6yj2FDN/Marketplaces.png',
              'https://i.ibb.co/MSYpVC1/Finance.png',
              'https://i.ibb.co/MDwGw3G/Games.png',
              'https://i.ibb.co/cXrYyFV/Gambling.png',
              'https://i.ibb.co/XsybYhg/Governance.png',
              'https://i.ibb.co/cCH6Vnn/Development.png',
              'https://i.ibb.co/BLXYnTb/Social.png',
              'https://i.ibb.co/R4S7pWy/Storage.png',
              'https://i.ibb.co/YWVkMSJ/High-risk.png',
              'https://i.ibb.co/VW5924n/Security.png',
              'https://i.ibb.co/tBw80Q2/Wallet.png',
              'https://i.ibb.co/5jnRCvv/Identity.png',
              'https://i.ibb.co/SmJ4fVH/Property.png',
              'https://i.ibb.co/qF3W5XC/Media.png',
              'https://i.ibb.co/QvZj0tc/Insurance.png',
              'https://i.ibb.co/kQhvYDx/Energy.png']


    for i, node in enumerate(noG.nodes()):
        noG.nodes[node]['size'] = normalized_degree_list[i]*40
        noG.nodes[node]['shape'] = 'image'
        noG.nodes[node]['image'] = 'https://i.ibb.co/xDjGPYL/user.png'


        for cat in category_list:
            try:
                if noG.nodes[node]['category'] == cat:
                    noG.nodes[node]['shape'] = 'image'
                    noG.nodes[node]['image'] = images[category_list.index(cat)]

            except:
                pass
    return noG


# pyvis_nt = net.Network(height='1100px', width='100%', bgcolor='#222222', font_color='white')
# pyvis_nt.from_nx(noG)
# # pyvis_nt.barnes_hut(gravity=-200,overlap=0.5)
# # pyvis_nt.hrepulsion()
# pyvis_nt.force_atlas_2based()
# pyvis_nt.show_buttons(filter_=['physics']) #filter_=['edges']
# # pyvis_nt.toggle_physics(False)
# pyvis_nt.save_graph('test2.html')
