# AI vs STEP
A Python program that uses only the text from the the 2024 STEP-Practice Exam and runs it through OpenAI and Ollama models to see how each scores and which is the best overall.
- Practice STEP: https://www.usmle.org/sites/default/files/2021-10/Step_1_Sample_Items.pdf


Choose which models to use (line 1229):
    models_to_test = [

        # OpenAI models:
        {"model_name": "gpt-4o", "engine": "openai"},
        {"model_name": "gpt-4o-mini", "engine": "openai"},
        {"model_name": "o1-mini", "engine": "openai"},
        {"model_name": "o1-preview", "engine": "openai"},

        # Ollama models:
        {"model_name": "deepseek-r1:8b-llama-distill-q8_0", "engine": "ollama"},
        #{"model_name": "deepseek-r1:7b-qwen-distill-q8_0", "engine": "ollama"}, #performed poorly, comment out to disable
        {"model_name": "deepseek-r1:14b-qwen-distill-q4_K_M", "engine": "ollama"},
        {"model_name": "openchat:7b-v3.5-1210-q8_0", "engine": "ollama"},
        {"model_name": "llama3.1:8b-instruct-q8_0", "engine": "ollama"}

**To use ChatGPT/OpenAI:** You must set the client.api_key to your OpenAI API Key (line 1075)

**To use Ollama models:** You must be running Ollama and have the proper model name entered. You can check by running the Command Prompt and typing 'ollama list' to see which ollama models you have installed.

**Use this on any test** by replacing the test data at the top with your own, that's it! Must be multiple-choice.
- You can copy/select the text in a PDF and use ChatGPT to provide you the test in a format matching the one provided

