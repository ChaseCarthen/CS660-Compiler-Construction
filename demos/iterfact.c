// Note to the grader: both the iterative and recursive factorial are here!

// recursive factorial implementation -- down below
int recurfact(int n);

// iterative factorial implementation -- down below
int iterfact(int n);

int main()
{
   int n = 5;
   //printf("What factorial(n) do you wish to compute (n=): ");
   //scanf("%d", &n);

   //printint(iterfact(n));
   printint(recurfact(n));
}


int recurfact(int n)
{
   if (n < 2)
   {
      return 1;
   }
   else
   {
      //int value = n - 1;
      return recurfact(n-1) * n;
   }
}

int iterfact(int n)
{
   int product = 1;
   int i = 1;
   for(i = 2; i <= n; i++)
   {
      product = product * i;
   }
   return product;
}


