#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>
#include <unistd.h>
#include <fcntl.h>
#include <poll.h>
#include <string.h>
 
#include <sys/ioctl.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <linux/i2c-dev.h>
#include <linux/spi/spidev.h>
 
enum { SPI_RX, SPI_TX, SPI_TXRX };
 
/****************************************************************
* Constants
****************************************************************/
 
#define SYSFS_GPIO_DIR "/sys/class/gpio"
#define POLL_TIMEOUT (3 * 1000) /* 3 seconds */
#define MAX_BUF 64
 
/****************************************************************
* spi_open
****************************************************************/
int spi_open(void)
{
int ret;
int handle;
 
handle = open("/dev/spidev1.0", O_RDWR);
if(handle < 0) return -1;
 
unsigned char lsb = 0;
unsigned int speed = 10000;
unsigned char mode = SPI_MODE_3;
unsigned char r_mode;
 
ret = ioctl(handle, SPI_IOC_WR_LSB_FIRST, &lsb);
if(ret < 0) return -2;
 
ret = ioctl(handle, SPI_IOC_WR_MAX_SPEED_HZ, &speed);
if(ret < 0) return -3;
 
ret = ioctl(handle, SPI_IOC_WR_MODE, &mode);
if(ret < 0) return -4;
 
ret = ioctl(handle, SPI_IOC_RD_MODE, &r_mode);
if(ret < 0) return -5;
 
//printf("MODE_r : %d\n", r_mode);
 
return handle;
}
 
/****************************************************************
* spi_read_write
****************************************************************/
int spi_read_write(int fd, struct spi_ioc_transfer *p_xfer, int rw)
{
int ret;
unsigned char lsb;
unsigned int speed;
unsigned char mode = SPI_MODE_3;
unsigned char r_mode = SPI_MODE_3;
 
ret = ioctl(fd, SPI_IOC_RD_LSB_FIRST, &lsb);
if(ret < 0) return -1;
//printf("LSB : %d\n", lsb);
 
speed = 500000;
ret = ioctl(fd, SPI_IOC_WR_MAX_SPEED_HZ, &speed);
 
ret = ioctl(fd, SPI_IOC_RD_MAX_SPEED_HZ, &speed);
if(ret < 0) return -1;
//printf("SPEED : %d\n", speed);
 
ret = ioctl(fd, SPI_IOC_WR_MODE, &mode);
if(ret < 0) return -1;
 
ret = ioctl(fd, SPI_IOC_RD_MODE, &r_mode);
if(ret < 0) return -1;
//printf("MODE : %d\n", r_mode);
 
if(rw == SPI_TX) {
ret = ioctl(fd, SPI_IOC_MESSAGE(1), p_xfer);
}
else if(rw == SPI_TXRX) {
ret = ioctl(fd, SPI_IOC_MESSAGE(2), p_xfer);
}
return ret;
}
 
int lis3dh_read_whoami(int fd, unsigned int *id)
{
int i;
int ret;
unsigned char    buf_t[2];
unsigned char    buf_r[2];
struct spi_ioc_transfer  xfer[2];
 
memset(xfer, 0, sizeof xfer);
memset(buf_t, 0, sizeof buf_t);
memset(buf_r, 0, sizeof buf_r);
 
buf_t[0] = 0x8f;
buf_t[1] = 0x00;
 
xfer[0].tx_buf = (unsigned long)buf_t;
xfer[0].rx_buf = (unsigned long)buf_r;
xfer[0].len = 2;
 
ret = spi_read_write(fd, xfer, SPI_TX);
 
if(ret < 0) {
printf("SPI_IOC_MESSAGE\n");
return ret;
}
 
*id = buf_r[1];
return 0;
}
 
int lis3dh_enable_axises(int fd)
{
int i;
int ret;
unsigned char    buf_t[2];
unsigned char    buf_r[2];
struct spi_ioc_transfer  xfer[2];
 
memset(xfer, 0, sizeof xfer);
memset(buf_t, 0, sizeof buf_t);
memset(buf_r, 0, sizeof buf_r);
 
buf_t[0] = 0x20;
buf_t[1] = 0x77;
 
xfer[0].tx_buf = (unsigned long)buf_t;
xfer[0].rx_buf = (unsigned long)buf_r;
xfer[0].len = 2;
 
ret = spi_read_write(fd, xfer, SPI_TX);
 
if(ret < 0) {
printf("SPI_IOC_MESSAGE\n");
return ret;
}
 
buf_t[0] = 0x23;
buf_t[1] = 0x08;
 
ret = spi_read_write(fd, xfer, SPI_TX);
 
if(ret < 0) {
printf("SPI_IOC_MESSAGE\n");
return ret;
}
 
return 0;
}
 
int lis3dh_read_axises(int fd, unsigned int *x, unsigned int *y, unsigned int *z)
{
int i;
int ret;
unsigned char    buf_t[4];
unsigned char    buf_r[4];
struct spi_ioc_transfer  xfer[4];
 
unsigned int temp_x;
unsigned int temp_y;
unsigned int temp_z;
 
memset(xfer, 0, sizeof xfer);
memset(buf_t, 0, sizeof buf_t);
memset(buf_r, 0, sizeof buf_r);
 
xfer[0].tx_buf = (unsigned long)buf_t;
xfer[0].rx_buf = (unsigned long)buf_r;
xfer[0].len = 2;
 
//--------------- status -------------------//
buf_t[0] = 0xA7;
buf_t[1] = 0x00;
 
ret = spi_read_write(fd, xfer, SPI_TX);
 
if(ret < 0) {
printf("SPI_IOC_MESSAGE\n");
return ret;
}
printf("%d buf_r : %02x \n", ret, buf_r[1]);
 
//--------------- axis-x -------------------//
buf_t[0] = 0xA8;
buf_t[1] = 0x00;
 
ret = spi_read_write(fd, xfer, SPI_TX);
 
if(ret < 0) {
printf("SPI_IOC_MESSAGE\n");
return ret;
}
 
temp_x = buf_r[1];
 
buf_t[0] = 0xA9;
 
ret = spi_read_write(fd, xfer, SPI_TX);
 
if(ret < 0) {
printf("SPI_IOC_MESSAGE\n");
return ret;
}
 
temp_x |= (buf_r[1] << 8);
 
//--------------- axis-y -------------------//
buf_t[0] = 0xAA;
 
ret = spi_read_write(fd, xfer, SPI_TX);
 
if(ret < 0) {
printf("SPI_IOC_MESSAGE\n");
return ret;
}
 
temp_y = buf_r[1];
 
buf_t[0] = 0xAB;
 
ret = spi_read_write(fd, xfer, SPI_TX);
 
if(ret < 0) {
printf("SPI_IOC_MESSAGE\n");
return ret;
}
 
temp_y |= (buf_r[1] << 8);
 
//--------------- axis-z -------------------//
buf_t[0] = 0xAC;
 
ret = spi_read_write(fd, xfer, SPI_TX);
 
if(ret < 0) {
printf("SPI_IOC_MESSAGE\n");
return ret;
}
 
temp_z = buf_r[1];
 
buf_t[0] = 0xAD;
 
ret = spi_read_write(fd, xfer, SPI_TX);
 
if(ret < 0) {
printf("SPI_IOC_MESSAGE\n");
return ret;
}
 
temp_z |= (buf_r[1] << 8);
 
*x = temp_x;
*y = temp_y;
*z = temp_z;
 
return 0;
}
 
/****************************************************************
* Main
****************************************************************/
int main(int argc, char **argv, char **envp)
{
unsigned int id;
int ret;
struct pollfd fdset[2];
int nfds = 2;
int gpio_fd, timeout, rc;
int spi_fd;
unsigned int x, y, z;
 
spi_fd = spi_open();
 
int count;
 
ret = lis3dh_read_whoami(spi_fd, &id);
printf("ID code : 0x%02x\n", id & 0xFF);
 
ret = lis3dh_enable_axises(spi_fd);
 
for(count = 0; count < 100; count++) {
usleep(500000);
 
ret = lis3dh_read_axises(spi_fd, &x, &y, &z);
printf("x : 0x%04x,  y : 0x%04x,  z : 0x%04x\n", x, y, z);
}
 
close(spi_fd);
printf("spi close\n");
 
return 0;
}
