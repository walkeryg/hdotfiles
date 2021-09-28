1. put the env variable in your build sciprt
  SOONG_GEN_COMPDB=1 SOONG_GEN_COMPDB_DEBUG=1
such as:
-    /bin/bash -i -c "source build/envsetup.sh && TARGET_PRODUCT=$TROM_BUILD_TARGET TARGET_BUILD_TYPE=$ANDROID_TARGET_BUILD_TYPE TARGET_BUILD_VARIANT=$TROM_BUILD_VARIANT make -j $JOBS";
+    /bin/bash -i -c "source build/envsetup.sh && TARGET_PRODUCT=$TROM_BUILD_TARGET TARGET_BUILD_TYPE=$ANDROID_TARGET_BUILD_TYPE TARGET_BUILD_VARIANT=$TROM_BUILD_VARIANT SOONG_GEN_COMPDB=1 SOONG_GEN_COMPDB_DEBUG=1 make -j $JOBS";

2. the copmile_commands.json will be at out/soong/development/ide/compdb
   But this only have modeuls in Android.bp. it is genereated by soong, module in Android.mk is not included
