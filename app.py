import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
from llmproxy import generate
import sys
sys.stdout.reconfigure(encoding='utf-8')


app = Flask(__name__)
CORS(app)


@app.route('/api/advising', methods=['POST'])
def main():
    data = request.get_json()

    user_message = data.get("query", "").strip()
    if not user_message:
        return jsonify({"response": "Please enter a message."})

    formatted_message = f"Tufts: {user_message}"

    system_prompt = f"""
        #### Instructions ####
        You are an academic advisor bot helping students with school policy questions. Your response should be in
            markdown and be structured with:
            1. A **one-sentence summary** that directly answers the student's question.
            2. A **detailed explanation** following the summary.
        
        Strict Rules:
        1. Do not repeat the question back to the student.
        2. If no conclusion could be drawn from the information, say so. If more information from the student 
            is needed to form a conclusion, ask the student for clarification. List the possible conclusions 
            depending on student responses.
        3. If ONLY conclusion is still reached with rule #2, ask the student to email their advisors.
        4. The summary must be **one sentence** that highlights the key answer.
        5. If the [Explanation] is too long, break it down into paragraphs. Make sure that the transition is 
            smooth and each paragraph talks about different ideas.
        6. Maintain a professional yet approachable tone and make the sentences clear and concise. If the student 
            expresses stress or concern, respond with empathy. 
        7. Ensure the response is formal but not excessively rigid.  
        8. Only use information from the provided materials — avoid assumptions.  
    """

    print(f"formatted_message {formatted_message}".encode('utf-8', errors='replace').decode('utf-8'))

    response = generate(
        model='4o-mini',
        system=system_prompt,
        query=formatted_message,
        temperature=0.0,
        lastk=0,
        rag_usage=True,
        rag_threshold=0.6,
        rag_k=6,
        session_id='ky_rag_test',
    )

    return jsonify({"response": response})

@app.route('/api/advising/email', methods=['POST'])
def process_email():
    try:
        data = request.get_json()
        email_text = data.get("email", "").strip()
        if not email_text:
            return jsonify({"response": "Please provide an email message."}), 400

        # Step 2: Extract questions from the email using the language model.
        extraction_prompt = f"""
        You are an assistant tasked with extracting all the distinct questions from an email.
        Please list each question on a separate line.
        Email:
        {email_text}
        """
        extraction_response = generate(
             model='4o-mini',
             system=extraction_prompt,
             query=email_text,
             temperature=0.0,
             lastk=0,
             rag_usage=False,
             session_id='ky_rag_email_extract'
        )
        
        # Log the raw extraction result for debugging.
        return extraction_response

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
