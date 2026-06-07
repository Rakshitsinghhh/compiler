from src.lexer.lexer import Lexer
from src.lexer.token import TokenType


def print_tokens(tokens):
    print("\nTOKENS:")
    print("-" * 60)

    for token in tokens:
        print(token)

    print("-" * 60)


def main():

    code = """
    int age = 19;
    float pi = 3.14;
    string name = "Rakshit";

    if (age >= 18) {
        print(name);
    } else {
        print("Minor");
    }

    while (age < 25) {
        age = age + 1;
    }

    // This is a comment

    func add(int a, int b) {
        return a + b;
    }
    """

    lexer = Lexer(code)

    try:
        tokens = lexer.tokenize()

        print_tokens(tokens)

        print(f"\nTotal Tokens: {len(tokens)}")

        if tokens[-1].type == TokenType.EOF:
            print("✓ Lexer completed successfully")

    except Exception as e:
        print(f"✗ Lexer Error: {e}")


if __name__ == "__main__":
    main()