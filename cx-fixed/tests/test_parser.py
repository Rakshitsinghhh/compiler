from src.lexer.lexer import Lexer
from src.parser.parser import Parser


def print_ast(node, indent=0):

    prefix = " " * indent

    print(f"{prefix}{type(node).__name__}")

    for attr, value in vars(node).items():

        if isinstance(value, list):

            print(f"{prefix}  {attr}:")

            for item in value:
                print_ast(item, indent + 4)

        elif hasattr(value, "__dict__"):

            print(f"{prefix}  {attr}:")
            print_ast(value, indent + 4)

        else:
            print(f"{prefix}  {attr}: {value}")


def main():

    code = """
    x = x + 1;
    """

    print("\nSOURCE CODE")
    print("=" * 50)
    print(code)

    lexer = Lexer(code)
    tokens = lexer.tokenize()

    print("\nTOKENS")
    print("=" * 50)

    for token in tokens:
        print(token)

    parser = Parser(tokens)

    ast = parser.parse()

    print("\nAST")
    print("=" * 50)

    print_ast(ast)


if __name__ == "__main__":
    main()