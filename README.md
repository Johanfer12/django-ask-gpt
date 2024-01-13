# ChatModel

This Django model provides a simple interface for interacting with OpenAI's text embedding and chat completion models. It allows you to query a collection of precomputed text embeddings and generate responses using OpenAI's GPT-3.5-turbo model. (Embedding page to upload documents in progress.)

## Usage

1. **Initialization:** Before using the `ChatModel`, ensure that you have set your OpenAI API key in the environment variable `OPENAI_API_KEY_H`. The `initialize` method sets up the required data structures.

    ```python
    ChatModel.initialize()
    ```

2. **Querying Related Strings:** You can find strings related to a query along with their relatedness scores using the `strings_ranked_by_relatedness` method.

    ```python
    strings, relatednesses = ChatModel.strings_ranked_by_relatedness(query, top_n=100)
    ```

3. **Generating Messages for GPT-3.5-turbo:** Use the `query_message` method to create a message for GPT-3.5-turbo based on the related strings and a specified token budget.

    ```python
    message = ChatModel.query_message(query, token_budget)
    ```

4. **Asking Questions:** The `ask` method takes a query and generates a response using GPT-3.5-turbo.

    ```python
    response = ChatModel.ask(query, token_budget=4096 - 500)
    ```

## Dependencies

- Django (for using Django models)
- OpenAI Python library
- pandas
- tiktoken
- scipy
- scikit-learn

## Note

Ensure you have the required Python packages installed (`Django`, `openai`, `pandas`, `tiktoken`, `scipy`, `scikit-learn`) before using the `ChatModel`.

## License

This code is provided under the [MIT License](LICENSE).
