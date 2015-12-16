
//void swap(int *s, int *d);

int main() 
{
  int arr[10];
  int i, j;
  int index;
  int temp;
  int temp_2;


  arr[0] = 45;
  arr[1] = 20;
  arr[2] = 10;
  arr[3] = 654;
  arr[4] = 78;
  arr[5] = 124;
  arr[6] = 678;
  arr[7] = 4;
  arr[8] = 13;
  arr[9] = 35;

  for(index = 0; index < 10; index++) {
    printint(arr[index]);
  }
  
  for(i = 0; i < 10; i++)
  {
    for(j = i+1; j < 10; j++)
    {
      if(arr[i] > arr[j]) 
      {
        // Swap function
        swap(&arr[i], &arr[j]);

        // Swap with dummy
        //temp = arr[i];
        //arr[i] = arr[j];
        //arr[j] = temp;

        // Swap with math
        //arr[j] = arr[j] - arr[i];
        //arr[i] = arr[j] + arr[i];
        //arr[j] = arr[i] - arr[j];
      }
    }
  }

  printint(0);
  printint(0);
  printint(0);
  for(index = 0; index < 10; index++) {
    printint(arr[index]);
  }

  return 0;
}


/*void swap(int *s, int *d)
{
  int temp = *d;
  //printint(d);
  //printint(d);
  *d = *s;
  *s = temp;
}*/

