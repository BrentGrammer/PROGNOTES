# Virtual Environments in Python

## MAIN TOOLS:

- venv - standard builtin virtual environment manager
- pipenv - combo of pip and venv. Combines managing packages and virtual environment together easier
- Anaconda/conda

### PIPENV

#### Start a virtual environment:

`pipenv shell`

Install deps and create a virtual environment at the same time:
`pipenv install`

#### To deactivate: use EXIT

`$ exit`
(this is different from deactivate and will close the subshell created by pipenv as well - it is the recommended way to deactivate a virtual env)

Check path to virtual environment:
`$ pipenv --venv`

#### check python executable:

1. start env with pipenv shell
2. start python in shell: $ python
3. `import sys`
   `sys.executable`
   # prints path to python executable being used (also shows you virtual environment folder)

Convert requirements.txt to Pipfile:
`$ pipenv install -r requirements.txt`
`# will create a Pipfile for the venv automatically`

Display requirements from Pipfile (in requirements.txt format if needed)
`$ pipenv lock -r `

#### Delete and recreate environment from scratch:

`$ pipenv --rm`
`# now you can recreate an environment with the Pipfile information:`
`pipenv install`

#### Deploying to Prod:

- Use the lock file, not the Pipfile to gaurantee working dep versions:
  `$ pipenv lock`
  `$ pipenv install --ignore-pipfile # cmd to install deps in prod`

#### Creating a Virtual Environment with Anaconda:

https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#creating-an-environment-with-commands
Adding to jupyter notebook: https://janakiev.com/blog/jupyter-virtual-envs/

List Environments:
`$ conda info --envs`

CREATE:
`$ conda create --name myenvname optionallibraries`
Ex: `conda create -n myenv python=3.7`

Activate the env:
`$ activate envname`

Deactivate (from the directory of the virtual env):
`$ deactivate`

To create an environment with a specific version of Python:
`conda create -n myenv python=3.4`

To create an environment with a specific version of a package:
`conda create -n myenv scipy=0.15.0`

To create an environment with a specific version of Python and multiple packages:
`conda create -n myenv python=3.4 scipy=0.15.0 astroid babel`

### Installing a virtual environment with venv:

create directory temp and cd into it.

`python -m venv venv`

syntax: `python -m venv <path/to/virtualenv>`

now you will have a ....temp/venv directory

#### To start:

`C:.../temp/venv/Scripts`

(on windows it's Scripts otherwise would be bin)

In that dir, run the activate.bat file to start the env:
`$ activate`

#### To remove a venv, first deactivate it with

`$ deactivate`

then:
`$ rm -rf /path/to/virtualenv`
on windows: `$ rd /s /q "FOLDER_NAME"`
