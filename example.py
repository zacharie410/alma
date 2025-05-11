from alma_interpreter import parse_alma_script, execute_alma_bytecode

examples = {
    "Basic Arithmetic (DIV)": """
        let x = 8
        let y = 2
        push x
        push y
        div
        ret_float
    """,

    "Float Addition (FADD)": """
        push 1.5
        push 2.0
        add
        ret_float
    """,

    "Vector Sum (VEC_SUM)": """
        vec_load 1.0 2.0 3.0
        vec_sum
        ret_float
    """,

    "Vector Dot Product (VEC_DOT)": """
        vec_load 1.0 2.0 3.0
        vec_dot 1.0 2.0 3.0
        ret_float
    """,

    "Hash of Vector (HASH32)": """
        vec_load 1.0 2.0 3.0
        hash32
        ret_float
    """,

    "Integer Arithmetic (MUL)": """
        push 3
        push 4
        mul
        ret_int
    """,

    "Conditional & Variables": """
        let a = 5
        if a 5
            push 10
            push 20
            add
        endif
        ret_int
    """,

    "Macro Expansion": """
        macro square2
            push 2
            push 2
            mul
        endmacro

        square2
        ret_int
    """
}

if __name__ == "__main__":
    for label, script in examples.items():
        bytecode = parse_alma_script(script)
        execute_alma_bytecode(bytecode, label=label, debug=True)
