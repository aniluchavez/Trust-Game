# MAIN FUNCTION OF THE TASK. RUN AS IS
# Parameters for the task are located in Code/Classes/Parameters.py
if __name__ == "__main__":
    # Go to the directory of this script
    import os
    os.chdir(f'{os.path.dirname(os.path.realpath(__file__))}')
    print(f'{os.path.dirname(os.path.realpath(__file__))}')

    # Launch the experiment
    from Code.experiment import run_experiment
    run_experiment()
