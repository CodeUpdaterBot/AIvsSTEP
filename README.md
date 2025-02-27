# AI vs STEP
A Python program that uses ****only the text**** from the the 2024 STEP-Practice Exams 1-3 and runs it through OpenAI, Claude, Groq, OpenRouter, and open-source Ollama models to see how each scores and which is the best overall.

![o1](https://github.com/user-attachments/assets/96a8ab8a-0b60-4496-a6ab-5e4e3f3ffa18)

![Step1-3 All models](https://github.com/user-attachments/assets/b7e54165-d322-40c3-a1a2-248afb83df92)

Models used (2-2-2025):

    mistralai/mistral-large-2411, qwen/qwen-max, meta-llama/llama-3.1-405b-instruct, deepseek-r1-distill-llama-70b, mistralai/mistral-small-24b-instruct-2501, deepseek/deepseek-r1, gpt-4o, gpt-4o-mini, o1-mini, o1-preview, o3-mini-low, o3-mini-medium, o3-mini-high, claude-3-5-haiku-latest, claude-3-5-sonnet-20241022, claude-3-opus-latest]

Choose which models to use at the bottom (uncomment to run):

    ### Open Source APIs
    {"model_name": "mistralai/mistral-large-2411", "engine": "openrouter"},
    {"model_name": "qwen/qwen-max", "engine": "openrouter"},
    {"model_name": "meta-llama/llama-3.1-405b-instruct", "engine": "openrouter"},
    {"model_name": "deepseek-r1-distill-llama-70b", "engine": "groq"},
    {"model_name": "mistralai/mistral-small-24b-instruct-2501", "engine": "openrouter"},
    {"model_name": "llama-3.3-70b-versatile", "engine": "groq"},
    {"model_name": "deepseek/deepseek-r1", "engine": "openrouter"},

    ### OpenAI
    {"model_name": "gpt-4o", "engine": "openai"},
    {"model_name": "gpt-4o-mini", "engine": "openai"},
    {"model_name": "o1-mini", "engine": "openai"},
    {"model_name": "o1-preview", "engine": "openai"},
    {"model_name": "o3-mini-low", "engine": "openai"},
    {"model_name": "o3-mini-medium", "engine": "openai"},
    {"model_name": "o3-mini-high", "engine": "openai"},

    ### Claude / Anthropic
    {"model_name": "claude-3-5-haiku-latest", "engine": "claude"},
    {"model_name": "claude-3-5-sonnet-20241022", "engine": "claude"},
    {"model_name": "claude-3-opus-latest", "engine": "claude"},

    ### Ollama (local)
    #{"model_name": "mistral-small:24b-instruct-2501-q8_0", "engine": "ollama"},
    #{"model_name": "deepseek-r1:14b-qwen-distill-q4_K_M", "engine": "ollama"},
    #{"model_name": "mistral-small:24b-instruct-2501-q4_K_M", "engine": "ollama"},
    #{"model_name": "openchat:7b-v3.5-1210-q8_0", "engine": "ollama"},
    #{"model_name": "llama3.1:8b-instruct-q8_0", "engine": "ollama"},

## Run with:
Python - https://www.python.org/downloads/

    C:\Users\PC\Downloads\medbot>python main.py

cd to the folder where the main.py file is stored and run
 `python main.py` 
 - See imports at the top of main.py, you might have to pip install a library like 'pip install anthropic'

## **To use ChatGPT/OpenAI:**

 You must set the openai.api_key to your OpenAI API Key

## **To use Claude/Anthropic:**

 You must set the anthropic_api_key to your Claude API Key

## **To use Groq:**

 You must set the groq_api_key to your Groq API Key

## **To use OpenRouter (any LLM/Model):**

 You must set the Bearer Authorization to your OpenRouter API Key

## **To use Ollama models:**

 You must be running Ollama and have the proper model name entered. You can check by running the Command Prompt and typing 'ollama list' to see which ollama models you have installed. 
- You only need a few GB of vRAM (GPU/video card memory) to run your own AI models for free

## **Use this on any test**

 By replacing the test data at the top with your own. Must be multiple-choice.
- You can copy/select the text in a PDF and use ChatGPT to provide you the test in a format matching the one provided

Note: From what I count in Step 1, there are 5 images that actually require interpretation to get it correct, meaning the best score possible is 95.8% (unless it guesses lucky on one of those). This runs on only the text of the questions.

Practice STEP 1: https://www.usmle.org/sites/default/files/2021-10/Step_1_Sample_Items.pdf
Step 2 & 3 are from the same source, see them in the .py file
You can Ctrl+A to select the content of a PDF, and have ChatGPT convert it to a python dictionary for you (provide it a few of the existing ones so it can match it exactly)
