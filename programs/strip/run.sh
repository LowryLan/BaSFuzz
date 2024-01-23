rm -rf out
rm -rf weight_info
rm -rf weight_info_r

./afl-fuzz -i in -o out ./strip-new @@ -o tmp_file
