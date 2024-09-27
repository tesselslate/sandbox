#include <stdio.h>

static const double X = 100;

/*
 * approx approximates the area between y=0 and y=x^2 for the given x.
 *
 * dx is used to define the accuracy of the approximation. Smaller values of dx yield a more
 * accurate result.
 */
double
approx(double x, double dx) {
    double area = 0;
    for (double xm = 0; xm < x; xm += dx) {
        area += dx * (xm * xm);
    }
    return area;
}

/*
 * integral calculates the area beneath y=0 and y=x^2 for the given x.
 *
 * d(area)
 * ------- = x^2    -->     d(area) = x^2
 * d(x)
 *
 * ==================
 *
 * d(1/3 * x^3) = x^2
 *
 * ==================
 *
 */
double
integral(double x) {
    return (x * x * x) / 3.0;
}

int
main() {
    for (double dx = 1; dx > 0.00001; dx /= 10) {
        printf("Approx %lf\t: %lf\n", dx, approx(X, dx));
    }
    printf("Integral: %lf\n", integral(X));

    return 0;
}
