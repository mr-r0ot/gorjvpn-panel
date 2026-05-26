# client.py
import sys
import hashlib
import uuid
import platform
import json
import base64
from datetime import datetime
from tkinter import messagebox
import psutil
import requests
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

# ========== تنظیمات اولیه ==========
# کلید رمزگذاری (بعداً می‌توانید آن را به یک مقدار قوی تغییر دهید)
ENCRYPTION_KEY = b'\x9f!\x8c\x7e\xd4\x1a\xb3\xc5\xe6\xf0\x2a\x3d\x5e\x7a\x8b\x9c\x0d\x1e\x2f\x3a\x4b\x5c\x6d\x7e\x8f\x9a\xab\xbc\xcd\xde\xef\xf0'
GITHUB_RAW_URL = "https://raw.githubusercontent.com/mr-r0ot/Chess-player-Cloner-AI/refs/heads/main/acc.txt"

VERSION = 2  # نسخه فعلی برنامه شما (در بروزرسانی‌ها زیاد می‌شود)

# ========== توابع کمکی ==========
def alertmsg(ms):
    messagebox.showerror("خطا", ms)
    sys.exit(1)

def decrypt_data(encrypted_b64: str, key: bytes):
    """رمزگشایی داده‌های AES (حالت CBC)"""
    try:
        raw = base64.b64decode(encrypted_b64)
        iv = raw[:16]
        ciphertext = raw[16:]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        decrypted = unpad(cipher.decrypt(ciphertext), AES.block_size)
        return decrypted.decode('utf-8')
    except Exception as e:
        alertmsg(f"خطا در رمزگشایی داده‌ها: {e}")

def simple_fingerprint():
    mac = uuid.getnode()
    cpu = platform.processor()
    ram = str(psutil.virtual_memory().total)
    host = platform.node()
    data = f"{mac}-{cpu}-{ram}-{host}"
    return hashlib.md5(data.encode()).hexdigest()

# ========== دریافت و بررسی داده از GitHub ==========
try:
    response = requests.get(GITHUB_RAW_URL, timeout=10)
    if response.status_code != 200:
        alertmsg(f"خطا در دریافت اطلاعات از سرور. کد خطا: {response.status_code}")
except Exception as e:
    alertmsg(f"دسترسی به اینترنت موجود نیست یا سرور در دسترس نیست. لطفاً اتصال خود را بررسی کنید. {e}")

encrypted_content = response.text.strip()
if not encrypted_content:
    alertmsg("فایل اطلاعاتی خالی است. لطفاً به پشتیبانی اطلاع دهید.")

# رمزگشایی
json_data = decrypt_data(encrypted_content, ENCRYPTION_KEY)
try:
    data = json.loads(json_data)
except:
    alertmsg("داده‌های دریافتی خراب است. لطفاً به پشتیبانی اطلاع دهید.")

# بررسی نسخه برنامه
server_version = data.get("version", 0)
if server_version > VERSION:
    alertmsg("نسخه جدیدی از برنامه منتشر شده است. لطفاً برای نصب بروزرسانی با پشتیبانی تماس بگیرید.")

# دریافت لیست اکانت‌ها
accounts = data.get("accounts", [])
if not accounts:
    alertmsg("هیچ اکانتی در سیستم تعریف نشده است.")

device_fingerprint = simple_fingerprint()
found_account = None

# جستجوی دستگاه در بین اکانت‌ها
for acc in accounts:
    devices = acc.get("devices", [])
    if device_fingerprint in devices:
        found_account = acc
        break

if not found_account:
    alertmsg("شما مجاز به استفاده از این برنامه نیستید. این دستگاه در لیست مجاز ثبت نشده است. لطفاً با پشتیبانی تماس بگیرید.")

# بررسی تاریخ انقضا
expiry_str = found_account.get("expiry")
if not expiry_str:
    alertmsg("تاریخ انقضا برای اکانت شما تعریف نشده است.")

try:
    expiry_date = datetime.strptime(expiry_str, "%d/%m/%Y")
except:
    alertmsg("فرمت تاریخ انقضا نامعتبر است. لطفاً با ادمین تماس بگیرید.")

if datetime.now() > expiry_date:
    alertmsg("حساب کاربری شما منقضی شده است. برای تمدید با پشتیبانی تماس بگیرید.")

# استخراج متغیرهای مورد نیاز برای ادامه برنامه
script_id = found_account.get("script_id")
auth_key = found_account.get("auth_key")
data_expiry = found_account.get("expiry")   # تاریخ انقضا (همان data)


if not script_id or not auth_key:
    alertmsg("اطلاعات اکانت ناقص است. با پشتیبانی تماس بگیرید.")


messagebox.showerror("توجه", "در صورت نیاز به خرید. افزدون کاربر دیگر. تمدید اشتراک. و هرگونه مشکل به آیدی تلگرام سازنده پیام دهید:@ImSadUser")



# ======================= HARDCODED CONFIGURATION =======================
fcon = {
    "mode": "apps_script",
    "google_ip": "216.239.38.120",
    "front_domain": "www.google.com",
    "script_id": script_id,
    "auth_key": auth_key,
    "listen_host": "127.0.0.1",
    "socks5_enabled": True,
    "listen_port": 8085,
    "socks5_port": 1391,
    "log_level": "INFO",
    "verify_ssl": True,
    "lan_sharing": True,
    "relay_timeout": 25,
    "tls_connect_timeout": 15,
    "tcp_connect_timeout": 10,
    "max_response_body_bytes": 209715200,
    "parallel_relay": 1,
    "chunked_download_extensions": [
        ".bin", ".zip", ".tar", ".gz", ".bz2", ".xz", ".7z", ".rar", ".exe",
        ".msi", ".dmg", ".deb", ".rpm", ".apk", ".iso", ".img", ".mp4", ".mkv",
        ".avi", ".mov", ".webm", ".mp3", ".flac", ".wav", ".aac", ".pdf", ".doc",
        ".docx", ".ppt", ".pptx", ".wasm"
    ],
    "chunked_download_min_size": 5242880,
    "chunked_download_chunk_size": 524288,
    "chunked_download_max_parallel": 8,
    "chunked_download_max_chunks": 256,
    "block_hosts": [],
    "bypass_hosts": ["localhost", ".local", ".lan", ".home.arpa"],
    "direct_google_exclude": [
        "gemini.google.com", "aistudio.google.com", "notebooklm.google.com",
        "labs.google.com", "meet.google.com", "accounts.google.com",
        "ogs.google.com", "mail.google.com", "calendar.google.com",
        "drive.google.com", "docs.google.com", "chat.google.com",
        "maps.google.com", "play.google.com", "translate.google.com",
        "assistant.google.com", "lens.google.com"
    ],
    "direct_google_allow": ["www.google.com", "safebrowsing.google.com"],
    "youtube_via_relay": False,
    "hosts": {}
}
# =========================================================================

import argparse
import asyncio
import json
import logging
import os
import sys

# Project modules live under ./src — put that folder on sys.path so the
# historical flat imports ("from proxy_server import …") keep working.
_SRC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "src")
if _SRC_DIR not in sys.path:
    sys.path.insert(0, _SRC_DIR)

from cert_installer import install_ca, uninstall_ca, is_ca_trusted
from constants import __version__
from lan_utils import log_lan_access
from google_ip_scanner import scan_sync
from logging_utils import configure as configure_logging, print_banner
from mitm import CA_CERT_FILE
from proxy_server import ProxyServer


def setup_logging(level_name: str):
    configure_logging(level_name)


_PLACEHOLDER_AUTH_KEYS = {
    "",
    "CHANGE_ME_TO_A_STRONG_SECRET",
    "your-secret-password-here",
}


def parse_args():
    parser = argparse.ArgumentParser(
        prog="domainfront-tunnel",
        description="Local HTTP proxy that relays traffic through Google Apps Script.",
    )
    # NOTE: --config argument removed because config is hardcoded.
    parser.add_argument(
        "-p", "--port",
        type=int,
        default=None,
        help="Override listen port (env: DFT_PORT)",
    )
    parser.add_argument(
        "--host",
        default=None,
        help="Override listen host (env: DFT_HOST)",
    )
    parser.add_argument(
        "--socks5-port",
        type=int,
        default=None,
        help="Override SOCKS5 listen port (env: DFT_SOCKS5_PORT)",
    )
    parser.add_argument(
        "--disable-socks5",
        action="store_true",
        help="Disable the built-in SOCKS5 listener.",
    )
    parser.add_argument(
        "--log-level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        default=None,
        help="Override log level (env: DFT_LOG_LEVEL)",
    )
    parser.add_argument(
        "-v", "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )
    parser.add_argument(
        "--install-cert",
        action="store_true",
        help="Install the MITM CA certificate as a trusted root and exit.",
    )
    parser.add_argument(
        "--uninstall-cert",
        action="store_true",
        help="Remove the MITM CA certificate from trusted roots and exit.",
    )
    parser.add_argument(
        "--no-cert-check",
        action="store_true",
        help="Skip the certificate installation check on startup.",
    )
    parser.add_argument(
        "--scan",
        action="store_true",
        help="Scan Google IPs to find the fastest reachable one and exit.",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    # Handle cert-only commands before loading config so they can run standalone.
    if args.install_cert or args.uninstall_cert:
        setup_logging("INFO")
        _log = logging.getLogger("Main")

        if args.install_cert:
            _log.info("Installing CA certificate…")
            if not os.path.exists(CA_CERT_FILE):
                from mitm import MITMCertManager
                MITMCertManager()  # side-effect: creates ca/ca.crt + ca/ca.key
            ok = install_ca(CA_CERT_FILE)
            sys.exit(0 if ok else 1)

        _log.info("Removing CA certificate…")
        ok = uninstall_ca(CA_CERT_FILE)
        if ok:
            _log.info("CA certificate removed successfully.")
        else:
            _log.warning("CA certificate removal may have failed. Check logs above.")
        sys.exit(0 if ok else 1)

    # ---------- USE HARDCODED CONFIGURATION ----------
    config = fcon.copy()

    # Environment variable overrides
    if os.environ.get("DFT_AUTH_KEY"):
        config["auth_key"] = os.environ["DFT_AUTH_KEY"]
    if os.environ.get("DFT_SCRIPT_ID"):
        config["script_id"] = os.environ["DFT_SCRIPT_ID"]

    # CLI argument overrides
    if args.port is not None:
        config["listen_port"] = args.port
    elif os.environ.get("DFT_PORT"):
        config["listen_port"] = int(os.environ["DFT_PORT"])

    if args.host is not None:
        config["listen_host"] = args.host
    elif os.environ.get("DFT_HOST"):
        config["listen_host"] = os.environ["DFT_HOST"]

    if args.socks5_port is not None:
        config["socks5_port"] = args.socks5_port
    elif os.environ.get("DFT_SOCKS5_PORT"):
        config["socks5_port"] = int(os.environ["DFT_SOCKS5_PORT"])

    if args.disable_socks5:
        config["socks5_enabled"] = False

    if args.log_level is not None:
        config["log_level"] = args.log_level
    elif os.environ.get("DFT_LOG_LEVEL"):
        config["log_level"] = os.environ["DFT_LOG_LEVEL"]

    # Required keys validation
    for key in ("auth_key",):
        if key not in config:
            print(f"Missing required config key: {key}")
            sys.exit(1)

    if config.get("auth_key", "") in _PLACEHOLDER_AUTH_KEYS:
        print(
            "Refusing to start: 'auth_key' is unset or uses a known placeholder.\n"
            "Pick a long random secret and set it in both config.json AND "
            "the AUTH_KEY constant inside Code.gs (they must match)."
        )
        sys.exit(1)

    # Always Apps Script mode — force-set for backward-compat configs.
    config["mode"] = "apps_script"
    sid = config.get("script_ids") or config.get("script_id")
    if not sid or (isinstance(sid, str) and sid == "YOUR_APPS_SCRIPT_DEPLOYMENT_ID"):
        print("Missing 'script_id' in config.")
        print("Deploy the Apps Script from Code.gs and paste the Deployment ID.")
        sys.exit(1)

    # ── Google IP Scanner ──────────────────────────────────────────────────
    if args.scan:
        setup_logging("INFO")
        front_domain = config.get("front_domain", "www.google.com")
        _log = logging.getLogger("Main")
        _log.info(f"Scanning Google IPs (fronting domain: {front_domain})")
        ok = scan_sync(front_domain)
        sys.exit(0 if ok else 1)

    setup_logging(config.get("log_level", "INFO"))
    log = logging.getLogger("Main")

    print_banner(__version__)
    log.info("DomainFront Tunnel starting (Apps Script relay)")

    log.info("Apps Script relay : SNI=%s → script.google.com",
             config.get("front_domain", "www.google.com"))
    script_ids = config.get("script_ids") or config.get("script_id")
    if isinstance(script_ids, list):
        log.info("Script IDs        : %d scripts (sticky per-host)", len(script_ids))
        for i, sid in enumerate(script_ids):
            log.info("  [%d] %s", i + 1, sid)
    else:
        log.info("Script ID         : %s", script_ids)

    # Ensure CA file exists before checking / installing it.
    # MITMCertManager generates ca/ca.crt on first instantiation.
    if not os.path.exists(CA_CERT_FILE):
        from mitm import MITMCertManager
        MITMCertManager()  # side-effect: creates ca/ca.crt + ca/ca.key

    # Auto-install MITM CA if not already trusted
    if not args.no_cert_check:
        if not is_ca_trusted(CA_CERT_FILE):
            log.warning("MITM CA is not trusted — attempting automatic installation…")
            ok = install_ca(CA_CERT_FILE)
            if ok:
                log.info("CA certificate installed. You may need to restart your browser.")
            else:
                log.error(
                    "Auto-install failed. Run with --install-cert (may need admin/sudo) "
                    "or manually install ca/ca.crt as a trusted root CA."
                )
        else:
            log.info("MITM CA is already trusted.")

    # ── LAN sharing configuration ────────────────────────────────────────
    lan_sharing = config.get("lan_sharing", False)
    listen_host = config.get("listen_host", "127.0.0.1")
    if lan_sharing:
        # If LAN sharing is enabled and host is still localhost, change to all interfaces
        if listen_host == "127.0.0.1":
            config["listen_host"] = "0.0.0.0"
            listen_host = "0.0.0.0"
            log.info("LAN sharing enabled — listening on all interfaces")

    # If either explicit LAN sharing is enabled or we bind to all interfaces,
    # print concrete IPv4 addresses users can use on other devices.
    lan_mode = lan_sharing or listen_host in ("0.0.0.0", "::")
    if lan_mode:
        socks_port = config.get("socks5_port", 1080) if config.get("socks5_enabled", True) else None
        log_lan_access(config.get("listen_port", 8080), socks_port)

    try:
        asyncio.run(_run(config))
    except KeyboardInterrupt:
        log.info("Stopped")


def _make_exception_handler(log):
    """Return an asyncio exception handler that silences Windows WinError 10054
    noise from connection cleanup (ConnectionResetError in
    _ProactorBasePipeTransport._call_connection_lost), which is harmless but
    verbose on Python/Windows when a remote host force-closes a socket."""
    def handler(loop, context):
        exc = context.get("exception")
        cb  = context.get("handle") or context.get("source_traceback", "")
        if (
            isinstance(exc, ConnectionResetError)
            and "_call_connection_lost" in str(cb)
        ):
            return  # suppress: benign Windows socket cleanup race
        log.error("[asyncio]  %s", context.get("message", context))
        if exc:
            loop.default_exception_handler(context)
    return handler


async def _run(config):
    loop = asyncio.get_running_loop()
    _log = logging.getLogger("asyncio")
    loop.set_exception_handler(_make_exception_handler(_log))
    server = ProxyServer(config)
    try:
        await server.start()
    finally:
        await server.stop()


# ======================== GORJ VPN GUI ========================
# اگر آرگومان "--proxy" وجود داشته باشد، فقط main را اجرا کن (برای زیرپروسس)
if "--proxy" in sys.argv:
    sys.argv.remove("--proxy")
    main()
    sys.exit(0)

# در غیر این صورت GUI را نمایش بده
import subprocess
import socket
import customtkinter as ctk

class GorjVPN(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Gorj VPN")
        self.geometry("500x550")
        self.resizable(False, False)
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.proxy_process = None
        self.is_connected = False

        self.create_widgets()
        self.check_connection_periodically()

    def create_widgets(self):
        main_frame = ctk.CTkFrame(self, corner_radius=20)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        title = ctk.CTkLabel(main_frame, text="Gorj VPN", font=ctk.CTkFont(size=32, weight="bold"))
        title.pack(pady=(20, 10))

        self.toggle_switch = ctk.CTkSwitch(main_frame, text="", command=self.toggle_proxy,
                                           width=100, height=40, switch_width=80, switch_height=30)
        self.toggle_switch.pack(pady=20)

        self.status_label = ctk.CTkLabel(main_frame, text="Disconnected", font=ctk.CTkFont(size=16),
                                         text_color="red")
        self.status_label.pack(pady=5)

        ctk.CTkFrame(main_frame, height=2, fg_color="gray").pack(fill="x", pady=20)

        ctk.CTkLabel(main_frame, text="V2Ray Configuration", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=(10, 5))

        self.config_text = ctk.CTkTextbox(main_frame, height=60, font=ctk.CTkFont(size=12))
        self.config_text.pack(fill="x", padx=10, pady=5)
        self.config_text.insert("1.0", "socks://Og==@127.0.0.1:1391#Gorj%20VPN%20%3A%29")
        self.config_text.configure(state="disabled")

        copy_btn = ctk.CTkButton(main_frame, text="Copy Config", command=self.copy_config, width=150, height=35)
        copy_btn.pack(pady=5)

        ctk.CTkLabel(main_frame, text="Use this config in V2Ray client", font=ctk.CTkFont(size=12), text_color="gray").pack(pady=2)

        warning_frame = ctk.CTkFrame(main_frame, fg_color="#2b2b2b", corner_radius=10)
        warning_frame.pack(fill="x", pady=20, padx=10)
        ctk.CTkLabel(warning_frame,
                     text="⚠️ Note: If you see repeated 503 errors and your internet is working,\nyour daily quota may have been exhausted.",
                     font=ctk.CTkFont(size=11), text_color="#ffaa00", justify="left").pack(padx=10, pady=10)

    def toggle_proxy(self):
        if self.is_connected:
            self.stop_proxy()
        else:
            self.start_proxy()

    def start_proxy(self):
        if self.is_connected:
            return
        self.status_label.configure(text="Connecting...", text_color="orange")
        self.update_idletasks()

        try:
            # اجرای همین فایل با آرگومان --proxy (که main را صدا می‌زند)
            self.proxy_process = subprocess.Popen(
                [sys.executable, __file__, "--proxy"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0
            )
            self.after(2000, self.check_connection)
        except Exception as e:
            self.status_label.configure(text=f"Error: {str(e)[:30]}", text_color="red")
            self.toggle_switch.deselect()
            self.is_connected = False

    def check_connection(self):
        self.is_connected = True
        self.status_label.configure(text="Connected", text_color="green")
        self.toggle_switch.select()

    def stop_proxy(self):
        if self.proxy_process:
            self.proxy_process.terminate()
            try:
                self.proxy_process.wait(timeout=3)
            except subprocess.TimeoutExpired:
                self.proxy_process.kill()
            self.proxy_process = None
        self.is_connected = False
        self.status_label.configure(text="Disconnected", text_color="red")
        self.toggle_switch.deselect()

    def copy_config(self):
        self.clipboard_clear()
        self.clipboard_append("socks://Og==@127.0.0.1:1391#Gorj%20VPN%20%3A%29")
        self.update()
        # تغییر موقت متن دکمه کپی (جستجوی ساده)
        for widget in self.winfo_children():
            for sub in widget.winfo_children():
                if isinstance(sub, ctk.CTkButton) and sub.cget("text") == "Copy Config":
                    original = sub.cget("text")
                    sub.configure(text="Copied!")
                    self.after(1500, lambda s=sub, orig=original: s.configure(text=orig))
                    break

    def check_connection_periodically(self):
        pass


if __name__ == "__main__":
    # اگر آرگومان --proxy وجود دارد، main را اجرا کن (حالت پروکسی)
    if "--proxy" in sys.argv:
        sys.argv.remove("--proxy")
        main()
    else:
        app = GorjVPN()
        app.mainloop()