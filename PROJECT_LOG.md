# Projekt-Log: CV Tailoring System

**Datum:** 25. Februar 2026

## Erreichtes

Heute haben wir den Grundstein gelegt, um deinen Lebenslauf (`cv.xtx`, basierend auf dem Deedy-Resume-Reversed Template) dynamisch auf spezifische Stellenanzeigen zuzuschneiden.

### Phase 1: Analyse & Namensanpassung

- **Projektverständnis:** Komplette Analyse deines XeLaTeX-Lebenslaufs und des Tech-Stacks (Frontend, Vue.js, TypeScript, DevOps).
- **Namenskorrektur:** Vorname von "Nimaa" auf "Nima" und Nachname von "Mir Marashi" auf "Marashi" geändert (Datei: `cv.xtx`).
- **Foto-Update:** Das Profilbild wurde auf `Flux2_00041_.jpg` aktualisiert.

### Phase 2: Strategie-Architektur (Multi-Agenten-System)

- **Konzept:** Wir haben ein System evaluiert, um den CV via KI (Orchestrator, HR Consultant, Tech Expert) auf Jobs anzupassen.
- **Constraints (Sehr wichtig für die Zukunft):**
  - Das Layout darf **auf keinen Fall** kaputt gehen.
  - Es darf **keinen Text-Overflow** (Umbrüche auf eine zweite Seite) geben. Text-Limits der Original-Einträge müssen strikt respektiert werden.

### Phase 3: Direkte Ausführung & Workflow-Bestätigung (BKA)

- **Workflow Pivot:** Wir haben entschieden, dass anstelle eines aufwändigen, lokalen Python/CrewAI-Skripts (mit kompliziertem Dependency-Management und API-Key Handling), **ich als dein KI-Assistent** direkt die Rollen der Agenten einnehme. Das ist robuster und deutlich schneller.
- **Test-Run "BKA (Senior) Softwareentwickler":**
  - Stellenanzeige (PDF) über `pdftotext` analysiert.
  - Deinen CV auf die BKA-Stelle zugeschnitten (Fokus-Shift von reinem Frontend auf Fullstack-Engineering, TDD, Agile Methoden, Architektur und Systematische Fehlerbehandlung).
  - `cv.xtx` erfolgreich per XeLaTeX zu `cv.pdf` kompiliert.
- **Sauberer Abschluss:** Die Änderungen (CV-Schnitt auf BKA inkl. PDF) wurden im Git-Repository commitet (`feat(cv): Tailor CV for BKA Software Developer role`).

## Wie wir beim nächsten Mal weitermachen

Dieser Log dient als Startpunkt für unsere nächste Sitzung.

**Wenn du morgen weiterarbeiten willst:**

1. **Neue Stelle:** Gib mir einfach den Link oder lade das PDF der nächsten Stellenbeschreibung hoch.
2. **Prompt (Beispiel):** _"Hier ist eine neue Stellenanzeige: [Link/Datei]. Bitte pass die Inhalte der `\item`-Blocks im `cv.xtx` genauso an wie gestern für das BKA. Beachte strikt die Textlängen-Limits, pass die Keywords an den neuen Stack an und kompiliere mir das PDF."_

Das System steht und der Workflow via direktem KI-Eingriff ist etabliert und einsatzbereit!
