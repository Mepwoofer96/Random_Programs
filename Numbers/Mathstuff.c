// Mathstuff.c
// to run gcc -g Mathstuff.c -o Mathstuff -lm 
// because it gets mad without -lm


//Library's
#include <math.h>
#include <stdio.h>


int main(){

    float number = 25.68;
    
    double num2 = round(number*100);
    double num4 = num2;
    int num3 = (int) num2;

    int ones = num3 % 10;
    int tens = num3/10 % 10;    
    int hundreds = num3/100 % 10;
    int thousands = num3/1000 % 10;
   
    printf("original Num %f\n", number);
    printf("Truncated Num %f\n", num4);
    printf("int Num %i\n", num3);
    printf("ones %i\n", ones);
    printf("tens %i\n", tens);
    printf("hundreds %i\n", hundreds);
    printf("thousants %i\n", thousands);
    printf("Reconstructed num: %i%i.%i%i\n",thousands,hundreds,tens,ones);

}

