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
      Winston chapter 9

    - implements fish hook algorithm to build CPL
    - Run the program via: python3 main.py
    - you can enable tracing via passing --trace flag (True / False)
    - press the key "Enter" to  iterate in the tracing mode
    - report.pdf contains the output of the program

"""

# parser to run trace mode
import argparse

from cpl import CPL, Graph


def main(trace):
    """Main body to run the program"""
    trace_mode = False
    if trace != "1":
        trace_mode = True if input(
            "Note: press key (Enter) to iterate in the tracing mode \n" +
            "Enter 1 for trace mode, 0 otherwise: ") == '1' else False

    # Define the Example A as an Adjacency List Graph
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

    # Define the Example B as an Adjacency List Graph
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

    # Example 1: Compute a CPL for “Squares”
    print("Example A: Squares")
    cpl = CPL(exampleA, "Squares", trace_mode)
    print("CPL List: ")
    print("high", " " * max(len(str(cpl.cpl))-10, 0), "low")
    print(cpl.cpl)

    # Example 2: Compute a CPL for “Isosceles Trapezoids”
    print("Example B: Isosceles Trapezoids")
    cpl = CPL(exampleB, "Isosceles Trapezoids", trace_mode)
    print("CPL List: ")
    print("high", " " * max(len(str(cpl.cpl))-10, 0), "low")
    print(cpl.cpl)

    # Example 2: Compute a CPL for “Squares”
    print("Example B: Squares")
    cpl = CPL(exampleB, "Squares", trace_mode)
    print("CPL List: ")
    print("high", " " * max(len(str(cpl.cpl))-10, 0), "low")
    print(cpl.cpl)

    exampleS = Graph({"Crazy", "Professors", "Hackers",
                      "Eccentrics", "Teachers", "Programmers",
                      "Dwarfs", "Athletes", "Everything", "Endomorphs",
                      "Weightlifters", "Shotputters", "Jacque"})
    exampleS.add_direct_superclasses("Crazy", ["Professors", "Hackers"])
    exampleS.add_direct_superclasses("Professors",
                                     ["Eccentrics", "Teachers"])
    exampleS.add_direct_superclasses("Hackers",
                                     ["Eccentrics", "Programmers"])
    exampleS.add_direct_superclasses("Eccentrics", ["Dwarfs"])
    exampleS.add_direct_superclasses("Teachers", ["Dwarfs"])
    exampleS.add_direct_superclasses("Programmers", ["Dwarfs"])
    exampleS.add_direct_superclasses("Dwarfs", ["Everything"])
    exampleS.add_direct_superclasses("Athletes", ["Dwarfs"])
    exampleS.add_direct_superclasses("Endomorphs", ["Dwarfs"])
    exampleS.add_direct_superclasses("Weightlifters",
                                     ["Athletes", "Endomorphs"])
    exampleS.add_direct_superclasses("Shotputters",
                                     ["Athletes", "Endomorphs"])
    exampleS.add_direct_superclasses("Jacque",
                                     ["Weightlifters",
                                      "Shotputters", "Athletes"])

    # Surprise Example: Compute a CPL for “Crazy”
    print("Surprise Example: Crazy")
    cpl = CPL(exampleS, "Crazy", trace_mode)
    print("CPL List: ")
    print("high", " " * max(len(str(cpl.cpl))-10, 0), "low")
    print(cpl.cpl)

    # Surprise Example: Compute a CPL for “Crazy”
    print("Surprise Example: Jacque")
    cpl = CPL(exampleS, "Jacque", trace_mode)
    print("CPL List: ")
    print("high", " " * max(len(str(cpl.cpl))-10, 0), "low")
    print(cpl.cpl)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create a tracing flag")
    parser.add_argument(
        "--trace",
        metavar="path",
        required=False,
        help="tracing option for the program ('1': True / '0': False)"
        + "press the key (Enter) to iterate in the tracing mode",
    )
    args = parser.parse_args()
    main(trace=args.trace)
