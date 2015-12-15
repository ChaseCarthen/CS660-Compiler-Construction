
struct Intel {
  int i;
  char j;
};

void main() 
{
  struct Intel item;
  item.i = 90;
  item.j = 'k';

  printint(item.i);
  printchar(item.j);

}
