import json
import os
import re

def generate_dashboard():
    # Paths
    report_json = "report.json"
    template_html = "dashboard_template.html"
    output_html = "dashboard.html"
    
    if not os.path.exists(report_json):
        print(f"Error: {report_json} not found. Please run pytest --json-report")
        return
        
    with open(report_json, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    summary = data.get("summary", {})
    total = summary.get("total", 0)
    passed = summary.get("passed", 0)
    failed = summary.get("failed", 0)
    duration = summary.get("duration", 0)
    
    pass_rate = (passed / total * 100) if total > 0 else 0
    pass_rate_str = f"{pass_rate:.1f}"
    
    with open(template_html, 'r', encoding='utf-8') as f:
        html = f.read()
        
    # Replace Stats
    summary_text = f"Generated on {data.get('created', 'N/A')} | Duration: {duration:.2f}s"
    html = html.replace("<!-- STAT_SUMMARY -->", summary_text)
    html = html.replace("<!-- STAT_TOTAL -->", str(total))
    html = html.replace("<!-- STAT_PASSED -->", str(passed))
    html = html.replace("<!-- STAT_FAILED -->", str(failed))
    html = html.replace("<!-- STAT_RATE -->", f"{pass_rate_str}%")
    
    # Generate Table Rows
    rows_html = ""
    for test in data.get("tests", []):
        nodeid = test.get("nodeid", "Unknown")
        outcome = test.get("outcome", "unknown").upper()
        
        # Color based on outcome
        if outcome == "PASSED":
            badge_class = "bg-emerald-50 text-emerald-700 border-emerald-100"
        elif outcome == "FAILED":
            badge_class = "bg-rose-50 text-rose-700 border-rose-100"
        elif outcome == "SKIPPED":
            badge_class = "bg-amber-50 text-amber-700 border-amber-100"
        else:
            badge_class = "bg-surface-container-low text-on-surface-variant border-outline-variant/30"
            
        test_duration = test.get("setup", {}).get("duration", 0) + test.get("call", {}).get("duration", 0) + test.get("teardown", {}).get("duration", 0)
        
        row = f'''
        <tr class="hover:bg-surface/50 transition-colors group">
            <td class="px-6 py-4 text-sm text-on-surface font-semibold">{nodeid.split('::')[-1]}</td>
            <td class="px-6 py-4 text-sm text-on-surface">{nodeid.split('::')[0]}</td>
            <td class="px-6 py-4 text-sm text-on-surface font-medium">{test_duration:.2f}s</td>
            <td class="px-6 py-4">
                <span class="px-3 py-1 {badge_class} text-xs font-bold rounded-lg border">{outcome}</span>
            </td>
        </tr>
        '''
        rows_html += row
        
    html = html.replace("<!-- TABLE_ROWS -->", rows_html)
    
    # Save output
    with open(output_html, 'w', encoding='utf-8') as f:
        f.write(html)
        
    print(f"Successfully generated {output_html}")

if __name__ == "__main__":
    generate_dashboard()
