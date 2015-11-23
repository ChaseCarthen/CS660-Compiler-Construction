
void fillMatrix(int array[], int row, int col);

//Main
int main()
{
  //Variables
  int A[25], B[25], C[25];
  int rowACalc, colBCalc, innerValue;
  int aRow = 5, aCol = 5, bRow = 5, bCol = 5;


  //Fill Each Matrix
  fillMatrix(A,aRow,aCol);
  fillMatrix(B,bRow,bCol);

  //Multiply Matrix
  for(rowACalc = 0; rowACalc < aRow; rowACalc++)
  {
    for(colBCalc = 0; colBCalc < bCol; colBCalc++)
    {
      C[(rowACalc*bCol)+colBCalc] = 0;
      for(innerValue = 0; innerValue < aCol; innerValue++)
      {
        C[(rowACalc*bCol)+colBCalc] = C[(rowACalc*bCol)+colBCalc] + (A[(rowACalc*aCol)+innerValue] * B[(innerValue*bCol)+colBCalc]);
      }
    }
  }

  //Return
  return 0;
}

void fillMatrix(int array[], int row, int col)
{
  int irow, icol;
  for(irow = 0; irow < row; irow++)
  {
    for(icol = 0; icol < col; icol++)
    {
      array[(irow * col) + icol] = (icol+irow)+1;
    }
  }
}
