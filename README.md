# Medication Agent

Terminal-based AI medication assistant that converts natural-language prompts into strict JSON actions and executes them against a local SQLite database.

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)
![OpenRouter](https://img.shields.io/badge/OpenRouter-LLM%20Routing-7C3AED)
![OpenAI SDK](https://img.shields.io/badge/OpenAI%20SDK-Compatible-202123)
![SQLite](https://img.shields.io/badge/SQLite-Local%20Database-003B57?logo=sqlite&logoColor=white)
![dotenv](https://img.shields.io/badge/python--dotenv-Config-ECD53F)
![JSON](https://img.shields.io/badge/JSON-Action%20Responses-000000)

## Tools / Stack
- Language: Python
- Model Provider: OpenRouter
- Client SDK: `openai`
- Local Database: SQLite
- Config: `python-dotenv`
- App Layout: modular package in `app/`

## Overview
This project is a small command-loop assistant with a simple action pipeline:

1. The user types a medication-related request.
2. The model is instructed to return JSON only.
3. The app parses the JSON and reads the `action` field.
4. The matching method on `MedicationService` runs against SQLite.
5. The terminal prints the result.

Implemented flows:
- get all medications
- create a medication
- delete a medication
- get medications by name
- get medications by dosage
- ask for missing information

Partially implemented flow:
- get medication by name and dosage

## Flow
1. `app/agent.py` loads `OPEN_ROUTER_API_KEY` from `.env`.
2. The app initializes an OpenAI-compatible client with the OpenRouter base URL.
3. A system prompt forces the model to respond with one supported JSON action.
4. The app parses the model output with `json.loads(...)`.
5. The parsed action is dispatched to `MedicationService`.
6. `app/services/medication_service.py` performs the SQLite operation using `data/medications.db`.

## Project Structure
- `app/agent.py` - terminal entrypoint and action dispatcher
- `app/services/medication_service.py` - SQLite-backed medication service
- `app/__init__.py` - package marker
- `app/services/__init__.py` - services package marker
- `data/medications.db` - local SQLite database file
- `requirements.txt` - Python dependencies
- `.env` - local environment variables

## Requirements
- Python 3.10+
- OpenRouter API key

Install:

```bash
py -3 -m venv venv
.\venv\Scripts\activate
py -3 -m pip install -r requirements.txt
```

## Environment Variables (`.env`)

```env
OPEN_ROUTER_API_KEY=your_openrouter_api_key
```

Notes:
- the client points to `https://openrouter.ai/api/v1`
- the current model is `nvidia/nemotron-3-super-120b-a12b:free`
- free OpenRouter models can hit daily request limits

## Run

```bash
.\venv\Scripts\python app\agent.py
```

Type `exit` or `quit` to stop the loop.

## Action Contract

The model is instructed to return JSON only with one of these actions:
- `get_all_medications`
- `create_medication`
- `delete_medication`
- `get_medication_by_name`
- `get_medication_by_dosage`
- `get_medication_by_name_and_dosage`
- `ask_for_missing_info`

Example responses:

```json
{"action": "get_all_medications"}
```

```json
{"action": "create_medication", "name": "Ibuprofen", "dosage": "200mg"}
```

```json
{"action": "delete_medication", "name": "Ibuprofen", "dosage": "200mg"}
```

```json
{"action": "get_medication_by_name", "name": "Ibuprofen"}
```

```json
{"action": "ask_for_missing_info", "message": "Please provide the dosage."}
```

## Example Prompts
- `Show all my medications`
- `Add Ibuprofen 200mg`
- `Delete Ibuprofen 200mg`
- `Find Ibuprofen`
- `Find medications with dosage 200mg`

## Notes
- `MedicationService` creates the `medications` table automatically if it does not exist
- records are stored locally in `data/medications.db`
- successful deletes return a boolean and print a different message when no matching row exists
- malformed JSON from the model is caught and surfaced as an error message
- the combined `name + dosage` lookup path is present in the prompt and service, but the current dispatcher passes the wrong arguments and needs a small fix
- keep `.env` out of git

## Next Improvements
- fix the combined `name + dosage` dispatcher call
- validate action payloads before dispatch
- return cleaner formatted medication output instead of raw SQLite tuples
- add tests for the dispatcher and service methods
- add a fallback provider or paid model path when free limits are exhausted

## License
This project is licensed under the MIT License. See [LICENSE](LICENSE).
