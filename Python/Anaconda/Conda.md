# Anaconda

## Virtual Environments

- Disable starting base virtual environment by default:

  - `conda config --set auto_activate_base false`

- Conda keeps creating environments in users folder
  - Create an environment with a prefix: `conda create --prefix="C:\anaconda\envs\envname"`

### Environments in custom folder

- To create with a name, cd into the env directory you want to the env to be in and then run `conda create -n myname pip`
  - Add pip at the end so the environment has it's own pip.exe and ipykernel for jupyter notebook
- Create an environment with a prefix: `conda create --prefix="C:\anaconda\envs\envname"` (this does not give it a name though)
- Activate with `conda activate "C:\anaconda\envs\envname"`
