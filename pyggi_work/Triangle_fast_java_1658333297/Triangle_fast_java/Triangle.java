public class Triangle {

    public enum TriangleType {
        INVALID, SCALENE, EQUALATERAL, ISOCELES
    }

    public static TriangleType classifyTriangle(int a, int b, int c) {

        delay();

        if (a > b) {
            int tmp = a;
            a = b;
            b = tmp;
        }

        // Sort the sides so that a <= b <= c
        if (a > b) {
            int tmp = a;
            a = b;
            b = tmp;
        }

        if (a > c) {
            int tmp = a;
            a = c;
            c = tmp;
        }

        if (b > c) {
            int tmp = b;
            b = c;
            c = tmp;
        }

        

    }

    private static void delay() {
        try {
            Thread.sleep(50);
        } catch (InterruptedException e) {
            // do nothing
        }
    }

}
