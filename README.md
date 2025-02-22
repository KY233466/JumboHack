# LLMProxy

This repository contains example code written in Python that demonstrates how to use the `LLMProxy`. The `LLMProxy` provides access to LLMs and the ability to upload documents that may be useful for additional context (see RAG).
The APIs exposed are `generate()`, `pdf_upload()`, and `text_upload()`.

---

## Getting Started

### Running the Python Example
1. Install Python 3.x and required dependencies by running the setup script:
    ```
    bash setup.sh
    ```
    If you already have Python and pip installed, you can directly install the requirements:
    `python3 -m pip install -r requirements.txt`

2. Add your API access key to config.json
3. Execute the example Python scripts:
    ```
    python3 example_gen.py
    ```

## API reference

### generate()
The generate() function sends a request to LLMProxy to generate a response based on the provided parameters.

#### Example Usage:
```
response = generate(
    model="4o-mini",
    system="Answer my question",
    query="What is the capital of France?",
    temperature=0.7,
    lastk=0,
    session_id='GenericSession',
)
```

For the `model` parameter the following options are available:
1. `4o-mini`
2. `anthropic.claude-3-haiku-20240307-v1:0`
3. `azure-phi3`
---

### text_upload()
The text_upload() function adds the provided string to the provided session's context, to be used for future generate() calls if relevant.
It may take some time for the provided information to be added to the session's context.

#### Example Usage:
```
response = text_upload(
    text = "The purple dinosaur lives in the yellow mountains",
    strategy = 'fixed',
    description = 'Information about where the purple dinosaur lives',
    session_id='GenericSession',
)
```

For the `strategy` parameter the following options are available:
1. `smart`
2. `fixed`

When the `smart` strategy is specified, the LLMProxy uses an LLM to chunk the provided information.
The `fixed` strategy chunks the information into fixed-sized chunks of a default length.

### pdf_upload()
Similar to text_upload(), the pdf_upload() function adds the provided document in PDF format to the provided session's context, to be used for future generate() calls if relevant.

#### Example Usage:
```
response = pdf_upload(
    path = "path/to/your/document.pdf",
    strategy = 'smart',
    description = 'The provided pdf contains some information about ABC',
    session_id='GenericSession',
)
```

When uploading PDFs, it is recommended to use the `smart` strategy, although it will take some time to add the document to the session's context.

---

