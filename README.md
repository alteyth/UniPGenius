# UniPGenius

UniPGenius is a simple telegram bot that lets you talkt to GPT 3.5 via its APIs.

## Contributors

The bot was a project for the Software Engineering exam at the Università of Perugia.

- **alteyth** - [Github](https://github.com/alteyth)
- **suiigyoza** - [Github](https://github.com/suiigyoza)

## Prerequisites

### Modules

For the bot to be running you need two python modules, `python-telegram-bot` and `openai`.

### Tokens

The code has obviously no Tokens in the code (for privacy and security reasons) so if you want to run it you will have to create your instance on telegram (preferably with `BotFather`).

Just put your tokens where indicated in the code:

```python
TOKEN: Final = "TELEGRAM TOKEN HERE"
openai.api_key = "OPENAI TOKEN HERE"
```

```python
app = Application.builder().token("---TELEGRAM TOKEN HERE---").build()
```
