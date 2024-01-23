rm -rf out
rm -rf weight_info
rm -rf weight_info_r

./afl-fuzz -i in2 -o out ./readelf -a @@
