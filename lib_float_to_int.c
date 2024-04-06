#include <stdio.h>

int round_float(float num) {
    if (num < 0) {
        return (int)(num - 0.5);
    } else {
        return (int)(num + 0.5);
    }
}

int main() {
    float float_number = 3.15;
    int int_number;

    int_number = round_float(float_number);

    printf("Float: %.2f\n", float_number);
    printf("Int: %d\n", int_number);

    return 0;
}
