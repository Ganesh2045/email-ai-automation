from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import gspread
from config import SHEET_NAME
import re

app = Flask(__name__, template_folder="templates", static_folder="static")
CORS(app)

# Initialize Google Sheets client
gc = gspread.service_account(filename="service_account.json")
sheet = gc.open(SHEET_NAME).sheet1

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/tasks", methods=["GET"])
def get_tasks():
    try:
        rows = sheet.get_all_values()
        
        # Check if first row is header
        start_idx = 1
        if rows and len(rows[0]) > 0:
            val0 = rows[0][0].lower()
            val1 = rows[0][1].lower() if len(rows[0]) > 1 else ""
            if "task" in val0 or "status" in val1:
                start_idx = 2
                
        tasks = []
        for idx, row in enumerate(rows[start_idx-1:], start=start_idx):
            if not row or len(row) < 1:
                continue
            task_text = row[0].strip()
            if not task_text:
                continue
            status = row[1].strip() if len(row) > 1 else "Pending"
            
            # Parse priority
            priority = "MEDIUM"
            title = task_text
            
            # Match priority formats like [HIGH] or [MEDIUM] or [LOW]
            match = re.match(r"^\[(HIGH|MEDIUM|LOW)\]", task_text, re.IGNORECASE)
            if match:
                priority = match.group(1).upper()
                title = task_text[match.end():].strip()
            else:
                # Check for other brackets like [URGENT] or similar
                general_match = re.match(r"^\[(.*?)\]", task_text)
                if general_match:
                    priority = general_match.group(1).upper()
                    title = task_text[general_match.end():].strip()
                    
            tasks.append({
                "id": idx,
                "task_raw": task_text,
                "title": title,
                "priority": priority,
                "status": status
            })
            
        return jsonify({"success": True, "tasks": tasks})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/api/tasks/toggle", methods=["POST"])
def toggle_task():
    try:
        data = request.json or {}
        row_idx = data.get("id")
        task_raw = data.get("task_raw")
        
        if not row_idx or not task_raw:
            return jsonify({"success": False, "error": "ID and task_raw are required"}), 400
            
        # Try direct access by index first
        try:
            val = sheet.cell(row_idx, 1).value
            if val and val.strip() == task_raw.strip():
                curr_status = sheet.cell(row_idx, 2).value or "Pending"
                new_status = "Completed" if curr_status != "Completed" else "Pending"
                sheet.update_cell(row_idx, 2, new_status)
                return jsonify({"success": True, "new_status": new_status})
        except Exception:
            pass
            
        # Search if index failed or shifted
        col1 = sheet.col_values(1)
        for idx, text in enumerate(col1, start=1):
            if text.strip() == task_raw.strip():
                curr_status = sheet.cell(idx, 2).value or "Pending"
                new_status = "Completed" if curr_status != "Completed" else "Pending"
                sheet.update_cell(idx, 2, new_status)
                return jsonify({"success": True, "new_status": new_status})
                
        return jsonify({"success": False, "error": "Task not found in sheet"}), 404
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/api/tasks/delete", methods=["POST"])
def delete_task():
    try:
        data = request.json or {}
        row_idx = data.get("id")
        task_raw = data.get("task_raw")
        
        if not row_idx or not task_raw:
            return jsonify({"success": False, "error": "ID and task_raw are required"}), 400
            
        # Try direct access first
        try:
            val = sheet.cell(row_idx, 1).value
            if val and val.strip() == task_raw.strip():
                sheet.delete_rows(row_idx)
                return jsonify({"success": True})
        except Exception:
            pass
            
        # Search if index failed or shifted
        col1 = sheet.col_values(1)
        for idx, text in enumerate(col1, start=1):
            if text.strip() == task_raw.strip():
                sheet.delete_rows(idx)
                return jsonify({"success": True})
                
        return jsonify({"success": False, "error": "Task not found in sheet"}), 404
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/api/tasks/add", methods=["POST"])
def add_task():
    try:
        data = request.json or {}
        title = data.get("title", "").strip()
        priority = data.get("priority", "MEDIUM").upper()
        
        if not title:
            return jsonify({"success": False, "error": "Title is required"}), 400
            
        task_raw = f"[{priority}] {title}"
        
        # Check duplicate
        col1 = sheet.col_values(1)
        if task_raw in [t.strip() for t in col1]:
            return jsonify({"success": False, "error": "Task already exists in Google Sheet"}), 400
            
        sheet.append_row([task_raw, "Pending"])
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)
