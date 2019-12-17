class SearchResult:
    def __init__(self, result, query):
        self.id = 'paperid' + str(result['paper'][0][:8].encode('utf-8')).replace(" ", "")
        self.title = result['title']
        self.abstract = self.highlightQuery(result['abstract'], query)
        self.url = self.getUrlFormat(result['paper'][0])
    
    def getUrlFormat(self, file):
        return "http://www.aclweb.org/anthology/" + file[0:8] + ".pdf"

    def highlightQuery(self, text, query):
        keywords = [w.lower() for w in query.split()]
        words = text.split()

        for i, word in enumerate(words):
            for keyword in keywords:
                if keyword in word.lower():
                    words[i] = '<b>' + word + '</b>'
                    break
        return ' '.join(words).rstrip("\"").rstrip(".") + "."