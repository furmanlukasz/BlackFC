import pandas as pd
import networkx as nx
from tqdm import tqdm
import numpy as np
import seaborn as sns
from sklearn.preprocessing import PowerTransformer
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt


def get_data():
    df_blackfriday_CA = pd.read_csv('blackfriday_CA_with_categories_and_tags.csv').drop(columns=['Unnamed: 0'])
    df_dapps = pd.read_csv('state_of_the_dapp.csv',encoding = "ISO-8859-1")
    return df_blackfriday_CA, df_dapps

def word_cloud(df):

    comment_words = ''
    stopwords = set(STOPWORDS)

    # iterate through the csv file
    for val in df:

        # typecaste each val to string
        val = str(val)

        # split the value
        tokens = val.split()

        # Converts each token into lowercase
        for i in range(len(tokens)):
            tokens[i] = tokens[i].lower()

        comment_words += " ".join(tokens)+" "

    wordcloud = WordCloud(width = 800, height = 800,
                          background_color ='black',
                          stopwords = stopwords,
                          min_font_size = 10).generate(comment_words)

    # plot the WordCloud image
    fig = plt.figure(figsize=[8,8],frameon=False)
    ax = fig.add_subplot(111)
    ax.imshow(wordcloud)
    ax.axes.get_xaxis().set_visible(False)
    ax.axes.get_yaxis().set_visible(False)


    return fig

def new_color_pallete(n):
    new_cl = []
    for i in range(len(n)):
        new_cl.append(list((np.random.random(size=3).tolist() +[1])))

    return sns.color_palette(new_cl).as_hex()


def get_graph(df, degree):
    df_blackfriday_CA = df

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
                G.add_node(row['to'], color=unique_colors[category_list.index(k)], size=2, title=row['category'], category=row['category'], hidden=False)
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

