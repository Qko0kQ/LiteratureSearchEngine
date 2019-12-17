from whoosh.index import create_in, open_dir
from whoosh.fields import *
from whoosh.qparser import MultifieldParser, OrGroup, QueryParser

class Search:
   
    def getResultDocs(query):
        indexDir = open_dir("index/")
        indexSearcher = indexDir.searcher()
        og = OrGroup.factory(0.9)
        queryParser = MultifieldParser(["abstract", "title", "introduction"], indexSearcher.schema, group=og)
        queryObject = queryParser.parse(query)
        results = indexSearcher.search(queryObject, limit=100)
        searchResults = list()
        for result in results:
            contents = dict()
            contents["paper"] = result["paper"]
            contents["abstract"] = result["abstract"]
            contents["title"] = result["title"]
            contents["introduction"] = result["introduction"]
            searchResults.append(contents)
        return searchResults