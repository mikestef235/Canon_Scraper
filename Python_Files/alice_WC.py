
from os import path
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import os

from wordcloud import WordCloud, STOPWORDS


# Read the whole text.
text = open("/Users/mikes/Documents/GetawayDevelopment/alice.txt").read()
print(text)
text = '''Alice remained looking thoughtfully at the mushroom for a minute, trying
to make out which were the two sides of it; and as it was perfectly
round, she found this a very difficult question. However, at last she
stretched her arms round it as far as they would go, and broke off a bit
of the edge with each hand.'''
# read the mask image
# taken from
# http://www.stencilry.org/stencils/movies/alice%20in%20wonderland/255fk.jpg
alice_mask = np.array(Image.open("/Users/mikes/Documents/GetawayDevelopment/alice_mask.jpg"))

wc = WordCloud(background_color="white", max_words=2000, mask=alice_mask)
# generate word cloud
wc.generate(text)

# store to file
wc.to_file("/Users/mikes/Documents/GetawayDevelopment/alice.jpg")

# show
plt.imshow(wc, interpolation='bilinear')
plt.axis("off")
#plt.figure()
# plt.imshow(alice_mask, cmap='gray', interpolation='bilinear')
# plt.axis("off")
plt.show()