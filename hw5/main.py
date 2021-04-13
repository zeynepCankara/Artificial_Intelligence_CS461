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
from zookeeper import Rule, Zookeeper, test_rules

def print_working_memory(animalName, wm):
    print("\nWorking Memory: ")
    for item in wm:
        print(animalName + item[2:])
    print()

def main(trace):
    """Main body to run the program"""

    traceMode = False
    if trace != "1":
       traceMode = True if input("Enter 1 for trace mode, 0 otherwise: ") == '1' else False
    
    print("First example of book :")
    animalName = "Stretch"
    wm = ["?x has hair", "?x chews cud", "?x has long legs", "?x has a long neck", "?x has a tawny color", "?x has dark spots"]

    # print initial working memory
    print_working_memory(animalName, wm)

    # run the program in single stepping mode
    zookeeper = Zookeeper(wm, traceMode)
    zookeeper.backward_chaining(animalName, "is a giraffe")

    print('#' * 25, "\nSecond example of book :")
    animalName = "Swifty"
    wm = ["?x has forward-pointing eyes", "?x has claws", "?x has pointed teeth", "?x has hair", "?x has a tawny color", "?x has dark spots"]

    # print initial working memory
    print_working_memory(animalName, wm)

    # run the program in single stepping mode
    zookeeper = Zookeeper(wm, traceMode)
    zookeeper.backward_chaining(animalName, "is a cheetah")

    print('#' * 25, "\nOur examples :")
    animalName = "Zoey"
    wm = ["?x has hoofs", "?x gives milk", "?x has white color", "?x has black stripes"]

    # print initial working memory
    print_working_memory(animalName, wm)

    # run the program in single stepping mode
    zookeeper = Zookeeper(wm, traceMode)
    zookeeper.backward_chaining(animalName, "is a zebra")

    animalName = "Coco"
    wm = ["?x has hair", "?x eats meat", "?x has a tawny color", "?x has black stripes"]

    # print initial working memory
    print('#' * 25)
    print_working_memory(animalName, wm)

    # run the program in single stepping mode
    zookeeper = Zookeeper(wm, traceMode)
    zookeeper.backward_chaining(animalName, "is a tiger")
    
    print('#' * 25, "\nSURPRISE example :")
    animalName = "Splashy"
    wm = ["?x has feathers", "?x lays eggs" , "?x swims" , "?x does not fly" , "?x is black and white", "?x has a tawny color"]

    # print initial working memory
    print_working_memory(animalName, wm)

    # run the program in single stepping mode
    zookeeper = Zookeeper(wm, traceMode)
    zookeeper.backward_chaining(animalName, "is a penguin")


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


