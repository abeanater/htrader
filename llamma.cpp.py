from llama_cpp import Llama

models = [
    r"C:\Users\abram\Downloads\Meta-Llama-3-70B-Instruct.IQ3_XS.gguf",
    r"D:\projects\models\Phi-3-mini-4k-instruct-q4.gguf",
    r"C:\Users\abram\Downloads\llama-3-neural-chat-v1-8b-Q8_0.gguf"
]

llm = Llama(
    model_path=models[1],  # path to GGUF file
    n_ctx=4096,  # The max sequence length to use - note that longer sequence lengths require much more resources
    n_threads=8, # The number of CPU threads to use, tailor to your system and the resulting performance
    n_gpu_layers=81, # The number of layers to offload to GPU, if you have GPU acceleration available. Set to 0 if no GPU acceleration is available on your system.
)

# Truncate or summarize the news article if it's too long
doc = """These Healthcare stocks are trading higher:
-Ocean Biomedical Inc (OCEA) stock is trading at $3.55, an increase of $1.55, or 74.5%, on high volume.
Ocean Biomedical Inc gets a Sentiment Score of Neutral from InvestorsObserver and receives an average analyst recommendation of Strong Buy with a price target of $18.07.
-LAVA Therapeutics NV (LVTX) stock is trading at $3.12, a gain of $0.92, or 44.45%, on moderate volume.
Lava Therapeutics N.V. gets a Sentiment Score of Very Bearish from InvestorsObserver and receives an average analyst recommendation of Strong Buy with a price target of $7.67.
-Ainos Inc (AIMD) stock is trading at $1.38, an increase of $0.33, or 31.43%, on high volume.
Ainos Inc gets a Sentiment Score of Very Bullish from InvestorsObserver. Ainos Inc next reports earnings on March 29.
-Renalytix PLC (RNLX) stock is trading at $1.33, an increase of $0.29, or 27.88%, on high volume.
Renalytix Ai Plc ADR gets a Sentiment Score of Bullish from InvestorsObserver and receives an average analyst recommendation of Strong Buy with a price target of $4.33.
Find the top stocks in the Healthcare Sector here.
These Healthcare stocks are trading lower:
-BioVie Inc (BIVI) stock is trading at $1.09, a decline of $0.8, or 42.59%, on high volume.
Biovie Inc gets a Sentiment Score of Bearish from InvestorsObserver and receives an average analyst recommendation of Buy.
-First Wave BioPharma Inc (FWBI) stock is trading at $7.17, a decline of $2.07, or 22.51%, on average volume.
First Wave Biopharma Inc gets a Sentiment Score of Very Bullish from InvestorsObserver and receives an average analyst recommendation of Strong Buy with a price target of $40.00. First Wave Biopharma Inc next reports earnings on March 18.
-Vivani Medical Inc (VANI) stock is trading at $2.44, a loss of $0.65, or 21.36%, on low volume.
Vivani Medical Inc gets a Sentiment Score of Bearish from InvestorsObserver and receives an average analyst recommendation of Strong Buy with a price target of $4.00. Vivani Medical Inc next reports earnings on March 29.
-Cardio Diagnostics Holdings Inc (CDIO) stock is trading at $1.48, a decline of $0.28, or 16.48%, on moderate volume.
Cardio Diagnostics Hldgs Inc gets a Sentiment Score of Bullish from InvestorsObserver and receives an average analyst recommendation of Strong Buy with a price target of $8.00."""

# Prompt to extract the price targets
extract_targets_prompt = (
    "Extract the ticker symbols and their corresponding price targets from the following news article. "
    "Return the results in the format [{'ticker': 'TICKER_SYMBOL', 'price_target': PRICE_TARGET}]. "
    "If no price targets are mentioned, return []."
    "Reply \"TERMINATE\" in the end when everything is done."
)
extract_targets_prompt = f'''Instruction: {extract_targets_prompt}
Input: {doc}
Answer: '''


# Simple inference example with the revised prompt
output = llm(
    extract_targets_prompt,
    max_tokens=1024*2,  # Set a reasonable limit for the output tokens
    stop=["TERMINATE"],  # Use explicit stop sequences
    echo=False,  # Whether to echo the prompt
)

print(output['choices'][0]['text'])
