import os
import argparse
from crewai import Agent, Task, Crew, Process
from tasks import CVContent, render_cv
from tools.latex_compiler import compile_latex
from dotenv import load_dotenv

load_dotenv()

# --- 1. Agents ---

orchestrator = Agent(
    role="Lead CV Orchestrator",
    goal="Coordinate the tailoring of the Developer CV to match the Job Description and ensure ZERO formatting/LaTeX breakage.",
    backstory="You are a meticulous Project Manager. You enforce strict rules: NEVER exceed character limits, and ALWAYS output valid JSON for the LaTeX template.",
    verbose=True,
    allow_delegation=True
)

hr_consultant = Agent(
    role="Elite IT Career Consultant",
    goal="Extract the true technical and cultural requirements from the Job Description and provide a Strategy Briefing.",
    backstory="As an elite Silicon Valley tech recruiter, you know exactly what hiring managers look for. You read between the lines to find implicit requirements.",
    verbose=True,
    allow_delegation=False
)

tech_expert = Agent(
    role="Senior Tech Lead & Content Writer",
    goal="Rewrite the CV bullet points to perfectly align with the HR Strategy Briefing and the exact tech stack of the Job Description.",
    backstory="You are a 10x Full-Stack Developer. You translate generic experience into high-impact, keyword-optimized bullet points that pass any ATS.",
    verbose=True,
    allow_delegation=False
)

# --- 2. Tasks ---

def build_crew(job_description: str):
    
    analyze_job_task = Task(
        description=f"Analyze the following Job Description: \n\n{job_description}\n\n1. Identify required hard skills.\n2. Identify desired soft skills.\n3. Create a brief Strategy Mapping of how to position the candidate (A Frontend/DevOps Developer with Vue, React, TS, Python experience).",
        expected_output="A concise 'Strategy Briefing' (bullet points) highlighting what to emphasize in the CV.",
        agent=hr_consultant
    )

    rewrite_cv_task = Task(
        description="""Using the Strategy Briefing from the Consultant, rewrite the developer's experience bullet points.
        
        CRITICAL CONSTRAINTS:
        - You must output exactly the 4 fields required by the CVContent JSON schema.
        - Start every single point with EXACTLY `\\item `.
        - Do NOT exceed the character limits specified in the schema. Check your lengths!
        - Keep the original meaning but swap terminology to match the job description where truthful.
        
        Original Hoom-IT (Limit: 275 chars):
        \\item Erstellung intuitiver, responsiver Vue.js UI-Komponenten (Dialoge etc.) nach Google MD3.
        \\item Erstellung eines generischen Storemanagements mittels TypeScript/Pinia -> bessere Wartung und Erweiterung der Anwendung.
        \\item Einbindung von Authentifizierung per REST und Erstellung von automatisierte Testfälle (Unit-Tests) für mehr Codequalität.
        
        Original Sugargang (Limit: 400 chars):
        \\item Maßgeschneiderte, interaktive Slides für diverse Webshop-Bereiche via Shopify Liquid, JavaScript, HTML & CSS; Demo-Integration im Shopify-Umfeld zur UX-Testung.
        \\item Erstellung eines Grid-Layouts zur verbesserten, responsiveren Darstellung der Abo-Box-Cards.
        \\item Einbidung des Shopify-CLI und Versionskontrollsystem Git zur besseren Verwaltung und Wartung der WebPages zu vorher.
        \\item Konzeptionierung des UX und Digital-Commerce in agiler Zusammenarbeit mit dem Design-Team.
        
        Original Igus (Limit: 220 chars):
        \\item Durchführung präziser Qualitätsprüfungen: Sicherstellung der Maßhaltigkeit und weiterer qualitativer Eigenschaften vor Kundenkommissionierung.
        \\item Fundierte Einarbeitung in die Igus-Produktpalette mittels Katalog zur Gewährleistung der Qualitätsanforderungen.
        
        Original Stock-Manager (Limit: 360 chars):
        \\item Saubere Integration der REST Schnittstellen mittels des Axios-Clients und Authentifizierung mit Credentials und JWT.
        \\item Entwurf zur Umsetzung mit UML-Diagramme, ... Erstellung eines Testfall-Katalogs für manuelles Testing.
        \\item Anforderungsermittlung mittels Mind-Mapping und in agiler Absprache mit dem Backend-Developer.
        \\item Projektplanung und -einrichtung anhand der ermittelten User-Stories.
        """,
        expected_output="A JSON object matching the CVContent Pydantic model containing the rewritten bullet points.",
        agent=tech_expert,
        output_json=CVContent
    )

    return Crew(
        agents=[hr_consultant, tech_expert, orchestrator],
        tasks=[analyze_job_task, rewrite_cv_task],
        process=Process.sequential,
        verbose=True
    )

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Tailor CV to Job Description")
    parser.add_argument("job", help="The Job Description text or core requirements.")
    args = parser.parse_args()

    print("🚀 Starting CV Tailor Agents...")
    crew = build_crew(args.job)
    
    # 1. Run the LLM Agents
    result = crew.kickoff()
    
    # 2. Extract JSON and run Jinja templating
    # Note: In CrewAI latest versions, task output is mapped well if the LLM followed schema
    try:
        final_task = crew.tasks[-1]
        if hasattr(final_task.output, 'json_dict') and isinstance(final_task.output.json_dict, dict):
            content = CVContent(**final_task.output.json_dict)
        else:
            # Fallback if raw dict isn't perfect
            import json
            content = CVContent.model_validate_json(final_task.output.raw_output)
            
        print("✅ LLM Output successfully parsed.")
        
        # 3. Render into LaTeX
        print("📝 Injecting into LaTeX Template...")
        output_path = render_cv(content)
        
        # 4. Compile PDF
        print(f"⚙️ Compiling PDF at {output_path}...")
        compile_msg = compile_latex()
        print(compile_msg)
        
    except Exception as e:
        print(f"❌ Error processing result parsing/compiling: {e}")
        print("Raw Output was:")
        print(crew.tasks[-1].output)
