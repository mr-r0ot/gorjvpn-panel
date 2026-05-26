import hashlib
import uuid
import platform
import psutil
import tkinter as tk
from tkinter import messagebox

# ============================
# تابع تولید اثر انگشت دستگاه
# ============================
def simple_fingerprint():
    mac = uuid.getnode()
    cpu = platform.processor()
    ram = str(psutil.virtual_memory().total)
    host = platform.node()
    data = f"{mac}-{cpu}-{ram}-{host}"
    return hashlib.md5(data.encode()).hexdigest()

# ============================
# پنجره tkinter
# ============================
def show_ctk_gui():
    device_id = simple_fingerprint()
    
    root = tk.Tk()
    root.title("GorjVPN - فعال‌سازی دستگاه")
    root.geometry("600x320")
    root.resizable(False, False)
    root.configure(bg="#1e1e2f")  # پس‌زمینه تیره و شیک
    
    # فریم اصلی
    main_frame = tk.Frame(root, bg="#1e1e2f")
    main_frame.pack(expand=True, fill="both", padx=20, pady=20)
    
    # عنوان
    title_label = tk.Label(
        main_frame,
        text="🔐 شناسه فعال‌سازی دستگاه (Gorj VPN)",
        font=("Segoe UI", 18, "bold"),
        fg="#ffffff",
        bg="#1e1e2f"
    )
    title_label.pack(pady=(0, 10))
    
    # زیرنویس
    sub_label = tk.Label(
        main_frame,
        text="این شناسه منحصربه‌فرد و غیرقابل تغییر است(Telegram:@ImSadUser)",
        font=("Segoe UI", 10),
        fg="#aaaaaa",
        bg="#1e1e2f"
    )
    sub_label.pack(pady=(0, 20))
    
    # کادر نمایش CTK (Entry فقط خواندنی)
    ctk_var = tk.StringVar(value=device_id)
    ctk_entry = tk.Entry(
        main_frame,
        textvariable=ctk_var,
        font=("Consolas", 12),
        bg="#2d2d3f",
        fg="#00ffcc",
        relief="solid",
        bd=2,
        justify="center",
        state="readonly",
        readonlybackground="#2d2d3f"
    )
    ctk_entry.pack(fill="x", pady=(0, 10), ipady=8)
    
    # دکمه کپی در کلیپ‌بورد
    def copy_to_clip():
        root.clipboard_clear()
        root.clipboard_append(device_id)
        root.update()  # لازم برای نگهداری در کلیپ‌بورد
        messagebox.showinfo("کپی شد", "شناسه CTK در کلیپ‌بورد کپی شد.")
    
    copy_btn = tk.Button(
        main_frame,
        text="📋 کپی شناسه",
        command=copy_to_clip,
        font=("Segoe UI", 10),
        bg="#3a3a55",
        fg="white",
        activebackground="#4f4f6f",
        activeforeground="white",
        cursor="hand2",
        relief="flat",
        padx=10,
        pady=5
    )
    copy_btn.pack(pady=(0, 20))
    
    # پیام راهنما
    msg_frame = tk.Frame(main_frame, bg="#2a2a3c", relief="groove", bd=1)
    msg_frame.pack(fill="both", padx=10, pady=10)
    
    msg_label = tk.Label(
        msg_frame,
        text="📌 برای فعال‌سازی GorjVPN، این شناسه را به ادمین ارسال کنید.\n"
             "⚠️ توجه: هر دستگاه دارای شناسه یکتا بوده و قابل جعل نیست.",
        font=("Segoe UI", 10),
        fg="#dddddd",
        bg="#2a2a3c",
        justify="center"
    )
    msg_label.pack(padx=15, pady=15)
    
    # اجرای پنجره
    root.mainloop()

if __name__ == "__main__":
    show_ctk_gui()