
---

## 🛠️ **Scripting Progress Plan: Automated Video Workflow**

### **Phase 1: Foundation Setup**
- [x] Set up `config.json` for paths (RAW, MASTER, SSD name, etc.)
- [x] Create base Python project structure
- [x] Define logging system (`loguru` or native `logging`)
- [x] Detect external SSD mount via `diskutil` or polling

---

### **Phase 2: SD Card Detection + Auto-Import**
- [x] Script to detect new SD card mount (watch `/Volumes/`)
- [x] Identify video files (.mp4, .mov) on SD card
- [x] Copy files to `/RAW/<date>/footage/` on SSD
- [x] Auto-create dated project folder

---

### **Phase 3: Folder Structure Generator**
- [x] Create subfolders: `footage/`, `proxies/`, `exports/`, `logs/`
- [x] Optionally copy DaVinci `.drp` template if configured
- [x] Include manual run flag in CLI (`--structure-only`)

---

### **Phase 4: Proxy Generator (Optional)**
- [x] ffmpeg script to batch convert RAW to proxies
- [x] Place output in `/proxies/`
- [x] Add toggle in config to enable/disable

---

### **Phase 5: Export Folder Watcher**
- [x] Watch DaVinci export folder (`watchdog`)
- [x] Auto-move new renders to `/MASTER/<date>/`
- [x] Rename files with project name + timestamp
- [x] Log all export activity

---

### **Phase 6: Playbook Upload Automation**
- [x] Investigate API / upload methods (Playbook or alternative)
- [x] Script auto-upload from MASTER folder
- [x] Avoid duplicates (filename hash or timestamp)
- [x] Notify on upload success/failure

---

### **Phase 7: GUI Interface (PyQt6)**
- [x] Create main window with tabs for each module
- [x] Implement SD detection tab with monitoring controls
- [x] Implement folder structure tab with project settings
- [x] Implement proxy generator tab with conversion options
- [x] Implement export watcher tab with monitoring controls
- [x] Implement upload tab with API settings
- [x] Implement config tab for application settings
- [x] Implement log viewer tab for monitoring activity
- [x] Add responsive scrollable layouts to prevent overlapping elements
  - SD card status
  - File copy progress
  - Export detection
  - Upload progress
- [ ] Manual override buttons (Start, Retry, Cancel)
- [ ] Log viewer and settings access

---

### **Final Phase: Packaging & Scheduling**
- [ ] Bundle CLI version for headless use
- [ ] Add `launchd` plist to run on SD card insert
- [ ] Add GUI app as optional frontend
- [ ] Test full pipeline start to finish

---

Would you like me to generate the project folder structure and starter code for Phase 1 now?