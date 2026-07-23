# Vivo OTA Tracker GUI

Vivo OTA Tracker GUI is a graphical frontend built on top of the [VIVO-OTA-Tracker](https://github.com/JerryTse-OSS/VIVO-OTA-Tracker) project. By loading specific native libraries locally, it constructs device parameters on your PC and fetches official OTA firmware download links for various Vivo / iQOO devices directly from official servers — no physical phone required.

---

**Core Features:**

* **Firmware Fetching**: Construct device parameters on your PC to request and extract firmware download direct links for various models from official servers (currently China only).
* **Automated Processing**: Automatically handles parameter conversion and data encapsulation required for fetching firmware.
* **Multi-Device Support**: Supports custom device models, system versions, and other parameters to flexibly fetch firmware for different devices.
* **Liquid Glass UI**: Acrylic blur background, fully transparent cards and controls, white text with Microsoft YaHei font.
* **Graphical Interface**: PyQt-Fluent-Widgets based GUI, no command line required, one-click to fetch.
* **Bilingual UI**: Chinese/English language toggle.
* **One-Click Copy**: Copy query results to clipboard with one click, compact/verbose dual log modes available.
* **Update Log**: Automatic update log fetching and display from official sources.
* **SNP & Full Package**: Serial Number (SNP) input and Full Package (IS_FULL) option for advanced users.

---

### Built With

| Technology | Purpose | Reference |
|------------|---------|-----------|
| **Python 3.8+** | Core runtime, GUI logic | — |
| **PyQt5** | Cross-platform GUI framework | [PyQt5](https://www.riverbankcomputing.com/software/pyqt/) |
| **PyQt-Fluent-Widgets** | Liquid Glass UI components | [PyQt-Fluent-Widgets](https://github.com/zhiyiYo/PyQt-Fluent-Widgets) |
| **pywinstyles** | Windows acrylic blur effects | [pywinstyles](https://github.com/Osanchez/pywinstyles) |
| **Java / JRE** | Runtime for unidbg Android emulator | [Oracle JRE](https://www.oracle.com/java/) |
| **unidbg** | Android native library emulation, executes `libverify_jni.so` to construct OTA request parameters | [zhkl0228/unidbg](https://github.com/zhkl0228/unidbg) |

**How it works:**

1. The GUI collects device parameters (model, SW version, Android version).
2. The program launches an embedded JRE and runs `unidbg-android`, which emulates Android's `libverify_jni.so` native library locally on your PC.
3. `libverify_jni.so` constructs the signed request parameters required by Vivo's OTA server.
4. The tool sends the request and extracts the firmware `.zip` download link from the server response.

> No physical Android device or ROOT is needed. The entire request construction runs locally via CPU emulation (unidbg).

---

### Environment Prerequisites

#### Option 1: Run the exe directly (Recommended, no environment needed)

Download the latest `VivoOtaTracker.exe` from the [Releases](../../releases) page, double-click to run. **No Python or Java installation required.**

> On first launch, it may take 10-20 seconds to extract resources. This is normal.

#### Option 2: Run from source

1. **Python Environment**:
   * Python 3.8+
   * Install dependencies: `pip install PyQt5 PyQt-Fluent-Widgets pywinstyles`
2. **Java Environment (JRE)**:
   * The project has an embedded JRE (`jre/` directory), no separate Java installation needed.
   * If Java 8+ is installed on the system, the program will also auto-detect and use it.

---

### File Structure

The project uses a single-directory structure. All resource files are built-in and must be placed exactly as shown below:

```
VIVO-OTA-Tracker/
├── main.py                                      # Main entry point
├── src/                                         # Python source modules
│   ├── __init__.py
│   ├── i18n.py                                  # Translations and version info
│   ├── models.py                                # Device model database (14 series, 395 models)
│   ├── ota_core.py                              # Java command builder and OTA core logic
│   ├── themes.py                                # Theme configuration
│   ├── widgets.py                               # Custom widgets
│   └── window.py                                # Main window (Liquid Glass GUI)
├── assets/                                      # Icons and image resources
│   ├── icon.png                                 # App icon (PNG)
│   ├── icon.ico                                 # App icon (ICO, for PyInstaller)
│   ├── logo_os11_img_pad.png                    # UI Logo
│   └── ic_upgrade.png                           # Fetch button icon
├── libs/                                        # Native libraries
│   └── libvivoseckey.so                         # Vivo security signature library
├── jre/                                         # Embedded Java Runtime (x64)
├── unidbg-android-0.9.10-SNAPSHOT.jar           # Android emulation core (unidbg)
├── VivoOtaTracker.java                          # Java source (latest synced)
└── VivoOtaTracker.onefile.spec                  # PyInstaller spec file
```

---

### How to Use

#### Step 1: Select Device Model

In the "Device Model Selection" area, first select the device series (e.g., `X Series`, `iQOO Flagship`, etc.), then select the specific model. The parameter input fields below will auto-fill.

You can also manually fill in the `Project Code` (codename) and `Network Access Model` (model_sw_ver) without using the dropdown selectors.

#### Step 2: Fill in Version Info

> **Important**: This tool does **NOT** support automatically detecting or fetching the device's current version number. You must manually check your phone and fill in the following two parameters:

| Parameter | Description | How to Find on Phone | Example |
|-----------|-------------|----------------------|---------|
| System Software Version | The current system version installed on your device (5 separate fields) | Settings - System Update - Top right gear - Upgrade Package Manager | 16 . 1 . 16 . 5 . W10 |
| Base Android Version | OriginOS major version's corresponding Android version | OriginOS 3=13, OS 4=14, OS 5=15, OS 6=16 | 16 |

> The tool queries for firmware packages greater than or equal to the version you entered. Enter your current version to get the latest available OTA update.

#### Step 3: (Optional) Advanced Parameters

* **Serial Number (SNP)**: Device serial number, leave empty to use default value.
* **Full Package**: Check to request full OTA package, uncheck for incremental.

#### Step 4: Start Fetching

Click the **"Get Download Link"** button. The program will invoke the embedded unidbg emulator to construct parameters and make the network request. Wait for the query to complete.

#### Step 5: Copy Result

After the query completes, the result area will display firmware version info and the download link. Click **"Copy to Clipboard"** to copy it. If update log is available, click the **"Update Log"** button to view it.

---

### Build from Source (PyInstaller)

If you want to package it as a single-file exe yourself, follow these steps:

#### Prerequisites

```bash
pip install PyQt5 PyQt-Fluent-Widgets pywinstyles PyInstaller
```

#### Step 1: Run PyInstaller

Execute in the project root directory:

```bash
pyinstaller VivoOtaTracker.onefile.spec --noconfirm
```

#### Step 2: Get the exe

After packaging completes, the executable is located at:

```
dist/VivoOtaTracker.exe
```

#### Step 3: Clean Up (Optional)

```bash
rm -rf build/ __pycache__/ src/__pycache__/
```

---

### FAQ and Troubleshooting

#### Error: `java not found` / `java.exe not found`

* **Cause**: Java is not installed on the system, and the project's embedded JRE path is incorrect.
* **Solution**:
  1. Check whether `jre/bin/java.exe` exists.
  2. Or install JRE 8+ yourself and add it to the system `PATH`.

#### Error: Server returns `{"message":"No update","retcode":210}`

* **Cause**: Firmware info cannot be obtained, usually because:
  1. The `System Software Version` you entered is not in the official open upgrade roadmap.
  2. The push quota for this model/version is full, or the official has temporarily taken down the package.
  3. Requests are too frequent and temporarily restricted.
* **Solution**: Modify the parameters to try other models/versions; or check forums to confirm the exact system version number that can currently receive updates for this model.

#### Error: Program launches but hangs / becomes unresponsive

* **Cause**: unidbg emulator initialization is slow, or the firewall is blocking network requests.
* **Solution**:
  1. Wait over 30 seconds on first launch.
  2. Check whether the firewall allows the program to access the network.
  3. Switch to "Verbose" log mode to see specific errors.

---

### Version History

| Version | Date | Description |
|---------|------|-------------|
| V1.3.0 | 2026-07-24 | Liquid Glass GUI rewrite, SNP/IS_FULL support, update log, about page |
| V1.2.0 | 2026-06-06 | PyQt5 GUI, auto device selection, bilingual UI |
| V1.0.0 | 2026-06-06 | Initial public release |

---

### Acknowledgments

* Original project author: [JerryTse-OSS / VIVO-OTA-Tracker](https://github.com/JerryTse-OSS/VIVO-OTA-Tracker)
* GUI developer: [mytiantian](https://github.com/mytiantian)
* Device model database source: [MobileModels](https://github.com/SecWiki/MobileModels)
* unidbg framework: [zhkl0228/unidbg](https://github.com/zhkl0228/unidbg)
* UI framework: [PyQt-Fluent-Widgets](https://github.com/zhiyiYo/PyQt-Fluent-Widgets)

---

### Disclaimer

**This project is for technical learning and communication purposes only. Do not use it for any illegal or commercial purposes. The user bears all consequences for any problems caused by improper use.**
