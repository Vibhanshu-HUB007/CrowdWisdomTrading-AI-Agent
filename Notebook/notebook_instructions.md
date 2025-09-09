# Jupyter Notebook Instructions

## Creating and Running the Interactive Demo Notebook

Since I cannot directly create `.ipynb` files, here are the instructions to create your own Jupyter notebook for the Twitter Financial Demo:

### Step 1: Create a New Jupyter Notebook

1. Install Jupyter if not already installed:
```bash
pip install jupyter
```

2. Start Jupyter:
```bash
jupyter notebook
```

3. Create a new Python 3 notebook named `Twitter_Financial_Demo.ipynb`

### Step 2: Notebook Cells

Copy and paste the following code into separate cells:

#### Cell 1: Setup and Imports
```python
# Install required packages (run this cell first)
!pip install pandas matplotlib seaborn ipython loguru

# Import the demo class
import sys
sys.path.append('.')
from jupyter_demo import TwitterFinancialDemo, run_interactive_demo

# Configure notebook display
from IPython.display import display, HTML
import warnings
warnings.filterwarnings('ignore')
```

#### Cell 2: Run Complete Demo
```python
# Run the complete interactive demo
results = run_interactive_demo()
```

#### Cell 3: Alternative - Step by Step Demo
```python
# Alternative: Run step by step for more control
from jupyter_demo import run_step_by_step_demo

# Initialize demo
demo = run_step_by_step_demo()
```

#### Cell 4: Step 1 - Keywords (if using step-by-step)
```python
# Step 1: Generate keywords
keywords_data = demo.step1_generate_keywords()
```

#### Cell 5: Step 2 - Search (if using step-by-step)
```python
# Step 2: Search users
search_data = demo.step2_search_users(keywords_data)
```

#### Cell 6: Step 3 - Filter (if using step-by-step)
```python
# Step 3: Filter users
filter_data = demo.step3_filter_users(search_data)
```

#### Cell 7: Step 4 - Format (if using step-by-step)
```python
# Step 4: Format results
format_data = demo.step4_format_results(filter_data)
```

#### Cell 8: Display Results (if using step-by-step)
```python
# Display comprehensive results
demo.display_results_summary()
demo.display_user_table()
```

#### Cell 9: Visualizations (if using step-by-step)
```python
# Create data visualizations
display(HTML("<h3>📊 Data Visualizations</h3>"))
demo.create_visualizations()
```

#### Cell 10: JSON Output (if using step-by-step)
```python
# Display and save JSON output
demo.display_json_output()
filename = demo.save_results()
print(f"Results saved to: {filename}")
```

### Step 3: Running the Notebook

1. Execute cells in order (Shift+Enter for each cell)
2. The complete demo (Cell 2) will run all steps automatically
3. The step-by-step approach (Cells 3-10) gives you more control

### Features You'll See:

- **Rich HTML displays** with styled headers and progress indicators
- **Interactive visualizations** showing user statistics and distributions
- **Data tables** with formatted user information
- **JSON output** with complete results
- **Processing statistics** and timing information
- **Automatic file saving** of results

### Output Files:

The notebook will generate:
- `jupyter_demo_results_YYYYMMDD_HHMMSS.json` - Complete results
- Rich visual output in the notebook cells
- Processing statistics and timing data

### Troubleshooting:

If you encounter issues:
1. Make sure all dependencies are installed: `pip install -r requirements.txt`
2. Ensure you're in the correct directory with the `jupyter_demo.py` file
3. Restart the kernel if imports fail: Kernel → Restart & Clear Output

This notebook provides a professional presentation of the CrewAI Twitter Financial Flow suitable for the internship submission video demonstration.
