import nltk, re, pprint
import random
from nltk import word_tokenize, regexp_tokenize
import statistics

class MarcovModel:
  def __init__(self, corpus_filename, level, order):
    '''
    Creates a MarcovModel object.

    Args:
      corpus_filename: 
        string representing the path to a text file containing sample sentences
      level: 
        "character" or "word" (which mode to train the model in)
      order: 
        integer defining the model's order 
    '''
    self.corpus_filename = corpus_filename
    self.corpus, self.testset = self._load_corpus(corpus_filename)
    self.tokens = []
    self.level = level
    self.order = order
    self.transitions = dict()
    self.authorship_estimator = (0, 0) # first number represents the mean likelihood value, second value represents the standard deviation 
    self.train()

  # Sue 
  def train(self):
    '''
    Populates 'transitions' dictionary of n-grams, where n is the given order of the model. In addition, calculates authorship_estimator (aka mean and stdev of likelihoods for the second half of the model).
    
    Requirements:
      key: n-grams
      value: list of tuples -> (token, probability_range)

      ex) "the quick" : [(“the”, (0.0, 0.0)), (“quick”, (0.0, 0.0)), (“brown”, (0.0, 0.65)),(“fox”, (0.65, 0.95)), (“jumps”, (0.95, 1.0))]

      except, we don't want to include tokens with 0 probability_range

      also, the probability ranges have to add up to 1

    Pseudocode:
      One pass, sliding window approach

      ['My', 'name', 'is', 'Yemi', 'Shin', '.', 'I', 'go', 'to', 'Carleton', ',', 'and', 'I', 'like', 'ramen', '.', 'Yemi', 'Shin', 'is', 'a', 'CS', 'Major', '.']

      if it's a bigram

      first consider the key ('My', 'name') -> 'is' is added to the list of values
      next, consider the key ('name', 'is') -> 'Yemi' is added to the list of values
      ...

      if key doesn't already exist in the dictionary, add a new entry
      if key already exists, just add the new value to the list of values

    '''

    # split the corpus in half
    split_corpus = self.corpus.split("\n")
    # assign the first half of the corpus to training

    # If the corpus is william shakespeare collected works, just reduce the size of the corpus for now (for future, make the code more efficient by serializing)
    if self.corpus_filename == "william_shakespeare_collected_works.txt":
      self.corpus = "\n".join(split_corpus[:len(split_corpus) // 3])
    else:
      self.corpus = "\n".join(split_corpus[:(len(split_corpus) * 8) // 10])
    # and second half to use for estimation
    corpus_to_be_used_for_estimation = split_corpus[((len(split_corpus) * 8) // 10) + 1:]

    '''
    POPULATING TRANSITIONS DICTIONARY portion
    '''
    self.tokens = self._tokenize(self.corpus) # tokenize the corpus

    #puntuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~\t'''
    puntuations = '''\t'''
    # count how many times each token appears when a given n-gram in a nested list
    num = 0 # position of the first word in the n-gram in the corpus
    for token in self.tokens:
      # puntuation does not go into the n-gram
      if token not in puntuations:
        gram = [token] # a list of tokens that go into the ngram
        cur_order = 1
        word_num = 1 # the length of the n-gram
        # create valid n-gram
        while cur_order < self.order:
          # make sure it is not out of index and the n-gram doesn't have puntuations
          if num+cur_order < len(self.tokens) and self.tokens[num+cur_order] not in puntuations:
            # gram = gram + " " + self.tokens[num+cur_order]
            gram.append(self.tokens[num+cur_order])
            word_num += 1
          cur_order += 1
         
        gram = self._construct_text(gram)
        
        # make sure n-gram do not contain puntuations and there is at least one more token in the corpus
        if word_num == self.order and num < len(self.tokens)-self.order:
          value = self.tokens[num+self.order] 
          # puntuation does not count as token
          if value not in puntuations:
            # create the dictionary with values in nested lists
            if gram in self.transitions:
              not_added = True
              for item in self.transitions[gram]: # "the" : [["fox", 3], ["bear", 5]]
                if item[0] == value:
                  item[1] += 1
                  not_added = False
              if not_added:
                self.transitions[gram].append([value,1])
            else:
              self.transitions[gram] = [[value,1]]   
      num += 1

    # calculate probablity and convert list to tuple
    
    all_keys = self.transitions.keys()
    for key in all_keys:
      total_appearance = 0
      specific_values = self.transitions[key]
      # calculate the total appearances
      # "the" : [["fox", 3], ["bear", 5]]
      for value in specific_values:
        total_appearance = total_appearance + value[1]
      # calculate the frequency_range for each token and convert the list to tuple
      range_num = 0 # start of a new range
      for value in specific_values:
        value[1] = (range_num, range_num+value[1]/total_appearance)
        range_num = value[1][1] # update lower bound
        # convert the nested list into a tuple
      token_num = 0
      while token_num < len(specific_values):
        specific_values[token_num] = tuple(specific_values[token_num])
        token_num += 1
    
    '''
    CALCULATING AUTHORSHIP ESTIMATOR portion
    '''
    self.authorship_estimator = self._caculate_authorship_estimator(corpus_to_be_used_for_estimation)

  # Maanya
  def _tokenize(self, text):
    '''
    Helper method to tokenize a certain line of sentence.

    Args:
      text: 
        text to be tokenized

    Returns:
      list of tokens

    Requirements:
      Have to make sure to deal with white space (include newline)
      tokenize at the level of the entire corpus
    '''
    #makes use of the nltk library and regular expressions to tokenize a corpus
    tokens_list = []
    if self.level == "word":
        tokens_list = regexp_tokenize(text,'\w+|\$[\d\.]+|\S+|\n|\r|\t')
    else:
        for char in text:
            tokens_list.append(char)
    #added this for loop and if statement, tabs were still in the list when only remove() was called
    for lists in tokens_list:
      if '\t' in lists:
        tokens_list.remove('\t')
    return tokens_list
  
  @staticmethod
  def _load_corpus(corpus_filename):
    '''
    Returns the contents of a corpus loaded from a corpus file.

    Credit to James (Took from Comp Med HW file)

    Args:
      corpus_filename:
        The filename for the corpus that's to be loaded.

    Returns:
      A single string

    Raises:
      IOError:
        There is no corpus file with the given name in the 'corpora' folder.
    '''
    corpus_text = open(f"corpora/{corpus_filename}").read()
    return corpus_text[:(len(corpus_text) * 8) // 10], corpus_text[:((len(corpus_text) * 8) // 10) + 1]

  # Nicole
  def generate(self, length, prompt="\n"):
    '''
    Generates a text of 'length' tokens which begins with 'prompt' token if given one.

    Args:
      length: 
        length of the text to be generated
      prompt: 
        starting tokens (default: "\n")
    
    Returns:
      A string containing the generated text

    Requirements:
      should use the transition probabilities of the model (use Random module)

      if no prompt, randomly select an n-gram that occurs after a newline chracter 
      this ensures that the first token is always one that can start the sentence
    '''
    gen_text = prompt
    n_gram = ""
    punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~\t\n'''

    tokenized_prompt = self._tokenize(prompt)
    length_of_prompt = len(tokenized_prompt)
    
    #prompt does not have a complete n-gram
    if length_of_prompt < self.order:
      n_gram, gen_text = self._find_n_gram(prompt, tokenized_prompt, length_of_prompt, gen_text, length)
    else: #prompt is longer than or equal to one n-gram, reduce/keep the same
      n_tokens = tokenized_prompt[length_of_prompt - self.order:]
      n_gram = self._construct_text(n_tokens, 1)
      #check if n_gram is in our dictionary
      if n_gram not in self.transitions.keys():
        #find key containing prompt
        n_gram, gen_text = self._find_n_gram(n_gram, self._tokenize(n_gram), len(self._tokenize(n_gram)), gen_text, length)

    while len(self._tokenize(gen_text)) < length:
      values = self.transitions.get(n_gram)
      if values is None:
        n_gram, gen_text = self._find_n_gram(n_gram, self._tokenize(n_gram), len(self._tokenize(n_gram)), gen_text, length)
        values = self.transitions.get(n_gram)
      random_num = random.random()
      # ["the": (("end", (0,.5)), ("fox", (.5,1)))]
      for t in values:
        probability_range = t[1]
        if random_num > probability_range[0] and random_num <= probability_range[1]:
          add_word = t[0]
      if self.level == "character":
        gen_text+=add_word
      else:
        if add_word in punctuations:
          gen_text += add_word
        else:
          gen_text += " " + add_word
      #get last n token of generated text
      tokenized_text = self._tokenize(gen_text)
      n_gram = self._construct_text(tokenized_text[len(tokenized_text) - self.order:],1)
      
    return gen_text
  
  def _find_n_gram(self, prompt, tokenized_prompt, length_of_prompt, gen_text, length):
    keys = self.transitions.keys()
    n_gram = ""
    #find n-gram CONTAINING the prompt or shortened prompt
    x = 0 #variable to decrement token length of prompt (ex. "the brown" not found, then check if some key begins with "brown")
    while n_gram == "":
      for k in keys:
        if prompt == "\n" and "\n" in k:
          n_gram = k
          break
        split_key = self._tokenize(k)
        #see if prompt is the start of key k
        shortened_key = split_key[0:length_of_prompt]
        #store to add to gen_text when valid key is found
        rest_of_key = split_key[length_of_prompt:]
        new_k = self._construct_text(shortened_key,1)
        if new_k == prompt:
          n_gram = k
          gen_text += self._construct_text(rest_of_key, 0)
          #add rest of key to gen_text, ex. key = "brown fox jumps", prompt = "the quick brown", gen_text = "the quick brown fox jumps", n_gram = brown fox jumps
          break #valid dictionary key found
      #if prompt not contained in any n-grams in dictionary, remove first token, check again
      x+=1
      shortened_prompt = tokenized_prompt[x:]
      prompt = self._construct_text(shortened_prompt, 1)
      length_of_prompt = len(shortened_prompt)
      #if no words in the prompt in any dictionary key, choose a random key to start text generation
      if x == len(tokenized_prompt):
        #note: random key not appended to gen_text
        entry_list = list(self.transitions.items())
        n_gram = random.choice(entry_list)[0]
    if len(self._tokenize(gen_text)) > length:
      less_tokens = self._tokenize(gen_text)[0:self.order]
      gen_text = self._construct_text(less_tokens, 1)
    return n_gram, gen_text

  def _construct_text(self, tokens, first_token=0):
    punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~\t\n'''
    text = ""
    if self.level == "character":
      for token in tokens:
        text+=token
    else:
      for token in tokens:
        if token in punctuations:
          text += token
        else:
          if first_token == 1:
            text += token
            first_token+=1
          else:
            text += " " + token
    return text

  # Yemi
  def estimate(self, text):
    '''
    Returns a single string floating-point value: a (normalized) z-score estimate of the likelihood that this text could have been produced by the model at hand

    Args:
      text: 
        text to be analyzed
    
    Returns:
      A floating point estimate of the likelihood of authorship
    
    Requirements:
      to normalize the likelihood values, split the corpus in half, train the model on one half, and then calculate the likelihoods for all sentences in the other half 

      now use the mean and standard deviation as an authorship estimator 
      given an anonymous text, estimate its likelihood using this model, and then determine how many standard deviations away it is from the mean likelihood for the model. (aka z-score)

      if z-score positive, it is more likely, if negative, it is less likely

      normalize to the length of a sequence

      at each step, the transition probabilities for a model are consulted to estimate the likelihood that the (given) next token would follow the (given) preceding n-gram

      the likelihood for each token is added to a cumulative likelihood for the entire text, and by the end of the processing that text, you have a single number representing how likely it is that the given model produced that text
    
    Pseudocode:
      given a text, caculate the likelihood
      compare this likelihood to the authorship_estimator (aka mean likelihood for the model)
      aka calculate the z-score
      aka calculate how many standard deviations away from the author_estimator this number is
    '''
    likelihood_of_this_text = self._calculate_likelihood(text)
    return (likelihood_of_this_text - self.authorship_estimator[0]) / self.authorship_estimator[1]

  def _caculate_authorship_estimator(self, corpus_to_be_used_for_estimation):
    '''
    Helper method to calculate the authorship estimator for the model.

    Args:
      corpus_to_be_used_for_estimation:
        corpus to be used for estimation
    
    Returns:
      the mean and stdev of the model's likelihood values
    '''
    total = 0
    likelihoods = []
    for line in corpus_to_be_used_for_estimation:
      likelihood = self._calculate_likelihood(line)
      likelihoods.append(likelihood)
    mean = statistics.mean(likelihoods)
    standard_dev = statistics.stdev(likelihoods) 
    
    return (mean, standard_dev)
  
  def _calculate_likelihood(self, text):
    '''
    Helper method to caculate the likelihood of a given text, based on the transitions dictionary of the trained model.

    Args:
      text:
        text to be analyzed
    
    Returns:
      A single number representing the likelihood (aggregate of probabilities) of this text being authored by the author of the model
    '''
    likelihood = 0

    # word_tokenize the string
    string_to_be_analyzed = self._tokenize(text) # this tokenize function should take care of whether to tokenize it in terms of words or characters depending on the object's level

    actual_successor = ""

    for i in range(len(string_to_be_analyzed) - self.order):
      # get the token according to the order
      # token = " ".join(string_to_be_analyzed[i:i + self.order])
      token = self._construct_text(string_to_be_analyzed[i:i + self.order])
      # retrieve the actual sucessor
      actual_successor = string_to_be_analyzed[i + self.order]
      # retrieve the values from the dictionary if one exists
      if token in self.transitions.keys():
        potential_successors = self.transitions[token]
        # if the actual sucessor of the token is in transitions dictionary, add the corresponding probability to likelihood
        for successor in potential_successors:
          if actual_successor == successor[0]:
            likelihood += successor[1][1] - successor[1][0]
    
    # take the average to account for normalizing with respect to length
    if (len(string_to_be_analyzed) != 0):
      return likelihood / len(string_to_be_analyzed)
    return likelihood

if __name__ == "__main__":
    corpus_filename = input("Enter filename for the corpus: ")
    level = input("Enter level or mode for training the model: ")
    order = int(input("Enter the model's order: "))
    prompt = input("Do you have a prompt that you would like to generate the text off of?: ")
    length = int(input("How long do you want the text to be? (Enter int): "))
    
    model = MarcovModel(corpus_filename, level, order)
    
    print("Here's your output!: \n")
    if (prompt != None):
      print(model.generate(length, prompt))
    else:
      print(model.generate(length))