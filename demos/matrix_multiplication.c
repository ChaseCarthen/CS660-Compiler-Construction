//Main
int main()
{
  //Variables
  int A[5][5], B[5][5], C[5][5];
  int rowACalc, colBCalc, innerValue;


  for(rowACalc = 0; rowACalc < 5; rowACalc++)
  {
    for(colBCalc = 0; colBCalc < 5; colBCalc++)
    {
      A[rowACalc][colBCalc] = rowACalc + colBCalc+1;
      B[rowACalc][colBCalc] = rowACalc + colBCalc+1;
    }
  }

  //Multiply Matrix
  for(rowACalc = 0; rowACalc < 5; rowACalc++)
  {
    for(colBCalc = 0; colBCalc < 5; colBCalc++)
    {
      C[rowACalc][colBCalc] = 0;
      for(innerValue = 0; innerValue < 5; innerValue++)
      {
        C[rowACalc][colBCalc] = C[rowACalc][colBCalc] + (A[rowACalc][innerValue] * B[innerValue][colBCalc]);
      }
    }
  }


  for(rowACalc = 0; rowACalc < 5; rowACalc++)
  {
    for(colBCalc = 0; colBCalc < 5; colBCalc++)
    {
        printint( C[rowACalc][colBCalc] );
    }
  }

  //Return
  return 0;
}
