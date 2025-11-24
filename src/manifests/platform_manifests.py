import ctypes
import os
import sys
import tempfile

def set_platform_manifest(base_path):
    """Platform-specific manifest setup"""
    if sys.platform == "win32":
        set_windows_manifest(base_path)
    elif sys.platform == "linux":
        set_linux_manifest(base_path)
    elif sys.platform == "darwin":
        set_apple_manifest(base_path)

def set_windows_manifest(base_path):
    """Windows manifest setup"""
    manifest_path = os.path.join(base_path, 'app.manifest')
    
    if os.path.exists(manifest_path):
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("Yarn.Text.Editor.1.0.0.0")

def set_linux_manifest(base_path):
    """Linux manifest setup - .desktop file"""
    if os.getenv('DESKTOP_SESSION'):
        desktop_content = f"""[Desktop Entry]
Name=Yarn Text Editor
Comment=A modern text editor for developers
Exec={sys.executable} {' '.join(sys.argv)}
Icon={os.path.join(base_path, 'yarn.png')}
Terminal=false
Type=Application
Categories=Development;TextEditor;
Keywords=text;editor;code;development;
StartupWMClass=Yarn
MimeType=text/plain;text/x-python;
"""
        
        desktop_path = os.path.join(tempfile.gettempdir(), 'yarn.desktop')
        with open(desktop_path, 'w') as f:
            f.write(desktop_content)
        
        set_linux_dpi()

def set_apple_manifest(base_path):
    """macOS/iOS manifest setup"""
    if is_ios():
        set_ios_manifest(base_path)
    else:
        set_macos_manifest(base_path)

def is_ios():
    """iOS or macOS"""
    try:
        if 'ios' in sys.platform or 'iphone' in sys.platform.lower():
            return True
        
        if sys.platform == 'darwin':
            if os.getenv('CFBundleIdentifier') or os.getenv('IOS_BUNDLE_ID'):
                return True
            if '/Applications/' in os.path.abspath(__file__) or '/var/mobile/' in os.path.abspath(__file__):
                return True
                
        return False
    except:
        return False

def set_ios_manifest(base_path):
    """iOS specific manifest"""
    info_plist_content = '''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleDisplayName</key>
    <string>Yarn</string>
    <!-- ... остальной XML ... -->
</dict>
</plist>'''
    
    plist_path = os.path.join(tempfile.gettempdir(), 'Yarn-Info.plist')
    with open(plist_path, 'w', encoding='utf-8') as f:
        f.write(info_plist_content)

def set_macos_manifest(base_path):
    """macOS specific manifest"""
    mac_plist_content = '''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleName</key>
    <string>Yarn</string>
    <!-- ... остальной XML ... -->
</dict>
</plist>'''
    
    plist_path = os.path.join(tempfile.gettempdir(), 'Yarn-Info.plist')
    with open(plist_path, 'w', encoding='utf-8') as f:
        f.write(mac_plist_content)

def set_linux_dpi():
    """automatic DPI for Linux"""
    scale_factor = 1.0
    
    if os.path.exists('/usr/bin/gsettings'):
        import subprocess
        try:
            result = subprocess.run(
                ['gsettings', 'get', 'org.gnome.desktop.interface', 'scaling-factor'],
                capture_output=True, text=True
            )
            if result.returncode == 0 and result.stdout.strip() not in ['0', 'uint32 0']:
                scale_factor = float(result.stdout.strip().split()[-1])
        except:
            pass
    
    if scale_factor > 1.0:
        os.environ['GDK_SCALE'] = str(scale_factor)
        os.environ['QT_SCALE_FACTOR'] = str(scale_factor)