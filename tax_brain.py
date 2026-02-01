# tax_brain.py
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# --- 1. THE KNOWLEDGE BASE (You can add more rules here) ---
# This is where you "Train" your AI.
knowledge_base = [
    {
        "question": "How to save tax on salary?",
        "answer": "To save tax on salary, you can use: 1. Section 80C (PPF, EPF, ELSS) up to ₹1.5 Lakh. 2. Section 80D (Health Insurance) up to ₹25,000. 3. HRA exemptions if you live in a rented house."
    },
    {
        "question": "What is the difference between Old and New Regime?",
        "answer": "The New Regime has lower tax rates but fewer deductions (No 80C, 80D). The Old Regime has higher rates but allows you to claim deductions. If your deductions are > ₹3.75 Lakh, choose Old Regime."
    },
    {
        "question": "What is standard deduction?",
        "answer": "Standard Deduction is a flat ₹50,000 (increased to ₹75,000 in recent updates) deduction available to all salaried employees, regardless of actual expenses."
    },
    {
        "question": "Is interest on savings bank taxable?",
        "answer": "Yes, but under Section 80TTA, interest up to ₹10,000 is tax-free for individuals below 60 years."
    },
    {
        "question": "What is Section 80C?",
        "answer": "Section 80C allows a maximum deduction of ₹1.5 Lakh per year. Investments include LIC, PPF, EPF, and 5-year Fixed Deposits."
    },
    {
        "question": "How do I file ITR?",
        "answer": "You can file ITR via the official Income Tax portal. You need Form 16 from your employer. Our Sahaj Tax AI can help you calculate your liability first!"
    },
    {
        "question": "Hi hello hey",
        "answer": "Hello! I am Sahaj Tax AI. Ask me anything about Indian Taxes, Deductions, or Form 16."
    }
]

def get_custom_response(user_query):
    """
    My Custom AI Engine:
    1. Vectorizes the user's query.
    2. Compares it against the Knowledge Base using Cosine Similarity.
    3. Returns the best match.
    """
    try:
        # Prepare data
        questions = [item["question"] for item in knowledge_base]
        
        # Add user query to the list temporarily to compare it
        all_text = questions + [user_query]

        # --- THE AI MAGIC (Vectorization) ---
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform(all_text)

        # Calculate Similarity (Last item is user query, compare to all others)
        user_vector = tfidf_matrix[-1]
        question_vectors = tfidf_matrix[:-1]

        similarity_scores = cosine_similarity(user_vector, question_vectors)
        
        # Find the highest score
        best_match_index = np.argmax(similarity_scores)
        best_score = similarity_scores[0][best_match_index]

        # Threshold: If similarity is too low (< 0.2), the AI is confused.
        if best_score < 0.2:
            return "I am not sure about that. I only know about Indian Tax Rules. Can you ask differently?"
        
        return knowledge_base[best_match_index]["answer"]

    except Exception as e:
        return f"Error in AI Engine: {str(e)}"