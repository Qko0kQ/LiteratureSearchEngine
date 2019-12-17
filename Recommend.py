from gensim.models.word2vec import *
import gensim

model_file = 'word2vec.model'

class Recommend:
   
    def getRecommendations(results):
        papers = []
        dict_idx = {}
        ans = []
        for i in results:
            papers.append([i['abstract']])
            dict_idx[i['abstract']] = i['title']
        model = Word2Vec(papers, size=1000, window=5, min_count=1, workers=4)
        for i in range(len(papers)):
            recommendations = model.most_similar(positive=papers[i])
            tmp = []
            for j in range(5):
                tmp.append(dict_idx[recommendations[j][0]])
            ans.append(tmp)
        return ans