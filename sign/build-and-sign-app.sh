#!/bin/bash

# Manual build-and-sign info here:
#   https://groups.google.com/g/kivy-users/c/5-G7wkbHb_k/m/LjH2TnTU7lMJ

if [[ ! $VIRTUAL_ENV ]]; then
    echo "Virtual environment not activated. Can't build and sign the app."
    exit 1
fi

# Set variables.
repo_root=$(realpath "${VIRTUAL_ENV}/..")
# echo "repo_root: $repo_root"
unsigned_apk=$(find "${repo_root}/bin" -name *.apk | sort -rn | head -1)
# echo "unsigned_apk: $unsigned_apk"
name_lower=$(basename "$unsigned_apk" | awk -F'-' '{print $1}')
# echo "name_lower: $name_lower"
version=$(basename "$unsigned_apk" | awk -F'-' '{print $2}')
# echo "version: $version"
debug1=''
debug2=''
if [[ "$(basename "$unsigned_apk" | awk -F'-' '{print $5}')" == 'debug.apk' ]]; then
    debug1='.debug'
    debug2='-debug'
fi
app="com.n8marti${debug1}.${name_lower}"
# echo "app: $app"
alias="${name_lower}-playstore${debug2}"
# echo "alias: $alias"
signed_apk="${repo_root}/bin/StumpStickguy.apk"
# echo "signed_apk: $signed_apk"

# Ensure keystore for app.
ks_dir=$(realpath ~/keystores)
mkdir -p "$ks_dir"
keystore="${app}.keystore"
if [[ ! -e "${ks_dir}/${keystore}" ]]; then
    # Generate keystore for app.
    keytool -genkey -v -keystore "${ks_dir}/${keystore}" -alias "$alias" -keyalg RSA -keysize 2048 -validity 10000
    ec=$?
    if [[ $ec -ne 0 ]]; then
        echo "keytool error"
        exit $ec
    fi
fi

# Ensure release build for app.
buildozer android release
ec=$?
if [[ $ec -ne 0 ]]; then
    echo "buildozer error"
    exit $ec
fi

# Ensure signed jar for app.
jarsigner -verbose -sigalg SHA1withRSA -digestalg SHA1 -keystore "${ks_dir}/${keystore}" "$unsigned_apk" "$alias"
ec=$?
if [[ $ec -ne 0 ]]; then
    echo "jarsigner error"
    exit $ec
fi

# Ensure zipalignment for app.
# TODO: android-sdk-21 doesn't exist in my .buildozer dir.
.buildozer/android/platform/android-sdk-21/tools/zipalign -v 4 "$unsigned_apk" "$signed_apk"
ec=$?
if [[ $ec -ne 0 ]]; then
    echo "zipalign error"
    exit $ec
fi
