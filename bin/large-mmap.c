#include <stdint.h>
#include <stdio.h>
#include <sys/mman.h>

static const size_t reserve = (size_t)1 << 36;
static const size_t commit = (size_t)1 << 32;

int
main() {
    void *data = mmap(NULL, reserve, PROT_NONE, MAP_PRIVATE | MAP_ANONYMOUS, -1, 0);
    if (data == MAP_FAILED) {
        perror("mmap");
        return 1;
    }

    printf("%p\n", data);
    fgets("\n", 100, stdin);

    if (mprotect(data, commit, PROT_READ | PROT_WRITE) != 0) {
        perror("mprotect");
        return 1;
    }

    printf("called mprotect\n");
    fgets("\n", 100, stdin);

    for (uint64_t i = 0; i < commit; i += 4096) {
        *(char*)(data + i) = '\0';
    }

    printf("backed memory\n");
    fgets("\n", 100, stdin);

    return 0;
}
