from hypothesis import given, strategies as st
import tempfile
import os

# Import the functions from your module
from log_op_miner import checkIfParsablePython, hasLogImport

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

if __name__ == "__main__":
    test_checkIfParsablePython()
    test_hasLogImport()
