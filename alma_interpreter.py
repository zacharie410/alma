# alma_interpreter.py — ALMA interpreter and execution logic

import struct
from wasmtime import Store, Module, Instance

WASM_PATH = "stack_vm.wasm"

def decode_float(i32_bits):
    return struct.unpack('<f', struct.pack('<I', i32_bits & 0xffffffff))[0]

class ALMA:
    def __init__(self):
        self.code = bytearray()
        self.vars = {}
        self.macros = {}

    def push_int(self, val):
        self.code.append(0x01)
        self.code.extend(struct.pack('<i', val))

    def push_float(self, val):
        self.code.append(0x02)
        self.code.extend(struct.pack('<f', val))

    def fadd(self): self.code.append(0x10)
    def fsub(self): self.code.append(0x05)
    def fmul(self): self.code.append(0x11)
    def fdiv(self): self.code.append(0x12)

    def vec_load(self, floats):
        self.code.append(0x20)
        self.code.append(len(floats))
        for f in floats:
            self.code.extend(struct.pack('<f', f))

    def vec_sum(self): self.code.append(0x21)
    def vec_dot(self, floats):
        for f in reversed(floats):
            self.push_float(f)
        self.code.append(0x22)

    def hash32(self): self.code.append(0x30)
    def ret_int(self): self.code.append(0xF0)
    def ret_float(self): self.code.append(0xF1)
    def build(self): return self.code

def parse_alma_script(text: str, alma=None) -> bytes:
    if alma is None:
        alma = ALMA()
    lines = text.strip().splitlines()
    i = 0
    recording_macro = None
    macro_buffer = []

    while i < len(lines):
        line = lines[i].split("#")[0].strip()
        if not line:
            i += 1
            continue
        parts = line.split()
        if not parts:
            i += 1
            continue

        cmd, *args = parts

        if cmd == "macro":
            recording_macro = args[0]
            macro_buffer = []
            i += 1
            continue

        if cmd == "endmacro":
            alma.macros[recording_macro] = list(macro_buffer)
            recording_macro = None
            i += 1
            continue

        if recording_macro:
            macro_buffer.append(line)
            i += 1
            continue

        if cmd in alma.macros:
            macro_lines = alma.macros[cmd]
            expanded_code = parse_alma_script("\n".join(macro_lines), alma)
            alma.code.extend(expanded_code)
            i += 1
            continue

        if cmd == "if":
            var = args[0]
            cond = float(args[1])
            if alma.vars.get(var, 0.0) == cond:
                i += 1
            else:
                while i < len(lines) and not lines[i].strip().startswith("endif"):
                    i += 1
                i += 1
            continue

        if cmd == "endif":
            i += 1
            continue

        match cmd:
            case "push":
                val = args[0]
                if val in alma.vars:
                    val = alma.vars[val]
                val = float(val)
                if val.is_integer():
                    alma.push_int(int(val))
                else:
                    alma.push_float(val)
            case "let":
                name, _, value = args
                alma.vars[name] = float(value)
            case "add": alma.fadd()
            case "sub": alma.fsub()
            case "mul": alma.fmul()
            case "div": alma.fdiv()
            case "vec_load":
                floats = [alma.vars.get(x, float(x)) for x in args]
                alma.vec_load(floats)
            case "vec_sum": alma.vec_sum()
            case "vec_dot":
                floats = [alma.vars.get(x, float(x)) for x in args]
                alma.vec_dot(floats)
            case "hash32": alma.hash32()
            case "ret_int": alma.ret_int()
            case "ret_float": alma.ret_float()
            case _: raise ValueError(f"Unknown instruction: {cmd}")

        i += 1

    return alma.build()

def execute_alma_bytecode(bytecode: bytearray, label="ALMA Result", wasm_path=WASM_PATH, debug=False):
    wasm_bytes = open(wasm_path, "rb").read()
    store = Store()
    module = Module(store.engine, wasm_bytes)
    instance = Instance(store, module, [])

    alloc = instance.exports(store)["alloc"]
    run = instance.exports(store)["run"]
    memory = instance.exports(store)["memory"]

    ptr = alloc(store, len(bytecode))
    mem = memory.data_ptr(store)
    for i in range(len(bytecode)):
        mem[ptr + i] = bytecode[i]

    result = run(store, ptr, len(bytecode))
    float_result = decode_float(result)
    if debug:
        print(f"{label}: [RESULT] → {result} | Float → {float_result}")
    return float_result
