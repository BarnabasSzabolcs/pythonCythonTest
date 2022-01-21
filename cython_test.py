import cython_wrapper


# Sample data for your call

x, y = 6, 2.3


answer = cython_wrapper.pymult(x, y)

print(f"    In Python: int: {x} float {y:.1f} return val {answer:.1f}")
