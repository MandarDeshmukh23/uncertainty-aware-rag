import math
from openai import OpenAI
from src.core.config import settings

# Point the standard OpenAI client to your local Ollama engine
client = OpenAI(
    base_url=settings.llm_base_url,
    api_key="ollama"  # Required by the SDK, but ignored by the local server
)

def calculate_generative_uncertainty(logprobs_data) -> float:
    """
    Calculates the average token confidence from logarithmic probabilities.
    Returns a score between 0.0 and 1.0.
    """
    if not logprobs_data or not hasattr(logprobs_data, 'content') or not logprobs_data.content:
        # Fallback if the specific model configuration omits logprobs
        return 1.0 
        
    total_prob = 0.0
    count = 0
    
    for token_info in logprobs_data.content:
        # Convert log probability back to linear probability: P = e^(logprob)
        prob = math.exp(token_info.logprob)
        total_prob += prob
        count += 1
        
    return total_prob / count if count > 0 else 1.0

def generate_answer(query: str, retrieved_chunks: list[dict]) -> dict:
    """
    Combines retrieved context with the user query to generate a probabilistic answer.
    """
    # 1. Format the context
    context_text = "\n\n".join([chunk["text"] for chunk in retrieved_chunks])
    
    prompt = f"""You are a precise technical assistant. Answer the user's query ONLY using the context below. 
    If the answer is not in the context, say 'I do not have enough information to answer.'
    
    Context:
    {context_text}
    
    Query: {query}
    """

    # 2. Call the local LLM
    response = client.chat.completions.create(
        model=settings.llm_model_name,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.0, # Greedy decoding minimizes variance for factual RAG
        logprobs=True,   # Explicitly request token probabilities
        top_logprobs=1
    )
    
    answer = response.choices[0].message.content
    
    # 3. Evaluate mathematical confidence
    raw_logprobs = response.choices[0].logprobs
    confidence_score = calculate_generative_uncertainty(raw_logprobs)
    
    return {
        "answer": answer,
        "confidence_score": confidence_score,
        "is_uncertain": confidence_score < 0.65 # Flag as uncertain if confidence drops below 85%
    }