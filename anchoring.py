import os
import glob
from time import sleep

from main import *

TARGET_NUM_CONTROL = 400
TARGET_NUM_TEST = 400

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


def count_existing_files(dir_path, prefix):
    if not os.path.exists(dir_path):
        return 0
    return len(glob.glob(os.path.join(dir_path, f"{prefix}*.json")))


def runTest():
    base_dir = f"./tests/anchoring/{MODEL_NAME}"
    os.makedirs(base_dir, exist_ok=True)
    
    existing_control = count_existing_files(base_dir, "test_c_")
    existing_test = count_existing_files(base_dir, "test_t_")
    
    needed_control = max(0, TARGET_NUM_CONTROL - existing_control)
    needed_test = max(0, TARGET_NUM_TEST - existing_test)
    
    print(f"[{MODEL_NAME}] Existing Controls: {existing_control}, target: {TARGET_NUM_CONTROL}. Need {needed_control} more.")
    print(f"[{MODEL_NAME}] Existing Tests: {existing_test}, target: {TARGET_NUM_TEST}. Need {needed_test} more.")
    
    try:
        # Test control first
        for i in range(needed_control):
            control = createControl()
            response = getResponse(control)

            report = {
                "model": MODEL_NAME,
                "response": response,
                "decoded": json.loads(response['choices'][0]['message']['content']),
                "type": "control",
                "results": {
                    "number": "???"
                }
            }

            with open(os.path.join(base_dir, f"test_c_{getSeed()}.json"), "w") as f:
                json.dump(report, f)

            print(f"Created \"anchoring\" control report ({i + 1}/{needed_control}).")
            sleep(1) # Reduced sleep time since retries and backoffs are handled in getResponse

        for i in range(needed_test):
            test = createTest()
            response = getResponse(test)

            report = {
                "model": MODEL_NAME,
                "response": response,
                "decoded": json.loads(response['choices'][0]['message']['content']),
                "type": "test",
                "results": {
                    "number": "???"
                }
            }

            with open(os.path.join(base_dir, f"test_t_{getSeed()}.json"), "w") as f:
                json.dump(report, f)

            print(f"Created \"anchoring\" test report ({i + 1}/{needed_test}).")
            sleep(1)
            
    except Exception as e:
        print(f"An error occurred during execution: {e}")

if __name__ == '__main__':
    runTest()
