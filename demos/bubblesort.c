// This function will do a bubble sort on a list of ints.
void bubblesort(int* list, int size);

// A generic swap function using pointers.. I assuming references will be passed in
void swap(int* a, int* b);

int main()
{
   // I have programed a static value, but this can be easily changed.
   int a[20];

   //  Iterate through and create random numbers that are between 0 and 1000.
   int i = 0;
   for (i = 0; i < 20; i++)
   {
      a[i] = i;
   }

   // sort the list 
   bubblesort(a, 20);

   return 0;
}

void bubblesort(int* list, int size)
{
   int i = 0;
   int j = 0;
   for (i = 0; i < size; i++)
   {
      int min = 10000000;
      int minindex = -1;

      for (j = i; j < size; j++ )
      {
         // I know that I could do my swapping here.
         if (list[j] < min)
         {
            minindex = j;
            min = list[j];
         }
      }

      // swap the min -- but I am doing it here
      if (minindex != -1)
      {
         int temp = list[i];
         list[i] = list[minindex];
         list[minindex] = temp;
      }
         //swap(&list[i], &list[minindex]);
   }
}

/*void swap(int* a, int* b)
{
   // swapping values, but not pointers.
   int temp = *a;
   *a = *b;
   *b = temp;
}*/
