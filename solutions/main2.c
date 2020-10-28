#include <stdio.h>

int main(void)
{
  char loyalty, cont;
  double total = 0;
  int item, quantity;

  printf("Are you a loyalty customer(Y/N)? ");
  scanf("%c", &loyalty);

  int i = 0;
 // while(1);
  
  while (i++ < 5)
  {
    printf("Input the item number: ");
    scanf("%d", &item);

    printf("Input the quantity: ");
    scanf("%d", &quantity);

    switch(item)
    {
      case 1:
        total += (quantity * 362);
        break;
      case 2:
        total += (quantity * 330);
        break;
      case 3:
        total += (quantity * 630);
        break;
      case 4:
        total += (quantity * 350);
        break;
    }

    printf("\nDo you want to continue (Y/N)? ");
    scanf("%*c%c", &cont);
    printf("\n");

    if (cont == 'N')
    {
      break;
    }
  } // end loop

  if (loyalty == 'Y')
  {
    if (total >= 10000)
    {
      total = total * 0.8;
    }
    else if (total >= 5000)
    {
      total = total * 0.85;
    }
    else if (total >= 1000)
    {
      total = total * 0.92;
    }
    else
    {
      total = total * 0.95;
    }
  }

  printf("Net amount is %.2f\n", total);
  return 0;
}
