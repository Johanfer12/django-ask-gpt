# Ask your Docs

This Django model enhances your document interaction by integrating OpenAI's text embedding and GPT-3.5-turbo chat completion models. It simplifies querying a collection of precomputed text embeddings and generating responses using GPT-3.5-turbo.

## Usage

1. **Initialization:** Prior to using `ChatModel`, set your OpenAI API key in the environment variable `OPENAI_API_KEY_H`. The `initialize` method configures the necessary data structures.

    ```python
    ChatModel.initialize()
    ```

2. **Querying Related Strings:** Discover related strings to a query and their relatedness scores with the `strings_ranked_by_relatedness` method.

    ```python
    strings, relatednesses = ChatModel.strings_ranked_by_relatedness(query, top_n=100)
    ```

3. **Generating Messages for GPT-3.5-turbo:** Create a message for GPT-3.5-turbo based on related strings and a specified token budget using the `query_message` method.

    ```python
    message = ChatModel.query_message(query, token_budget)
    ```

4. **Asking Questions:** Utilize the `ask` method to input a query and generate a response using GPT-3.5-turbo.

    ```python
    response = ChatModel.ask(query, token_budget=4096 - 500)
    ```

## Dependencies

- Django (for Django model usage)
- OpenAI Python library
- pandas
- tiktoken
- scipy
- scikit-learn

## Note

Ensure that the required Python packages (`Django`, `openai`, `pandas`, `tiktoken`, `scipy`, `scikit-learn`) are installed before deploying `ChatModel`.

## License

This code is distributed under the [MIT License](LICENSE).

# Process Docs View

The `ProcessFilesView` in this Django application streamlines document management. It facilitates file uploads, automatic processing of unprocessed files, and displays lists of uploaded and processed files. The interface ensures a user-friendly experience.

## Usage

1. **Upload Files:**
   - Select the "Upload File" button to upload documents from your device. The list of uploaded files updates automatically.

2. **Process Files:**
   - Click the "Process" button to automatically process the uploaded files. Processed files are displayed in the corresponding list.

3. **File Visualization:**
   - Clear presentation of both uploaded and processed files for easy identification.

## Considerations

- The view utilizes the `openai` library for text embeddings, involving calls to the OpenAI API.
- Configure your OpenAI API key in the environment before using the view.