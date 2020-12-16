### Install spell check
- [jupyterlab_spellchecker](https://github.com/ijmbarr/jupyterlab_spellchecker)

### Using debug in jupyter lab
- A visual debugger for Jupyter [watch on youtube](https://www.youtube.com/watch?v=CdZN_vVfHqw)
- [install jupyterlab/debugger](https://github.com/jupyterlab/debugger)

### Installation Command
```
conda create -n jupyterlab-debugger -c conda-forge xeus-python=0.8.0 notebook=6 jupyterlab=2 ptvsd nodejs
conda activate jupyterlab-debugger

jupyter labextension install @jupyterlab/debugger

conda install xeus-python jupyterlab -c conda-forge

pip install --upgrade ptvsd

jupyter lab
```
