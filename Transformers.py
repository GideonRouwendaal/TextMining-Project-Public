print("Loading libraries")
from transformers import AutoTokenizer, DataCollatorWithPadding, TextClassificationPipeline, AutoModelForSequenceClassification, TrainingArguments, Trainer
from datasets import Dataset
import pandas as pd
import os
from sklearn.model_selection import train_test_split

#Parameters
num_train_epochs = 20
batch_size = 16 #batch  size is grad_acc * batch size. Keep batch size 4 times smaller than grad_acc
gradient_accumulation_steps = 64
transformer_location = "vinai/bertweet-base" #Define a huggingface transformer location
#Set seeds for reproducability
seed = 1234

#Assign the model tokenizer
tokenizer = AutoTokenizer.from_pretrained(transformer_location, normalization=True)
#Tokenize and preprocess the tweet using the tokenizer from the defined model
def tokenize_text(tweet):
    return tokenizer(tweet["text"], truncation=True)

#Read the tweets csv file
print("Reading and transforming data")
tweets = pd.read_csv("cyberbullying_tweets(good).csv")
#Rename the dataframe columns to label and text, this has to be done for tensorflow to understand where the labels are
tweets = tweets.rename(columns={"cyberbullying_type": "label", "tweet_text": "text"})
#Convert the labels to 0-5
tweets.label = pd.Categorical(tweets.label)
tweets['label'] = tweets.label.cat.codes

#Split the dataset into testing and training.
tweets_train, _, _, _ = train_test_split(tweets, tweets['label'], test_size=0.2, random_state=seed)

#Convert the loaded tweets to a huggingface dataset
dataset = Dataset.from_pandas(tweets_train)
#Tokenize all words in the dataset using the function defined above
print("Tokenizing Data")
tokenized_dataset = dataset.map(tokenize_text, batched=True)
#Init the data collator, enables batching and padds each batch
data_collator = DataCollatorWithPadding(tokenizer=tokenizer)
#Define the model
model = AutoModelForSequenceClassification.from_pretrained(transformer_location, num_labels=6)

#Set huggingface training arguments, currently optimized for speed and vram reduction
training_args = TrainingArguments(
    output_dir="./results",
    learning_rate=2e-5,
    per_device_train_batch_size=batch_size,
    per_device_eval_batch_size=batch_size,
    gradient_accumulation_steps=gradient_accumulation_steps,
    num_train_epochs=num_train_epochs,
    weight_decay=0.01,
    gradient_checkpointing=True,
    fp16=True,
    optim="adafactor",
    report_to="none"
)
#Set the huggingface trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset,
    eval_dataset=tokenized_dataset,
    tokenizer=tokenizer,
    data_collator=data_collator,
)
print("Starting training")
train = trainer.train()

#Define a pipeline so we can predict but also store the model and tokenizer
pipe = TextClassificationPipeline(model=model, tokenizer=tokenizer, return_all_scores=True)
#Check if Models folder exists, if not create
models_folder_check  = os.path.isdir('Models')
if not models_folder_check:
    os.makedirs('Models')
    print('Created Models folder as it was not present')
#Store the pipeline to folder
pipe.save_pretrained("Models/Transformer")
print("Saved pipeline")