#include <assert.h>
#include <fcntl.h>
#include <inttypes.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/mman.h>
#include <sys/stat.h>

#if __BYTE_ORDER__ != __ORDER_LITTLE_ENDIAN__
#error "psf2h assumes little endian"
#endif

struct psf_font {
    uint32_t magic;
    uint32_t version;
    uint32_t header_size;
    uint32_t flags;
    uint32_t num_glyphs;
    uint32_t bytes_per_glyph;
    uint32_t height;
    uint32_t width;
};

static struct psf_font *
psf_load(const char *file) {
    int fd = open(file, O_RDONLY);
    if (fd == -1) {
        perror("open");
        return NULL;
    }

    struct stat st;
    if (fstat(fd, &st) == -1) {
        perror("fstat");
        return NULL;
    }

    struct psf_font *font = mmap(NULL, st.st_size, PROT_READ, MAP_PRIVATE, fd, 0);
    if (font == MAP_FAILED) {
        perror("mmap");
        return NULL;
    }

    return font;
}

static int
psf2h(struct psf_font *font, FILE *out) {
    char *data = calloc(font->num_glyphs, font->bytes_per_glyph);
    if (data == NULL) {
        perror("calloc");
        return 1;
    }

    for (uint32_t i = 0; i < font->num_glyphs; i++) {
        for (uint32_t y = 0; y < font->height; y++) {
            char *glyph = (char *)font + font->header_size + (i * font->bytes_per_glyph);

            assert((y * font->num_glyphs + i) <= font->num_glyphs * font->bytes_per_glyph);
            data[(y * font->num_glyphs) + i] = *(glyph + y);
        }
    }

    fprintf(out, "static const unsigned char PSF_FONT[] = {");
    for (size_t i = 0; i < font->num_glyphs * font->bytes_per_glyph; i++) {
        fprintf(out, "%"PRIu8",", (unsigned char)data[i]);
    }
    fprintf(out, "};\n");

    return 0;
}

int
main(int argc, char **argv) {
    if (argc < 3) {
        fprintf(stderr, "psf2h INPUT OUTPUT\n");
        return 1;
    }

    struct psf_font *font = psf_load(argv[1]);
    if (!font) {
        return 1;
    }
    if (font->width != 8) {
        fprintf(stderr, "expected width of 8, got %" PRIu32 "\n", font->width);
        return 1;
    }

    FILE *out = fopen(argv[2], "w");
    if (out == NULL) {
        perror("fopen");
        return 1;
    }

    if (psf2h(font, out) != 0) {
        return 1;
    }

    return 0;
}
