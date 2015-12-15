
int recurfact(int n);
int iterfact(int n);

int main()
{
   int n = 5;
   printint(iterfact(n));
   printint(recurfact(n));
}


int recurfact(int n)
{
   if (n == 1 || n <= 0)
   {
      return 1;
   }
   else
   {
      return n *recurfact(n-1);
   }
}

int iterfact(int n)
{
   int product = 1;
   int i = 1;
   for(i = 2; i <= n; i++)
   {
      //printint(10);
      product = product * i;
   }
   return product;
}


