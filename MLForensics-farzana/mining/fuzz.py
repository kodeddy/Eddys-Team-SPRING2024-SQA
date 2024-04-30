from hypothesis import given, strategies as st
import tempfile
import os
import ast
import constants

# Assuming 'log_op_miner' is the module where the functions are located
from log_op_miner import checkIfParsablePython, hasLogImport, commonAttribCallBody, getPythonAtrributeFuncs

# Fuzz test to check file parsing capability
@given(st.text())
def test_checkIfParsablePython(code):
    with tempfile.NamedTemporaryFile(delete=False, suffix='.py') as tmp:
        tmp.write(code.encode('utf-8'))
        tmp.close()
        # The function should return a boolean indicating if the file is parsable
        assert isinstance(checkIfParsablePython(tmp.name), bool)
    os.unlink(tmp.name)  # Clean up the temporary file

# Fuzz test for checking logging imports
@given(st.lists(st.text(), min_size=1, max_size=10))  # Generate lists of random strings
def test_hasLogImport(lines):
    code = "\n".join(lines + ['import logging'])  # Ensure there's always at least one correct import
    with tempfile.NamedTemporaryFile(delete=False, suffix='.py') as tmp:
        tmp.write(code.encode('utf-8'))
        tmp.close()
        # Should return True as 'import logging' is present
        assert hasLogImport(tmp.name) == True
    os.unlink(tmp.name)  # Clean up the temporary file

# Fuzz test for commonAttribCallBody function
@given(st.text(min_size=1))
def test_commonAttribCallBody(function_name):
    code = f"{function_name}('test')"
    try:
        tree = ast.parse(code)
        call_node = next(node for node in ast.walk(tree) if isinstance(node, ast.Call))
        result = commonAttribCallBody(call_node)
        assert isinstance(result, list) and len(result) > 0
        assert result[0][1] == function_name
    except SyntaxError:
        pass

# Fuzz test for getPythonAtrributeFuncs function
@given(st.text(min_size=1), st.text(min_size=1))
def test_getPythonAtrributeFuncs(class_name, method_name):
    code = f"""
class {class_name}:
    def {method_name}(self):
        pass
{class_name}().{method_name}()
"""
    try:
        tree = ast.parse(code)
        result = getPythonAtrributeFuncs(tree)
        assert isinstance(result, list) and len(result) > 0
        assert result[0][1] == method_name
    except SyntaxError:
        pass

if __name__ == "__main__":
    test_checkIfParsablePython()
    test_hasLogImport()
    test_commonAttribCallBody()
    test_getPythonAtrributeFuncs()
