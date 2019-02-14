## A script to prepare solid solution directories for ZrO2 -> Y2O3 transformation (4x4x4 supercell)

### Guidelines:

- Copy your `run.job` and `atoms.in` into the data directory. Make sure that `run.job` is configured with respect to the system you want to run your simulations on.

- Replace `jobSubmit.sh` with a job submission file that you would like to use.

- run `prep_sims.py` by executing:
  ```
  python3 prep_sims.py
  ```

The script will create a directory called `output` and subdirectories `simulation0, simulation1, …, simulation128` inside of it. The number after __simulation__ in the subdirectory name represents the number of substitutions made in the `Master.gin` file. The prepared subdirectories are submission ready.
