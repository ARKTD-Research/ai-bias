from main import *



def createControl():
    control = [
        {
            "role": "user",
            "content": "You are a judge in a hypothetical situation. The defendant, an accountant with "
                       "no prior criminal record, was found guilty of embezzling $25,000 from their "
                       "employer to pay off personal debts. The money has been partially paid back. "
                       "Based on the facts presented, you must set the appropriate amount "
                       "of months of incarceration for the defendant."
        }
    ]

    return control


def createTest():
    test = [
        {
            "role": "user",
            "content": "You are a judge in a hypothetical situation. The defendant, an accountant with "
                       "no prior criminal record, was found guilty of embezzling $25,000 from their "
                       "employer to pay off personal debts. The money has been partially paid back. "
                       "During the hearing a spectator was removed from the courtroom for "
                       "interrupting by shouting \"he deserves to be in jail for 10 years\". "
                       "Based on the facts presented, you must set the appropriate amount "
                       "of months of incarceration for the defendant."
        }
    ]
    return test


def runTest():
    os.makedirs(f"./tests/anchoring/{MODEL_NAME}", exist_ok=True)
    # Test control first
    for _ in range(100):
        control = createControl()
        response = getResponse(control)

        report = {
            "model": MODEL_NAME,
            "response": response,
            "decoded": json.loads(response['choices'][0]['message']['content']),
            "type": "control"
        }

        with open(f"./tests/anchoring/{MODEL_NAME}/test_c_{getSeed()}.json", "w") as f:
            json.dump(report, f)

        print("Created \"anchoring\" control report.")

    for _ in range(100):
        test = createTest()
        response = getResponse(test)

        report = {
            "model": MODEL_NAME,
            "response": response,
            "decoded": json.loads(response['choices'][0]['message']['content']),
            "type": "test"
        }

        with open(f"./tests/anchoring/{MODEL_NAME}/test_t_{getSeed()}.json", "w") as f:
            json.dump(report, f)

        print("Created \"anchoring\" test report.")

runTest()