from llmproxy import pdf_upload

if __name__ == '__main__':
    # response = pdf_upload(
    #     path = '2024-2025_Bulletin.pdf',
    #     session_id='ky_rag_test',
    #     strategy = 'smart')
    
    # response = pdf_upload(
    #     path = '2023-2024_Bulletin.pdf',
    #     session_id='ky_rag_test',
    #     strategy = 'smart')
    
    # response = pdf_upload(
    #     path = '2022-2023_Bulletin.pdf',
    #     session_id='ky_rag_test',
    #     strategy = 'smart')

    # response = pdf_upload(
    #     path = '2021-2022_Bulletin.pdf',
    #     session_id='ky_rag_test',
    #     strategy = 'smart')

    # response = pdf_upload(
    #     path = '2020-2021_Bulletin.pdf',
    #     session_id='ky_rag_test',
    #     strategy = 'smart')

    # response = pdf_upload(
    #     path = '2019-2020_Bulletin.pdf',
    #     session_id='ky_rag_test',
    #     strategy = 'smart')

    # response = pdf_upload(
    #     path = 'Deans_List_Honors.pdf',
    #     session_id='ky_rag_test',
    #     strategy = 'smart')

    # response = pdf_upload(
    #     path = 'Academic_Standing_Progress.pdf',
    #     session_id='ky_rag_test',
    #     strategy = 'smart')

    # response = pdf_upload(
    #     path = 'Transfer_of_Credit.pdf',
    #     session_id='ky_rag_test',
    #     strategy = 'smart')

    # response = pdf_upload(
    #     path = 'Deans_Forms.pdf',
    #     session_id='ky_rag_test',
    #     strategy = 'smart')

    response = pdf_upload(
        path = 'writing_req_faq.pdf',
        session_id='ky_rag_test',
        strategy = 'smart')

    response = pdf_upload(
        path = 'writing_req.pdf',
        session_id='ky_rag_test',
        strategy = 'smart')

    print(response)
