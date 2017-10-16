from __future__ import print_function
import uuid
import json
import sys
import logging
import os
from qa_squirtle import run_func
import tensorflow as tf

logging.disable(logging.CRITICAL)
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 
def create_question(q):
    question = {}
    question['answers'] = []
    question['question'] = q
    question['id'] = uuid.uuid4().hex
    return question

def main():

    if len(sys.argv) == 2:
        with open(sys.argv[1], 'r') as f:
            text = f.read().replace('\n',' ')
    else:
        text = raw_input("Text:\n")

    print('\nEnter "exit" when done\n')

    while True:
        tf.reset_default_graph()
        q = raw_input("Q) ")
        if q == "exit":
            break
        questions = []
        questions.append(create_question(q))

        paras = []
        para = {}
        para['context'] = text 
        para['qas'] = questions
        paras.append(para)

        dump = {}
        dump['data'] = [{'title':'FuseMachines', 'paragraphs':paras}]

        with open('data/squad/fuse.json', 'w') as f:
            json.dump(dump, f)

        save_stdout = sys.stdout
        sys.stdout = open('temp/trash', 'w')
        run_func()
        sys.stdout = save_stdout

        with open('temp/fuse-answer.json') as f:
            answers = json.load(f)

        print(answers[questions[0]['id']])
        print('\n')

if __name__ == "__main__":
    main()
