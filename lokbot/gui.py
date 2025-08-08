#!/usr/bin/env python3
"""
LokBot GUI Application
Giao diện đồ họa để quản lý config và chạy multiple tokens
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import threading
import subprocess
import sys
import os
from pathlib import Path
import time
from datetime import datetime
import re

class LokBotGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("LokBot Manager - League of Kingdoms Bot")
        self.root.geometry("900x700")
        self.root.resizable(True, True)
        
        # Biến lưu trữ
        self.profiles = {}  # {profile_name: {token: str, config: dict, status: str}}
        self.running_processes = {}  # {profile_name: process}
        self.config_file = "profiles.json"
        self.bot_statistics = {}  # {profile_name: statistics}
        
        # Tạo GUI trước
        self.create_widgets()
        
        # Load profiles từ file sau khi GUI đã sẵn sàng
        self.load_profiles()
        
        # Timer để cập nhật status
        self.update_status_timer()
    
    def create_widgets(self):
        """Tạo giao diện chính"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="🤖 LokBot Manager", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Notebook (tabs)
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Tab 1: Token Management
        self.create_token_tab()
        
        # Tab 2: Config Editor
        self.create_config_tab()
        
        # Tab 3: Status
        self.create_status_tab()
        
        # Tab 4: Logs
        self.create_logs_tab()
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, 
                              relief=tk.SUNKEN, anchor=tk.W)
        status_bar.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
    
    def create_token_tab(self):
        """Tạo tab quản lý tokens"""
        token_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(token_frame, text="Token Management")
        
        # Left panel - Profile list
        left_frame = ttk.Frame(token_frame)
        left_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        
        ttk.Label(left_frame, text="Profiles:", font=("Arial", 12, "bold")).grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        
        # Profile listbox
        self.profile_listbox = tk.Listbox(left_frame, height=15, width=25)
        self.profile_listbox.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.profile_listbox.bind('<<ListboxSelect>>', self.on_profile_select)
        
        # Profile buttons
        profile_btn_frame = ttk.Frame(left_frame)
        profile_btn_frame.grid(row=2, column=0, pady=(10, 0), sticky=tk.W)
        
        ttk.Button(profile_btn_frame, text="New", command=self.new_profile).grid(row=0, column=0, padx=(0, 5))
        ttk.Button(profile_btn_frame, text="Delete", command=self.delete_profile).grid(row=0, column=1, padx=(0, 5))
        ttk.Button(profile_btn_frame, text="Clone", command=self.clone_profile).grid(row=0, column=2)
        
        # Right panel - Profile details
        right_frame = ttk.Frame(token_frame)
        right_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Profile name
        ttk.Label(right_frame, text="Profile Name:").grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        self.profile_name_var = tk.StringVar()
        profile_name_entry = ttk.Entry(right_frame, textvariable=self.profile_name_var, width=30)
        profile_name_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=(0, 5))
        
        # Token
        ttk.Label(right_frame, text="X-Access-Token:").grid(row=1, column=0, sticky=tk.W, pady=(0, 5))
        self.token_var = tk.StringVar()
        token_entry = ttk.Entry(right_frame, textvariable=self.token_var, width=50, show="*")
        token_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=(0, 5))
        
        # Show/Hide token
        self.show_token_var = tk.BooleanVar()
        show_token_cb = ttk.Checkbutton(right_frame, text="Show Token", 
                                       variable=self.show_token_var,
                                       command=lambda: token_entry.config(show="" if self.show_token_var.get() else "*"))
        show_token_cb.grid(row=2, column=1, sticky=tk.W, pady=(0, 10))
        
        # Status
        ttk.Label(right_frame, text="Status:").grid(row=3, column=0, sticky=tk.W, pady=(0, 5))
        self.profile_status_var = tk.StringVar()
        self.profile_status_label = ttk.Label(right_frame, textvariable=self.profile_status_var, 
                                            foreground="gray")
        self.profile_status_label.grid(row=3, column=1, sticky=tk.W, pady=(0, 5))
        
        # Control buttons
        control_frame = ttk.Frame(right_frame)
        control_frame.grid(row=4, column=0, columnspan=2, pady=(20, 0), sticky=tk.W)
        
        self.start_btn = ttk.Button(control_frame, text="▶ Start Bot", command=self.start_bot)
        self.start_btn.grid(row=0, column=0, padx=(0, 10))
        
        self.stop_btn = ttk.Button(control_frame, text="⏹ Stop Bot", command=self.stop_bot, state=tk.DISABLED)
        self.stop_btn.grid(row=0, column=1, padx=(0, 10))
        
        ttk.Button(control_frame, text="💾 Save Profile", command=self.save_profile).grid(row=0, column=2)
        
        # Configure grid weights
        token_frame.columnconfigure(1, weight=1)
        token_frame.rowconfigure(0, weight=1)
        left_frame.rowconfigure(1, weight=1)
        right_frame.columnconfigure(1, weight=1)
        
        # Load profiles into listbox
        self.refresh_profile_list()
    
    def create_config_tab(self):
        """Tạo tab chỉnh sửa config"""
        config_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(config_frame, text="Config Editor")
        
        # Config selection
        config_select_frame = ttk.Frame(config_frame)
        config_select_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(config_select_frame, text="Config for Profile:").grid(row=0, column=0, padx=(0, 10))
        self.config_profile_var = tk.StringVar()
        self.config_profile_combo = ttk.Combobox(config_select_frame, textvariable=self.config_profile_var,
                                                state="readonly", width=20)
        self.config_profile_combo.grid(row=0, column=1, padx=(0, 10))
        self.config_profile_combo.bind('<<ComboboxSelected>>', self.load_config_for_profile)
        
        ttk.Button(config_select_frame, text="Load Default", command=self.load_default_config).grid(row=0, column=2, padx=(0, 5))
        ttk.Button(config_select_frame, text="Load Example", command=self.load_example_config).grid(row=0, column=3, padx=(0, 5))
        ttk.Button(config_select_frame, text="Save Config", command=self.save_config).grid(row=0, column=4)
        
        # Config editor (JSON)
        ttk.Label(config_frame, text="Configuration (JSON):").grid(row=1, column=0, sticky=tk.W, pady=(0, 5))
        
        # Text editor with scrollbar
        text_frame = ttk.Frame(config_frame)
        text_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.config_text = tk.Text(text_frame, wrap=tk.NONE, font=("Consolas", 10))
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=self.config_text.yview)
        h_scrollbar = ttk.Scrollbar(text_frame, orient=tk.HORIZONTAL, command=self.config_text.xview)
        self.config_text.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Grid scrollbars and text
        self.config_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        v_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        h_scrollbar.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        # Configure grid weights
        config_frame.columnconfigure(0, weight=1)
        config_frame.rowconfigure(2, weight=1)
        text_frame.columnconfigure(0, weight=1)
        text_frame.rowconfigure(0, weight=1)
        
        # Load default config
        self.load_default_config()
    
    def create_status_tab(self):
        """Tạo tab trạng thái chi tiết"""
        status_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(status_frame, text="📊 Status")
        
        # Profile selector cho status
        profile_frame = ttk.LabelFrame(status_frame, text="Select Profile", padding="5")
        profile_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.status_profile_var = tk.StringVar()
        self.status_profile_combo = ttk.Combobox(profile_frame, textvariable=self.status_profile_var, 
                                               width=30, state="readonly")
        self.status_profile_combo.grid(row=0, column=0, padx=(0, 10))
        self.status_profile_combo.bind('<<ComboboxSelected>>', self.on_status_profile_change)
        
        refresh_btn = ttk.Button(profile_frame, text="🔄 Refresh", command=self.refresh_status)
        refresh_btn.grid(row=0, column=1)
        
        # Main status frame
        main_status_frame = ttk.Frame(status_frame)
        main_status_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        main_status_frame.columnconfigure(0, weight=1)
        main_status_frame.columnconfigure(1, weight=1)
        
        # Left column - Statistics
        stats_frame = ttk.LabelFrame(main_status_frame, text="📈 Statistics", padding="10")
        stats_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 5))
        
        # Statistics labels
        self.mines_label = ttk.Label(stats_frame, text="Mines Gathered: 0", font=("Arial", 12, "bold"))
        self.mines_label.grid(row=0, column=0, sticky=tk.W, pady=2)
        
        self.monsters_label = ttk.Label(stats_frame, text="Monsters Killed: 0", font=("Arial", 12, "bold"))
        self.monsters_label.grid(row=1, column=0, sticky=tk.W, pady=2)
        
        self.uptime_label = ttk.Label(stats_frame, text="Uptime: 0h 0m", font=("Arial", 10))
        self.uptime_label.grid(row=2, column=0, sticky=tk.W, pady=2)
        
        self.mines_per_hour_label = ttk.Label(stats_frame, text="Mines/Hour: 0.0", font=("Arial", 10))
        self.mines_per_hour_label.grid(row=3, column=0, sticky=tk.W, pady=2)
        
        self.monsters_per_hour_label = ttk.Label(stats_frame, text="Monsters/Hour: 0.0", font=("Arial", 10))
        self.monsters_per_hour_label.grid(row=4, column=0, sticky=tk.W, pady=2)
        
        # Right column - Bot Info
        info_frame = ttk.LabelFrame(main_status_frame, text="🤖 Bot Info", padding="10")
        info_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(5, 0))
        
        self.bot_level_label = ttk.Label(info_frame, text="Level: Unknown", font=("Arial", 10))
        self.bot_level_label.grid(row=0, column=0, sticky=tk.W, pady=2)
        
        self.alliance_label = ttk.Label(info_frame, text="Alliance: None", font=("Arial", 10))
        self.alliance_label.grid(row=1, column=0, sticky=tk.W, pady=2)
        
        self.march_limit_label = ttk.Label(info_frame, text="March Limit: 0", font=("Arial", 10))
        self.march_limit_label.grid(row=2, column=0, sticky=tk.W, pady=2)
        
        self.active_marches_label = ttk.Label(info_frame, text="Active Marches: 0", font=("Arial", 10))
        self.active_marches_label.grid(row=3, column=0, sticky=tk.W, pady=2)
        
        # Resources frame
        resources_frame = ttk.LabelFrame(status_frame, text="💰 Resources", padding="10")
        resources_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        resources_frame.columnconfigure(0, weight=1)
        resources_frame.columnconfigure(1, weight=1)
        resources_frame.columnconfigure(2, weight=1)
        resources_frame.columnconfigure(3, weight=1)
        
        self.food_label = ttk.Label(resources_frame, text="🍖 Food: 0", font=("Arial", 10))
        self.food_label.grid(row=0, column=0, sticky=tk.W)
        
        self.lumber_label = ttk.Label(resources_frame, text="🪵 Lumber: 0", font=("Arial", 10))
        self.lumber_label.grid(row=0, column=1, sticky=tk.W)
        
        self.stone_label = ttk.Label(resources_frame, text="🪨 Stone: 0", font=("Arial", 10))
        self.stone_label.grid(row=0, column=2, sticky=tk.W)
        
        self.gold_label = ttk.Label(resources_frame, text="🪙 Gold: 0", font=("Arial", 10))
        self.gold_label.grid(row=0, column=3, sticky=tk.W)
        
        # Status info
        status_info_frame = ttk.LabelFrame(status_frame, text="ℹ️ Status Info", padding="10")
        status_info_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.start_time_label = ttk.Label(status_info_frame, text="Start Time: Not running", font=("Arial", 9))
        self.start_time_label.grid(row=0, column=0, sticky=tk.W, pady=2)
        
        self.last_update_label = ttk.Label(status_info_frame, text="Last Update: Never", font=("Arial", 9))
        self.last_update_label.grid(row=1, column=0, sticky=tk.W, pady=2)
        
        # Configure grid weights
        status_frame.columnconfigure(0, weight=1)
        status_frame.rowconfigure(1, weight=1)

    def create_logs_tab(self):
        """Tạo tab logs"""
        logs_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(logs_frame, text="Logs")
        
        # Log controls
        log_control_frame = ttk.Frame(logs_frame)
        log_control_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Button(log_control_frame, text="Clear Logs", command=self.clear_logs).grid(row=0, column=0, padx=(0, 10))
        ttk.Button(log_control_frame, text="Save Logs", command=self.save_logs).grid(row=0, column=1, padx=(0, 10))
        
        self.auto_scroll_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(log_control_frame, text="Auto Scroll", variable=self.auto_scroll_var).grid(row=0, column=2)
        
        # Log text area
        log_text_frame = ttk.Frame(logs_frame)
        log_text_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.log_text = tk.Text(log_text_frame, wrap=tk.WORD, font=("Consolas", 9), state=tk.DISABLED)
        log_scrollbar = ttk.Scrollbar(log_text_frame, orient=tk.VERTICAL, command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=log_scrollbar.set)
        
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        log_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Configure grid weights
        logs_frame.columnconfigure(0, weight=1)
        logs_frame.rowconfigure(1, weight=1)
        log_text_frame.columnconfigure(0, weight=1)
        log_text_frame.rowconfigure(0, weight=1)
        
        # Initial log message
        self.log_message("LokBot GUI started", "INFO")
    
    def load_profiles(self):
        """Load profiles từ file"""
        try:
            if Path(self.config_file).exists():
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    self.profiles = json.load(f)
                if hasattr(self, 'log_text'):
                    self.log_message(f"Loaded {len(self.profiles)} profiles", "INFO")
            else:
                self.profiles = {}
                if hasattr(self, 'log_text'):
                    self.log_message("No profiles file found, starting fresh", "INFO")
        except Exception as e:
            if hasattr(self, 'log_text'):
                self.log_message(f"Error loading profiles: {str(e)}", "ERROR")
            self.profiles = {}
    
    def save_profiles(self):
        """Save profiles ra file"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.profiles, f, indent=2, ensure_ascii=False)
            self.log_message("Profiles saved successfully", "INFO")
        except Exception as e:
            self.log_message(f"Error saving profiles: {str(e)}", "ERROR")
            messagebox.showerror("Error", f"Failed to save profiles: {str(e)}")
    
    def refresh_profile_list(self):
        """Refresh danh sách profiles"""
        self.profile_listbox.delete(0, tk.END)
        for profile_name in sorted(self.profiles.keys()):
            self.profile_listbox.insert(tk.END, profile_name)
        
        # Update config combo if it exists
        if hasattr(self, 'config_profile_combo'):
            profile_names = list(self.profiles.keys())
            self.config_profile_combo['values'] = profile_names
    
    def on_profile_select(self, event):
        """Khi chọn profile"""
        selection = self.profile_listbox.curselection()
        if selection:
            profile_name = self.profile_listbox.get(selection[0])
            profile_data = self.profiles.get(profile_name, {})
            
            self.profile_name_var.set(profile_name)
            self.token_var.set(profile_data.get('token', ''))
            
            status = profile_data.get('status', 'Stopped')
            self.profile_status_var.set(status)
            
            # Update button states
            if status == 'Running':
                self.start_btn.config(state=tk.DISABLED)
                self.stop_btn.config(state=tk.NORMAL)
                self.profile_status_label.config(foreground="green")
            else:
                self.start_btn.config(state=tk.NORMAL)
                self.stop_btn.config(state=tk.DISABLED)
                self.profile_status_label.config(foreground="gray")
    
    def new_profile(self):
        """Tạo profile mới"""
        name = tk.simpledialog.askstring("New Profile", "Enter profile name:")
        if name and name not in self.profiles:
            self.profiles[name] = {
                'token': '',
                'config': self.get_default_config(),
                'status': 'Stopped'
            }
            self.refresh_profile_list()
            self.save_profiles()
            
            # Select new profile
            items = list(self.profile_listbox.get(0, tk.END))
            if name in items:
                self.profile_listbox.selection_set(items.index(name))
                self.on_profile_select(None)
        elif name in self.profiles:
            messagebox.showerror("Error", "Profile name already exists!")
    
    def delete_profile(self):
        """Xóa profile"""
        selection = self.profile_listbox.curselection()
        if selection:
            profile_name = self.profile_listbox.get(selection[0])
            if messagebox.askyesno("Confirm", f"Delete profile '{profile_name}'?"):
                # Stop bot if running
                if profile_name in self.running_processes:
                    self.stop_bot_for_profile(profile_name)
                
                del self.profiles[profile_name]
                self.refresh_profile_list()
                self.save_profiles()
                
                # Clear form
                self.profile_name_var.set('')
                self.token_var.set('')
                self.profile_status_var.set('')
    
    def clone_profile(self):
        """Clone profile"""
        selection = self.profile_listbox.curselection()
        if selection:
            source_name = self.profile_listbox.get(selection[0])
            new_name = tk.simpledialog.askstring("Clone Profile", 
                                                f"Enter new name for clone of '{source_name}':")
            if new_name and new_name not in self.profiles:
                self.profiles[new_name] = self.profiles[source_name].copy()
                self.profiles[new_name]['status'] = 'Stopped'
                self.refresh_profile_list()
                self.save_profiles()
    
    def save_profile(self):
        """Save profile hiện tại"""
        profile_name = self.profile_name_var.get().strip()
        token = self.token_var.get().strip()
        
        if not profile_name:
            messagebox.showerror("Error", "Profile name is required!")
            return
        
        if not token:
            messagebox.showerror("Error", "Token is required!")
            return
        
        # Save to profiles dict
        if profile_name not in self.profiles:
            self.profiles[profile_name] = {'config': self.get_default_config(), 'status': 'Stopped'}
        
        self.profiles[profile_name]['token'] = token
        
        self.refresh_profile_list()
        self.save_profiles()
        
        messagebox.showinfo("Success", f"Profile '{profile_name}' saved!")
    
    def start_bot(self):
        """Start bot cho profile được chọn"""
        profile_name = self.profile_name_var.get().strip()
        token = self.token_var.get().strip()
        
        if not profile_name or not token:
            messagebox.showerror("Error", "Please select a profile and ensure token is set!")
            return
        
        if profile_name in self.running_processes:
            messagebox.showwarning("Warning", f"Bot for '{profile_name}' is already running!")
            return
        
        try:
            # Create config file for this profile
            config_data = self.profiles[profile_name].get('config', self.get_default_config())
            config_filename = f"config_{profile_name}.json"
            
            with open(config_filename, 'w', encoding='utf-8') as f:
                json.dump(config_data, f, indent=2, ensure_ascii=False)
            
            # Start bot process
            cmd = [sys.executable, '-m', 'lokbot', token]
            process = subprocess.Popen(cmd, 
                                     stdout=subprocess.PIPE, 
                                     stderr=subprocess.STDOUT,
                                     universal_newlines=True,
                                     bufsize=1)
            
            self.running_processes[profile_name] = process
            self.profiles[profile_name]['status'] = 'Running'
            self.profiles[profile_name]['start_time'] = time.time()  # Lưu thời gian start
            
            # Update UI
            self.profile_status_var.set('Running')
            self.profile_status_label.config(foreground="green")
            self.start_btn.config(state=tk.DISABLED)
            self.stop_btn.config(state=tk.NORMAL)
            
            # Start thread to read output
            threading.Thread(target=self.read_bot_output, 
                           args=(profile_name, process), daemon=True).start()
            
            self.log_message(f"Started bot for profile '{profile_name}'", "INFO")
            self.save_profiles()
            
        except Exception as e:
            self.log_message(f"Error starting bot: {str(e)}", "ERROR")
            messagebox.showerror("Error", f"Failed to start bot: {str(e)}")
    
    def stop_bot(self):
        """Stop bot cho profile được chọn"""
        profile_name = self.profile_name_var.get().strip()
        if profile_name:
            self.stop_bot_for_profile(profile_name)
    
    def stop_bot_for_profile(self, profile_name):
        """Stop bot cho profile cụ thể"""
        if profile_name in self.running_processes:
            process = self.running_processes[profile_name]
            process.terminate()
            del self.running_processes[profile_name]
            
            self.profiles[profile_name]['status'] = 'Stopped'
            
            # Update UI if this is the selected profile
            if self.profile_name_var.get() == profile_name:
                self.profile_status_var.set('Stopped')
                self.profile_status_label.config(foreground="gray")
                self.start_btn.config(state=tk.NORMAL)
                self.stop_btn.config(state=tk.DISABLED)
            
            self.log_message(f"Stopped bot for profile '{profile_name}'", "INFO")
            self.save_profiles()
    
    def read_bot_output(self, profile_name, process):
        """Đọc output từ bot process"""
        try:
            while True:
                output = process.stdout.readline()
                if output == '' and process.poll() is not None:
                    break
                if output:
                    self.log_message(f"[{profile_name}] {output.strip()}", "BOT")
        except Exception as e:
            self.log_message(f"Error reading bot output: {str(e)}", "ERROR")
        finally:
            # Process ended
            if profile_name in self.running_processes:
                del self.running_processes[profile_name]
                self.profiles[profile_name]['status'] = 'Stopped'
                
                # Update UI if this is the selected profile
                if self.profile_name_var.get() == profile_name:
                    self.root.after(0, self.update_stopped_status)
    
    def update_stopped_status(self):
        """Update UI khi bot stop"""
        self.profile_status_var.set('Stopped')
        self.profile_status_label.config(foreground="gray")
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
    
    def get_default_config(self):
        """Lấy config mặc định từ config.example.json"""
        try:
            config_example_path = Path("config.example.json")
            if config_example_path.exists():
                with open(config_example_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                # Fallback config nếu không tìm thấy config.example.json
                self.log_message("config.example.json not found, using fallback config", "WARNING")
                return self._get_fallback_config()
        except Exception as e:
            self.log_message(f"Error loading config.example.json: {str(e)}", "ERROR")
            return self._get_fallback_config()
    
    def _get_fallback_config(self):
        """Config dự phòng khi không load được config.example.json"""
        return {
            "main": {
                "jobs": [
                    {
                        "name": "alliance_farmer",
                        "enabled": True,
                        "kwargs": {
                            "gift_claim": True,
                            "help_all": True,
                            "research_donate": True,
                            "shop_auto_buy_item_code_list": []
                        },
                        "interval": {"start": 120, "end": 200}
                    },
                    {
                        "name": "socf_thread",
                        "enabled": True,
                        "kwargs": {
                            "targets": [
                                {
                                    "code": 20100105,
                                    "level": [1]
                                }
                            ],
                            "radius": 8,
                            "share_to": {
                                "chat_channels": []
                            }
                        },
                        "interval": {"start": 1, "end": 1}
                    }
                ],
                "threads": [
                    {
                        "name": "free_chest_farmer_thread",
                        "enabled": True
                    },
                    {
                        "name": "quest_monitor_thread",
                        "enabled": True
                    }
                ]
            },
            "socketio": {
                "debug": False
            }
        }
    
    def load_default_config(self):
        """Load config mặc định vào editor"""
        config = self.get_default_config()
        self.config_text.delete(1.0, tk.END)
        self.config_text.insert(1.0, json.dumps(config, indent=2, ensure_ascii=False))
    
    def load_example_config(self):
        """Load config từ config.example.json vào editor"""
        try:
            config_example_path = Path("config.example.json")
            if config_example_path.exists():
                with open(config_example_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                self.config_text.delete(1.0, tk.END)
                self.config_text.insert(1.0, json.dumps(config, indent=2, ensure_ascii=False))
                self.log_message("Loaded config from config.example.json", "INFO")
            else:
                messagebox.showerror("Error", "config.example.json not found!")
                self.log_message("config.example.json not found", "ERROR")
        except json.JSONDecodeError as e:
            messagebox.showerror("Error", f"Invalid JSON in config.example.json: {str(e)}")
            self.log_message(f"Invalid JSON in config.example.json: {str(e)}", "ERROR")
        except Exception as e:
            messagebox.showerror("Error", f"Error loading config.example.json: {str(e)}")
            self.log_message(f"Error loading config.example.json: {str(e)}", "ERROR")
    
    def load_config_for_profile(self, event=None):
        """Load config cho profile được chọn"""
        profile_name = self.config_profile_var.get()
        if profile_name and profile_name in self.profiles:
            config = self.profiles[profile_name].get('config', self.get_default_config())
            self.config_text.delete(1.0, tk.END)
            self.config_text.insert(1.0, json.dumps(config, indent=2, ensure_ascii=False))
    
    def save_config(self):
        """Save config từ editor"""
        profile_name = self.config_profile_var.get()
        if not profile_name:
            messagebox.showerror("Error", "Please select a profile!")
            return
        
        try:
            config_text = self.config_text.get(1.0, tk.END).strip()
            config_data = json.loads(config_text)
            
            if profile_name not in self.profiles:
                self.profiles[profile_name] = {'token': '', 'status': 'Stopped'}
            
            self.profiles[profile_name]['config'] = config_data
            self.save_profiles()
            
            messagebox.showinfo("Success", f"Config saved for profile '{profile_name}'!")
            
        except json.JSONDecodeError as e:
            messagebox.showerror("Error", f"Invalid JSON: {str(e)}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save config: {str(e)}")
    
    def log_message(self, message, level="INFO"):
        """Thêm message vào log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {level}: {message}\n"
        
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, log_entry)
        
        # Color coding
        if level == "ERROR":
            self.log_text.tag_add("error", f"end-{len(log_entry)}c", "end-1c")
            self.log_text.tag_config("error", foreground="red")
        elif level == "WARNING":
            self.log_text.tag_add("warning", f"end-{len(log_entry)}c", "end-1c")
            self.log_text.tag_config("warning", foreground="orange")
        elif level == "BOT":
            self.log_text.tag_add("bot", f"end-{len(log_entry)}c", "end-1c")
            self.log_text.tag_config("bot", foreground="blue")
        
        self.log_text.config(state=tk.DISABLED)
        
        # Auto scroll
        if self.auto_scroll_var.get():
            self.log_text.see(tk.END)
    
    def clear_logs(self):
        """Clear logs"""
        self.log_text.config(state=tk.NORMAL)
        self.log_text.delete(1.0, tk.END)
        self.log_text.config(state=tk.DISABLED)
    
    def save_logs(self):
        """Save logs ra file"""
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(self.log_text.get(1.0, tk.END))
                messagebox.showinfo("Success", f"Logs saved to {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save logs: {str(e)}")
    
    def on_status_profile_change(self, event=None):
        """Khi thay đổi profile trong status tab"""
        self.refresh_status()
    
    def refresh_status(self):
        """Refresh thông tin status"""
        profile_name = self.status_profile_var.get()
        if not profile_name or profile_name not in self.running_processes:
            self.clear_status_display()
            return
        
        # Đọc thống kê từ log file hoặc từ bot process
        self.update_status_display(profile_name)
    
    def clear_status_display(self):
        """Clear hiển thị status"""
        self.mines_label.config(text="Mines Gathered: 0")
        self.monsters_label.config(text="Monsters Killed: 0")
        self.uptime_label.config(text="Uptime: 0h 0m")
        self.mines_per_hour_label.config(text="Mines/Hour: 0.0")
        self.monsters_per_hour_label.config(text="Monsters/Hour: 0.0")
        self.bot_level_label.config(text="Level: Unknown")
        self.alliance_label.config(text="Alliance: None")
        self.march_limit_label.config(text="March Limit: 0")
        self.active_marches_label.config(text="Active Marches: 0")
        self.food_label.config(text="🍖 Food: 0")
        self.lumber_label.config(text="🪵 Lumber: 0")
        self.stone_label.config(text="🪨 Stone: 0")
        self.gold_label.config(text="🪙 Gold: 0")
        self.start_time_label.config(text="Start Time: Not running")
        self.last_update_label.config(text="Last Update: Never")
    
    def update_status_display(self, profile_name):
        """Cập nhật hiển thị status"""
        # Parse logs để lấy thống kê
        stats = self.parse_bot_statistics(profile_name)
        
        if stats:
            # Update statistics
            self.mines_label.config(text=f"Mines Gathered: {stats.get('mines_gathered', 0)}")
            self.monsters_label.config(text=f"Monsters Killed: {stats.get('monsters_killed', 0)}")
            
            uptime_hours = stats.get('uptime_hours', 0)
            uptime_minutes = (uptime_hours % 1) * 60
            self.uptime_label.config(text=f"Uptime: {int(uptime_hours)}h {int(uptime_minutes)}m")
            
            self.mines_per_hour_label.config(text=f"Mines/Hour: {stats.get('mines_per_hour', 0):.1f}")
            self.monsters_per_hour_label.config(text=f"Monsters/Hour: {stats.get('monsters_per_hour', 0):.1f}")
            
            # Update bot info
            self.bot_level_label.config(text=f"Level: {stats.get('level', 'Unknown')}")
            alliance_id = stats.get('alliance_id')
            alliance_text = f"Alliance: {alliance_id}" if alliance_id else "Alliance: None"
            self.alliance_label.config(text=alliance_text)
            self.march_limit_label.config(text=f"March Limit: {stats.get('march_limit', 0)}")
            self.active_marches_label.config(text=f"Active Marches: {stats.get('troop_queue_count', 0)}")
            
            # Update resources
            resources = stats.get('resources', [0, 0, 0, 0])
            self.food_label.config(text=f"🍖 Food: {self.format_number(resources[0])}")
            self.lumber_label.config(text=f"🪵 Lumber: {self.format_number(resources[1])}")
            self.stone_label.config(text=f"🪨 Stone: {self.format_number(resources[2])}")
            self.gold_label.config(text=f"🪙 Gold: {self.format_number(resources[3])}")
            
            # Update status info
            start_time = stats.get('start_time')
            if start_time:
                start_time_str = datetime.fromtimestamp(start_time).strftime("%Y-%m-%d %H:%M:%S")
                self.start_time_label.config(text=f"Start Time: {start_time_str}")
            
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.last_update_label.config(text=f"Last Update: {current_time}")
    
    def format_number(self, num):
        """Format số với K, M, B"""
        if num >= 1000000000:
            return f"{num/1000000000:.1f}B"
        elif num >= 1000000:
            return f"{num/1000000:.1f}M"
        elif num >= 1000:
            return f"{num/1000:.1f}K"
        else:
            return str(int(num))
    
    def parse_bot_statistics(self, profile_name):
        """Parse thống kê từ logs của bot"""
        # Đọc output từ process hoặc log file
        # Đây là implementation đơn giản, có thể cải thiện bằng cách
        # lưu statistics vào file JSON hoặc communicate với bot process
        
        current_time = time.time()
        
        # Tìm thống kê trong logs
        mines_gathered = 0
        monsters_killed = 0
        
        # Parse từ log text nếu có
        if hasattr(self, 'log_text'):
            log_content = self.log_text.get(1.0, tk.END)
            
            # Đếm số mỏ từ logs
            mines_matches = re.findall(r'Tổng số mỏ đã khai thác: (\d+)', log_content)
            if mines_matches:
                mines_gathered = int(mines_matches[-1])  # Lấy số cuối cùng
            
            # Đếm số quái từ logs  
            monsters_matches = re.findall(r'Tổng số quái đã đánh: (\d+)', log_content)
            if monsters_matches:
                monsters_killed = int(monsters_matches[-1])  # Lấy số cuối cùng
        
        # Ước tính thời gian chạy (từ khi start bot)
        if profile_name in self.profiles and 'start_time' in self.profiles[profile_name]:
            start_time = self.profiles[profile_name]['start_time']
        else:
            start_time = current_time - 3600  # Default 1 hour ago
        
        uptime_seconds = current_time - start_time
        uptime_hours = uptime_seconds / 3600
        
        return {
            'mines_gathered': mines_gathered,
            'monsters_killed': monsters_killed,
            'uptime_seconds': uptime_seconds,
            'uptime_hours': uptime_hours,
            'mines_per_hour': mines_gathered / uptime_hours if uptime_hours > 0 else 0,
            'monsters_per_hour': monsters_killed / uptime_hours if uptime_hours > 0 else 0,
            'start_time': start_time,
            'current_time': current_time,
            'level': 'Unknown',
            'alliance_id': None,
            'resources': [1500000, 2000000, 1200000, 800000],  # Mock data
            'march_limit': 3,
            'troop_queue_count': 2
        }

    def update_status_timer(self):
        """Timer để cập nhật status"""
        # Update status bar
        running_count = len(self.running_processes)
        if running_count > 0:
            self.status_var.set(f"Running {running_count} bot(s)")
        else:
            self.status_var.set("Ready")
        
        # Update status tab profile list
        if hasattr(self, 'status_profile_combo'):
            current_profiles = list(self.profiles.keys())
            self.status_profile_combo['values'] = current_profiles
            
            # Auto refresh if profile is selected
            if self.status_profile_var.get() in self.running_processes:
                self.update_status_display(self.status_profile_var.get())
        
        # Schedule next update
        self.root.after(5000, self.update_status_timer)  # Update every 5 seconds
    
    def on_closing(self):
        """Khi đóng ứng dụng"""
        # Stop all running bots
        for profile_name in list(self.running_processes.keys()):
            self.stop_bot_for_profile(profile_name)
        
        # Save profiles
        self.save_profiles()
        
        self.root.destroy()

def main():
    """Main function để chạy GUI"""
    try:
        import tkinter.simpledialog
        
        root = tk.Tk()
        app = LokBotGUI(root)
        
        # Handle window close
        root.protocol("WM_DELETE_WINDOW", app.on_closing)
        
        # Center window
        root.update_idletasks()
        width = root.winfo_width()
        height = root.winfo_height()
        x = (root.winfo_screenwidth() // 2) - (width // 2)
        y = (root.winfo_screenheight() // 2) - (height // 2)
        root.geometry(f"{width}x{height}+{x}+{y}")
        
        root.mainloop()
        
    except ImportError as e:
        print(f"Error: {e}")
        print("GUI requires tkinter. Please install it or use command line version.")
        sys.exit(1)

if __name__ == "__main__":
    main()