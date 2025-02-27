from typing import Any
import requests
from flask import Flask, request, jsonify, current_app
from flask_cors import CORS
from llmproxy import generate
import sys
sys.stdout.reconfigure(encoding='utf-8')

app = Flask(__name__)
CORS(app)

def process_email(email_text: str = None):
    # If email_text is not provided, get it from the request body.
    if email_text is None:
        data: Any = request.get_json()
        email_text = data.get("email", "").strip()
    if not email_text:
        current_app.logger.error("No email text provided.")
        return jsonify({"response": "Please provide an email message."}), 400

    current_app.logger.info("Processing email: %s", email_text)
    extraction_prompt = f"""
    You are an assistant tasked with extracting all the distinct questions from an email.
    Please list each question on a separate line.
    Email:
    {email_text}
    """
    try:
        extraction_response = generate(
            model='4o-mini',
            system=extraction_prompt,
            query=email_text,
            temperature=0.0,
            lastk=0,
            rag_usage=False,
            session_id='ky_rag_email_extract'
        )
        current_app.logger.info("Extraction response: %s", extraction_response)
        # If the response is a dict, extract the string from the "response" key.
        if isinstance(extraction_response, dict) and "response" in extraction_response:
            extraction_response = extraction_response["response"]
        return extraction_response
    except Exception as e:
        current_app.logger.error("Error in generate (process_email): %s", str(e))
        return jsonify({"response": "Internal error during extraction."}), 500

@app.route('/api/advising/email', methods=['POST'])
def process_email_route():
    return process_email()

@app.route('/api/advising/batch', methods=['POST'])
def process_email_questions():
    data = request.get_json()
    email_text = data.get("email", "").strip()
    if not email_text:
        return jsonify({"response": "Please provide an email message."}), 400

    try:
        # Use the provided email_text so we don't re-read the request body.
        extraction_response = process_email(email_text)
    except Exception as e:
        app.logger.error("Error calling process_email: %s", str(e))
        return jsonify({"final_response": "An internal error occurred."}), 500

    # Determine extraction_text from the returned value.
    if hasattr(extraction_response, "get_data"):
        extraction_text = extraction_response.get_data(as_text=True)
    elif isinstance(extraction_response, dict):
        extraction_text = extraction_response.get("response", "")
    else:
        extraction_text = extraction_response

    current_app.logger.info("Extraction text: %s", extraction_text)

    # Split the extracted text into individual questions.
    questions = [q.strip() for q in extraction_text.split('\n') if q.strip()]
    if not questions:
        current_app.logger.error("No questions extracted.")
        return jsonify({"final_response": "No questions extracted from the email."})

    # System prompt for generating individual responses.
    system_prompt = """
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

    # Generate individual answers.
    answers = []
    for question in questions:
        formatted_question = f"Question: {question}\n\nAnswer:"
        try:
            answer = generate(
                model='4o-mini',
                system=system_prompt,
                query=formatted_question,
                temperature=0.0,
                lastk=0,
                rag_usage=True,
                rag_threshold=0.6,
                rag_k=6,
                session_id='ky_rag_test'
            )
            if isinstance(answer, dict) and "response" in answer:
                answer = answer["response"]
            answers.append(answer)
        except Exception as e:
            current_app.logger.error("Error generating answer for '%s': %s", question, str(e))
            answers.append("An error occurred processing this question. Please try again.")

    # Combine all individual answers into one block.
    combined_answers = "\n\n".join(answers)
    current_app.logger.info("Combined answers: %s", combined_answers)

    # Final system prompt to combine all responses into one formatted email.
    final_system_prompt = """
You are an academic advisor responding to student emails based on provided materials.
Please combine the following responses into one coherent, formatted email response that follows this format exactly:

{{Reply}}


Guidelines:
1. You part of the advising team for this student. You are one person. DO NOT ask the student to confirm, discuss, or consult with their advising team.
2. Do not repeat the question back to the student.
3. If no conclusion could be drawn from the information, state so and mention that you will get back to the student.
4. If more information is needed to form a conclusion, ask the student for clarification and list possible conclusions.
5. If the reply is too long, break it into paragraphs with smooth transitions.
6. Maintain a professional yet approachable tone and respond with empathy if needed. 
7. Ensure the response is formal but not excessively rigid.
8. Only use information from the provided materials — avoid assumptions.
9. This is only the response part of the email. Do NOT greet the student or sign the email.
10. Whenever you introduce a new topic, idea, or point within your message, start a new paragraph.
11. Whenever there is a change in tone, start a new paragraph. 
12. Because you are talking to one student, address them as "You" unless there are more than one student who have sent you the message.
13. Start a new paragraph at the half-way point of your email.

Combine the following responses:
"""
    try:
        final_response = generate(
            model='4o-mini',
            system=final_system_prompt,
            query=combined_answers,
            temperature=0.0,
            lastk=0,
            rag_usage=True,
            rag_threshold=0.6,
            rag_k=6,
            session_id='ky_rag_final'
        )
        if isinstance(final_response, dict) and "response" in final_response:
            final_response = final_response["response"]
    except Exception as e:
        current_app.logger.error("Error generating final combined answer: %s", str(e))
        final_response = "An error occurred generating the final response. Please try again."

    return jsonify({"final_response": final_response})


@app.route('/api/advising/query', methods=['POST'])
def process_query():
    data = request.get_json()
    email_text = data.get("query", "").strip()
    if not email_text:
        return jsonify({"response": "Please provide an email message."}), 400

    try:
        # Use the provided email_text so we don't re-read the request body.
        extraction_response = process_email(email_text)
    except Exception as e:
        app.logger.error("Error calling process_email: %s", str(e))
        return jsonify({"final_response": "An internal error occurred."}), 500

    # Determine extraction_text from the returned value.
    if hasattr(extraction_response, "get_data"):
        extraction_text = extraction_response.get_data(as_text=True)
    elif isinstance(extraction_response, dict):
        extraction_text = extraction_response.get("response", "")
    else:
        extraction_text = extraction_response

    current_app.logger.info("Extraction text: %s", extraction_text)

    # Split the extracted text into individual questions.
    questions = [q.strip() for q in extraction_text.split('\n') if q.strip()]
    if not questions:
        current_app.logger.error("No questions extracted.")
        return jsonify({"final_response": "No questions extracted from the email."})

    # System prompt for generating individual responses.
    system_prompt = """
        #### Instructions ####
        You are an academic advisor bot helping students with school policy questions. Your response should be in
        PLAIN TEXT and be structured with:
        1. A one-sentence plain-text summary that directly answers the student's question.
        2. A plain-text detailed explanation following the summary.
        
        Strict Rules:
        1. Do not repeat the question back to the student.
        2. If no conclusion could be drawn from the information, say so. If more information from the student 
           is needed to form a conclusion, ask the student for clarification. List the possible conclusions 
           depending on student responses.
        3. If ONLY conclusion is still reached with rule #2, ask the student to email their advisors.
        4. The summary must be one sentence that highlights the key answer.
        5. If the [Explanation] is too long, break it down into paragraphs. Make sure that the transition is 
           smooth and each paragraph talks about different ideas.
        6. Maintain a professional yet approachable tone and make the sentences clear and concise. If the student 
           expresses stress or concern, respond with empathy.
        7. Ensure the response is formal but not excessively rigid.
        8. Only use information from the provided materials — avoid assumptions.
        9. Your response must be ONLY PLAIN TEXT.
        10. Start a new paragraph when you get to the detailed response. The summary will be one paragraph and the
            the detailed response will be another.
    """

    # Generate individual answers.
    answers = []
    for question in questions:
        formatted_question = f"Question: {question}\n\nAnswer:"
        try:
            answer = generate(
                model='4o-mini',
                system=system_prompt,
                query=formatted_question,
                temperature=0.0,
                lastk=0,
                rag_usage=True,
                rag_threshold=0.6,
                rag_k=6,
                session_id='ky_rag_test'
            )
            if isinstance(answer, dict) and "response" in answer:
                answer = answer["response"]
            answers.append(answer)
        except Exception as e:
            current_app.logger.error("Error generating answer for '%s': %s", question, str(e))
            answers.append("An error occurred processing this question. Please try again.")

    # Combine all individual answers into one block.
    combined_answers = "\n\n".join(answers)
    current_app.logger.info("Combined answers: %s", combined_answers)

    # Final system prompt to combine all responses into one formatted response.
    final_system_prompt = """
You are a chatbot responding to student questions based on provided materials.
Please combine the following responses into one coherent, formatted response that follows this format exactly:


Guidelines:
1. If no conclusion could be drawn from the information, say so. If more information from the student 
    is needed to form a conclusion, ask the student for clarification. List the possible conclusions 
    depending on student responses.
2. If ONLY conclusion is still reached with rule #1, ask the student to email their advisors.
3. Do not repeat the question back to the student.
4. If no conclusion could be drawn from the information, state so and mention that you will get back to the student.
5. If more information is needed to form a conclusion, ask the student for clarification and list possible conclusions.
6. If the reply is too long, break it into paragraphs with smooth transitions.
7. Maintain a professional yet approachable tone and respond with empathy if needed.
8. Ensure the response is formal but not excessively rigid.
9. Only use information from the provided materials — avoid assumptions.
10. Tell the user that you do not understand their question.

Combine the following responses:
"""
    try:
        final_response = generate(
            model='4o-mini',
            system=final_system_prompt,
            query=combined_answers,
            temperature=0.0,
            lastk=0,
            rag_usage=True,
            rag_threshold=0.6,
            rag_k=6,
            session_id='ky_rag_final'
        )
        if isinstance(final_response, dict) and "response" in final_response:
            final_response = final_response["response"]
    except Exception as e:
        current_app.logger.error("Error generating final combined answer: %s", str(e))
        final_response = "An error occurred generating the final response. Please try again."

    return jsonify({"final_response": final_response})


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
