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
    
    # คำแปลภาษาไทยสำหรับ Test Case ต่างๆ
    THAI_DESCRIPTIONS = {
        "test_homepage_load_and_title": "ทดสอบการโหลดหน้าแรกและชื่อเว็บ",
        "test_extract_links": "ทดสอบการดึงลิงก์ทั้งหมดบนหน้าเว็บ",
        "test_e2e_search_journey": "ทดสอบระบบค้นหา",
        "test_accessibility": "ทดสอบการเข้าถึง (Accessibility)",
        "test_language_switch": "ทดสอบการเปลี่ยนภาษา",
        "test_menu_navigation": "ทดสอบการกดเมนู",
        "test_dashboard_ui": "ทดสอบหน้าจอ Dashboard",
        "test_search_function": "ทดสอบฟังก์ชันค้นหา",
        "test_register_button": "ทดสอบปุ่มสมัครสมาชิก",
        "test_search_list_page_loads": "ทดสอบการโหลดหน้ารายการค้นหา",
        "test_content_page_loads": "ทดสอบการโหลดหน้าเนื้อหา",
        "test_mobile_menu_toggle": "ทดสอบปุ่มเมนูบนมือถือ",
        "test_no_broken_links_on_home_page": "ทดสอบลิงก์เสียบนหน้าแรก",
        "test_visual_regression": "ทดสอบความผิดเพี้ยนของ UI (Visual)",
        "test_custom_url_load": "ทดสอบการเปิด URL จากไฟล์ CSV"
    }

    # Generate Table Rows
    rows_html = ""
    for test in data.get("tests", []):
        nodeid = test.get("nodeid", "Unknown")
        outcome = test.get("outcome", "unknown").upper()
        
        # Color based on outcome
        if outcome == "PASSED":
            badge_class = "bg-emerald-50 text-emerald-700 border-emerald-100"
            outcome_th = "ผ่าน (PASSED)"
        elif outcome == "FAILED":
            badge_class = "bg-rose-50 text-rose-700 border-rose-100"
            outcome_th = "ไม่ผ่าน (FAILED)"
        elif outcome == "SKIPPED":
            badge_class = "bg-amber-50 text-amber-700 border-amber-100"
            outcome_th = "ข้าม (SKIPPED)"
        else:
            badge_class = "bg-surface-container-low text-on-surface-variant border-outline-variant/30"
            outcome_th = outcome
            
        test_duration = test.get("setup", {}).get("duration", 0) + test.get("call", {}).get("duration", 0) + test.get("teardown", {}).get("duration", 0)
        
        raw_test_name = nodeid.split('::')[-1]
        base_name_match = re.match(r'([^\[]+)', raw_test_name)
        base_name = base_name_match.group(1) if base_name_match else raw_test_name
        
        thai_desc = THAI_DESCRIPTIONS.get(base_name, "ทดสอบระบบทั่วไป")
        
        param_match = re.search(r'\[(.*)\]', raw_test_name)
        
        target_site_url = "https://uat-frontend.constitutionalcourt.or.th"
        target_site = f'<a href="{target_site_url}" target="_blank" class="text-blue-600 hover:underline font-semibold">เว็บไซต์ศาลรัฐธรรมนูญ</a><br><span class="text-[10px] text-gray-500">{target_site_url}</span>'
        if param_match:
            thai_desc += f" ({param_match.group(1)})"
            if base_name == "test_custom_url_load":
                parts = param_match.group(1).split('-')
                if len(parts) >= 3:
                    desc = parts[1]
                    url_str = "-".join(parts[2:])
                    target_site = f'<a href="{url_str}" target="_blank" class="text-blue-600 hover:underline font-semibold">{desc}</a><br><span class="text-[10px] text-gray-500">{url_str}</span>'
                else:
                    target_site = param_match.group(1)
            
        error_msg = ""
        if outcome == "FAILED":
            call_info = test.get("call", {})
            crash = call_info.get("crash", {})
            message = crash.get("message", "ไม่พบรายละเอียดข้อผิดพลาด")
            message = message.replace('<', '&lt;').replace('>', '&gt;')
            error_msg = f'<div class="mt-3 p-3 bg-rose-50 text-rose-700 text-xs rounded-lg border border-rose-100 whitespace-pre-wrap font-mono overflow-x-auto shadow-inner"><strong class="font-bold">สาเหตุที่พัง:</strong><br>{message}</div>'
        
        row = f'''
        <tr class="hover:bg-surface/50 transition-colors group border-b border-outline-variant/10">
            <td class="px-6 py-4">
                <div class="text-sm font-semibold text-on-surface">{thai_desc}</div>
                <div class="text-xs text-on-surface-variant mt-1 opacity-70">{raw_test_name}</div>
                {error_msg}
            </td>
            <td class="px-6 py-4 text-sm text-on-surface leading-snug">{target_site}</td>
            <td class="px-6 py-4 text-sm text-on-surface">{nodeid.split('::')[0]}</td>
            <td class="px-6 py-4 text-sm text-on-surface font-medium">{test_duration:.2f}s</td>
            <td class="px-6 py-4">
                <span class="px-3 py-1 {badge_class} text-xs font-bold rounded-lg border">{outcome_th}</span>
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
