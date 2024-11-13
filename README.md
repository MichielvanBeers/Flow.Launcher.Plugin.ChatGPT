# Flow Launcher ChatGPT Plugin
This plugin allows you to use OpenAI's ChatGPT models (gpt-3.5-turbo and gpt-4) with [Flow Launcher](https://www.flowlauncher.com/).

![Demo video of the Flow Launcher ChatGPT Plugin](https://i.imgur.com/WQwNY7y.gif)

## Features
- 💡 Set which chat model you want to use (gpt-3.5-turbo or gpt-4)
- 📝 Use keywords to select if you want a short, long or standard answer
- 💬 Add custom keywords and system prompts to change the style and content of the output
- 🗃️ Copy the answer or open it in a new text file
- ✋ Activate the query via a custom "stop keyword"

## Prerequisites
1. An account at OpenAI.
2. A payment method configured in your OpenAI profile [here](https://platform.openai.com/account/billing/payment-methods).
3. An API key for OpenAI that can be retrieved [here](https://platform.openai.com/account/api-keys).

## Installation
1. Download and install [Flow Launcher](https://www.flowlauncher.com/).
2. Launch Flow Launcher, then enter `Settings` to open its settings.
3. Go to the `Plugin Store` module.
4. Search for `ChatGPT`.
5. Click `ChatGPT` and then `Install`.
6. `Flow Launcher` should automatically restart. If not, manually restart `Flow Launcher`.
7. Go to the `Plugins` module in Flow Launcher.
8. The ChatGPT plugin should be visible. Select it.
9. Paste your OpenAI API key in the API Key field.
10. Adjust the setting (see below) to your own liking.
11. Run the 'Save Settings' command in Flow Launcher.

## Usage
### Basic
1. Activate by using the `ai` keyword.
2. Type any prompt and add the stop keyword at the end (default: `||`).
3. Wait until the list is updated.
4. Copy the content or open it in a new text file.

### Using system prompts
System prompts are the messages that are being sent to ChatGPT to set the behavior of the responses. System prompts can be activated by adding a Keyword at the start of the sentences. When no Keyword is found, the default system prompt will be used (see below).

By default the plugin contains the following system prompts:
|Keyword | System Prompt |
|---------|---------------|
|normal|You are an all-knowing AI bot.|
|short|You are an all-knowing AI bot. All your answers are short, to the point, and don't give any additional context.|
|long|You are an all-knowing AI bot. All your answers are in-depth and give both a step-by-step explanation how you came to that answer, as well as references to the resources you used.|

The different outputs for the prompt "Test" are as follows:
|Keyword| Output|
|--------|-------|
|normal|I'm here to help. How may I assist you with your test?|
|short|Passed.|
|long|As an all-knowing AI bot, when I receive the input "test," I determine whether you are asking me to provide a test-related response or evaluate my knowledge and capabilities. Here, your query is brief and ambiguous, but I will provide an example of how I process and respond to questions. Step 1: Analyze the input: I examine the key term "test" and search for relevant context or additional details to understand your intention. Step 2: Generate a response: Based on your input, I try to cover the evident possibilities in my reply, thus accommodating your potential purpose. This includes testing my understanding, problem-solving capabilities, or demonstrating my knowledge on a specific topic. Step 3: Retrieve relevant resources: Since you did not provide specific details with your query, I cannot include references or resources that support my response. However, a more contextually-rich question will allow me to conduct comprehensive research and cite appropriate resources If you can provide additional information or clarify the context for your query, I will be able to generate an in-depth response based on your request. 

## Adding your own system prompts
You can add your own prompts in the following way:
1. Open Flow Launcher.
2. Type `Settings`.
3. Go to Plugins -> ChatGPT.
4. Click the small folder icon.
5. In the folder that opens, open `system_messages.csv`.
6. In the first column, add a new Keyword (without spaces).
7. In the second column, add the System Prompt that you would like to trigger with that Keyword.
8. Save the file.

Check out [this Github page](https://github.com/f/awesome-chatgpt-prompts) for some awesome prompts.

## Settings
|Setting|Description|Default value|
|-------|-----------|-------------|
|Action keyword|keyword to type to enable this plugin|_ai_|
|API Key|API Key to use with OpenAI's API's. Can be found [here](https://platform.openai.com/account/api-keys).|_none_|
|Model|The ChatGPT model version that will be used to call the API. Note: you need access to the model to be able to use it.|_gpt-3.5-turbo_|
|Prompt stop|Characters at the end of the sentence that will trigger the search| &#124;&#124; |
|Default system prompt|The default keyword that will be used to lookup a System Prompt when no specific prompt has been given.| _normal_ |
|Custom URL|Custom OpenAI Format API endpoint|_https://api.openai.com/v1/chat/completions_|

# Backlog
* Ability to take into account the context of the previous prompts.
