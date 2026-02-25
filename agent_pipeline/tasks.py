from pydantic import BaseModel, Field
import os
from jinja2 import Environment, FileSystemLoader

class CVContent(BaseModel):
    hoomit_bullets: str = Field(description="The updated bullet points for the Hoom-IT experience. Absolute maximum: 275 characters.", max_length=275)
    sugargang_bullets: str = Field(description="The updated bullet points for the Sugargang experience. Absolute maximum: 400 characters.", max_length=400)
    igus_bullets: str = Field(description="The updated bullet points for the Igus experience. Absolute maximum: 220 characters.", max_length=220)
    stock_bullets: str = Field(description="The updated bullet points for the Stock-Manager project. Absolute maximum: 360 characters.", max_length=360)

def render_cv(content: CVContent) -> str:
    \"\"\"Reads the Jinja2 LaTeX template, injects content, and saves as cv.xtx in the root.\"\"\"
    
    # 1. Setup Jinja Environment
    # Use custom delimiters so it doesn't break LaTeX syntax like { }
    env = Environment(
        loader=FileSystemLoader(searchpath="./templates"),
        block_start_string='[%',
        block_end_string='%]',
        variable_start_string='{{',
        variable_end_string='}}',
        comment_start_string='[#',
        comment_end_string='#]',
    )
    
    template = env.get_template("cv_base.xtx.jinja")
    
    # 2. Render Template
    rendered_latex = template.render(
        hoomit_bullets=content.hoomit_bullets,
        sugargang_bullets=content.sugargang_bullets,
        igus_bullets=content.igus_bullets,
        stock_bullets=content.stock_bullets
    )
    
    # 3. Save to output file (overwriting the root cv.xtx)
    output_filepath = "../cv.xtx"
    with open(output_filepath, "w", encoding="utf-8") as f:
        f.write(rendered_latex)
        
    return output_filepath
