// vm.rs — Scientific Stack-Based VM for WASM execution with typed return support

use std::vec::Vec;
use std::slice;
use std::mem;
use std::f32;

#[no_mangle]
pub extern "C" fn alloc(size: usize) -> *mut u8 {
    static mut HEAP: [u8; 8192] = [0; 8192];
    unsafe { HEAP.as_mut_ptr() }
}

#[no_mangle]
pub extern "C" fn run(ptr: *const u8, len: usize) -> i32 {
    let code = unsafe { slice::from_raw_parts(ptr, len) };
    let mut ip = 0;
    let mut stack: Vec<f32> = Vec::new();
    let mut buffer: Vec<f32> = Vec::new();

    while ip < code.len() {
        match code[ip] {
            0x01 => {  // PUSH_INT (next 4 bytes)
                if ip + 4 >= code.len() { return -1; }
                let bytes = &code[ip+1..ip+5];
                let val = i32::from_le_bytes(bytes.try_into().unwrap()) as f32;
                stack.push(val);
                ip += 4;
            },
            0x02 => {  // PUSH_FLOAT (next 4 bytes)
                if ip + 4 >= code.len() { return -1; }
                let bytes = &code[ip+1..ip+5];
                let val = f32::from_le_bytes(bytes.try_into().unwrap());
                stack.push(val);
                ip += 4;
            },
            0x05 => {  // FSUB
                let b = stack.pop().unwrap_or(0.0);
                let a = stack.pop().unwrap_or(0.0);
                stack.push(a - b);
            },            
            0x10 => {  // FADD
                let b = stack.pop().unwrap_or(0.0);
                let a = stack.pop().unwrap_or(0.0);
                stack.push(a + b);
            },
            0x11 => {  // FMUL
                let b = stack.pop().unwrap_or(0.0);
                let a = stack.pop().unwrap_or(0.0);
                stack.push(a * b);
            },
            0x12 => {  // FDIV
                let b = stack.pop().unwrap_or(1.0);
                let a = stack.pop().unwrap_or(0.0);
                stack.push(a / b);
            },
            0x20 => {  // VEC_LOAD (N floats)
                if ip + 1 >= code.len() { return -2; }
                let n = code[ip+1] as usize;
                buffer.clear();
                for i in 0..n {
                    let start = ip + 2 + i * 4;
                    if start + 4 > code.len() { return -3; }
                    let f = f32::from_le_bytes(code[start..start+4].try_into().unwrap());
                    buffer.push(f);
                }
                ip += 1 + n * 4;
            },
            0x21 => {  // VEC_SUM
                let sum: f32 = buffer.iter().sum();
                stack.push(sum);
            },
            0x22 => {  // VEC_DOT (dot product of top buffer and stored)
                let mut other: Vec<f32> = Vec::new();
                let n = buffer.len();
                for _ in 0..n {
                    other.push(stack.pop().unwrap_or(0.0));
                }
                other.reverse();
                let dot: f32 = buffer.iter().zip(other.iter()).map(|(a, b)| a * b).sum();
                stack.push(dot);
            },
            0x30 => {  // HASH32 (simple rolling hash)
                let mut hash: u32 = 2166136261;
                for &f in &buffer {
                    hash ^= f.to_bits();
                    hash = hash.wrapping_mul(16777619);
                }
                stack.push(hash as f32);
            },
            0xF0 => {  // RETURN INT
                return *stack.last().unwrap_or(&0.0) as i32;
            },
            0xF1 => {  // RETURN FLOAT BITS
                return stack.last().unwrap_or(&0.0).to_bits() as i32;
            },
            0x40 => break,
            _ => return -999,
        }
        ip += 1;
    }

    stack.last().copied().unwrap_or(-111.0) as i32
}