import argparse
from utils import *

build_testcases_prompt_advanced="""Task Overview:
You are given a problem and a set of solution code, please:
1. Select the optimal solution code among them.
2. Provide the key steps to solve the problem based on the chosen solution.
3. Provide the chosen solution code with its explanation.
[Question start]
<<<<question>>>>
[Question end]

[solution codes Start]
<<<<code>>>>
[solution codes End]

Your final output should be like this:
## key steps
## solution code
## explanation
"""

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--raw_code_file', type=str, default='data/cleaned_data.json')
    parser.add_argument('--raw_code_msg_file', type=str, default='data/train_some_msg2.jsonl')
    args = parser.parse_args()
    dt = read_jsonl(args.raw_code_file)
    messages = []
    i = 0
    for item in dt:
        if len(item['solutions']+item["question"])<=1048576 and item["id"] >= 500:
            messages.append(
                            {
                                "custom_id": str(item["id"]),
                                "method": "POST",
                                "url": "/v1/chat/completions",
                                "body": {
                                    "model": "deepseek-v3",
                                    "messages": [
                                        {
                                            "role": "user",
                                            "content": build_testcases_prompt_advanced.replace("<<<<code>>>>",
                                                                                               item["solutions"])
                                         .replace("<<<<question>>>>", item["question"])
                                        }
                                    ]
                                }
                            }
                            )
            i = i+1
            if i > 500:
                break

    write_jsonl(messages, args.raw_code_msg_file)
    






