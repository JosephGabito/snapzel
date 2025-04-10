from openai import OpenAI

class HTMLGenerator:
    def __init__(self, md_contents, model="gpt-4o", theme="light", use_tailwind=False):
        self.model = model
        self.theme = theme
        self.use_tailwind = use_tailwind

        self.__starter_template = f"""
Use the following HTML structure as inspiration. Adapt the content, but preserve the layout and design quality:

<html>
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />

    <!-- Google Fonts -->
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">

    <!-- Font Awesome Free -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css" integrity="sha512-..." crossorigin="anonymous" referrerpolicy="no-referrer" />

    {"<script src='https://cdn.tailwindcss.com'></script>" if self.use_tailwind else ""}

    <style>
      :root {{
        --bg: {{"#ffffff" if theme == "light" else "#0f172a"}};
        --text: {{"#1a1a1a" if theme == "light" else "#f8fafc"}};
        --card-bg: {{"#ffffff" if theme == "light" else "#1e293b"}};
      }}

      body {{
        font-family: 'Inter', sans-serif;
        background-color: var(--bg);
        color: var(--text);
        margin: 0;
        padding: 0;
        line-height: 1.6;
        transition: background 0.3s ease, color 0.3s ease;
      }}

      header {{
        background: linear-gradient(135deg, #4f46e5, #6366f1);
        color: white;
        padding: 60px 20px;
        text-align: center;
        position: relative;
      }}

      .theme-toggle {{
        position: absolute;
        top: 20px;
        right: 20px;
        background: rgba(255,255,255,0.1);
        border: 1px solid rgba(255,255,255,0.3);
        color: white;
        padding: 8px 12px;
        border-radius: 8px;
        cursor: pointer;
        font-size: 14px;
        display: flex;
        align-items: center;
        gap: 6px;
      }}

      section {{
        background: var(--card-bg);
        padding: 30px;
        margin: 30px auto;
        max-width: 800px;
        border-radius: 16px;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.05);
      }}

      footer {{
        text-align: center;
        font-size: 14px;
        padding: 40px 20px;
        opacity: 0.6;
      }}

      .image-placeholder {{
        width: 100%;
        height: 200px;
        border-radius: 12px;
        margin-top: 20px;
        background-image: url('https://placehold.co/400x200');
        background-size: cover;
        background-position: center;
      }}
    </style>

    <script>
      function toggleTheme() {{
        const root = document.documentElement;
        const current = root.style.getPropertyValue('--bg');
        const isLight = current === '#ffffff';
        root.style.setProperty('--bg', isLight ? '#0f172a' : '#ffffff');
        root.style.setProperty('--text', isLight ? '#f8fafc' : '#1a1a1a');
        root.style.setProperty('--card-bg', isLight ? '#1e293b' : '#ffffff');
      }}
    </script>
  </head>
  <body>
    <header>
      <h1>Title</h1>
      <p>Subtitle</p>
      <button class="theme-toggle" onclick="toggleTheme()">
        <i class="fas fa-adjust"></i> Toggle Theme
      </button>
    </header>
    <main>
      <section>
        <h2>Section Title</h2>
        <p>Section content...</p>
        <div class="image-placeholder"></div>
        <p><i class="fas fa-rocket"></i> Font Awesome Icon Example</p>
      </section>
    </main>
    <footer>
      <p><i class="fas fa-code"></i> Made with love by (company name here...)</p>
    </footer>
  </body>
</html>
"""

        self.__system_prompt = f"""
You are a senior front-end developer and designer. Convert the Markdown into a clean, modern SaaS-style landing page like Vercel or Clerk. Each section should have a good spacing between them.

Use semantic HTML5 and embedded CSS. Include Google Fonts (Use applicable Google dont). Apply grid or flexbox, soft shadows, rounded cards, and spacing. Include a header, footer, and visually distinct sections.

Replace emojis with appropriate Font Awesome icons (e.g. use <i class='fas fa-users'></i> for team, <i class='fas fa-laugh'></i> for fun, <i class='fas fa-briefcase'></i> for careers, etc.).
Use Font Awesome Free icons for things like features, testimonials, social links, or buttons.
Use https://placehold.co instead of via.placeholder.com for image placeholders.

Use the design structure and layout pattern shown below as your base:

{self.__starter_template}

Output only a single valid HTML page. No comments, explanations, or extra content.
"""

        self.__user_prompt = f"""
Convert the following Markdown into a beautifully designed landing page that feels like Vercel, Clerk, or Linear.

Replace all emojis with matching Font Awesome Free icons.
Use spacing and typography to make the layout elegant.

Markdown:
{md_contents}
"""

    def generate_landing_page_html(self):
        print("Generating landing page")
        client = OpenAI()
        response = client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": self.__system_prompt},
                {"role": "user", "content": self.__user_prompt}
            ],
        )
        result = response.choices[0].message.content
        return self.strip_code_fence(result)

    def strip_code_fence(self, content: str) -> str:
        lines = content.strip().splitlines()
        if lines[0].startswith("```") and lines[-1].startswith("```"):
            return "\n".join(lines[1:-1])
        return content.strip()

    def save_html(self, html: str, path="output.html"):
        with open(path, "w", encoding="utf-8") as f:
            f.write(html)
