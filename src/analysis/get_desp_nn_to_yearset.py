# -*- coding: utf-8 -*-
import nltk
from nltk.corpus import brown
import os
import random
import sys
# This is our fast Part of Speech tagger
#############################################################################
brown_train = brown.tagged_sents(categories='news')
regexp_tagger = nltk.RegexpTagger(
    [(r'^-?[0-9]+(.[0-9]+)?$', 'CD'),
     (r'(-|:|;)$', ':'),
     (r'\'*$', 'MD'),
     (r'(The|the|A|a|An|an)$', 'AT'),
     (r'.*able$', 'JJ'),
     (r'^[A-Z].*$', 'NNP'),
     (r'.*ness$', 'NN'),
     (r'.*ly$', 'RB'),
     (r'.*s$', 'NNS'),
     (r'.*ing$', 'VBG'),
     (r'.*ed$', 'VBD'),
     (r'.*', 'NN')
])
unigram_tagger = nltk.UnigramTagger(brown_train, backoff=regexp_tagger)
bigram_tagger = nltk.BigramTagger(brown_train, backoff=unigram_tagger)
#############################################################################
# This is our semi-CFG; Extend it according to your own needs
#############################################################################
cfg = {}
cfg["NNP+NNP"] = "NNP"
cfg["NN+NN"] = "NNI"
cfg["NNI+NN"] = "NNI"
cfg["JJ+JJ"] = "JJ"
cfg["JJ+NN"] = "NNI"
#############################################################################
class NPExtractor(object):
  
    def __init__(self, sentence):
        self.sentence = sentence
  
    # Split the sentence into singlw words/tokens
    def tokenize_sentence(self, sentence):
        tokens = nltk.word_tokenize(sentence)
        return tokens
  
    # Normalize brown corpus' tags ("NN", "NN-PL", "NNS" > "NN")
    def normalize_tags(self, tagged):
        n_tagged = []
        for t in tagged:
            if t[1] == "NP-TL" or t[1] == "NP":
                n_tagged.append((t[0], "NNP"))
                continue
            if t[1].endswith("-TL"):
                n_tagged.append((t[0], t[1][:-3]))
                continue
            if t[1].endswith("S"):
                n_tagged.append((t[0], t[1][:-1]))
                continue
            n_tagged.append((t[0], t[1]))
        return n_tagged

    # Extract the main topics from the sentence
    def extract(self, year_name, xml_doc, yearTopicWordsFile):
        tokens = self.tokenize_sentence(self.sentence)
        tags = self.normalize_tags(bigram_tagger.tag(tokens))
  
        merge = True
        while merge:
            merge = False
            for x in range(0, len(tags) - 1):
                t1 = tags[x]
                t2 = tags[x + 1]
                key = "%s+%s" % (t1[1], t2[1])
                value = cfg.get(key, '')
                if value:
                    merge = True
                    tags.pop(x)
                    tags.pop(x)
                    match = "%s %s" % (t1[0], t2[0])
                    pos = value
                    tags.insert(x, (match, pos))
                    break

        for t in tags:
            if t[1] == "NNP"  or t[1] == "NN":
                if(len(t[0]) > 2):
                    strs = str(t[0].strip())
                    strs = strs.replace(' ','_')
                    yearTopicWordsFile.write(strs+' ')

def readDataTest(year_name, xml_doc):
    yearTopicWordsFile = open("year_nn_set/" + year_name + '.txt', 'a+')

    contentFileName = "year_desp/" + year_name + "/" + xml_doc
    file = open(contentFileName)

    while 1:
        line = file.readline()
        if not line:
            yearTopicWordsFile.write('\n')
            break
        line.encode('unicode_escape')
        try:
            np_extractor = NPExtractor(line)
            np_extractor.extract(year_name, xml_doc, yearTopicWordsFile)
        except:
            print "error"

    file.close()
    yearTopicWordsFile.close()

#scan work dir to check each XML document.
def scanDir(year_name):
    yearTopicWordsFile2 = open("year_nn_set/" + year_name + '.txt', 'w+')#clean the file
    file_num = 1000
    i = 0;
    yearTopicWordsFile2.write(str(file_num) + '\n')
    yearTopicWordsFile2.close()

    file_list = os.listdir('year_desp/' + year_name)
    xml_samples = random.sample(file_list, file_num)
    for xml_doc in xml_samples:
        if(xml_doc != '.DS_Store'):
            readDataTest(year_name, xml_doc)
       

if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf-8')

    #os.system("rm year_nn_set/*")

    scanDir("2011")
    scanDir("2011")
    scanDir("2013")
    scanDir("2014")

