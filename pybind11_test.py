import example
from demo_package.prio_lexer import prio_lexer_tokenize

if __name__ == "__main__":
    # Sample data for your call
    x, y = 6, 3

    answer = example.add(x, y)
    print(example.greet("World"))
    print(answer)
    v0 = ['s']
    v = example.VectorStr(v0)
    example.changes(v)
    print(v)

    print(prio_lexer_tokenize('', []))
    print(prio_lexer_tokenize('aba', ['ab', 'a', 'b']))
    # print(f"    In Python: int: {x} float {y:.1f} return val {answer:.1f}")
