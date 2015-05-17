class someClass
{
public:
    //Some code here
    void fun() const
    {
        grid[0][0] ='1';
    }
private:

    char grid[20][20];

    //Some code here

};

int main()
{
    someClass x;
    x.fun();

}
