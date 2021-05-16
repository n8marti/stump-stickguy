#!/bin/bash

# Manual build-and-sign info here:
#   https://groups.google.com/g/kivy-users/c/5-G7wkbHb_k/m/LjH2TnTU7lMJ

app="com.n8marti.debug.stumpstickguy"
alias="stump-stickguy-playstore-debug"
unsigned_apk="./stump-stickguy/bin/stumpstickguy-0.1-armeabi-v7a-debug.apk"
signed_apk="./stump-stickguy/bin/StumpStickguy.apk"

init_dir=$PWD

# Ensure keystore for app.
ks_dir="~/keystores"
keystore="${app}.keystore"
if [[ ! -e "${ks_dir}/${keystore}" ]]; then
    # Generate keystore for app.
    keytool -genkey -v -keystore "${ks_dir}/${keystore}" -alias "$alias" -keyalg RSA -keysize 2048 -validity 10000
fi

# Ensure release build for app.
buildozer android release

# Ensure signed jar for app.
jarsigner -verbose -sigalg SHA1withRSA -digestalg SHA1 -keystore "${ks_dir}/${keystore}" "$unsigned_apk" "$alias"

# Ensure zipalignment for app.
# TODO: android-sdk-21 doesn't exist in my .buildozer dir.
.buildozer/android/platform/android-sdk-21/tools/zipalign -v 4 "$unsigned_apk" "$signed_apk"
