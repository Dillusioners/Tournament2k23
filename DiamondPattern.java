import java.util.Scanner;
class DiamondPattern {
    private static void printPattern(int s, int e) {
        //Printing the upper part of the diamond
        for(int i = s; i <= e; i++) {
            //Printing spacing in correspondence with ending and starting
            for(int j=e; j >=i; j--)
                System.out.print(" ");
            //Left half of diamond
            for(int j=i; j > s; j--) 
                System.out.print(j);
            //Right half of diamond
            for(int j = s; j <= i; j++)
                System.out.print(j);
            //Next line printer
            System.out.println();
        }
        //Printing the lower partg of the diamond
        for(int i = e; i >= s; i--) {
            //Printing spacing is descending order
            for(int j = e; j >= i - 1; j--)
                System.out.print(" ");
            //Left half of diamond opposite logic
            for(int j = i-1; j > s; j--)
                System.out.print(j);
            //Right half of diamond opposite logic
            for(int j = s; j < i; j++)
                System.out.print(j);
            //Next line printer
            System.out.println();
        }
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        //Taking Inputs
        System.out.println("Enter the starting : ");
        //Starting
        int start = sc.nextInt();
        System.out.println("Enter ending number : ");
        //Ending
        int end = sc.nextInt();
        if(start > end)
            System.out.println("Starting cannot be greater than ending !");
        //caling the method to print the pattern
        printPattern(start,end);
        sc.close();
    }
}
