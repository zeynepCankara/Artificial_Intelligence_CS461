"""
@Date: 28/04/2021 ~ Version: 1.0
@Group: RIDDLER
@Author: Ahmet Feyzi Halaç
@Author: Aybars Altınışık
@Author: Ege Şahin
@Author: Göktuğ Gürbüztürk
@Author: Zeynep Cankara


@Description: Obtains the class-precedence list (CPL)
      for a given class hierarchy from "fish hook algorithm",
      Winston chapter 14

    - implements fish hook algorithm to build CPL
    - Run the program via: python3 main.py
    - you can enable tracing via passing --trace flag (True / False)
    - press the key "Enter" to  iterate in the tracing mode
    - report.pdf contains the output of the program

"""

# queue
from collections import deque

# parser to run trace mode
import argparse

from cpl import CPL, Graph


def main(trace):
    """Main body to run the program"""

    traceMode = False
    if trace != "1":
        traceMode = True if input(
            "Note: press key (Enter) to iterate in the tracing mode \n" +
            "Enter 1 for trace mode, 0 otherwise: ") == '1' else False

    # Define the examples A and B
    exampleA = Graph({"Squares", "Rectangles", "Rhombuses",
                      "Parallelograms", "Isosceles Trapezoids", "Trapezoids",
                      "Cyclic Quadrilaterals", "Kites", "Quadrilaterals"})
    exampleA.add_direct_superclasses("Squares", ["Rectangles", "Rhombuses"])
    exampleA.add_direct_superclasses("Rectangles",
                                     ["Isosceles Trapezoids", "Parallelograms"])
    exampleA.add_direct_superclasses("Rhombuses",
                                     ["Parallelograms", "Kites"])
    exampleA.add_direct_superclasses("Isosceles Trapezoids",
                                     ["Cyclic Quadrilaterals", "Trapezoids"])
    exampleA.add_direct_superclasses("Parallelograms", ["Trapezoids"])
    exampleA.add_direct_superclasses(
        "Cyclic Quadrilaterals", ["Quadrilaterals"])
    exampleA.add_direct_superclasses("Trapezoids", ["Quadrilaterals"])
    exampleA.add_direct_superclasses("Kites", ["Quadrilaterals"])

    cpl = CPL(exampleA, "Squares")
    print("fish hook table")
    print(cpl.fish_hook_pairs)  # check fish hook pairs
    print("cpl list")
    print(cpl.cpl)

    exampleB = Graph({"Squares", "Rectangles", "Rhombuses",
                      "Parallelograms", "Isosceles Trapezoids", "Trapezoids",
                      "Cyclic Quadrilaterals", "Kites", "Quadrilaterals"})
    exampleB.add_direct_superclasses("Squares", ["Rectangles", "Rhombuses"])
    exampleB.add_direct_superclasses("Rectangles",
                                     ["Cyclic Quadrilaterals", "Parallelograms"])
    exampleB.add_direct_superclasses("Rhombuses",
                                     ["Parallelograms", "Kites"])
    exampleB.add_direct_superclasses("Isosceles Trapezoids",
                                     ["Trapezoids", "Cyclic Quadrilaterals"])
    exampleB.add_direct_superclasses("Parallelograms", ["Quadrilaterals"])
    exampleB.add_direct_superclasses(
        "Cyclic Quadrilaterals", ["Quadrilaterals"])
    exampleB.add_direct_superclasses("Trapezoids", ["Quadrilaterals"])
    exampleB.add_direct_superclasses("Kites", ["Quadrilaterals"])

    print("example B, Isosceles Trapezoids")
    cpl = CPL(exampleB, "Isosceles Trapezoids")
    print("fish hook table")
    print(cpl.fish_hook_pairs)  # check fish hook pairs
    print("cpl list")
    print(cpl.cpl)
    print("example B, Squares")
    cpl = CPL(exampleB, "Squares")
    print("fish hook table")
    print(cpl.fish_hook_pairs)  # check fish hook pairs
    print("cpl list")
    print(cpl.cpl)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create a tracing flag")
    parser.add_argument(
        "--trace",
        metavar="path",
        required=False,
        help="tracing option for the program ('1': True / '0': False)"
        + "press key (Enter) to iterate in the tracing mode",
    )
    args = parser.parse_args()
    main(trace=args.trace)
