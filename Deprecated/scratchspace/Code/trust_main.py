from experiment import run_experiment
import os


if __name__ == "__main__":
    # Go to the directory of this script
    os.chdir(f'{os.path.dirname(os.path.realpath(__file__))}/..')

    # Launch the experiment using the configuration specified in parameters.py
    run_experiment()
