### Notes
- Play Store checklist: https://blog.felgo.com/mobile-development-tips/how-to-publish-an-app-on-google-play
- App guidelines: https://developer.android.com/docs/quality-guidelines/core-app-quality
- Material Design: https://material.io/components?platform=android
- KivyMD base: https://kivymd.readthedocs.io/en/latest/getting-started/
- MD icons: https://fonts.google.com/icons?selected=Material+Icons

### Development
- Build the test app.
  - buildozer.spec: https://buildozer.readthedocs.io/en/latest/specifications.html
  - sample: https://raw.githubusercontent.com/kivy/buildozer/master/buildozer/default.spec
- Fixes:
  - Stickguy sometimes guesses the same number twice.

### Publishing
- Content rating "Everyone"
- Get crypto key: http://developer.android.com/tools/publishing/app-signing.html#cert
- Create app store home page materials
  - https://support.google.com/googleplay/android-developer/answer/1078870
  - https://felgo.com/2015/09/7-useful-tips-that-will-improve-your-aso/

### Running the app locally
1. Ensure Python and git are installed.
  - https://www.python.org/downloads/
  - https://git-scm.com/downloads
1. Clone and enter this repository.
  ```bash
  # Linux
  ~$ git clone https://github.com/n8marti/stump-stickguy.git
  #... output of git clone command...
  ~$ cd stump-stickguy
  ```
  ```powershell
  # Windows Powershell
  C:\Users\[Username]\> git clone https://github.com/n8marti/stump-stickguy.git
  #... output of git clone command...
  C:\Users\[Username]\> cd stump-stickguy
  ```
1. Create and activate a virtual environment.
  https://docs.python.org/3/library/venv.html
  ```bash
  ~/stump-stickguy$ python3 -m venv env
  ~/stump-stickguy$ source env/bin/activate
  ```
  ```powershell
  C:\Users\[Username]\stump-stickguy\> py -m venv env
  C:\Users\[Username]\stump-stickguy\> env/scripts/activate.bat
  ```
1. Install dependencies.
  ```bash
  (env) ~/stump-stickguy$ pip3 install -r requirements.txt
  ```
  ```powershell
  (env) C:\Users\[Username]\stump-stickguy\> pip install -r requirements.txt
  ```
1. Run the app.
  ```bash
  (env) ~/stump-stickguy$ python3 app.py
  ```
  ```powershell
  (env) C:\Users\[Username]\stump-stickguy\> py app.py
  ```
