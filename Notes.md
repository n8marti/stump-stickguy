### Notes
- Play Store checklist: https://blog.felgo.com/mobile-development-tips/how-to-publish-an-app-on-google-play
- App guidelines: https://developer.android.com/docs/quality-guidelines/core-app-quality
- Material Design: https://material.io/components?platform=android
- KivyMD base: https://kivymd.readthedocs.io/en/latest/getting-started/
- MD icons: https://fonts.google.com/icons?selected=Material+Icons

### Development
- [ ] Set up testing
  - Try various values for confidence variable.
  - Evaluate Stickguy's success rate.
  - Verify different ways of inputting upper limit numbers.
- [ ] Build the test app.
- [x] Create [animated?] stick figures
- [x] Create number line graph
- [x] Allow user to set max value.
- [x] Add "Go" or "Restart" button.

### Publishing
- [ ] Content rating "Everyone"
- [ ] Get crypto key: http://developer.android.com/tools/publishing/app-signing.html#cert
- [ ] Create app icon
- [ ] Create app store home page materials
  - https://support.google.com/googleplay/android-developer/answer/1078870
  - https://felgo.com/2015/09/7-useful-tips-that-will-improve-your-aso/

### Running the app locally
1. Ensure Python and git are installed.
  - https://www.python.org/downloads/
  - https://git-scm.com/downloads
1. Clone and enter this repository.
```
~$ git clone https://github.com/n8marti/stump-stickguy.git
[... output of git clone command...]
~$ cd stump-stickguy
```
1. Create and activate a virtual environment.
```
~/stump-stickguy$ python3 -m venv env
~/stump-stickguy$ source env/bin/activate
```
  Or in Windows:
```cmd
C:\Users\[Username]\stump-stickguy\> env/scripts/activate.bat
```
1. Install dependencies.
```
(env) ~/stump-stickguy$ pip3 install --requirement requirements.txt
```
1. Run the app.
```
(env) ~/stump-stickguy$ python3 app.py
```
