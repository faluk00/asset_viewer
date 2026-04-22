#include <stdio.h>
#include <ctype.h>
#include <string.h>

__declspec(dllexport) int check_version(char* dir_name)
{
    int i, condition = 0;
    for (i = 0; dir_name[i] != '\0'; i++)
    {
        //printf("%c\n", dir_name[i]);
        if (i == 0 && 'v' == dir_name[0])
        {
            condition++;
        }
        else if (dir_name[i] >= '0' && dir_name[i] <= '9' && i > 0)
        {
            condition++;
        }
        else
        {
            condition = 0;
            break;
        }
    }
    if (0 < condition)
    {
        return 1;
    }
    else
    {
        return 0;
    }
}