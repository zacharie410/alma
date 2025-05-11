# ALMA: Abstract Language for Modeling & Analysis

ALMA is a minimal, stack-based bytecode language and execution environment designed for portable, low-power scientific computation. It enables consistent and secure execution of mathematical and vector operations across heterogeneous and legacy hardware, compiled to WebAssembly for broad compatibility and reproducibility.

The rapid turnover of consumer hardware, driven by market cycles and planned obsolescence, produces significant e-waste and limits access to scientific computing. Many older devices remain computationally viable, yet are excluded from modern frameworks due to architecture drift or runtime bloat.

## Key Features

- Stack-based execution with 32-bit `int` and `float` support
- Typed arithmetic and vector instructions
- Deterministic bytecode format for reproducible computation
- ALMA-script language with macros and conditionals
- WebAssembly runtime targeting underpowered or distributed devices
- JS interpreter for in-browser execution of `.alma` scripts

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

---

## Architecture

ALMA consists of three key components:

* A Rust-based virtual machine compiled to `stack_vm.wasm` using the `wasm32-unknown-unknown` target.
* A Python interpreter (`alma_interpreter.py`) that parses ALMA-script and executes bytecode using Wasmtime.
* A JavaScript-based interpreter (`alma_browser.js`) that compiles ALMA-script in the browser and runs it via WebAssembly.

---

## Usage

### Python Example

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

### Browser Example (JS)

```html
<script type="module">
  import { runAlma } from './alma_browser.js';

  const almaScript = `
    let x = 10
    let y = 2
    push x
    push y
    div
    ret_float
  `;

  runAlma(almaScript).then(result => {
    console.log("ALMA Output:", result);
  });
</script>
```

---

## Supported Instructions

| Opcode | Instruction  | Description                    |
| ------ | ------------ | ------------------------------ |
| 0x01   | `PUSH_INT`   | Push 32-bit signed integer     |
| 0x02   | `PUSH_FLOAT` | Push 32-bit float              |
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

---

## Philosophy

ALMA is designed to reduce electronic waste by enabling the use of older hardware as useful compute agents in distributed scientific systems. By combining a predictable VM with a low-level but expressive instruction set, ALMA provides a foundation for transparent, auditable, and platform-neutral computing.

---

## Rationale for a Custom Bytecode System

Compared to dynamic scripting (`eval`/`loadstring`), ALMA offers:

* **Security**: No dynamic parsing; deterministic opcodes.
* **Portability**: WASM execution on any modern device or browser.
* **Formality**: Fully definable instruction set and VM.
* **Energy Efficiency**: Minimal overhead for embedded and edge nodes.
* **Scientific Reproducibility**: Bytecode ensures consistent results across platforms.

---

## Use Cases

* Vectorized AI math on edge or browser nodes
* Bioinformatics pipelines
* Reproducible scientific experiments
* Peer-to-peer distributed computation
* Education (VM architecture, compiler design)
* Web-based citizen science platforms

---

## Future Work

* Loop and branch control
* Distributed execution protocol (with fallback and retries)
* Parameterized macros and template blocks
* Browser-hosted task queues
* ALMA-to-LLVM transpiler for backend acceleration
* ALMA Jupyter kernel for notebooks

---

## Conclusion

ALMA is a step toward more efficient, accessible scientific computing. Its design encourages equitable access to computation by enabling devices of all classes — from outdated laptops to modern browsers — to participate in scientific workloads. With both Python and JavaScript runtimes, ALMA is flexible enough to serve as the foundation for cooperative computing at global scale.

---

## License

Apache 2.0 License. Developed by Zacharie Fortin, 2025.
