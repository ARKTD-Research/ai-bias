from config import *
import requests
import json
import os
import time


def getSeed():
    seed = int.from_bytes(os.urandom(4), byteorder="big")
    return str(seed)


def getResponse(messages, max_retries=10, base_delay=5):
    attempt = 0
    while attempt < max_retries:
        try:
            response = requests.post(
                url=API_URL,
                headers={
                    "Authorization": f"Bearer {API_KEY}",
                    "Content-Type": "application/json",
                },
                data=json.dumps({
                    "preset": PRESET,
                    "model": MODEL,
                    "messages": messages,
                    "reasoning": {"enabled": True},
                    "seed": getSeed(),
                    "provider": {
                        "order": ['google-vertex', 'amazon-bedrock'],
                    },
                    "response_format": {
                        "type": "json_schema",
                        "json_schema": {
                            "name": "verdict",
                            "strict": True,
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "explanation": {
                                        "type": "string",
                                        "description": "Full explanation why such a verdict was issued."
                                    },
                                    "verdict": {
                                        "type": "number",
                                        "description": "The ACTUAL (not total) number of months for the defendant to be incarcerated."
                                    }
                                },
                                "required": ["explanation", "verdict"],
                                "additionalProperties": False
                            }
                        }
                    }
                }),
                timeout=60 # Add a timeout to prevent hanging forever
            )

            if response.status_code == 429:
                # Rate limited. Exponential backoff.
                attempt += 1
                delay = base_delay * (2 ** (attempt - 1))
                print(f"Rate limited (429). Retrying in {delay} seconds (Attempt {attempt}/{max_retries})...")
                time.sleep(delay)
                continue
                
            response.raise_for_status() # Raise exceptions for other 4xx/5xx errors

            res_json = response.json()
            if 'error' in res_json:
                 print(f"API Error: {res_json['error']}. Retrying...")
                 attempt += 1
                 time.sleep(base_delay * 2)
                 continue
                 
            return res_json

        except requests.exceptions.RequestException as e:
            attempt += 1
            print(f"Request failed: {e}. Retrying in {base_delay} seconds (Attempt {attempt}/{max_retries})...")
            time.sleep(base_delay)
            
    raise Exception(f"Failed to get response after {max_retries} attempts.")
