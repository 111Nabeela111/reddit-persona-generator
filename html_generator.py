def save_as_html_card(persona: str, filename: str):
    import re

    # Define expected field headers (supporting emojis too)
    field_map = {
        "Goals and Needs": "Goals and Needs",
        "🎯 Goals": "Goals and Needs",
        "🎯 Goals and Needs": "Goals and Needs",
        "💡 Interests": "Interests",
        "Interests": "Interests",
        "🧠 Personality Traits": "Personality Traits",
        "Personality Traits": "Personality Traits",
        "🔥 Strengths": "Skills",
        "Strengths": "Skills",
        "Skills": "Skills",
        "😤 Frustrations": "Frustrations",
        "Frustrations": "Frustrations",
        "📌 Behavior": "Behavior",
        "Behavior": "Behavior",
        "Other Unique Traits": "Other Unique Traits",
        "Tone": "Tone",
        "Username": "Username"
    }

    fields = {v: "" for v in set(field_map.values())}
    current = None

    for line in persona.splitlines():
        line = line.strip()
        if not line:
            continue
        matched = False
        for label in field_map:
            if re.match(rf"^{re.escape(label)}\s*[:\-\uff1a]", line):
                current = field_map[label]
                parts = re.split(r"[:\uff1a\-]", line, 1)
                fields[current] = parts[1].strip() if len(parts) > 1 else ""
                matched = True
                break
        if not matched and current:
            fields[current] += " " + line

    def get(key):
        return fields.get(key, "").strip()

    if all(not v.strip() for v in fields.values()):
        html = f"""
        <html><head><title>Reddit Persona</title></head>
        <body><h2>Raw Persona Output</h2><pre>{persona}</pre></body></html>
        """
    else:
        html = f"""
<!DOCTYPE html>
<html lang=\"en\">
<head>
  <meta charset=\"UTF-8\" />
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\" />
  <title>Reddit Persona - {get('Username') or 'User'}</title>
  <link href=\"https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap\" rel=\"stylesheet\">
  <style>
    :root {{
      --bg: #f4f6fa;
      --text: #333;
      --card-bg: #fff;
      --primary: #2c74b3;
      --accent: #e0e0e0;
    }}
    [data-theme='dark'] {{
      --bg: #121212;
      --text: #f0f0f0;
      --card-bg: #1e1e1e;
      --primary: #4a90e2;
      --accent: #444;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      font-family: 'Poppins', sans-serif;
      margin: 0;
      background: var(--bg);
      color: var(--text);
    }}
    .container {{
      max-width: 1200px;
      margin: 2rem auto;
      display: grid;
      grid-template-columns: 1fr 2fr;
      background: var(--card-bg);
      border-radius: 10px;
      overflow: hidden;
      box-shadow: 0 0 15px rgba(0,0,0,0.1);
    }}
    .left {{
      background: var(--primary);
      color: white;
      padding: 2rem;
      display: flex;
      flex-direction: column;
      align-items: center;
    }}
    .left img {{
      border-radius: 50%;
      width: 260px;
      height: 260px;
      object-fit: cover;
      border: 4px solid white;
    }}
    .upload-label {{
      margin-top: 1rem;
      background: white;
      color: var(--primary);
      padding: 0.4rem 1rem;
      border-radius: 20px;
      cursor: pointer;
      font-weight: 600;
    }}
    .info p {{
      margin: 0.8rem 0;
      width: 100%;
    }}
    .info label {{
      display: block;
      margin-bottom: 0.3rem;
      font-weight: bold;
    }}
    .info input[type='text'] {{
      width: 100%;
      padding: 0.4rem;
      border-radius: 6px;
      border: none;
      font-family: 'Poppins', sans-serif;
    }}
    .right {{ padding: 2rem; }}
    .right h2 input {{
      font-size: 1.5rem;
      font-weight: 600;
      border: none;
      background: transparent;
      color: var(--text);
    }}
    .grid {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 1.5rem;
    }}
    .section {{ margin-bottom: 1.5rem; }}
    .section h3 {{
      margin-bottom: 0.3rem;
      color: var(--primary);
    }}
    .section textarea {{
      width: 100%;
      min-height: 60px;
      padding: 0.5rem;
      border-radius: 6px;
      border: 1px solid var(--accent);
      font-family: 'Poppins', sans-serif;
    }}
    blockquote textarea {{
      width: 100%;
      background: #e9f1ff;
      border-left: 4px solid var(--primary);
      padding: 1rem;
      border: none;
      font-style: italic;
    }}
    .actions {{
      text-align: center;
      margin-top: 2rem;
    }}
    .actions button {{
      margin: 0.5rem;
      padding: 0.6rem 1.2rem;
      background: var(--primary);
      color: white;
      border: none;
      border-radius: 6px;
      cursor: pointer;
    }}
  </style>
  <script>
    function updateAvatar(e) {{
      const reader = new FileReader();
      reader.onload = function(event) {{
        localStorage.setItem('avatar', event.target.result);
        document.getElementById('avatar').src = event.target.result;
      }};
      reader.readAsDataURL(e.target.files[0]);
    }}
    function toggleTheme() {{
      const html = document.documentElement;
      if (html.getAttribute('data-theme') === 'dark') {{
        html.removeAttribute('data-theme');
        localStorage.setItem('theme', 'light');
      }} else {{
        html.setAttribute('data-theme', 'dark');
        localStorage.setItem('theme', 'dark');
      }}
    }}
    window.onload = function () {{
      if (localStorage.getItem('theme') === 'dark') {{
        document.documentElement.setAttribute('data-theme', 'dark');
      }}
      const avatar = localStorage.getItem('avatar');
      if (avatar) document.getElementById('avatar').src = avatar;
    }}
  </script>
</head>
<body>
  <div class="container">
    <div class="left">
      <img src="" id="avatar" alt="avatar">
      <label class="upload-label">Upload Avatar<input type="file" accept="image/*" onchange="updateAvatar(event)"></label>
      <div class="info">
        <p><label for="age">Age</label><input type="text" id="age" placeholder="Enter age"></p>
        <p><label for="status">Status</label><input type="text" id="status" placeholder="Enter status"></p>
        <p><label for="location">Location</label><input type="text" id="location" placeholder="Enter location"></p>
        <p><label for="archetype">Archetype</label><input type="text" id="archetype" placeholder="Enter archetype"></p>
      </div>
    </div>
    <div class="right">
      <h2><input type="text" value="{get('Username') or 'Reddit User'}"></h2>
      <blockquote><textarea>{get('Tone')}</textarea></blockquote>
      <div class="grid">
        <div class="section"><h3>Interests</h3><textarea>{get('Interests')}</textarea></div>
        <div class="section"><h3>Goals & Needs</h3><textarea>{get('Goals and Needs')}</textarea></div>
        <div class="section"><h3>Personality</h3><textarea>{get('Personality Traits')}</textarea></div>
        <div class="section"><h3>Behavior</h3><textarea>{get('Behavior')}</textarea></div>
        <div class="section"><h3>Frustrations</h3><textarea>{get('Frustrations')}</textarea></div>
        <div class="section"><h3>Skills</h3><textarea>{get('Skills')}</textarea></div>
        <div class="section" style="grid-column: span 2;"><h3>Other Unique Traits</h3><textarea>{get('Other Unique Traits')}</textarea></div>
      </div>
    </div>
  </div>
  <div class="actions">
    <button onclick="window.print()">🖨️ Print or Save as PDF</button>
    <button onclick="toggleTheme()">🌓 Toggle Light/Dark</button>
  </div>
</body>
</html>
"""

    with open(filename, "w", encoding="utf-8") as f:
        f.write(html)
