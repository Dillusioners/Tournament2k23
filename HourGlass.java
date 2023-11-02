import java.util.*;

class HourGlass {
    public static void main(String[] args) {
        // Making the Scanner object
        Scanner sc = new Scanner(System.in);

        // Taking the input from the user.
        System.out.print("Enter the middle value of the hour glass: ");
        int num = sc.nextInt();

        // Making a new line
        System.out.println();

        // Assigning Values for the print statements
        int left = 1;
        int right = (num * 2) - 1;

        // Loop for the top half of the hourglass
        for (int i = 1; i <= num; i++) {

            // Print leading spaces
            for (int j = 1; j < i; j++) {
                System.out.print(" ");
            }

            // Loop for each row
            for (int j = i; j <= num; j++) {
                if (j == i) {
                    // Print the left part of the hourglass
                    System.out.print(left + " ");
                    left++;
                } else if (i == 1 && j != 1 && j != num) {
                    // For the first row, print zeros in the middle
                    System.out.print(0 + " ");
                } else if (j == num) {
                    // Print the right part of the hourglass
                    System.out.print(right + " ");
                    right--;
                } else {
                    // Print spaces for the middle part
                    System.out.print("  ");
                }
            }

            // Making a new line
            System.out.println();
        }

        // Decrease the right value for the next loop
        right--;

        // Loop for the bottom half of the hourglass
        for (int i = num - 1; i >= 1; i--) {

            // Print leading spaces
            for (int j = 1; j < i; j++) {
                System.out.print(" ");
            }

            // Loop for each row
            for (int j = i; j <= num; j++) {
                if (j == i) {
                    // Print the right part of the hourglass
                    System.out.print(right + " ");
                    right--;
                } else if (i == 1 && j != 1 && j != num) {
                    // For the first row, print zeros in the middle
                    System.out.print(0 + " ");
                } else if (j == num) {
                    // Print the left part of the hourglass
                    System.out.print(left + " ");
                    left++;
                } else {
                    // Print spaces for the middle part
                    System.out.print("  ");
                }
            }

            // Making a new line
            System.out.println();
        }

        // Closing the Scanner object
        sc.close();
    }
}
