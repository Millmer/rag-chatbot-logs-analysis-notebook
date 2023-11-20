# Chatbot Logs "Sentiment" Analysis
In this repository, I showcase the analytical techniques I've used to examine chatbot log data. It's a demonstration of how I extract and interpret interactions from a chatbot I've been working on. The data used here is fake and can be generated using the [generate-logs.py](./generate-logs.py) script.

## Parsing and Metadata
In the [parsing notebook](./parsing.ipynb), I handle the initial processing of the raw log files. My focus here is on key metrics such as average request counts, question frequencies, and insights into users' geographic locations and device usage. It also generates the `output_questions` file to be used in further analysis.

## Sentiment and Cluster Analysis
The [sentiment notebook](./sentiment.ipynb) takes a closer look at the types of questions posed to the chatbot. Similar to how sentiment analysis is done, I've grouped these questions into clusters to better understand the recurring themes by checking their "similarity" (i.e. vector distance in embedding space) to a manually created set of clusters, initially guessed from a brief look at the dataset. For visualisation, I've employed the [t-SNE method](https://en.wikipedia.org/wiki/T-distributed_stochastic_neighbor_embedding) method, which helps in making the data more comprehensible by collapsing the vectors to 2 dimensions.

### Automated Clustering and Visualization
As manually creating clusters inherently contains bias, I've also explored automatic clustering using the [k-means](https://en.wikipedia.org/wiki/K-means_clustering) method. After the clusters are formed, I use a GPT to name them. Finally, I visualise these clusters using the t-SNE method, offering a clear depiction of the chatbot interactions. This analysis can then be used to help steer the product team by providing them with a clearer empirical understanding of how the users are interacting with the chatbot.