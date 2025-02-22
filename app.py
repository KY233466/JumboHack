import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
from llmproxy import generate

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

    print(f"formatted_message {formatted_message}")

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


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
