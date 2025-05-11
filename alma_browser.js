// alma_browser.js — Minimal browser-based ALMA interpreter

async function loadWasm(url) {
    const response = await fetch(url);
    const buffer = await response.arrayBuffer();
    const wasm = await WebAssembly.instantiate(buffer, {});
    return wasm.instance;
}

function floatToBytes(f) {
    const buf = new ArrayBuffer(4);
    new DataView(buf).setFloat32(0, f, true);
    return new Uint8Array(buf);
}

function intToBytes(i) {
    const buf = new ArrayBuffer(4);
    new DataView(buf).setInt32(0, i, true);
    return new Uint8Array(buf);
}

function parseAlmaScript(script) {
    const code = [];
    const lines = script.split('\n').map(l => l.split('#')[0].trim()).filter(Boolean);
    const vars = {};

    for (let line of lines) {
        const parts = line.split(/\s+/);
        const cmd = parts[0];
        const args = parts.slice(1);

        switch (cmd) {
            case 'let':
                vars[args[0]] = parseFloat(args[2]);
                break;
            case 'push':
                let val = vars[args[0]] ?? parseFloat(args[0]);
                if (Number.isInteger(val)) {
                    code.push(0x01, ...intToBytes(val));
                } else {
                    code.push(0x02, ...floatToBytes(val));
                }
                break;
            case 'add': code.push(0x10); break;
            case 'sub': code.push(0x05); break;
            case 'mul': code.push(0x11); break;
            case 'div': code.push(0x12); break;
            case 'vec_load':
                code.push(0x20, args.length);
                for (let v of args) {
                    let f = vars[v] ?? parseFloat(v);
                    code.push(...floatToBytes(f));
                }
                break;
            case 'vec_sum': code.push(0x21); break;
            case 'vec_dot':
                for (let v of args.reverse()) {
                    let f = vars[v] ?? parseFloat(v);
                    code.push(0x02, ...floatToBytes(f));
                }
                code.push(0x22);
                break;
            case 'hash32': code.push(0x30); break;
            case 'ret_int': code.push(0xF0); break;
            case 'ret_float': code.push(0xF1); break;
            default:
                console.warn("Unknown command:", cmd);
        }
    }

    return new Uint8Array(code);
}

function decodeFloat(i32) {
    const buf = new ArrayBuffer(4);
    new DataView(buf).setUint32(0, i32, true);
    return new DataView(buf).getFloat32(0, true);
}

export async function runAlma(script, wasmPath = 'stack_vm.wasm', debug=false) {
    const instance = await loadWasm(wasmPath);
    const memory = instance.exports.memory;
    const alloc = instance.exports.alloc;
    const run = instance.exports.run;

    const bytecode = parseAlmaScript(script);
    const ptr = alloc(bytecode.length);
    const mem = new Uint8Array(memory.buffer, ptr, bytecode.length);
    mem.set(bytecode);

    const result = run(ptr, bytecode.length);
    const float = decodeFloat(result);
    if (debug) {
        console.log(`ALMA Result → Int: ${result} | Float: ${float}`);
    }
    
    return { int: result, float };
}
