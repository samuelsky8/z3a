
#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <termios.h>
#include <unistd.h>
#include <errno.h>

int main(void)
{
    int fd;
    
    fd = open("/dev/ttyUSB0", O_RDWR | O_NOCTTY);

    if( fd == -1 )
    {
        printf("\n    Error!! in Opening ttyUSB0\n");
    }
    else
    {
        printf("\n\n  ttyUSB0 Opened Successfully\n");
    }

    
    struct termios SerialPortSettings;
    
    tcgetattr(fd, &SerialPortSettings);
    
    cfsetispeed(&SerialPortSettings, B115200);
    cfsetispeed(&SerialPortSettings, B115200);
    
    
    close(fd);


    return 0;
}
