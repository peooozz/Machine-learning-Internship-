
# 🛠️ Complete Setup & Organization Guide

**Machine Learning Internship - Cognifyz Technologies**

---

## 📋 Table of Contents

1. [New Folder Organization](#new-folder-organization)
2. [Installation Steps](#installation-steps)
3. [File Checklist](#file-checklist)
4. [Testing Each Task](#testing-each-task)
5. [Creating Screenshots](#creating-screenshots)
6. [Packaging for Submission](#packaging-for-submission)
7. [Troubleshooting](#troubleshooting)

---

## 📁 New Folder Organization

### Step 1: Create Main Project Folder

```bash
# Create main folder
mkdir Cognifyz_ML_Internship
cd Cognifyz_ML_Internship
```

### Step 2: Create All Subfolders

```bash
# Create task folders
mkdir Task1_Rating_Prediction
mkdir Task2_Recommendation_System
mkdir Task4_Location_Analysis
mkdir Dashboard
mkdir Screenshots
```

### Step 3: Organize Your Files

Move files to their respective folders following this structure:

```
Cognifyz_ML_Internship/
│
├── Task1_Rating_Prediction/
│   ├── task1_main.py
│   ├── data_preprocessing.py
│   ├── model_training.py
│   ├── model_evaluation.py
│   ├── feature_analysis.py
│   ├── README.md
│   ├── requirements.txt
│   └── Dataset.csv
│
├── Task2_Recommendation_System/
│   ├── task2_main.py
│   ├── recommendation_preprocessing.py
│   ├── recommendation_engine.py
│   ├── recommendation_utils.py
│   ├── README.md
│   ├── requirements.txt
│   └── Dataset.csv
│
├── Task4_Location_Analysis/
│   ├── task4_main.py
│   ├── location_preprocessing.py
│   ├── location_analysis.py
│   ├── location_visualization.py
│   ├── location_insights.py
│   ├── README.md
│   ├── requirements.txt
│   └── Dataset.csv
│
├── Dashboard/
│   └── dashboard.html
│
├── Screenshots/
│   └── (empty for now)
│
└── MAIN_README.md
```

---

## 🔧 Installation Steps

### Option 1: Install Globally (Recommended)

```bash
# Install all required libraries at once
pip install pandas numpy folium

# Verify installation
python -c "import pandas; print('Pandas:', pandas.__version__)"
python -c "import numpy; print('NumPy:', numpy.__version__)"
python -c "import folium; print('Folium:', folium.__version__)"
```

### Option 2: Install Per Task

```bash
# Navigate to each task folder and install
cd Task1_Rating_Prediction
pip install -r requirements.txt

cd ../Task2_Recommendation_System
pip install -r requirements.txt

cd ../Task4_Location_Analysis
pip install -r requirements.txt
```

### Option 3: Use Virtual Environment (Advanced)

```bash
# Create virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install packages
pip install pandas numpy folium

# Deactivate when done
deactivate
```

---

## ✅ File Checklist

### Task 1 Files (7 total)

- [ ] `task1_main.py` (main execution)
- [ ] `data_preprocessing.py` (data handling)
- [ ] `model_training.py` (ML model)
- [ ] `model_evaluation.py` (metrics)
- [ ] `feature_analysis.py` (feature importance)
- [ ] `README.md` (documentation)
- [ ] `requirements.txt` (dependencies)
- [ ] `Dataset.csv` (data - copy from original)

### Task 2 Files (6 total)

- [ ] `task2_main.py` (main execution)
- [ ] `recommendation_preprocessing.py` (data prep)
- [ ] `recommendation_engine.py` (recommendation logic)
- [ ] `recommendation_utils.py` (utilities)
- [ ] `README.md` (documentation)
- [ ] `requirements.txt` (dependencies)
- [ ] `Dataset.csv` (data - copy from original)

### Task 4 Files (7 total)

- [ ] `task4_main.py` (main execution)
- [ ] `location_preprocessing.py` (data validation)
- [ ] `location_analysis.py` (analysis functions)
- [ ] `location_visualization.py` (maps & charts)
- [ ] `location_insights.py` (insights)
- [ ] `README.md` (documentation)
- [ ] `requirements.txt` (dependencies)
- [ ] `Dataset.csv` (data - copy from original)

### Additional Files

- [ ] `Dashboard/dashboard.html`
- [ ] `MAIN_README.md`
- [ ] `Screenshots/` (folder with images)

---

## 🧪 Testing Each Task

### Test Task 1

```bash
cd Task1_Rating_Prediction
python task1_main.py
```

**Expected Output:**
- Data loaded successfully
- Model trained
- Performance metrics displayed
- Feature importance shown
- Results saved

**Success Indicators:**
- ✅ R² score around 0.30
- ✅ MAE around 1.08
- ✅ No errors

### Test Task 2

```bash
cd Task2_Recommendation_System
python task2_main.py
```

**Expected Output:**
- Data prepared
- 4 test cases executed
- Recommendations displayed
- Statistics shown

**Success Indicators:**
- ✅ Recommendations found for each test case
- ✅ Match scores calculated
- ✅ No errors

### Test Task 4

```bash
cd Task4_Location_Analysis
python task4_main.py
```

**Expected Output:**
- Location data validated
- City/locality analysis completed
- Patterns identified
- Map created (if folium installed)
- Insights generated

**Success Indicators:**
- ✅ All cities analyzed
- ✅ Insights displayed
- ✅ Files created
- ✅ No errors

### Test Dashboard

```bash
# Open in browser
Dashboard/dashboard.html
```

**Expected Output:**
- Dashboard loads in browser
- All tabs work
- Interactive demos functional
- Professional appearance

---

## 📸 Creating Screenshots

### What to Capture

#### Task 1 Screenshots
1. **Terminal output** - Full execution results
2. **Performance metrics** - R², MAE, RMSE
3. **Feature importance** - Weight visualization

#### Task 2 Screenshots
1. **Terminal output** - Recommendation results
2. **Sample recommendations** - All 4 test cases
3. **Statistics** - System summary

#### Task 4 Screenshots
1. **Terminal output** - Analysis results
2. **Interactive map** - If folium works
3. **City statistics** - Top cities table
4. **Insights** - Key findings

#### Dashboard Screenshots
1. **Overview tab** - Main dashboard view
2. **Task 1 demo** - Prediction interface
3. **Task 2 demo** - Recommendation interface
4. **File structure** - Complete organization

### How to Take Screenshots

**Windows:**
- Press `Windows + Shift + S` for Snipping Tool
- Press `Windows + PrtScn` for full screenshot
- Save to Screenshots folder

**Mac:**
- Press `Cmd + Shift + 4` for selection
- Press `Cmd + Shift + 3` for full screen
- Drag to Screenshots folder

**Linux:**
- Use built-in screenshot tool
- Or install `scrot` or `flameshot`

### Naming Convention

```
task1_output.png
task1_metrics.png
task1_features.png
task2_output.png
task2_recommendations.png
task4_output.png
task4_map.png
task4_insights.png
dashboard_overview.png
dashboard_task1.png
dashboard_task2.png
file_structure.png
```

---

## 📦 Packaging for Submission

### Step 1: Final Checklist

Before creating ZIP, verify:

- [ ] All Python files run without errors
- [ ] All README files are complete
- [ ] Screenshots are clear and properly named
- [ ] Dashboard opens in browser
- [ ] MAIN_README.md is updated with your name
- [ ] All folders are organized correctly

### Step 2: Create ZIP File

**Windows:**
1. Right-click on `Cognifyz_ML_Internship` folder
2. Select "Send to" → "Compressed (zipped) folder"
3. Rename to: `Cognifyz_ML_Internship_YourName.zip`

**Mac:**
1. Right-click on `Cognifyz_ML_Internship` folder
2. Select "Compress"
3. Rename to: `Cognifyz_ML_Internship_YourName.zip`

**Linux:**
```bash
zip -r Cognifyz_ML_Internship_YourName.zip Cognifyz_ML_Internship/
```

### Step 3: Verify ZIP Contents

Extract the ZIP to a different location and verify:
- All folders present
- All files intact
- Can run tasks from extracted folder

### Step 4: Upload

1. Go to submission link provided by Cognifyz
2. Upload the ZIP file
3. Fill out any required forms
4. Submit before deadline (Nov 21, 2025)

---

## 🔧 Troubleshooting

### Issue 1: "No module named 'pandas'"

**Solution:**
```bash
pip install pandas numpy
# OR
python -m pip install pandas numpy
```

### Issue 2: "Permission Denied" during pip install

**Solution:**
```bash
# Add --user flag
pip install --user pandas numpy
```

### Issue 3: Dataset.csv not found

**Solution:**
- Ensure Dataset.csv is in the same folder as the Python file
- Check filename spelling (case-sensitive on Linux/Mac)
- Use absolute path if needed

### Issue 4: Folium map not working

**Solution:**
```bash
# Install folium
pip install folium

# If still not working, tasks will run without map
# Map is optional feature
```

### Issue 5: Files in wrong folders

**Solution:**
```bash
# Move files to correct location
# Windows:
move file.py correct_folder\

# Mac/Linux:
mv file.py correct_folder/
```

### Issue 6: Python version too old

**Solution:**
```bash
# Check version
python --version

# Should be 3.8 or higher
# If not, download from python.org
```

### Issue 7: Code runs but shows errors

**Check these common issues:**
1. Dataset.csv in correct location?
2. All imports at top of file?
3. Correct Python version?
4. All libraries installed?

### Issue 8: Dashboard not loading

**Solution:**
1. Open dashboard.html directly in browser
2. Don't open through file explorer, use "Open with" → Browser
3. Try different browser (Chrome, Firefox, Edge)

---

## ⏰ Timeline Checklist

### Today (Nov 17) - Setup Day
- [x] Create folder structure
- [x] Organize all files
- [x] Install dependencies
- [x] Test all 3 tasks
- [ ] Take screenshots
- [ ] Update MAIN_README with your name

### Tomorrow (Nov 18) - Testing Day
- [ ] Re-run all tasks
- [ ] Verify outputs
- [ ] Check all screenshots
- [ ] Test dashboard in browser
- [ ] Verify ZIP creation

### Nov 19 - Documentation Day
- [ ] Review all README files
- [ ] Record LinkedIn video
- [ ] Write video description
- [ ] Post on LinkedIn with hashtags

### Nov 20 - Final Review
- [ ] Create final ZIP
- [ ] Test ZIP extraction
- [ ] Prepare for submission
- [ ] Double-check deadline

### Nov 21 - Submission Day
- [ ] Submit before deadline!
- [ ] Keep backup copy
- [ ] Confirm submission received

---

## 🎯 Quick Commands Reference

```bash
# Navigate to task
cd Task1_Rating_Prediction

# Run task
python task1_main.py

# Go back to main folder
cd ..

# List files
# Windows: dir
# Mac/Linux: ls -la

# Check Python version
python --version

# Check if library installed
pip show pandas

# Install library
pip install library_name

# Create folder
# Windows: mkdir folder_name
# Mac/Linux: mkdir folder_name

# Copy file
# Windows: copy source dest
# Mac/Linux: cp source dest
```

---

## 📝 Final Notes

### Important Reminders

1. **Always test before submitting**
2. **Keep backups of everything**
3. **Name files exactly as specified**
4. **Submit before Nov 21 deadline**
5. **Include your name in ZIP filename**

### Contact for Help

If you encounter issues:
1. Review this guide
2. Check individual task READMEs
3. Re-read error messages carefully
4. Ask for help if stuck

---

## ✅ Pre-Submission Checklist

Run through this before creating final ZIP:

```
[ ] All 3 tasks run without errors
[ ] All 20 Python files present
[ ] All 4 README files complete
[ ] Dashboard opens in browser
[ ] Screenshots captured (8+ images)
[ ] Your name in MAIN_README.md
[ ] Folders organized correctly
[ ] Dataset.csv in all task folders
[ ] ZIP file created and tested
[ ] Ready to submit!
```

---

**Good luck with your submission! You've got this! 🚀**

---

Last Updated: November 17, 2025