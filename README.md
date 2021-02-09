# NVFEL498

## Setup:
### First setup a conda environment for this project
```
wget https://repo.anaconda.com/archive/Anaconda3-5.3.1-Linux-x86_64.sh
bash ./Anaconda3-5.3.1-Linux-x86_64.sh
conda create -n nvfel python=3.7
conda activate nvfel
pip install -r requirements.txt
```
### Second setup a symlink
We do this so we can access data outside of the project.
Run the following command in the directory with the NVFEL498 git repo:
```
ln -s /nfs/turbo/midas-applied-ds/ ./
```
We can then reference `../midas-applied-ds/` inside this repo to access data.

## Project Structure

- `Data`
	- `Raw`
		- `VED`
			- Vehicle Data
