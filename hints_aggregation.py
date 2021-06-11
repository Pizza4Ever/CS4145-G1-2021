from wordcloud import WordCloud
import matplotlib.pyplot as plt
from os import path
import pandas as pd
from PIL import Image
import os
import numpy as np
from sent2vec.vectorizer import Vectorizer
import seaborn as sns
from numpy import dot
from numpy.linalg import norm
import matplotlib.gridspec as gridspec

root_path = ""
# Read the whole text
df = pd.read_csv(path.join(root_path, "hints.csv"))
df_images = pd.read_csv(path.join(root_path, "images.csv"))

df["flag"] = df["hint"].apply(lambda x: 1 if " " in x else 0)

def hints_aggregation(df, df_images):
    df_words = df[df["flag"]==0]

    image_id_list = list(set((df_words["image_id"].tolist())))
    df_sentences = df[df["flag"] == 1]
    df_sentences = df_sentences.reset_index()

    for i in image_id_list:

        # get all of the words
        words = df_words[(df_words["image_id"]==i) & (df_words["hint_orig"] != "honeypot")]["hint"].tolist()

        text = " ".join(words)
        honey_label = df[(df["image_id"]==i) & (df["hint_orig"] == "honeypot")]["hint"].values.item()
        image_des = df_images[df_images["image_id"]==i]["cv_description"].values.item()
        # cv_tags = df_images[df_images["image_id"]==i]["cv_tags"].values.item()
        image_path =df_images[df_images["image_id"]==i]["path"].values.item()
        wordcloud = WordCloud(background_color='white', width=800, height=800, margin=2, max_font_size=40).generate(text)

        # get all of the sentences
        sen_list = df_sentences[df_sentences["image_id"] == i]["hint"].tolist()
        if len(sen_list)>1:

            emb_list = bert_vector(df_sentences[df_sentences["image_id"] == i]["hint"].tolist())

            # calculate similarity
            corr = [ [ dot(emb_list[k], emb_list[j])/(norm(emb_list[k])*norm(emb_list[j])) for k in range(len(emb_list)) ] for j in range(len(emb_list)) ]
            # Generate a mask for the upper triangle
            mask = np.triu(np.ones_like(corr, dtype=bool))
            # Generate a custom diverging colormap
            cmap = sns.diverging_palette(230, 20, as_cmap=True)

            # Create 2x2 sub plots
            gs = gridspec.GridSpec(3, 2)
            fig = plt.figure(figsize=(40,40))
            font={'family':'Times New Roman',
                  'weight':'normal',
                  'size':40
                  }

            ax1 = fig.add_subplot(gs[0, :]) # row 0
            img = Image.open(os.path.join('/Users/sylvia/PycharmProjects/CS4145-G1-2021/static', image_path))
            ax1.imshow(img)
            ax1.axis('off')
            ax1.set_title('Original Image'+"\n"+"Image Description: "+image_des, font)

            ax2 = fig.add_subplot(gs[1, 0]) # row 1, col 1
            ax2.imshow(wordcloud, interpolation='bilinear')
            ax2.axis('off')
            ax2.set_title("Word Cloud"+"\n"+"Honeypot Label: "+honey_label, font)


            ax3 = fig.add_subplot(gs[1, 1:2]) # row 1,
            # Draw the heatmap with the mask and correct aspect ratio
            h = sns.heatmap(corr, cmap=cmap, mask=mask,
                        square=True, linewidths=.5, cbar_kws={"shrink": .5},xticklabels=sen_list, yticklabels=sen_list, cbar=False, annot=True, annot_kws={"fontsize":20})
            cb = h.figure.colorbar(h.collections[0])
            cb.ax.tick_params(labelsize=28)
            plt.xticks(rotation=75, fontsize=26)
            plt.yticks(fontsize=26, rotation=0)
            ax3.set_title("Sentence Similarity Heatmap"+"\n"+"Honeypot Label: "+honey_label, font)
            plt.xticks()


def bert_vector(sentences):
    vectorizer = Vectorizer()
    vectorizer.bert(sentences)
    vectors_bert = vectorizer.vectors
    return vectors_bert


if __name__ == "__main__":
    hints_aggregation(df, df_images)









