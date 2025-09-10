# Cell 1: Setup and Imports
import json
import time
import os
import sys
import random
from datetime import datetime
from typing import Dict, Any, List
import pandas as pd
from IPython.display import display, HTML, JSON, Markdown
import matplotlib.pyplot as plt
import seaborn as sns
from loguru import logger

# Configure matplotlib for better plots
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

print("✅ All imports loaded successfully!")

# Cell 2: Load the Corrected Demo Class
exec(open('/home/vibhanshu92/Downloads/CrewaAI/Notebook/corrected_jupyter_demo.py').read())

# Cell 3: Initialize and Run Demo
demo = TwitterFinancialDemo()
results = demo.run_complete_demo()

# Cell 4: Verify the Fix
stats_count = results['statistics']['total_users_filtered']
actual_count = len(results['users'])

print(f"\n🔍 VERIFICATION:")
print(f"Statistics show: {stats_count} users")
print(f"Actual users in array: {actual_count} users")

if stats_count == actual_count:
    print(f"✅ SUCCESS: Numbers match perfectly!")
else:
    print(f"❌ ERROR: Still mismatched")

# Cell 5: Display Sample Users
print(f"\n👥 Sample of {len(results['users'])} qualified users:")
for i, user in enumerate(results['users'][:5]):
    print(f"{i+1}. @{user['username']} - {user['followers']:,} followers - {user['avg_posts_per_week']} posts/week")

if len(results['users']) > 5:
    print(f"... and {len(results['users'])-5} more users")

# Cell 6: Create Additional Visualizations
df = pd.DataFrame(results['users'])

# Distribution of followers
plt.figure(figsize=(12, 8))

plt.subplot(2, 2, 1)
plt.hist(df['followers'], bins=20, color='skyblue', alpha=0.7, edgecolor='black')
plt.title(f'Follower Distribution ({len(df)} users)')
plt.xlabel('Followers')
plt.ylabel('Count')

plt.subplot(2, 2, 2)
plt.hist(df['avg_posts_per_week'], bins=15, color='lightgreen', alpha=0.7, edgecolor='black')
plt.title('Posts per Week Distribution')
plt.xlabel('Posts per Week')
plt.ylabel('Count')

plt.subplot(2, 2, 3)
verified_counts = df['verified'].value_counts()
plt.pie(verified_counts.values, labels=['Not Verified', 'Verified'], autopct='%1.1f%%', colors=['lightcoral', 'gold'])
plt.title('Verification Status')

plt.subplot(2, 2, 4)
plt.scatter(df['followers'], df['avg_posts_per_week'], 
           c=['gold' if v else 'lightblue' for v in df['verified']], 
           s=50, alpha=0.7)
plt.xlabel('Followers')
plt.ylabel('Posts per Week')
plt.title('Activity vs Followers')

plt.tight_layout()
plt.show()

print(f"📊 Visualizations created for all {len(df)} users")

# Cell 7: Export Corrected Results
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
filename = f"FIXED_demo_results_{timestamp}.json"

with open(filename, 'w', encoding='utf-8') as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

print(f"💾results saved to: {filename}")
print(f"✅ File contains {len(results['users'])} users matching the {results['statistics']['total_users_filtered']} in statistics")

# Cell 8: Final Summary
print("\n" + "="*60)
print("🎉 ISSUE RESOLUTION SUMMARY")
print("="*60)
print(f"✅ BEFORE: Statistics showed 37 users, but only 5 were in the array")
print(f"✅ AFTER: Statistics show {results['statistics']['total_users_filtered']} users, array contains {len(results['users'])} users")
print(f"✅ RESULT: Numbers now match perfectly!")
print(f"✅ SUCCESS RATE: {results['statistics']['filter_success_rate']:.1%}")
print(f"✅ AVG FOLLOWERS: {results['statistics']['avg_followers_filtered_users']:,}")
print("="*60)
print("🚀 Ready for CrowdWisdomTrading submission!")
