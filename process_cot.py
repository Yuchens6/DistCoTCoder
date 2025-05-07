import argparse
from utils import *

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--raw_code_file', type=str, default='../data/train.jsonl')
    parser.add_argument('--llm_code_file', type=str, default='data/train_some_llm2.jsonl')
    parser.add_argument('--raw_code_msg_file', type=str, default='data/train_some_data2.jsonl')
    args = parser.parse_args()
    dt1 = read_jsonl(args.raw_code_file)
    dt2 = read_jsonl(args.llm_code_file)
    messages = []
    for item1 in dt1:
        for item2 in dt2:
            if str(item1["id"]) == item2["custom_id"]:
                messages.append(
                    {
                        "instruction":item1["question"],
                        "output":item2["response"]["body"]["choices"][0]["message"]["content"],
                    }
                )
                break

    write_jsonl(messages, args.raw_code_msg_file)