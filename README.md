# ALMA: Abstract Language for Modeling & Analysis

ALMA is a minimal, stack-based bytecode language and execution environment designed for portable, low-power scientific computation. It enables consistent and secure execution of mathematical and vector operations across heterogeneous and legacy hardware, compiled to WebAssembly for broad compatibility and reproducibility.

The rapid turnover of consumer hardware, driven by market cycles and planned obsolescence, produces significant e-waste and limits access to scientific computing. Many older devices remain computationally viable, yet are excluded from modern frameworks due to architecture drift or runtime bloat.

## Key Features

- Stack-based execution with 32-bit `int` and `float` support
- Typed arithmetic and vector instructions
- Deterministic bytecode format for reproducible computation
- ALMA-script language with macros and conditionals
- WebAssembly runtime targeting underpowered or distributed devices

## Example ALMA Script

```alma
let x = 8
let y = 2
push x
push y
div
ret_float
````

Expected output: `4.0`

## Architecture

ALMA consists of two components:

* A Rust-based VM compiled to `stack_vm.wasm` using the `wasm32-unknown-unknown` target.
* A Python interpreter (`alma_interpreter.py`) that compiles ALMA-script into bytecode and executes it using Wasmtime.

## Usage (Python)

```python
from alma_interpreter import parse_alma_script, execute_alma_bytecode

script = '''
vec_load 1.0 2.0 3.0
vec_sum
ret_float
'''

bytecode = parse_alma_script(script)
result = execute_alma_bytecode(bytecode, debug=True)
```

## Supported Instructions

| Opcode | Instruction  | Description                    |
| ------ | ------------ | ------------------------------ |
| 0x01   | `PUSH_INT`   | Push 4-byte signed integer     |
| 0x02   | `PUSH_FLOAT` | Push 4-byte float              |
| 0x05   | `FSUB`       | Float subtraction              |
| 0x10   | `FADD`       | Float addition                 |
| 0x11   | `FMUL`       | Float multiplication           |
| 0x12   | `FDIV`       | Float division                 |
| 0x20   | `VEC_LOAD`   | Load N floats into vector      |
| 0x21   | `VEC_SUM`    | Sum the loaded vector          |
| 0x22   | `VEC_DOT`    | Dot product with top stack vec |
| 0x30   | `HASH32`     | FNV-like hash of buffer        |
| 0xF0   | `RET_INT`    | Return top of stack as int     |
| 0xF1   | `RET_FLOAT`  | Return top of stack as float   |

## Philosophy

ALMA is designed to reduce electronic waste by enabling the use of older hardware as useful compute agents in distributed scientific systems. By combining a predictable VM with a low-level but expressive instruction set, ALMA provides a foundation for transparent, auditable, and platform-neutral computing.

## Rationale for a Custom Bytecode System

Compared to dynamic scripting (`eval`/`loadstring` in Lua or Python), ALMA offers:

* **Security**: No dynamic parsing; deterministic opcodes.
* **Portability**: WASM execution on any modern device or browser.
* **Formality**: Full instruction set definable in formal methods.
* **Energy Efficiency**: Predictable, low-overhead runtime.
* **Scientific Reproducibility**: Bytecode guarantees result stability.

This supports goals of distributed, low-trust scientific computing.

## Use Cases

* Vectorized AI math on edge nodes
* Bioinformatics pipelines
* Reproducible numerical experiments
* Cooperative compute over LANs of mixed hardware
* Educational demonstrations of compilers and VMs
* WASM execution on smart devices, thin clients, and public infrastructure

## Future Work

* Loop and branch control
* Distributed execution protocol
* Parameterized macros
* Energy-per-instruction benchmarking

## Conclusion

ALMA is a step toward more efficient, accessible scientific computing. By lowering runtime complexity and removing dependency on full interpreters, it provides a robust base for deterministic and scalable task execution across devices. Through ALMA, idle or legacy hardware can contribute directly to modern research.

The Python implementation is only the beginning. ALMA's portability through WASM positions it as a universal compute layer, capable of running securely across thousands of heterogeneous endpoints. Its small footprint and open design offer a foundation for equitable, globally distributed scientific computation.

## License

Apache 2.0 License. Developed by Zacharie Fortin 2025
