# AI vs STEP
A Python program that uses ****only the text**** from the the 2024 STEP-Practice Exam and runs it through OpenAI, Claude, and open-source Ollama models to see how each scores and which is the best overall.
- Practice STEP: https://www.usmle.org/sites/default/files/2021-10/Step_1_Sample_Items.pdf


Choose which models to use (line 2745):

        # OpenAI models:
        {"model_name": "gpt-4o", "engine": "openai"},
        {"model_name": "gpt-4o-mini", "engine": "openai"},
        {"model_name": "o1-mini", "engine": "openai"},
        {"model_name": "o1-preview", "engine": "openai"},

        # Claude models:
        {"model_name": "claude-3-5-haiku-latest", "engine": "claude"},
        {"model_name": "claude-3-5-sonnet-20241022", "engine": "claude"},
        {"model_name": "claude-3-opus-latest", "engine": "claude"},

        # Ollama models:
        {"model_name": "deepseek-r1:14b-qwen-distill-q4_K_M", "engine": "ollama"},
        {"model_name": "openchat:7b-v3.5-1210-q8_0", "engine": "ollama"},
        {"model_name": "llama3.1:8b-instruct-q8_0", "engine": "ollama"}

Run with: python main.py (see imports at top, you might have to pip install a library like 'pip install anthropic')

**To use ChatGPT/OpenAI:** You must set the client.api_key to your OpenAI API Key

**To use Claude:** You must set the anthropic_api_key to your Claude API Key

**To use Ollama models:** You must be running Ollama and have the proper model name entered. You can check by running the Command Prompt and typing 'ollama list' to see which ollama models you have installed. 
- You only need a few GB of vRAM (GPU/video card memory) to run your own AI models for free

**Use this on any test** by replacing the test data at the top with your own, that's it! Must be multiple-choice.
- You can copy/select the text in a PDF and use ChatGPT to provide you the test in a format matching the one provided

Note: From what I count, there are 5 images that actually require interpretation to get it correct, meaning the best score possible is 95.8% (unless it guesses lucky on one of those).

