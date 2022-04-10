# TextMiningProject

## Explanation
The main branch utilizes huggingface and transformers as a backend for learning. It uses [BERTweet](https://github.com/VinAIResearch/BERTweet) as the transformer model. This model was finetuned using [this](https://www.kaggle.com/andrewmvd/cyberbullying-classification) dataset from Kaggle. This repository is copied from a private repository and does not contain all past pushes and branches.

## How to run
**Attention: the model in this branch can only be run on Nvidia GPU's with CUDA installed, for a CPU only approach please see the [CPU Branch](../../tree/Transformer-CPU).**

1. Install all the required python packages (recommended to do this in a separate conda environment):
```
pip install -r requirements.txt
```
2. Install the [torch package](https://pytorch.org/get-started/locally/) for gpu's
```
See the torch website (linked above) for the correct pip command. 
Version used for this project is 1.11.0+cu113.
```
3. Download the [kaggle dataset](https://www.kaggle.com/andrewmvd/cyberbullying-classification) and put the csv in the root folder of this project

4. Run data_cleanup.py
```
python data_cleanup.py
```
5. Run transformers.py to update the transformers model, finetuning the model takes about 2.6GB of video memory
```
python transformers.py
```
6. Point to the correct file for flask
```
set FLASK_APP=Server
```
7. Run flask
```
flask run
```
8. Open the server on your local host

## Demo
A demo of the webpage can be found on [YouTube](https://youtu.be/EsPP_s-Ag24).
