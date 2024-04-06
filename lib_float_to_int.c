#include <stdio.h>

int float_to_int(float num) {
    if (num < 0) {
        return (int)(num - 0.5);
    } else {
        return (int)(num + 0.5);
    }
}
