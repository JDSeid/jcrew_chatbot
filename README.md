# JCrew AI Chatbot

### Created by Jake Seidman

## About

This chatbot can answer basic questions about the products at JCrew.

The chatbot was constructed as follows:

1. Index over 4,000 product pages from the JCrew website
2. Scrape information including product name, price, description, and sizes from each product page
3. Create an instance of an OpenAi model
4. Load product information as documents to the AI model
5. Feed user prompts to the model and output its response

## Getting started
Run the following to install the required packages:
```bash
pip install --upgrade pip
pip install -r requirements.txt
```
And the following to start the chatbot
```bash
python chatbot.py
```

## Notes
- The model is currently using an API key I registered at OpenAI. If this key expires for any reason, you may have to generate a new key at https://platform.openai.com/account/api-keys
- ~4000 product pages were indexed and had their data scraped. Due to the large number of requests made, JCrew blocked my ip address from making additional requests, so I was not able to index the entirety of the site.



## Contact Me

For any questions/comments about this repository, contact me at Jacob.Seidman@tufts.edu