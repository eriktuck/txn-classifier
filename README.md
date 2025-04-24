# README

Financial modeling for individuals can be improved by referencing past transaction data to establish spending patterns for budgets and financial forecasts. However, transactions must be correctly categorized to be useful for fine-grained analysis. While most individuals can access transaction data from bank and credit card records, labels for each transaction that match the needs of the financial model are typically not available.

This project seeks to create a classifier for transactions for use in a financial model. The model employs the "Conscious Spending Plan" logic promoted by finance coach Ramit Sehti. The model requires at a minimum the labels fixed and discretionary ("guilt-free" according to Sehti), however subclasses like housing, restaurant, etc. are also desired. The  data model for transactions data match that of the service Plaid.

The project leverages techniques from deep learning in two parts:

1.    Train a generative adversarial neural network (CTGAN) to produce realistic training data from a small sample of correctly labeled data
2.    Train a transformer-based neural network to correctly classify the generated transactions with an appropriate label.
3.    Fine-tune a transformer-based neural network (BERT) to compare with custom NN approaches.

**PLEASE FIND NOTEBOOKS ON GOOGLE COLAB**

-   [Transaction Data Generator](https://colab.research.google.com/drive/1c29dSDa1hOkBw3tzefejr3dkUYFZLmJZ#scrollTo=0A8oSTpdgfki)
-   [Transaction Classifier](https://colab.research.google.com/drive/1aBjRTEzCOstnZ6Pyae6QRgce-VLhsZsu#scrollTo=UCsEB0tO9ynK)

## Environment

These notebooks were originally run in Google Colab but may be run locally with appropriate revisions to input file paths. 

>   Google Colab recently updated package versions causing an irresolvable conflict between Gensim which requires numpy <=2.0.0 and other packages. Take care when creating the environment to use pinned package versions.

To reproduce this workflow, use the provided `environment.yml` file to create a conda environment (you should already have Python and conda installed on your system).

After cloning this directory to your system, use the following bash commands to create and activate the environment:

```bashg
conda env create -f environment.yml
conda activate txn_classifier
```

You must have Jupyter Notebook installed on your system to run this analysis. For installation instructions, consult the documentation [here](https://jupyter.org/).

## Data

The initial dataset will be provided by real transaction data as provided by the service Plaid. As I want to protect the real data, if you would like to follow along please provide your own similarly-structured transaction data.

Your data should have at a minimum the columns:

-   date (datetime): data of transaction 
-   merchant_name (str): the name of the merchant (or whatever string is provided by plaid)
-   amount (float): amount of transaction in currency
-   cat_label (str): category label

## Workflow

First run the notebook `txn-data-gen.ipynb` to create synthetic transaction data based on your transaction data. (Upload your transaction data to Google Colab first).

Next run the notebook `txn-data-classifier.ipynb` to repeat the workflow. You may test with either raw transaction data or synthetic transaction data. Run with both to compare outputs. (Again upload your data or the output from the first notebook in Google Colab.)

>   There are two scripts in the scripts folder for extracting transaction data from the service Monarch Money and processing to the correct format. You may run those scripts from the CLI to extract transactions from Monarch Money. You will need to provide your device UUID in a .env file. See the [monarchmoney](https://github.com/hammem/monarchmoney) repo for details.
