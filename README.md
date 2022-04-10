# TextMiningProject

## Explanation
The main branch utilizes huggingface and transformers as a backend for learning. It uses [BERTweet](https://github.com/VinAIResearch/BERTweet) as the transformer model. This model was finetuned using [this](https://www.kaggle.com/andrewmvd/cyberbullying-classification) dataset from Kaggle. This repository is copied from a private repository and does not contain all past pushes and branches.

## How to run
**Attention: this branch is enables you to fine tune the model on CPU, this will take a very long time. If available please use a Nvidia CUDA gpu and the [main branch](/../../tree/main)**

1. Install all the required python packages (recommended to do this in a separate conda environment):
```
pip install -r requirements.txt
```
2. Install the [torch package](https://pytorch.org/get-started/locally/) for cpu
```
See the torch website (linked above) for the correct pip command. 
Version used for this project is 1.11.0.
```
3. Download the [kaggle dataset](https://www.kaggle.com/andrewmvd/cyberbullying-classification) and put the csv in the root folder of this project

4. Run data_cleanup.py
```
python data_cleanup.py
```
5. Run transformers.py to update the transformers model
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