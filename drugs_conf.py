system_prompt="""
""" #"""You are a helpful assistant."""

#paste huge thing of text here:
content = """Write an epic rap battle between William Rowe Hamilton and Lord Kelvin"""

#Write what you want it to do with the huge thing of text here.
instruction = """Write an epic rap battle between William Rowe Hamilton and Lord Kelvin
"""


questions_list = []


QA = [
]
q_prepend = ["A) ", "B) ", "C) ", "D) "]

def generateQs(iteration):
    q_string ="""
Please answer the following questions about the text above. 

"""
    for q, answers in QA:
        q_string += f"""
{q}
"""
        for i in range(len(answers)):
            selected = (i+iteration)%len(answers)
            q_string += f"""
    {q_prepend[i]}{answers[selected]}
"""
    return q_string



import numpy as np
import torch
import torch.nn.functional as F
def print_top_k_logits_histogram(logits, tokenizer, top_k=10, max_width=100):
    """
    Print a histogram of the top_k predicted next tokens' logits in the console,
    after applying a softmax to convert logits to probabilities. The token text
    and its probability are right-aligned.

    :param logits: A numpy array of logits from a language model prediction.
    :param tokenizer: The tokenizer used with the model to map indices to tokens.
    :param top_k: Number of top logits to display in the histogram.
    :param max_width: The maximum width of the histogram in characters.
    """
    # Extract the last logits (for the last token)
    last_logits = logits[0, -1, :]

    # Apply softmax to convert logits to probabilities
    probabilities = F.softmax(torch.tensor(last_logits), dim=-1).numpy()

    # Get the indices of the top_k probabilities
    top_k_indices = np.argsort(probabilities)[-top_k:]

    # Extract the top_k probabilities
    top_k_probs = probabilities[top_k_indices]

    # Decode tokens and find the maximum length for formatting
    tokens = [tokenizer.decode([idx]) for idx in top_k_indices]
    max_token_length = max(len(token) for token in tokens)

    # Normalize the probabilities to the max_width
    max_prob = max(top_k_probs)
    scaled_probs = (top_k_probs / max_prob) * max_width

    # Print the histogram with right-aligned token text and probability
    print("--- \n")
    for token, prob, raw_prob in zip(tokens, scaled_probs, top_k_probs):
        bar = '#' * int(prob)
        prob_text = f"{raw_prob * 100:.2f}%".rjust(25)  # Probability formatted to two decimal places
        print(f"{bar.ljust(max_width)} {token.rjust(max_token_length*2)}{prob_text}")
    print("---::::"+tokens[len(tokens)-1]+":::   \n")



