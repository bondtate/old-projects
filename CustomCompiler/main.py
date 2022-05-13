from compiler.solution import lex_source
from helpers import capture_intermediate_exec
from compiler.solution import lex_source
src = """
def fib(int:n) -> int:
    if n <= 2 then
        return 1
    end
    return fib(n-1) + fib(n-2)
end
println { fib(4) }
"""
to_input = ""
expected = "0\n1\n2\n3\n99\n"
stdout, st = capture_intermediate_exec(src, to_input)
result = stdout.split()
print(result)
print(stdout)
print(st)