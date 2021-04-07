from MarcovModel import MarcovModel
import random 

def component3b():
  print("-----Component 3b (Check results folder)-----")
  f = open("results/component3b.txt", "a")

  # Sue
  model1 = MarcovModel("harry_potter_1.txt", "word", 5)
  # Yemi
  model2 = MarcovModel("franz_kafka_collected_works.txt", "word", 5)
  # Nicole
  model3 = MarcovModel("origin_of_species.txt", "word", 5)
  # Maanya
  model4 = MarcovModel("practice_phrenology_simplified.txt", "word", 5)

  models = [model1, model2, model3, model4]

  for model in random.sample(models, len(models)):
    f.write("\nmodel: \n")
    f.write(model.generate(30))

def component3c():
  print("-----Component 3c (Check results folder)-----")
  f = open("results/component3c.txt", "a")

  # Sue
  model1 = MarcovModel("harry_potter_1.txt", "word", 4)
  # Yemi
  model2 = MarcovModel("franz_kafka_collected_works.txt", "word", 4)
  # Nicole
  model3 = MarcovModel("origin_of_species.txt", "word", 4)
  # Maanya
  model4 = MarcovModel("practice_phrenology_simplified.txt", "word", 4)

  models = [model1, model2, model3, model4]

  for model in random.sample(models, len(models)):
    f.write(f"\n-----{model.corpus_filename}/ Level: Word / Order: 4-----\n")
    f.write(model.generate(35))

def component3():
  component3b()
  component3c()

if __name__ == "__main__":
  component3b()