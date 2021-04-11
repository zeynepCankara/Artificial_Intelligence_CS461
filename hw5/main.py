"""
@Date: 11/04/2021 ~ Version: 1.0
@Author: Ahmet Feyzi Halaç
@Author: Aybars Altınışık
@Author: Ege Şahin
@Author: Göktuğ Gürbüztürk
@Author: Zeynep Cankara


@Description: A rule based Zookeeper System from Winston chapter 7
    - implements backward chaining to identify zoo-animals
    - Run the program via: python3 main.py
    - you can enable tracing via passing --trace flag (True / False)

"""
# queue
from collections import deque

# parser to run trace mode
import argparse

# the zookeeper system
from zookeeper import Rule, Zookeeper


def main(trace):
    """Main body to run the program"""

    traceMode = "0"
    if trace != "1":
        traceMode = input("Enter 1 for trace mode, 0 otherwise: ")
    # run the program in single stepping mode
    zookeeper = Zookeeper()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create a tracing flag")
    parser.add_argument(
        "--trace",
        metavar="path",
        required=False,
        help="tracing option for the program ('1': True / '0': False)",
    )
    args = parser.parse_args()
    main(trace=args.trace)
