# Flow Launcher ChatGPT Plugin
This plugin allows you to use the OpenAI's ChatGPT models (gpt-3.5-turbo and gpt-4) with [Flow Launcher](https://www.flowlauncher.com/).

![Demo video of the Flow Launcher ChatGPT Plugin](https://i.imgur.com/WQwNY7y.gif)

## Features
- 💡 Set which chat model you want to use (gpt-3.5-turbo or gpt-4)
- 📝 Use keywords to select if you want a short, long or standard answer
- 💬 Add custom key words and system prompts to change the style and content of the output
- 🗃️ Copy the answer or open in a new text file
- ✋ Add custom stop word to activate the query

## Prerequisites
1. An account at OpenAI
2. An API key for OpenAI that can be retrieved [here](https://platform.openai.com/account/api-keys)

## Installation
1. Download and install [Flow Launcher](https://www.flowlauncher.com/).
2. Go to the [Releases overview](https://github.com/MichielvanBeers/Flow.Launcher.Plugin.ChatGPT/releases)
3. Open Flow Launcher settings by entering `Settings` in Flow Launcher
4. Go the `Plugin Store` module
5. Search for `ChatGPT`
6. Click `ChatGPT` and then `Install` 
8. `Flow Launcher` should automatically restart. If not, Restart `Flow Launcher`
9. Go to the `Plugins` module in Flow Launcher
10. The ChatGPT plugin should be visible
11. Paste your OpenAI API key in the API Key field
12. Adjusting the setting (see below) to your own liking.

## Usage
### Basic
1. Activate by using the `ai` key word
2. Type any prompt and add the stop keyword at the end (default: `||`)
3. Wait until the list is updated
4. Copy the content or open in a new text file

### Adding system prompts
System prompts are the messages that are being send to ChatGPT to set the behavior of the responses. System prompts can be activated by adding the Key Word at the start of the sentences. When no Key Word is found, the default system prompt will be used (see below).

By default the plugin contains the following system prompts:
|Key Word | System Prompt |
|---------|---------------|
|normal|You are an all-knowning AI bot|
|short|You are an all-knowning AI bot. All your answers are short, to the point and don't give any additional context.|
|long|You are an all-knowning AI bot. All you answers are in depth, give both a step-by-step explanation how you came to that answer and references to the resources you used.|

The different outputs for the prompt "Test" are as follows:
|Key word| Output|
|--------|-------|
|normal|I'm here to help. How may I assist you with your test?|
|short|Passed.|
|long|As an all-knowing AI bot, when I receive the input "test," I determine whether you are asking me to provide a test-related response or evaluate my knowledge and capabilities. Here, your query is brief and ambiguous, but I will provide an example of how I process and respond to questions. Step 1: Analyze the input: I examine the key term "test" and search for relevant context or additional details to understand your intention. Step 2: Generate a response: Based on your input, I try to cover the evident possibilities in my reply, thus accommodating your potential purpose. This includes testing my understanding, problem-solving capabilities, or demonstrating my knowledge on a specific topic. Step 3: Retrieve relevant resources: Since you did not provide specific details with your query, I cannot include references or resources that support my response. However, a more contextually-rich question will allow me to conduct comprehensive research and cite appropriate resources If you can provide additional information or clarify the context for your query, I will be able to generate an in-depth response based on your request. 

You can add your own prompts by opening `system_messages.csv` adding a Key Word (without spaces) and a System Prompts that can be used. Check out [this Github page](github.com/f/awesome-chatgpt-prompts) for some awesome prompts.

## Settings
|Setting|Description|Default value|
|-------|-----------|-------------|
|Action keyword|key word to type to enable this plugin|_ai_|
|API Key|API Key to use with the OpenAI API's. Can be found [here](https://platform.openai.com/account/api-keys)|_none_|
|Model|Model that will be used to call the API. Note: you need access to the model to be able to use it.|_gpt-3.5-turbo_|
|Prompt stop|Characters at the end of the sentence that will trigger the search| &#124;&#124; |
|Defaul system prompt|The default key word that will be used to lookup a System Prompt when no specific prompt has been given| _normal_ |