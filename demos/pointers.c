
void main() 
{
  int temp = 90;
  int temp_2 = 24;
  int *t = &temp;
  int *s;
  s = &temp_2;
  printint(temp);
  printint(&temp);
  printint(temp_2);
  printint(&temp_2);
  printint(*t);
  printint(t);
  printint(*s);
  printint(s);
}
