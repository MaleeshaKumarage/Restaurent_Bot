from rasa.nlu.components import Component
from rasa.nlu import utils
from rasa.nlu.model import Metadata

import nltk
from nltk.classify import NaiveBayesClassifier
import os
import csv
import time
import re

import typing
from typing import Any, Optional, Text, Dict

MODEL_FILE_NAME = "sinhala_classifier.pkl"

class SinhalaClassifier(Component):
    """A custom Entity Extraction component"""
    name = "SinhalaClassifier"
    provides = ["entities"]
    requires = ["tokens"]
    defaults = {}
    language_list = ["si"]
    print('initialised the class')

    def __init__(self, component_config=None):
        super(SinhalaClassifier, self).__init__(component_config)

    def train(self, training_data, cfg, **kwargs):
       
        with open('productlist.txt', 'r') as f:
            labels = f.read().splitlines()

        training_data = training_data.training_examples #list of Message objects
        tokens = [list(map(lambda x: x.text, t.get('tokens'))) for t in training_data]
        processed_tokens = [self.preprocessing(t) for t in tokens]
        labeled_data = [(t, x) for t,x in zip(processed_tokens, labels)]
        self.clf = NaiveBayesClassifier.train(labeled_data)



    def convert_to_rasa(self, value, confidence):
        """Convert model output into the Rasa NLU compatible output format."""

        entity = {"value": value,
                  "confidence": confidence,
                  "entity": "Food_Type",
                  "extractor": "SinhalaClassifier"}

        return entity
        

    def preprocessing(self, tokens):
        """Create bag-of-words representation of the training examples."""
        
        return ({word: True for word in tokens})


    def process(self, message, **kwargs):
        """Retrieve the tokens of the new message, pass it to the classifier
            and append prediction results to the message class."""
        
        if not self.clf:
            # component is either not trained or didn't
            # receive enough training data
            entity = None
        else:
            tokens = [t.text for t in message.get("tokens")]
            tb = self.preprocessing(tokens)
            pred = self.clf.prob_classify(tb)

            sentiment = pred.max()
            confidence = pred.prob(sentiment)

            entity = self.convert_to_rasa(sentiment, confidence)

            message.set("entities", [entity], add_to_output=True)



    def word_sim(str1,str2):

      str1 = str1.lower()
      str2 = str2.lower()

      x_set={c for c in str1}
      y_set={c for c in str2}

      l1 =[]

      rvector = x_set.union(y_set) 

      for w in rvector:

        if (str1.find(w)==str2.find(w)):l1.append(1)
        else: l1.append(0)
  
      percentage = 0.0
      if not len(rvector) ==0 : percentage= (sum(l1)/len(rvector))
  

    return percentage

    def levenshtein_distance(s1, s2):
      if len(s1) > len(s2):
        s1, s2 = s2, s1

      distances = range(len(s1) + 1)
      for i2, char2 in enumerate(s2):
        distances_ = [i2+1]
        for i1, char1 in enumerate(s1):
            if char1 == char2:
                distances_.append(distances[i1])
            else:
                distances_.append(1 + min((distances[i1], distances[i1 + 1], distances_[-1])))
        distances = distances_
        
    
      if distances[-1] <= 2 and distances[-1] > 0 :
        return 2/distances[-1]
      else:
        return 0
    

    def jaccard_index(s1, s2):
        s1 = set(s1.split())
        s2 = set(s2.split())
        union_ = s1.union(s2)
        intersection_ = s1.intersection(s2)

        union_ = s1.union(s2)
        intersection_ = s1.intersection(s2)

        return len(intersection_)/len(union_)

    def setSortKey(elem):
        return elem['confidance']

    regex = re.compile(r"[-()\"#/@;:<>{}`+=~|.!?,'–]")

    
    result_count=0
    result={'stage_1':[],
          'stage_2':[]}

    input_str='red'

    with open('csv/Products.csv','r')as f:

    data = csv.reader(f)

      for row in data:
            prod_str = row[1] + row[2]

            prod_str=regex.sub('', prod_str)

            if ( row[4] not in prod_str):
              prod_str = row[4] +' '+ prod_str
              #print(prod_str)
        
        

            confidance = jaccard_index(input_str.lower(), prod_str.lower())
            # confidance = confidance + jaccard_index(input_str.lower(), row[2])

            if confidance > 0.2:
              result['stage_0'].append({'product_name':prod_str, 'confidance':confidance})
        
            elif (input_str.lower() in prod_str.lower()):
              result['stage_1'].append(prod_str)   

            else:

              conf=[]

              for usr_word in input_str.split(' '):
            
                for prod_word in prod_str.split(' '):
                  if (word_sim(usr_word, prod_word) + levenshtein_distance(usr_word, prod_word)*0.5 > 0.8): conf.append(1)
                  else: conf.append(0)

                  #print('word accuracy :',word_sim(usr_word, prod_word),' ',prod_word,',',usr_word,'\n')


              percentage=sum(conf)/len(conf)

              #print('total accuracy :', percentage, '\n')

              if(percentage > 0.06):
                result['stage_2'].append({'product_name':prod_str, 'confidance':percentage})


    result['stage_2'].sort(key=setSortKey, reverse=True)
        

    print("stage_0", result['stage_0'])

      def persist(self, file_name, model_dir):
          """Persist this model into the passed directory."""
          classifier_file = os.path.join(model_dir, MODEL_FILE_NAME)
          utils.json_pickle(classifier_file, self)
          return {"classifier_file": MODEL_FILE_NAME}

      @classmethod
      def load(cls,
              meta: Dict[Text, Any],
              model_dir=None,
              model_metadata=None,
              cached_component=None,
              **kwargs):
          file_name = meta.get("classifier_file")
          classifier_file = os.path.join(model_dir, file_name)
          return utils.json_unpickle(classifier_file)
