# Vivo OTA Tracker GUI

Vivo OTA Tracker GUI is a graphical frontend built on top of the [VIVO-OTA-Tracker](https://github.com/JerryTse-OSS/VIVO-OTA-Tracker) project, powered by PyQt5. By loading specific native libraries locally, it constructs device parameters on your PC and fetches official OTA firmware download links for various Vivo / iQOO devices directly from official servers — no physical phone required.

---

**Core Features:**

* 📦 **Firmware Fetching**: Construct device parameters on your PC to request and extract firmware download direct links for various models from official servers (currently China only).
* ⚙️ **Automated Processing**: Automatically handles parameter conversion and data encapsulation required for fetching firmware.
* 📱 **Multi-Device Support**: Supports custom device models, system versions, and other parameters to flexibly fetch firmware for different devices.
* 🖱️ **Graphical Interface**: PyQt5-based GUI, no command line required, one-click to fetch.
* 🌓 **Theme & Language**: Light/Dark theme toggle, Chinese/English bilingual UI.
* 📋 **One-Click Copy**: Copy query results to clipboard with one click, compact/verbose dual log modes available.

---

### 🔧 Built With

| Technology | Purpose | Reference |
|------------|---------|-----------|
| **Python 3.8+** | Core runtime, GUI logic | — |
| **PyQt5** | Cross-platform GUI framework | [PyQt5](https://www.riverbankcomputing.com/software/pyqt/) |
| **Java / JRE** | Runtime for unidbg Android emulator | [Oracle JRE](https://www.oracle.com/java/) |
| **unidbg** | Android native library emulation, executes `libverify_jni.so` to construct OTA request parameters | [zhkl0228/unidbg](https://github.com/zhkl0228/unidbg) |

**How it works:**

1. The GUI collects device parameters (model, SW version, Android version).
2. The program launches an embedded JRE and runs `unidbg-android`, which emulates Android's `libverify_jni.so` native library locally on your PC.
3. `libverify_jni.so` constructs the signed request parameters required by Vivo's OTA server.
4. The tool sends the request and extracts the firmware `.zip` download link from the server response.

> 💡 No physical Android device or ROOT is needed. The entire request construction runs locally via CPU emulation (unidbg).

---

### 🛠️ Environment Prerequisites

#### Option 1: Run the exe directly (Recommended, no environment needed)

Download the latest `VivoOtaTracker.exe` from the [Releases](../../releases) page, double-click to run. **No Python or Java installation required.**

> On first launch, it may take 10–20 seconds to extract resources. This is normal.

#### Option 2: Run from source

1. **Python Environment**:
   * Python 3.8+, install PyQt5: `pip install PyQt5`
2. **Java Environment (JRE)**:
   * The project has an embedded JRE (`jre/` directory), no separate Java installation needed.
   * If Java 8+ is installed on the system, the program will also auto-detect and use it.

---

### 📁 File Structure

The project uses a single-directory structure. All resource files are built-in and must be placed exactly as shown below (**do not move files arbitrarily**):

```
vivo_portable/
├── main.py                                                     # Main entry point (PyQt5 GUI)
├── assets/                                                     # Icons and image resources
│   ├── icon.png                                               # App icon (PNG)
│   ├── icon.ico                                               # App icon (ICO, for PyInstaller)
│   ├── logo_os11_img_pad.png                                  # UI Logo
│   ├── ic_upgrade.png                                         # Fetch button icon
│   ├── originui_vtoolbar_icon_details_rom13_5.png            # Warning dialog icon
│   └── originui_vtoolbar_icon_save_rom13_5.png              # Copy button icon
├── libs/                                                      # Java dependency libraries
│   ├── Updater.apk                                            # Vivo updater APK
│   └── libvivoseckey_n4.so                                  # Security signature library
├── natives/windows_64/                                        # Native dynamic libraries (Windows x64)
│   └── unicorn.dll                                            # CPU emulation engine
├── jre/                                                       # Embedded Java Runtime (x64)
└── unidbg-android-0.9.10-SNAPSHOT.jar                      # Android emulation core (unidbg)
```

---

### 🎯 How to Use

#### Step 1: Select Device Model

In the "Device Model Selection" area, first select the device series (e.g., `X Series`, `iQOO Flagship`, etc.), then select the specific model. The parameter input fields below will auto-fill.

You can also manually fill in the `Project Code` (codename) and `Network Access Model` (model_sw_ver) without using the dropdown selectors.

#### Step 2: Fill in Version Info

> ⚠️ **Important**: This tool does **NOT** support automatically detecting or fetching the device's current version number. You must manually check your phone and fill in the following two parameters:

| Parameter | Description | How to Find on Phone | Example |
|-----------|-------------|----------------------|---------|
| System Software Version | The current system version installed on your device | **Settings → System Update → 右上角 ⚙ → Upgrade Package Manager** | `16.1.16.5.W10` |
| Base Android Version | OriginOS major version's corresponding Android version | OriginOS 3=13, OS 4=14, OS 5=15, OS 6=16 | `16` |

> 💡 The tool queries for firmware packages **≥ the version you entered**. Enter your current version to get the latest available OTA update.

#### Step 3: Start Fetching

Click the **"Get Download Link"** button. The program will invoke the embedded unidbg emulator to construct parameters and make the network request. Wait for the query to complete.

#### Step 4: Copy Result

After the query completes, the result area will display firmware version info and the **`.zip` firmware package direct link**. Click **"Copy to Clipboard"** to copy it.

---

### 🔧 Build from Source (PyInstaller)

If you want to package it as a single-file exe yourself, follow these steps:

#### Prerequisites

```bash
pip install PyQt5 PyInstaller Pillow
```

#### Step 1: Prepare Icon

If you have `icon.png` but lack `icon.ico`, use the following script to convert:

```python
from PIL import Image
img = Image.open("assets/icon.png")
img.save("assets/icon.ico", format="ICO",
    sizes=[(16,16),(32,32),(48,48),(64,64),(128,128),(256,256)])
```

#### Step 2: Run PyInstaller

Execute in the project root directory:

**Windows:**
```bash
pyinstaller --onefile --windowed ^
  --name VivoOtaTracker ^
  --icon assets/icon.ico ^
  --add-data "assets;assets" ^
  --add-data "libs;libs" ^
  --add-data "natives/windows_64;natives/windows_64" ^
  --add-data "jre;jre" ^
  --add-data "unidbg-android-0.9.10-SNAPSHOT.jar;." ^
  --exclude-module matplotlib ^
  --exclude-module scipy ^
  --exclude-module pandas ^
  main.py
```

**Linux / macOS:**
```bash
pyinstaller --onefile --windowed \
  --name VivoOtaTracker \
  --icon assets/icon.ico \
  --add-data "assets:assets" \
  --add-data "libs:libs" \
  --add-data "natives/windows_64:natives/windows_64" \
  --add-data "jre:jre" \
  --add-data "unidbg-android-0.9.10-SNAPSHOT.jar:." \
  --exclude-module matplotlib \
  --exclude-module scipy \
  --exclude-module pandas \
  main.py
```

> **Note**: On Linux/macOS, the `--add-data` separator is colon `:` instead of semicolon `;`.

#### Step 3: Get the exe

After packaging completes, the executable is located at:

```
dist/VivoOtaTracker.exe    # Windows
dist/VivoOtaTracker        # Linux/macOS
```

#### Step 4: Clean Up (Optional)

```bash
rm -rf build/ __pycache__/ VivoOtaTracker.spec
```

---

### 🆘 FAQ & Troubleshooting

Due to differences in Java/Python environments across computers, you may encounter the following common errors during compilation and runtime:

#### ❌ Error 1: `TypeError: _path_exists: path should be ... not NoneType`

* **Cause**: After the first successful run, `_cleanup_work_dir()` sets `self.work_dir` to `None`. Clicking fetch again causes `os.path.exists(None)` to error.
* **Solution**: This bug was fixed in `V1.0.0_Release_mytiantian`. Please use the latest version.

#### ❌ Error 2: `java not found` / `java.exe not found`

* **Cause**: Java is not installed on the system, and the project's embedded JRE path is incorrect.
* **Solution**:
  1. Check whether `jre/bin/java.exe` exists.
  2. Or install JRE 8+ yourself and add it to the system `PATH`.

#### ❌ Error 3: Server returns `{"message":"No update","retcode":210}`

* **Cause**: Firmware info cannot be obtained, usually because:
  1. The `System Software Version` (SW_VERSION) you entered is not in the official open upgrade roadmap.
  2. The push quota for this model/version is full, or the official has temporarily taken down the package.
  3. Requests are too frequent and temporarily restricted.
* **Solution**: Modify the parameters to try other models/versions; or check forums/tieba to confirm the exact system version number that can currently receive updates for this model, then retry after filling it in.

#### ❌ Error 4: Icons disappear after PyInstaller packaging

* **Cause**: Resource file paths were not correctly resolved in packaged mode.
* **Solution**: This issue was fixed in `V1.0.0_Release_mytiantian` using the `resource_path()` function to uniformly handle `_MEIPASS` and development mode paths.

#### ❌ Error 5: Program launches but hangs / becomes unresponsive

* **Cause**: unidbg emulator initialization is slow, or the firewall is blocking network requests.
* **Solution**:
  1. Wait over 30 seconds on first launch.
  2. Check whether the firewall allows the program to access the network.
  3. Switch to "Verbose" log mode to see specific errors.

---

### 📜 Version History

| Version | Date | Description |
|---------|------|-------------|
| V1.0.0_Release_mytiantian | 2026-06-06 | Initial public release, PyQt5 GUI, embedded JRE, PyInstaller onefile build |

---

### 🙏 Acknowledgments

* Original project author: [JerryTse-OSS / VIVO-OTA-Tracker](https://github.com/JerryTse-OSS/VIVO-OTA-Tracker)
* GUI developer: [mytiantian](https://github.com/mytiantian)
* Device model database source: [MobileModels](https://github.com/SecWiki/MobileModels)
* unidbg framework: [zhkl0228/unidbg](https://github.com/zhkl0228/unidbg)

---

### 📝 Disclaimer

**This project is for technical learning and communication purposes only. Do not use it for any illegal or commercial purposes. The user bears all consequences for any problems caused by improper use.**
