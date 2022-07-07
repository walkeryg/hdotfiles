sudo apt install qemu-system-arm qemu-efi
sudo apt install qemu-user
sudo apt install gcc-arm-linux-gnueabihf

cd test/qemu
arm-linux-gnueabihf-gcc -static test.c -o test 
qemu-arm test
