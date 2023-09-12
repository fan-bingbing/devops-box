#include<stdio.h>
// print Fahrenheit-Celsius table
// main()
// {
//     int fahr;
//     for (fahr=0; fahr<=300, fahr=fahr+20;) {
//         printf("%3d %6.1f\n", fahr, (5.0/9.0)*(fahr-32));
//     }
//         return 0;
// }


int main(int argc, char *argv[])
{
    int fahr;
    for (fahr=0; fahr<=300; fahr=fahr+20) 
    {
        printf("%3d %6.1f\n", fahr, (5.0/9.0)*(fahr-32));
    }
        return 0;
}

// int main(int argc, char *argv[])
// {
//     int i = 0;
//     // go through each string in argv
//     // why am I skipping argv[0]?
//     for(i = 1; i < argc; i++) 
//     {
//     printf("arg %d: %s\n", i, argv[i]);
//     }
//     // let's make our own array of strings
//     char *states[] = {
//     "California", "Oregon",
//     "Washington", "Texas"
//     };
//     int num_states = 4;
//     for(i = 0; i < num_states; i++) 
//     {
//     printf("state %d: %s\n", i, states[i]);
//     }
//     return 0;
// }