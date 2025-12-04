// lib.rs
// use pyo3::prelude::*;

// #[pyfunction]
fn example(data: &str) -> String {
    format!("Processed: {}", data)
}

// #[pymodule]
fn core() {
    // позже
}

fn main() {
    println!("{}", example("test"));
}