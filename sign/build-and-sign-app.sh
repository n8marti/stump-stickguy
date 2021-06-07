#!/bin/bash

# Manual build-and-sign info here:
#   https://groups.google.com/g/kivy-users/c/5-G7wkbHb_k/m/LjH2TnTU7lMJ

# Set java version.
export JAVA_HOME="/usr/lib/jvm/java-11-openjdk-amd64/"

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
alias="${name_lower}-playstore${debug2}"
signed_apk="${repo_root}/bin/StumpStickguy.apk"

# Get password.
ks_pwd=''
while [[ -z "$ks_pwd" ]]; do
    read -s -p "Set keystore password: " pwd_1
    echo
    read -s -p "Confirm password: " pwd_2
    echo
    if [[ "$pwd_1" == "$pwd_2" ]]; then
        ks_pwd="$pwd_1"
    fi
done

# Ensure keystore for app.
ks_dir=$(realpath ~/keystores)
mkdir -p "$ks_dir"
keystore="${app}.keystore"
ks_path="${ks_dir}/${keystore}"
if [[ ! -e "$ks_path" ]]; then
    # Generate keystore for app (using correct version of java keytool).
    "${JAVA_HOME}/bin/keytool" -genkey -v -keystore "$ks_path" -alias "$alias" -keyalg RSA \
        -keysize 2048 -validity 10000 -storepass "$ks_pwd" \
        -dname "cn=Nate Marti, ou=, o=, c=USA"
        # -dname "cn=myname, ou=mygroup, o=mycompany, c=mycountry"
    ec=$?
    if [[ $ec -ne 0 ]]; then
        echo -e "\nkeytool -genkey error"
        rm -f "$ks_path"
        exit $ec
    fi
    # Convert keystore to JKS format.
    "${JAVA_HOME}/bin/keytool" -importkeystore -srckeystore "$ks_path" -destkeystore "$ks_path" -deststoretype pkcs12 -srcstorepass "$ks_pwd" -deststorepass "$ks_pwd"
    ec=$?
    if [[ $ec -ne 0 ]]; then
        echo "keytool -importkeystore error"
        rm -f "$ks_path"
        exit $ec
    fi
    # # Re-encrypt using different algorithm.
    # # THIS LOSES THE KEY'S alias.
    # openssl pkcs12 -in "$ks_path" -nodes | openssl pkcs12 -export -out "$ks_path"
    # ec=$?
    # if [[ $ec -ne 0 ]]; then
    #     echo "openssl re-encryption error"
    #     rm -f "$ks_path"
    #     exit $ec
    # fi
fi

# Export variables.
export P4A_RELEASE_KEYSTORE="${ks_path}"
export P4A_RELEASE_KEYSTORE_PASSWD="$ks_pwd"
export P4A_RELEASE_KEYALIAS_PASSWD="$ks_pwd"
export P4A_RELEASE_KEYALIAS="$alias"

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
