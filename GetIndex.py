from whoosh.fields import *
from whoosh.index import create_in
import xml.dom.minidom as dom
import os, os.path

class GetIndex:
    def __init__(self):
        self.schema = Schema(paper=ID(stored=True), abstract=TEXT(stored=True), title=TEXT(stored=True), intro=TEXT(stored=True))
        self.ix = create_in("index/", self.schema)
        self.path = "papers_to_index/"
    
    def build(self):
        file_list = []
        for (dirpath, dirnames, filenames) in os.walk(self.path):
            file_list.extend(filenames)
        
        writer = self.ix.writer()
        count = 0
        for file in file_list:
            fileNew = dirpath+file
            count += 1
            # print(count)
            paperId = os.path.splitext(file)
            f = open(fileNew, encoding="utf8")
            for line in f:
                xmltree = dom.parseString(line)
                if (xmltree.getElementsByTagName('abstract')):
                    if xmltree.getElementsByTagName('abstract')[0].firstChild is None:
                        abstractContent = ""
                    else:
                        abstractContent = xmltree.getElementsByTagName('abstract')[0].firstChild.nodeValue
                
                elif (xmltree.getElementsByTagName('title')):
                    if xmltree.getElementsByTagName('title')[0].firstChild is None:
                        titleContent = ""
                    else:
                        titleContent = xmltree.getElementsByTagName('title')[0].firstChild.nodeValue

                elif (xmltree.getElementsByTagName('introduction')):
                    if (xmltree.getElementsByTagName('introduction')[0].firstChild is None):  
                        introContent = ""
                    else:
                        introContent = xmltree.getElementsByTagName('introduction')[0].firstChild.nodeValue
                
            writer.add_document(paper = paperId, abstract = abstractContent, title = titleContent, intro = introContent)

        writer.commit()
        # writer.close()

def build():
    indexbuilder = GetIndex()
    indexbuilder.build()

if __name__ == "__main__":
    build()
