from config import *
import requests
import json
import os


def getSeed():
    seed = int.from_bytes(os.urandom(4), byteorder="big")
    return str(seed)


def getResponse(messages):
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
        })
    )

    return response.json()
