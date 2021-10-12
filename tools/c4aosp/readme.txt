1. put the env variable in your build sciprt
  SOONG_GEN_COMPDB=1 SOONG_GEN_COMPDB_DEBUG=1
such as:
-    /bin/bash -i -c "source build/envsetup.sh && TARGET_PRODUCT=$TROM_BUILD_TARGET TARGET_BUILD_TYPE=$ANDROID_TARGET_BUILD_TYPE TARGET_BUILD_VARIANT=$TROM_BUILD_VARIANT make -j $JOBS";
+    /bin/bash -i -c "source build/envsetup.sh && TARGET_PRODUCT=$TROM_BUILD_TARGET TARGET_BUILD_TYPE=$ANDROID_TARGET_BUILD_TYPE TARGET_BUILD_VARIANT=$TROM_BUILD_VARIANT SOONG_GEN_COMPDB=1 SOONG_GEN_COMPDB_DEBUG=1 make -j $JOBS";

2. the copmile_commands.json will be at out/soong/development/ide/compdb
   But this only have modeuls in Android.bp. it is genereated by soong, module in Android.mk is not included

3. Using generate_compdb.py to get copmile_commands for Android.mk modules
   python generate_compdb.py -r {your_root_dir} --ninja_file {your_project_ninja_file} will genereate all copmile_commands from build-{project}.ninja
   such as my aosp root dir is /home/xxx/android/R, my project is aosp_arm:
    python3 generate_compdb.py --ninja_file /home/xxx/android/R/out/build-aosp_arm.ninja  -r /home/xxx/android/R
  
  if you just want to generate copmile_commands for modules or some files, you can use -m or -f

4. extract copmile_commands from bigger copmile_commands files
   such as:
   python3 cut_compdb.py --infile /home/xxx/android/R/out/soong/development/ide/compdb/compile_commands.json --outfile /home/xxx/android/R/system/netd/server/compile_commands.json --prefix system/netd/server

  --infile: which large compile_commands you want to split
  --outfile: the splitted compile_commands file
  --prefix: which path's files you want to splitted from the whole bigger compile_commands

5. install clangd extension for vscode

6. clangd_user_settings.json should merge into ~/.config/Code/User/settings.json

7. clangd/config.yaml should merge into ~/.config/clangd/config.yaml 