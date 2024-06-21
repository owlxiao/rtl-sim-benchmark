import os
import subprocess

base_dir = os.getcwd()
runs_dir = os.path.join(base_dir, "runs")
cases_dir = os.path.join(base_dir, "cases")

simulator_list = []
model_list = []


def load_simulators():
    for simulator in os.listdir(runs_dir):
        simulator_dir = os.path.join(runs_dir, simulator)
        simulator_list.append(simulator_dir)


def load_models():
    for model in os.listdir(cases_dir):
        model_dir = os.path.join(cases_dir, model)
        model_list.append(model_dir)


def main():
    load_simulators()
    load_models()

    print(simulator_list)
    print(model_list)


if __name__ == "__main__":
    main()
