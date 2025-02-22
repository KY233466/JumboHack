from llmproxy import pdf_upload

if __name__ == '__main__':
    response = pdf_upload(
        path = '2024-2025_Bulletin.pdf',
        session_id='ky_rag_test',
        strategy = 'smart')

    print(response)
