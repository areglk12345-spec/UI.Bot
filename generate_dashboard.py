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
        
    # Replace headers
    html = html.replace("<title>Enterprise SaaS Dashboard - Clean &amp; Minimal</title>", "<title>UI Bot Test Dashboard</title>")
    html = html.replace("Enterprise", "UI Bot Report")
    html = html.replace("Management", "Test Automation")
    html = html.replace("Executive Overview", "Test Execution Overview")
    html = html.replace("Performance metrics for the current billing cycle.", f"Generated on {data.get('created', 'N/A')} | Duration: {duration:.2f}s")
    
    # Replace Card 1
    html = html.replace("Total Revenue", "Total Tests")
    html = html.replace("$248,392", str(total))
    
    # Replace Card 2
    html = html.replace("Active Users", "Passed Tests")
    html = html.replace("14.2k", str(passed))
    
    # Replace Card 3
    html = html.replace("New Signups", "Failed Tests")
    html = html.replace("1,204", str(failed))
    
    # Replace Card 4
    html = html.replace("Conv. Rate", "Pass Rate")
    html = html.replace("3.42%", f"{pass_rate_str}%")
    
    # Replace Chart Title
    html = html.replace("Revenue Growth", "Execution Time")
    html = html.replace("Comparative analysis vs. last fiscal month", "Time taken by each test module")
    
    # Replace Table Title
    html = html.replace("Recent Transactions", "Test Details")
    
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
            badge_class = "bg-surface-container-high text-on-surface-variant border-outline-variant/30"
            
        test_duration = test.get("setup", {}).get("duration", 0) + test.get("call", {}).get("duration", 0) + test.get("teardown", {}).get("duration", 0)
        
        row = f'''
        <tr class="hover:bg-surface-container-low/50 transition-colors group">
            <td class="px-section-margin py-gutter font-label-md text-on-surface font-semibold">{nodeid.split('::')[-1]}</td>
            <td class="px-gutter py-gutter font-body-md text-on-surface">{nodeid.split('::')[0]}</td>
            <td class="px-gutter py-gutter font-body-md text-on-surface font-medium">{test_duration:.2f}s</td>
            <td class="px-gutter py-gutter">
                <span class="px-3 py-1 {badge_class} text-[11px] font-bold rounded-full border">{outcome}</span>
            </td>
        </tr>
        '''
        rows_html += row
        
    # We need to replace the entire tbody contents.
    # Find tbody and replace inner
    tbody_pattern = re.compile(r'<tbody[^>]*>.*?</tbody>', re.DOTALL)
    new_tbody = f'<tbody class="divide-y divide-outline-variant/10">{rows_html}</tbody>'
    html = tbody_pattern.sub(lambda m: new_tbody, html)
    
    # Fix table headers
    thead_pattern = re.compile(r'<thead[^>]*>.*?</thead>', re.DOTALL)
    new_thead = '''
    <thead>
        <tr class="bg-surface-container-low/30 border-b border-outline-variant/10">
            <th class="px-section-margin py-gutter font-label-md text-on-surface-variant/60 uppercase tracking-widest">Test Case</th>
            <th class="px-gutter py-gutter font-label-md text-on-surface-variant/60 uppercase tracking-widest">Module</th>
            <th class="px-gutter py-gutter font-label-md text-on-surface-variant/60 uppercase tracking-widest">Duration</th>
            <th class="px-gutter py-gutter font-label-md text-on-surface-variant/60 uppercase tracking-widest">Status</th>
        </tr>
    </thead>
    '''
    html = thead_pattern.sub(lambda m: new_thead, html)
    
    # Save output
    with open(output_html, 'w', encoding='utf-8') as f:
        f.write(html)
        
    print(f"Successfully generated {output_html}")

if __name__ == "__main__":
    generate_dashboard()
