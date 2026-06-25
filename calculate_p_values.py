import csv
import statistics
import scipy.stats
import os
from collections import defaultdict

def main():
    model_data = defaultdict(lambda: {"control": [], "test": []})
    
    csv_path = os.path.join(os.path.dirname(__file__), "anchoring_results.csv")
    try:
        with open(csv_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    verdict = float(row["verdict"])
                except ValueError:
                    continue
                model = row["model"]
                test_type = row["type"]
                model_data[model][test_type].append(verdict)
    except FileNotFoundError:
        print(f"{csv_path} not found.")
        return

    print(f"Option | Control Mean | Test Mean | Diff | t-stat | p-value")
    print("-" * 80)

    for model, data in model_data.items():
        control = data["control"]
        test = data["test"]
        
        if len(control) < 2 or len(test) < 2:
            print(f"{model}: Not enough data")
            continue
            
        m1 = statistics.mean(control)
        m2 = statistics.mean(test)
        
        result = scipy.stats.ttest_ind(control, test, equal_var=False)
        t_stat = result.statistic
        p_val = result.pvalue
        diff = m2 - m1
        
        print(f"{model:<20} | {m1:>12.2f} | {m2:>9.2f} | {diff:>5.2f} | {t_stat:>6.2f} | {p_val:.2e}")

if __name__ == "__main__":
    main()

