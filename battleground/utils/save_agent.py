import argparse
import os.path

from battleground.persistence import agent_data


def go():
    parser = argparse.ArgumentParser()

    parser.add_argument('--name', required=True, help='name of the agent')
    parser.add_argument('--type', required=True, help='the game type')
    parser.add_argument('--owner', required=False, default="command_line",
                        help='the agent owner')

    parser.add_argument('path', help='file path')

    args = parser.parse_args()
    
    if not os.path.isfile(args.path):
        raise Exception("File '{}' not found.".format(args.path))

    with open(args.path, 'r') as file:
        code = file.read()

    agent_id = agent_data.save_agent_code(owner=args.owner,
                                          name=args.name,
                                          game_type=args.type,
                                          code=code)

    print("data saved as: {}.".format(agent_id))


if __name__ == "__main__":
    go()
