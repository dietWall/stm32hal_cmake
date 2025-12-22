

int main(void)
{
    volatile int x = 0;
    volatile int y = 0xFFFFFFFF;
    while(1)
    {  
        x--;
        y--;
    }
}