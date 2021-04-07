from MarcovModel import MarcovModel

def component2a():
  print("-----Component 2a (Check results folder)-----")
  f = open("results/component2a.txt", "a")

  for order in range(1,6):
    f.write(f"\n-----Level: Character / Order: {order}-----\n")
    model = MarcovModel("franz_kafka_collected_works.txt", "character", order)
    f.write(model.generate(20, "The"))

def component2b():
  print("-----Component 2b (Check results folder)-----")
  f = open("results/component2b.txt", "a")

  for order in range(1,6):
    f.write(f"\n-----Level: Word / Order: {order}-----\n")
    model = MarcovModel("franz_kafka_collected_works.txt", "word", order)
    f.write(model.generate(20, "The"))

def component2c():
  print("-----Component 2c (Check results folder)-----")
  f = open("results/component2c.txt", "a")

  for order in range(1,6):
    f.write(f"\n-----Mystery Model / Level: Word / Order: {order}-----\n")

    model1 = MarcovModel("franz_kafka_collected_works.txt", "word", order)
    model2 = MarcovModel("arthur_conan_doyle_collected_works.txt", "word", order)

    f.write("\n Level: word \n")
    f.write(f"\n Order: {order} \n")
    f.write("\n Results for Mystery Model \n")
    f.write(model1.generate(50, "The"))
    f.write("\n Results for Mystery Model \n")
    f.write(model2.generate(50, "The"))

def component2d():
  print("-----Component 2d (Check results folder)-----")
  f = open("results/component2d.txt", "a")
  f.write(f"\n-----Mystery Model / Level: Character / Order: 3-----\n")

  model1 = MarcovModel("franz_kafka_collected_works.txt", "character", 3)
  model2 = MarcovModel("arthur_conan_doyle_collected_works.txt", "character", 3)
  
  f.write("\n Results for Mystery Model \n")
  f.write(model1.generate(50, "The"))
  f.write("\n\n Results for Mystery Model \n")
  f.write(model2.generate(50, "The"))

def component2e():
  print("-----Component 2e (Check results folder)-----")
  model1 = MarcovModel("franz_kafka_collected_works.txt", "character", 5)
  model2 = MarcovModel("arthur_conan_doyle_collected_works.txt", "word", 3)
  model3 = MarcovModel("edgar_allan_poe_collected_works.txt", "word", 2)

  models = [model1, model2, model3]
  f = open("results/component2e.txt", "a")
  
  for model in models:
    f.write(f"\n-----Results for {model.corpus_filename} / Level: {model.level} / Order: {model.order}-----\n")
    f.write(model.generate(30))
  

def component2f():
  print("-----Component 2f (Check results folder)-----")
  f = open("results/component2f.txt", "a")

  for order in range(1,13):
    f.write(f"\n Order: {order} \n")
    model = MarcovModel("harry_potter_1.txt", "word", order)
    f.write(model.generate(40))

def component2():
  component2a()
  component2b()
  component2c()
  component2d()
  component2e()
  component2f()

if __name__ == "__main__":
  component2f()