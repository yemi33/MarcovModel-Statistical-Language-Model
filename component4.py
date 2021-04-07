from MarcovModel import MarcovModel
from datetime import datetime
import statistics

def component4d():
  print("-----Component 4d (Check results folder)-----")
  model1 = MarcovModel("franz_kafka_collected_works.txt", "word", 3)
  model2 = MarcovModel("practice_phrenology_simplified.txt", "word", 3)
  model3 = MarcovModel("william_shakespeare_collected_works.txt", "word", 3)

  models = [model1, model2, model3]

  f = open("results/component4d.txt", "a")

  length_of_test_input = 60
  for model in models:
    f.write(f"\n\n-----Estimation Results for {model.corpus_filename}-----\n")
    for estimator_model in models:
      f.write(f"\n-----When estimated by: {estimator_model.corpus_filename}-----\n")
      estimates = []
      text = ""
      nextPos = 0
      while nextPos < (len(model.testset) - length_of_test_input):
        text = model.testset[nextPos:nextPos + length_of_test_input]
        estimate = estimator_model.estimate(text)
        # print(estimate)
        estimates.append(estimate)
        text = ""
        nextPos += length_of_test_input
      f.write(f"{statistics.mean(estimates)}")

def component4f():
  # intentionally chose Franz Kafka and Edgar Allan Poe because we thought they were similar
  print("-----Component 4f (Check results folder)-----")
  f = open("results/component4f.txt", "a")
  for order in range(1, 4):
    f.write("\n Level: Word\n")
    f.write(f"\n Order: {order}\n")
    model1 = MarcovModel("franz_kafka_collected_works.txt", "word", 1)
    model2 = MarcovModel("edgar_allan_poe_collected_works.txt", "word", 1)

    models = [model1, model2]

    length_of_test_input = 60
    for model in models:
      f.write(f"\n\n-----Estimation Results for {model.corpus_filename}-----\n")
      for estimator_model in models:
        f.write(f"\n-----When estimated by: {estimator_model.corpus_filename}-----\n")
        estimates = []
        text = ""
        nextPos = 0
        while nextPos < (len(model.testset) - length_of_test_input):
          text = model.testset[nextPos:nextPos + length_of_test_input]
          estimate = estimator_model.estimate(text)
          # print(estimate)
          estimates.append(estimate)
          text = ""
          nextPos += length_of_test_input
        f.write(f"{statistics.mean(estimates)}")

def component4():
  component4d()
  component4f()

if __name__ == "__main__":
  component4f()
