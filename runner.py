"""Offline Python execution for Albahrawy / البحراوي.
A small execution guard stops common accidental infinite loops in study exercises.
"""
import ast
import contextlib
import io
import json
import sys

class LoopGuard(ast.NodeTransformer):
    def __init__(self):
        self.counter_name = "__albahrawy_loop_count"

    def _guard(self, node):
        tick = ast.parse(
            f"{self.counter_name} += 1\n"
            f"if {self.counter_name} > 100000:\n"
            f"    raise TimeoutError('توقف التنفيذ: عدد تكرارات الحلقة كبير جدًا')"
        ).body
        node.body = tick + node.body
        return node

    def visit_For(self, node):
        self.generic_visit(node)
        return self._guard(node)

    def visit_While(self, node):
        self.generic_visit(node)
        return self._guard(node)


def run_code_json(code, input_text=""):
    output = io.StringIO()
    namespace = {"__name__": "__main__"}
    old_stdin = sys.stdin
    try:
        sys.stdin = io.StringIO(input_text or "")
        tree = ast.parse(code, filename="<code>", mode="exec")
        tree = LoopGuard().visit(tree)
        ast.fix_missing_locations(tree)
        namespace["__albahrawy_loop_count"] = 0
        compiled = compile(tree, "<code>", "exec")
        with contextlib.redirect_stdout(output), contextlib.redirect_stderr(output):
            exec(compiled, namespace, namespace)
        return json.dumps({"out": output.getvalue().rstrip("\n").splitlines() if output.getvalue().rstrip("\n") else [], "err": None}, ensure_ascii=False)
    except Exception as exc:
        message = "{}: {}".format(type(exc).__name__, exc)
        captured = output.getvalue().rstrip("\n")
        lines = captured.splitlines() if captured else []
        return json.dumps({"out": lines, "err": message}, ensure_ascii=False)
    finally:
        sys.stdin = old_stdin
