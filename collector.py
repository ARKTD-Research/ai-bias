import json
import os
import csv

spent = 0

def collect_anchoring_data():
    global spent
    input_dir = 'tests/anchoring/total'
    output_csv = 'anchoring_results.csv'
    
    # Check if the directory exists
    if not os.path.exists(input_dir):
        print(f"Directory {input_dir} not found.")
        return
        
    data = []
    
    # Read all JSON files
    for filename in os.listdir(input_dir):
        if filename.endswith('.json'):
            filepath = os.path.join(input_dir, filename)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = json.load(f)
                    
                    # Extract the required fields
                    model = content.get('model', 'Unknown')
                    test_type = content.get('type', 'Unknown')
                    
                    # Extract number from results
                    decoded = content.get('decoded', {})
                    verdict = decoded.get('verdict', 'REFUSAL') if isinstance(decoded, dict) else 'REFUSAL'
                    
                    data.append({
                        'filename': filename,
                        'model': model,
                        'type': test_type,
                        'verdict': verdict
                    })

                    spent += content['response']['usage']['cost_details']['upstream_inference_cost']
            except Exception as e:
                print(f"Error processing {filename}: {e}")
                
    # Write to CSV
    if data:
        with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['filename', 'model', 'type', 'verdict']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for row in data:
                writer.writerow(row)
        print(f"Successfully collected {len(data)} results and saved to {output_csv}")
    else:
        print("No valid JSON files found to process.")

if __name__ == '__main__':
    collect_anchoring_data()
    print(f"Total cost to run: {spent}")
