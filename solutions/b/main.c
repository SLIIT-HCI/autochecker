#include <stdio.h>

int main(void)
{
  char employee_category = 'E';
  float salary = 0;
  int hours = 0, overtime = 0;

  printf("Input Employee's Category (A/B/C/D/E): ");
  scanf("%c", &employee_category);

  printf("Input basic salary: ");
  scanf("%f", &salary);

  switch (employee_category)
  {
    case 'A':
      salary = salary * 1.12;
      break;
    case 'B':
      salary = salary * 1.10;
      break;
    case 'C':
      salary = salary * 1.06;
      break;
    case 'D':
      salary = salary * 1.03;
      break;
  }

  int week=1;
  while (week <= 4)
  {
    printf("Input OT hours for week %d : ", week);
    scanf("%d", &hours);

    if (hours > 20)
    {
      printf("OT hours cannot exceed 20 per week\n");
    }
    else
    {
      if (hours <= 5)
        overtime = hours * 200;
      else if (hours <= 10)
        overtime = hours * 300;
      else if (hours <= 15)
        overtime = hours * 400;
      else if (hours <= 20)
        overtime = hours * 500;

      salary += overtime;
      week++;
    } // end else
  } // end loop

  printf("Total Salary: %.2f\n", salary);

  return 0;
}
