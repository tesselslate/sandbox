use criterion::{black_box, criterion_group, criterion_main, Criterion};

pub fn bench_add(c: &mut Criterion) {
    c.bench_function("add", |b| b.iter(|| black_box(2 + 3)));
}

criterion_group!(add, bench_add);
criterion_main!(add);
