#Code by google gemini
#Prompt by Taidanasaki
#this is my frist-time using AI to coding

#What can this do?
#make a s**t
#save time in make chart, let you efficient make chart

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import os
import sys
import random
import webbrowser
from datetime import datetime

class OsuManiaGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("osu!mania Random Chart Generator")
        self.root.geometry("900x750")

        if os.path.isfile("icon.ico"): #設定視窗圖標

            self.root.iconbitmap("icon.ico")
        else:
            self.root.iconbitmap(default=sys.executable) 

        self.root.resizable(True, True)

        # 基礎變數
        self.key_count_var = tk.IntVar(value=4)
        self.duration_var = tk.IntVar(value=120)
        self.delay_ms = tk.IntVar(value=0)

        
        # 軌道限制變數
        self.min_interval_mult_var = tk.DoubleVar(value=1)
        self.limit_a_var = tk.IntVar(value=4)
        self.limit_b_var = tk.IntVar(value=3)
        
        # 間隔模式變數
        self.interval_mode_var = tk.StringVar(value="ms")
        self.interval_ms_var = tk.DoubleVar(value=200)
        self.bpm_var = tk.DoubleVar(value=150)
        
        # 生成模式變數
        self.gen_mode_var = tk.StringVar(value="sequence")
        self.sequence_var = tk.StringVar(value="4 2 3 2")
        self.weight_vars = {} # 存放各鍵數比重的變數字典
        
        # 元數據變數
        self.meta_title = tk.StringVar(value="Random Generated Map")
        self.meta_artist = tk.StringVar(value="None")
        self.meta_creator = tk.StringVar(value="ManiaGenerator")
        self.meta_version = tk.StringVar(value=".")
        self.meta_source = tk.StringVar(value="")
        self.meta_tags = tk.StringVar(value="")

        self.setup_ui()
        
    def setup_ui(self):
        # 主佈局
        main_paned = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        main_paned.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        left_frame = ttk.Frame(main_paned)
        right_frame = ttk.Frame(main_paned)
        main_paned.add(left_frame, weight=1)
        main_paned.add(right_frame, weight=1)

        self.setup_left_panel(left_frame)
        self.setup_right_panel(right_frame)

    def setup_left_panel(self, parent):
        canvas = tk.Canvas(parent, borderwidth=0, highlightthickness=0)
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # 1. 基礎參數設定
        lf_basic = ttk.LabelFrame(scrollable_frame, text="Basic Settings")
        lf_basic.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(lf_basic, text="Duration (sec):").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        ttk.Entry(lf_basic, textvariable=self.duration_var, width=10).grid(row=0, column=1, padx=5, pady=5, sticky="w")
        
        ttk.Label(lf_basic, text="Key Count (4-10):").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        cb_keys = ttk.Combobox(lf_basic, textvariable=self.key_count_var, values=(2,3,4,5,6,7,8,9,10,12,14,16,18), width=8, state="readonly")

        ttk.Label(lf_basic, text="Delay(ms)").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        ttk.Entry(lf_basic, textvariable=self.delay_ms, width=10).grid(row=2, column=1, padx=5, pady=5, sticky="w")

        cb_keys.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        cb_keys.bind("<<ComboboxSelected>>", self.update_weight_inputs)

        # 2. 軌道限制
        lf_track = ttk.LabelFrame(scrollable_frame, text="Track Restrictions & Conflict Avoidance")
        lf_track.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(lf_track, text="Min Note Interval (Multiplier):").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        ttk.Entry(lf_track, textvariable=self.min_interval_mult_var, width=10).grid(row=0, column=1, padx=5, pady=5, sticky="w")
        
        frame_ab = ttk.Frame(lf_track)
        frame_ab.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="w")
        ttk.Label(frame_ab, text="Stream Limit per Track: Max").pack(side=tk.LEFT)
        ttk.Entry(frame_ab, textvariable=self.limit_b_var, width=4).pack(side=tk.LEFT, padx=2)
        ttk.Label(frame_ab, text="note(s) every").pack(side=tk.LEFT)
        ttk.Entry(frame_ab, textvariable=self.limit_a_var, width=4).pack(side=tk.LEFT, padx=2)
        ttk.Label(frame_ab, text="interval").pack(side=tk.LEFT)

        # 3. 間隔模式
        lf_interval = ttk.LabelFrame(scrollable_frame, text="Interval Mode")
        lf_interval.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Radiobutton(lf_interval, text="Milliseconds (ms)", variable=self.interval_mode_var, value="ms", command=self.toggle_interval_mode).grid(row=0, column=0, padx=5, pady=2, sticky="w")
        self.entry_ms = ttk.Entry(lf_interval, textvariable=self.interval_ms_var, width=10)
        self.entry_ms.grid(row=0, column=1, padx=5, pady=2, sticky="w")
        
        ttk.Radiobutton(lf_interval, text="Based on BPM (16th Note)", variable=self.interval_mode_var, value="bpm", command=self.toggle_interval_mode).grid(row=1, column=0, padx=5, pady=2, sticky="w")
        self.entry_bpm = ttk.Entry(lf_interval, textvariable=self.bpm_var, width=10)
        self.entry_bpm.grid(row=1, column=1, padx=5, pady=2, sticky="w")
        self.entry_bpm.configure(state="disabled")

        # 4. 生成模式
        lf_gen = ttk.LabelFrame(scrollable_frame, text="Note Generation Mode")
        lf_gen.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Radiobutton(lf_gen, text="Sequential Generation", variable=self.gen_mode_var, value="sequence").pack(anchor="w", padx=5, pady=2)
        self.frame_seq = ttk.Frame(lf_gen)
        self.frame_seq.pack(fill=tk.X, padx=20, pady=2)
        ttk.Label(self.frame_seq, text="Input Sequence :").pack(side=tk.LEFT)
        self.entry_seq = ttk.Entry(self.frame_seq, textvariable=self.sequence_var)
        self.entry_seq.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        ttk.Radiobutton(lf_gen, text="Random Generation (Weights)", variable=self.gen_mode_var, value="random").pack(anchor="w", padx=5, pady=2)
        self.frame_rand = ttk.Frame(lf_gen)
        self.frame_rand.pack(fill=tk.X, padx=20, pady=2)
        self.update_weight_inputs()

        # 5. 元數據 (可折疊)
        self.lf_meta = ttk.LabelFrame(scrollable_frame, text="▼ Custom Metadata")
        self.lf_meta.pack(fill=tk.X, padx=5, pady=5)
        self.lf_meta.bind("<Button-1>", self.toggle_metadata)
        
        self.frame_meta_content = ttk.Frame(self.lf_meta)
        self.frame_meta_content.pack(fill=tk.X, padx=5, pady=5)
        
        #6. 其他
        lf_more = ttk.LabelFrame(scrollable_frame, text="// Links & Info")
        lf_more.pack(fill=tk.X, padx=5, pady=5)
        ttk.Button(lf_more, text="GitHub Repositories", command=lambda: webbrowser.open_new("https://github.com/Taidanasaki/ManiaRandomChartGenerator")).pack(fill=tk.X, anchor="w", padx=2, pady=2)

        meta_fields = [
            ("Title:", self.meta_title), ("Artist:", self.meta_artist),
            ("Creator:", self.meta_creator), ("Version:", self.meta_version),
            ("Source:", self.meta_source), ("Tags:", self.meta_tags)
        ]
        for i, (label_text, var) in enumerate(meta_fields):
            ttk.Label(self.frame_meta_content, text=label_text).grid(row=i, column=0, sticky="w", padx=2, pady=2)
            ttk.Entry(self.frame_meta_content, textvariable=var, width=25).grid(row=i, column=1, sticky="ew", padx=2, pady=2)

    def setup_right_panel(self, parent):
        # 資訊顯示區
        lf_info = ttk.LabelFrame(parent, text="Execution Log & Statistics")
        lf_info.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.log_text = scrolledtext.ScrolledText(lf_info, wrap=tk.WORD, state="disabled")
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.progress = ttk.Progressbar(parent, orient="horizontal", mode="determinate")
        self.progress.pack(fill=tk.X, padx=5, pady=5)

        # 按鈕區
        frame_btn = ttk.Frame(parent)
        frame_btn.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(frame_btn, text="Generate Beatmap", command=self.generate_beatmap).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_btn, text="Clear Log", command=self.clear_log).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_btn, text="Open Output Directory", command=self.open_output_dir).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_btn, text="Exit", command=self.root.destroy).pack(side=tk.RIGHT, padx=5)

    def toggle_interval_mode(self):
        mode = self.interval_mode_var.get()
        if mode == "ms":
            self.entry_ms.configure(state="normal")
            self.entry_bpm.configure(state="normal")
        else:
            self.entry_ms.configure(state="normal")
            self.entry_bpm.configure(state="normal")


    def toggle_metadata(self, event):
        if self.frame_meta_content.winfo_ismapped():
            self.frame_meta_content.pack_forget()
            self.lf_meta.config(text="▶ Custom Metadata")
        else:
            self.frame_meta_content.pack(fill=tk.X, padx=5, pady=5)
            self.lf_meta.config(text="▼ Custom Metadata")

    def update_weight_inputs(self, event=None):
        for widget in self.frame_rand.winfo_children():
            widget.destroy()
            
        keys = self.key_count_var.get()
        self.weight_vars.clear()
        
        # 為了保持隨機生成模式的一致性，隨機生成的下限依然從 1 開始，
        # 如果用戶希望隨機生成也有 0，也可以手動改這裡的 range(0, keys + 1)，
        # 但通常隨機模式不需要 0，留空主要依賴順序生成模式設定。
        for k in range(1, keys + 1):
            frame_row = ttk.Frame(self.frame_rand)
            frame_row.pack(fill=tk.X, pady=1)
            ttk.Label(frame_row, text=f"{k} Key Weights:").pack(side=tk.LEFT, padx=5)
            var = tk.DoubleVar(value=1.0)
            self.weight_vars[k] = var
            entry = ttk.Entry(frame_row, textvariable=var, width=8)
            entry.pack(side=tk.LEFT)
            if self.gen_mode_var.get() == "sequence":
                entry.configure(state="normal")

    def log(self, msg):
        self.log_text.configure(state="normal")
        self.log_text.insert(tk.END, msg + "\n")
        self.log_text.see(tk.END)
        self.log_text.configure(state="disabled")
        self.root.update_idletasks()

    def clear_log(self):
        self.log_text.configure(state="normal")
        self.log_text.delete(1.0, tk.END)
        self.log_text.configure(state="disabled")

    def open_output_dir(self):
        out_dir = os.path.abspath("generated_mania_maps")
        os.makedirs(out_dir, exist_ok=True)
        if os.name == 'nt':
            os.startfile(out_dir)
        elif os.name == 'posix':
            os.system(f'xdg-open "{out_dir}"')

    def generate_beatmap(self):
        try:
            self.clear_log()
            self.log("Generating beatmap...")
            
            # 取出並驗證參數
            keys = self.key_count_var.get()
            duration_ms = self.duration_var.get() * 1000
            limit_a = self.limit_a_var.get()
            limit_b = self.limit_b_var.get()
            delay = self.delay_ms.get()

            
            if limit_a < limit_b:
                raise ValueError("Track restriction error: 'a' must be greater than or equal to 'b'")

            interval_mode = self.interval_mode_var.get()
            if interval_mode == "ms":
                interval_ms = self.interval_ms_var.get()
                if interval_ms <= 0: raise ValueError("Interval (ms) must be greater than 0")
                bpm = 60000 / (interval_ms * 4)
            else:
                bpm = self.bpm_var.get()
                if bpm <= 0: raise ValueError("BPM must be greater than 0")
                interval_ms = (60000 / bpm) / 4
            
            min_interval_ms = interval_ms * self.min_interval_mult_var.get()
            beat_length = interval_ms * 4
            
            gen_mode = self.gen_mode_var.get()
            sequence = []
            if gen_mode == "sequence":
                seq_str = self.sequence_var.get().strip()
                if not seq_str: raise ValueError("Sequence cannot be empty in Sequential Generation mode")
                try:
                    sequence = [int(x) for x in seq_str.split()]
                except ValueError:
                    raise ValueError("Invalid sequence format. Please enter space-separated numbers")
            else:
                weights = {k: v.get() for k, v in self.weight_vars.items()}
                if sum(weights.values()) <= 0:
                    raise ValueError("Total weight must be greater than 0")

            # 初始化狀態
            current_time = 0.0
            step_index = 0
            track_history = {k: [] for k in range(keys)}
            last_note_time = {k: -9999.0 for k in range(keys)}
            hit_objects = []
            
            track_usage_counts = {k: 0 for k in range(keys)}
            # 讓陣列支援 0 鍵組合的計算
            key_count_dist = {k: 0 for k in range(0, keys + 1)}

            self.progress["maximum"] = duration_ms
            self.progress["value"] = 0

            # 生成主迴圈
            while current_time <= duration_ms:
                # 決定當前時間點的按鍵數量 N
                target_notes = 0
                if gen_mode == "sequence":
                    target_notes = sequence[step_index % len(sequence)]
                else:
                    total_weight = sum(weights.values())
                    r = random.uniform(0, total_weight)
                    for k, w in weights.items():
                        r -= w
                        if r <= 0:
                            target_notes = k
                            break
                            
                # 【修改處】將下限從 1 放寬至 0，讓 target_notes 允許為 0
                target_notes = min(max(0, target_notes), keys)
                
                # --- 軌道分級篩選 ---
                ideal_tracks = []     # 優先級 1: 完美滿足所有限制
                backup_tracks = []    # 優先級 2: 滿足防撞，但違反軌道歷史上限
                emergency_tracks = [] # 優先級 3: 連間隔防撞都違反
                
                for t in range(keys):
                    time_ok = (current_time - last_note_time[t] >= min_interval_ms - 0.001)
                    history_ok = True
                    
                    if limit_a > 1 and limit_b > 0:
                        recent_history = track_history[t][-(limit_a - 1):] if len(track_history[t]) > 0 else []
                        if sum(recent_history) >= limit_b:
                            history_ok = False
                    elif limit_b == 0:
                        history_ok = False
                        
                    if time_ok and history_ok:
                        ideal_tracks.append(t)
                    elif time_ok and not history_ok:
                        backup_tracks.append(t)
                    else:
                        emergency_tracks.append(t)
                
                placed_tracks = []
                
                # 輔助函式：從給定的軌道池中，盡可能抽取需要的數量，且優先選擇相鄰軌道
                def pick_from_pool(pool, needed_count, current_placed):
                    if not pool or needed_count <= 0:
                        return []
                    picked = []
                    rem_pool = pool.copy()
                    
                    while len(picked) < needed_count and rem_pool:
                        candidates = []
                        all_placed = current_placed + picked
                        
                        # 在剩餘池中尋找與已放置軌道相鄰的合法軌道
                        for p in all_placed:
                            if (p - 1) in rem_pool and (p - 1) not in candidates: candidates.append(p - 1)
                            if (p + 1) in rem_pool and (p + 1) not in candidates: candidates.append(p + 1)
                        
                        # 若有相鄰軌道則優先隨機挑選，否則在池中任意隨機挑選
                        if candidates:
                            nxt = random.choice(candidates)
                        else:
                            nxt = random.choice(rem_pool)
                            
                        picked.append(nxt)
                        rem_pool.remove(nxt)
                        
                    return picked

                # 如果 target_notes 為 0，下方的 pick_from_pool 都不會觸發，placed_tracks 維持空陣列 []
                placed_tracks.extend(pick_from_pool(ideal_tracks, target_notes - len(placed_tracks), placed_tracks))
                placed_tracks.extend(pick_from_pool(backup_tracks, target_notes - len(placed_tracks), placed_tracks))
                placed_tracks.extend(pick_from_pool(emergency_tracks, target_notes - len(placed_tracks), placed_tracks))
                
                # 生成 osu 物件格式
                for t in placed_tracks:
                    x = int((t * 512 + 256) / keys)
                    obj_str = f"{x},192,{int(current_time + delay)},1,0,0:0:0:0:"
                    hit_objects.append(obj_str)
                    last_note_time[t] = current_time
                    track_usage_counts[t] += 1
                    
                # 記錄 0 鍵及多鍵的數量分布
                key_count_dist[len(placed_tracks)] += 1
                
                # 更新歷史軌跡紀錄
                for t in range(keys):
                    track_history[t].append(1 if t in placed_tracks else 0)

                current_time += interval_ms
                step_index += 1
                
                if step_index % 100 == 0:
                    self.progress["value"] = current_time
                    self.root.update_idletasks()
            
            self.progress["value"] = duration_ms
            
            # 輸出檔案
            out_dir = "generated_mania_maps"
            os.makedirs(out_dir, exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"mania_{keys}K_{timestamp}.osu"
            filepath = os.path.join(out_dir, filename)
            
            title = self.meta_title.get()
            artist = self.meta_artist.get()
            creator = self.meta_creator.get()
            version = self.meta_version.get() + f" ({timestamp})"
            
            osu_content = f"""osu file format v14

[General]
AudioFilename: audio.mp3
Mode: 3


[Metadata]
Title:{title}
TitleUnicode:{title}
Artist:{artist}
ArtistUnicode:{artist}
Creator:{creator}
Version:{version}
Source:{self.meta_source.get()}
Tags:{self.meta_tags.get()}

[Difficulty]
CircleSize:{keys}
OverallDifficulty:5

[TimingPoints]
0,{beat_length},4,2,0,100,1,0

[HitObjects]
"""
            osu_content += "\n".join(hit_objects)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(osu_content)

            # 顯示統計資料
            total_notes = len(hit_objects)
            duration_sec = self.duration_var.get()
            density = total_notes / duration_sec if duration_sec > 0 else 0
            
            self.log("=== Generation Completed ===")
            self.log(f"Saved Path: {filepath}")
            self.log(f"TimingPoint Setup: 0,{beat_length:.4f},4,2,0,100,1,0")
            self.log(f"Corresponding BPM: {bpm:.2f} | Note Interval: {interval_ms:.2f}ms")
            self.log("-" * 30)
            self.log("#Detailed Statistics")
            self.log(f"Total Notes: {total_notes}")
            self.log(f"Note Density: {density:.2f} Notes/sec")
            
            self.log("\n【Simultaneous key count distribution】")
            for k, count in key_count_dist.items():
                if count > 0:
                    if k == 0:
                        self.log(f"  休止符 (0鍵): {count} 次")
                    else:
                        self.log(f"  {k} 鍵組合: {count} 次")
                    
            self.log("\n#Track Usage Distribution")
            for t in range(keys):
                self.log(f"  軌道 {t+1}: {track_usage_counts[t]} 次")
                
            self.log("\n#First 5 Generated Timestamps Example")
            sample_objs = hit_objects[:min(5*keys, len(hit_objects))]
            printed_times = set()
            count = 0
            for obj in sample_objs:
                time_val = int(obj.split(',')[2])
                if time_val not in printed_times:
                    if count >= 5: break
                    self.log(f"  Time: {time_val}ms")
                    printed_times.add(time_val)
                    count += 1
                    
            messagebox.showinfo("Success", "Beatmap generated successfully!\nYou can check the detailed statistics in the right panel.")

        except Exception as e:
            self.log(f"Error occurred: {str(e)}")
            messagebox.showerror("Error", str(e))
            self.progress["value"] = 0

if __name__ == "__main__":
    root = tk.Tk()
    app = OsuManiaGeneratorApp(root)
    root.mainloop()