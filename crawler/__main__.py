# -*- coding: utf-8 -*-

import argparse
from core import Board
import json
import jsonpickle

def main(args=None):
    print("Init...")
    print("Pulling {0} posts from {1} board".format(args.num_post, args.board))

    b = Board(args.board)
    posts = b.get_post_list(args.num_post)
    print("Processed ")

    serialized = jsonpickle.encode(posts)

    if args.output:
        with open(args.output, 'w') as f:
            json.dump(json.loads(serialized), f, indent=2)
    else:
        print(json.dumps(json.loads(serialized), indent=2))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Pull post data from PTT.')
    parser.add_argument('--num_post', '-n', type=int)
    parser.add_argument('--board', type=str)
    parser.add_argument('--output', '-o', type=str)

    args = parser.parse_args()

    print(args)

    main(args)