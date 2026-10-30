import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches

os.makedirs("paper/figures", exist_ok=True)

# Set global matplotlib parameters for clean academic look
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman', 'DejaVu Serif', 'Liberation Serif', 'serif']
plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams['font.size'] = 7.5

def save_fig(fig, filename_base):
    png_path = f"paper/figures/{filename_base}.png"
    pdf_path = f"paper/figures/{filename_base}.pdf"
    fig.savefig(png_path, dpi=300, bbox_inches='tight', pad_inches=0.04)
    fig.savefig(pdf_path, bbox_inches='tight', pad_inches=0.04)
    plt.close(fig)
    print(f"Saved {png_path} and {pdf_path}")

# ==========================================
# FIGURE 1: Three-Tier Architecture
# ==========================================
def create_figure1():
    fig, ax = plt.subplots(figsize=(3.38, 3.8))
    ax.axis('off')
    ax.set_xlim(0, 3.38)
    ax.set_ylim(0, 3.8)

    tiers = [
        ("PRESENTATION TIER", 2.65, 1.0, "#E8F0FE", [
            ("React + Vite Frontend (TypeScript + Tailwind)", "Offensive Sandbox | Incident Dashboard | Analytics"),
        ]),
        ("APPLICATION TIER", 1.35, 1.15, "#F8F9FA", [
            ("FastAPI Backend & REST Router", "PhishingSimulationEngine | GeminiSimulationHandler"),
            ("RiskEngine (40% Sem / 25% Beh / 35% URL)", "IncidentManager & ActivityFeedManager"),
        ]),
        ("DATA TIER", 0.15, 1.0, "#E8F0FE", [
            ("SQLite Storage via SQLAlchemy & Alembic", "Tables: simulations, incidents, activity_feed, threat_reports"),
        ])
    ]

    for title, y, h, bg_color, boxes in tiers:
        # Tier Container
        rect = patches.FancyBboxPatch(
            (0.05, y), 3.28, h,
            boxstyle="round,pad=0.02,rounding_size=0.05",
            linewidth=0.8, edgecolor="#212529", facecolor=bg_color
        )
        ax.add_patch(rect)
        ax.text(0.12, y + h - 0.16, title, fontsize=8, fontweight='bold', color='#111827')

        # Sub-boxes
        sub_y = y + h - 0.42
        for box_title, box_sub in boxes:
            sub_rect = patches.FancyBboxPatch(
                (0.15, sub_y - 0.28), 3.08, 0.32,
                boxstyle="square,pad=0",
                linewidth=0.5, edgecolor="#495057", facecolor="#FFFFFF"
            )
            ax.add_patch(sub_rect)
            ax.text(1.69, sub_y - 0.13, box_title, fontsize=7, fontweight='bold', ha='center', va='center')
            ax.text(1.69, sub_y - 0.24, box_sub, fontsize=6.2, ha='center', va='center', color='#495057')
            sub_y -= 0.36

    # Connecting Arrows
    ax.annotate("", xy=(1.69, 2.65), xytext=(1.69, 2.50),
                arrowprops=dict(arrowstyle="<->", lw=0.8, color="#212529"))
    ax.text(1.75, 2.575, "REST / SSE / WebSockets", fontsize=6, va='center')

    ax.annotate("", xy=(1.69, 1.35), xytext=(1.69, 1.15),
                arrowprops=dict(arrowstyle="<->", lw=0.8, color="#212529"))
    ax.text(1.75, 1.25, "SQLAlchemy ORM", fontsize=6, va='center')

    save_fig(fig, "fig1_three_tier_architecture")

# ==========================================
# FIGURE 2: Data Flow Diagram (DFD)
# ==========================================
def create_figure2():
    fig, ax = plt.subplots(figsize=(3.38, 3.8))
    ax.axis('off')
    ax.set_xlim(0, 3.38)
    ax.set_ylim(0, 3.8)

    # External Entities (Rectangles with double side lines or thick borders)
    # Attacker / Admin Simulator (Top Left)
    rect1 = patches.Rectangle((0.1, 3.2), 1.0, 0.45, linewidth=0.8, edgecolor='#000000', facecolor='#FFFFFF')
    ax.add_patch(rect1)
    ax.text(0.6, 3.425, "External Entity:\nSecurity Admin", fontsize=6.5, ha='center', va='center', fontweight='bold')

    # Security Analyst / End User (Top Right)
    rect2 = patches.Rectangle((2.28, 3.2), 1.0, 0.45, linewidth=0.8, edgecolor='#000000', facecolor='#FFFFFF')
    ax.add_patch(rect2)
    ax.text(2.78, 3.425, "External Entity:\nSOC Analyst", fontsize=6.5, ha='center', va='center', fontweight='bold')

    # Process 1.0: Simulation Ingestion
    p1 = patches.FancyBboxPatch((0.1, 2.3), 1.35, 0.5, boxstyle="round,pad=0.03,rounding_size=0.1", linewidth=0.8, edgecolor='#000000', facecolor='#F8F9FA')
    ax.add_patch(p1)
    ax.text(0.775, 2.55, "1.0 Simulation\nIngestion & Prompting", fontsize=6.5, ha='center', va='center')

    # Process 2.0: LLM Agent Reasoning
    p2 = patches.FancyBboxPatch((1.93, 2.3), 1.35, 0.5, boxstyle="round,pad=0.03,rounding_size=0.1", linewidth=0.8, edgecolor='#000000', facecolor='#F8F9FA')
    ax.add_patch(p2)
    ax.text(2.605, 2.55, "2.0 Gemini LLM\nAgent Execution", fontsize=6.5, ha='center', va='center')

    # Process 3.0: Risk Engine & Scoring
    p3 = patches.FancyBboxPatch((0.1, 1.3), 1.35, 0.5, boxstyle="round,pad=0.03,rounding_size=0.1", linewidth=0.8, edgecolor='#000000', facecolor='#F8F9FA')
    ax.add_patch(p3)
    ax.text(0.775, 1.55, "3.0 Risk Scoring\n& Classification", fontsize=6.5, ha='center', va='center')

    # Process 4.0: Incident & Telemetry Broadcast
    p4 = patches.FancyBboxPatch((1.93, 1.3), 1.35, 0.5, boxstyle="round,pad=0.03,rounding_size=0.1", linewidth=0.8, edgecolor='#000000', facecolor='#F8F9FA')
    ax.add_patch(p4)
    ax.text(2.605, 1.55, "4.0 Telemetry &\nWebSocket Broadcast", fontsize=6.5, ha='center', va='center')

    # Data Store D1: SQLite Database
    ds1 = patches.Rectangle((0.7, 0.3), 1.98, 0.4, linewidth=0.8, edgecolor='#000000', facecolor='#E8F0FE')
    ax.add_patch(ds1)
    ax.plot([0.7, 0.7], [0.3, 0.7], color='#000000', lw=1.2)
    ax.plot([0.9, 0.9], [0.3, 0.7], color='#000000', lw=0.8)
    ax.text(1.79, 0.5, "D1  SQLite Datastore (simulations, incidents, feed)", fontsize=6.5, ha='center', va='center', fontweight='bold')

    # Data Flow Arrows
    ax.annotate("", xy=(0.6, 2.8), xytext=(0.6, 3.2), arrowprops=dict(arrowstyle="->", lw=0.8, color='#000000'))
    ax.text(0.62, 3.0, "Payload", fontsize=5.8)

    ax.annotate("", xy=(1.93, 2.55), xytext=(1.45, 2.55), arrowprops=dict(arrowstyle="->", lw=0.8, color='#000000'))
    ax.text(1.69, 2.62, "Prompt", fontsize=5.8, ha='center')

    ax.annotate("", xy=(0.775, 1.8), xytext=(2.605, 2.3), arrowprops=dict(arrowstyle="->", lw=0.8, color='#000000'))
    ax.text(1.69, 2.1, "Reasoning & Tag", fontsize=5.8, ha='center')

    ax.annotate("", xy=(1.93, 1.55), xytext=(1.45, 1.55), arrowprops=dict(arrowstyle="->", lw=0.8, color='#000000'))
    ax.text(1.69, 1.62, "Score", fontsize=5.8, ha='center')

    ax.annotate("", xy=(2.78, 3.2), xytext=(2.605, 1.8), arrowprops=dict(arrowstyle="->", lw=0.8, color='#000000'))
    ax.text(2.82, 2.5, "WS Stream", fontsize=5.8)

    ax.annotate("", xy=(1.69, 0.7), xytext=(1.69, 1.3), arrowprops=dict(arrowstyle="->", lw=0.8, color='#000000'))
    ax.text(1.73, 1.0, "Persist Records", fontsize=5.8)

    save_fig(fig, "fig2_data_flow_diagram")

# ==========================================
# FIGURE 3: Use Case Diagram
# ==========================================
def create_figure3():
    fig, ax = plt.subplots(figsize=(3.38, 3.8))
    ax.axis('off')
    ax.set_xlim(0, 3.38)
    ax.set_ylim(0, 3.8)

    # System boundary box
    sys_box = patches.Rectangle((0.85, 0.1), 1.68, 3.6, linewidth=0.8, edgecolor='#000000', facecolor='#F8F9FA')
    ax.add_patch(sys_box)
    ax.text(1.69, 3.56, "SemanticShield AI System Boundary", fontsize=7, ha='center', va='center', fontweight='bold')

    use_cases = [
        ("UC1: Execute Phishing Simulation", 3.1),
        ("UC2: Select Behavioral Profile", 2.5),
        ("UC3: Stream LLM Reasoning", 1.9),
        ("UC4: Calculate Composite Risk", 1.3),
        ("UC5: Manage Incidents & Feed", 0.7),
    ]

    uc_centers = {}
    for uc_text, y in use_cases:
        ellipse = patches.Ellipse((1.69, y), 1.5, 0.42, linewidth=0.8, edgecolor='#212529', facecolor='#FFFFFF')
        ax.add_patch(ellipse)
        ax.text(1.69, y, uc_text, fontsize=6.2, ha='center', va='center')
        uc_centers[uc_text[:3]] = (1.69, y)

    # Actors
    # Actor 1: Security Analyst/Admin (Left)
    ax.plot([0.35], [2.8], 'o', ms=8, color='#000000') # head
    ax.plot([0.35, 0.35], [2.7, 2.3], color='#000000', lw=1.2) # body
    ax.plot([0.2, 0.5], [2.55, 2.55], color='#000000', lw=1.2) # arms
    ax.plot([0.2, 0.35, 0.5], [2.05, 2.3, 2.05], color='#000000', lw=1.2) # legs
    ax.text(0.35, 1.9, "Security Admin /\nSOC Analyst", fontsize=6.5, ha='center', va='top', fontweight='bold')

    # Actor 2: AI Agent (Right Top)
    ax.plot([3.03], [3.0], 'o', ms=8, color='#000000')
    ax.plot([3.03, 3.03], [2.9, 2.5], color='#000000', lw=1.2)
    ax.plot([2.88, 3.18], [2.75, 2.75], color='#000000', lw=1.2)
    ax.plot([2.88, 3.03, 3.18], [2.25, 2.5, 2.25], color='#000000', lw=1.2)
    ax.text(3.03, 2.1, "Gemini AI\nAgent", fontsize=6.5, ha='center', va='top', fontweight='bold')

    # Actor 3: Employee / End User (Right Bottom)
    ax.plot([3.03], [1.1], 'o', ms=8, color='#000000')
    ax.plot([3.03, 3.03], [1.0, 0.6], color='#000000', lw=1.2)
    ax.plot([2.88, 3.18], [0.85, 0.85], color='#000000', lw=1.2)
    ax.plot([2.88, 3.03, 3.18], [0.35, 0.6, 0.35], color='#000000', lw=1.2)
    ax.text(3.03, 0.2, "Simulated\nEmployee", fontsize=6.5, ha='center', va='top', fontweight='bold')

    # Lines connecting Actors to Use Cases
    # Admin -> UC1, UC2, UC5
    ax.plot([0.45, 0.94], [2.55, 3.1], color='#000000', lw=0.6)
    ax.plot([0.45, 0.94], [2.55, 2.5], color='#000000', lw=0.6)
    ax.plot([0.45, 0.94], [2.35, 0.7], color='#000000', lw=0.6)

    # AI Agent -> UC3
    ax.plot([2.88, 2.44], [2.65, 1.9], color='#000000', lw=0.6)

    # Simulated Employee -> UC2
    ax.plot([2.88, 2.44], [0.75, 2.5], color='#000000', lw=0.6)

    save_fig(fig, "fig3_use_case_diagram")

# ==========================================
# FIGURE 4: Sequence Diagram
# ==========================================
def create_figure4():
    fig, ax = plt.subplots(figsize=(3.38, 4.0))
    ax.axis('off')
    ax.set_xlim(0, 3.38)
    ax.set_ylim(0, 4.0)

    lifelines = [
        ("Simulator", 0.35),
        ("FastAPI", 1.02),
        ("PhishEngine", 1.69),
        ("GeminiLLM", 2.36),
        ("SQLiteDB", 3.03),
    ]

    # Draw Lifeline Headers & Vertical Dashed Lines
    for name, x in lifelines:
        box = patches.Rectangle((x - 0.28, 3.65), 0.56, 0.3, linewidth=0.8, edgecolor='#000000', facecolor='#F8F9FA')
        ax.add_patch(box)
        ax.text(x, 3.8, name, fontsize=6.5, ha='center', va='center', fontweight='bold')
        ax.plot([x, x], [0.3, 3.65], color='#888888', linestyle='--', linewidth=0.7)

    # Sequence Messages
    messages = [
        (3.4, 0.35, 1.02, "1. POST /simulate"),
        (3.05, 1.02, 1.69, "2. execute_simulation()"),
        (2.7, 1.69, 2.36, "3. stream_response()"),
        (2.35, 2.36, 1.69, "4. reasoning + [VULNERABLE]"),
        (2.0, 1.69, 1.69, "5. calculate_risk() [84]"), # Self call
        (1.65, 1.69, 3.03, "6. persist_simulation()"),
        (1.3, 1.69, 1.02, "7. PhishingSimulationResponse"),
        (0.95, 1.02, 0.35, "8. SSE / JSON Stream"),
    ]

    for y, x1, x2, msg in messages:
        if x1 == x2: # Self call
            ax.annotate("", xy=(x1 + 0.25, y - 0.15), xytext=(x1, y),
                        arrowprops=dict(arrowstyle="->", lw=0.7, color='#000000', connectionstyle="arc3,rad=-0.5"))
            ax.text(x1 + 0.28, y - 0.08, msg, fontsize=5.8, va='center')
        else:
            style = "->" if x1 < x2 else "<-"
            ax.annotate("", xy=(x2, y), xytext=(x1, y),
                        arrowprops=dict(arrowstyle=style, lw=0.7, color='#000000', linestyle='--' if x1 > x2 else '-'))
            mid_x = (x1 + x2) / 2.0
            ax.text(mid_x, y + 0.06, msg, fontsize=5.8, ha='center', va='bottom')

    save_fig(fig, "fig4_sequence_diagram")

# ==========================================
# FIGURE 5: Class Model
# ==========================================
def create_figure5():
    fig, ax = plt.subplots(figsize=(3.38, 3.8))
    ax.axis('off')
    ax.set_xlim(0, 3.38)
    ax.set_ylim(0, 3.8)

    classes = [
        ("DBSimulation", 0.1, 2.2, 1.45, 1.4, [
            "+ simulation_id: String",
            "+ scenario_type: String",
            "+ behavior_profile: String",
            "+ agent_decision: String",
            "+ risk_score: Integer",
            "+ duration_seconds: Float",
        ]),
        ("DBIncident", 1.83, 2.2, 1.45, 1.4, [
            "+ incident_id: String",
            "+ title: String",
            "+ severity: String",
            "+ risk_score: Integer",
            "+ is_simulation: Boolean",
            "+ status: String",
        ]),
        ("RiskEngine", 0.1, 0.3, 1.45, 1.4, [
            "- WEIGHTS: Dict",
            "+ calculate_risk()",
            "+ apply_overrides()",
            "+ classify_severity()",
        ]),
        ("AgentResponsePayload", 1.83, 0.3, 1.45, 1.4, [
            "+ agent_name: String",
            "+ threat_score: Float",
            "+ confidence: Float",
            "+ detected_signals: List",
            "+ flags: Dict",
        ]),
    ]

    for name, x, y, w, h, members in classes:
        # Class box
        box = patches.Rectangle((x, y), w, h, linewidth=0.8, edgecolor='#000000', facecolor='#FFFFFF')
        ax.add_patch(box)
        # Header box
        hdr = patches.Rectangle((x, y + h - 0.3), w, 0.3, linewidth=0.8, edgecolor='#000000', facecolor='#F8F9FA')
        ax.add_patch(hdr)
        ax.text(x + w/2.0, y + h - 0.15, name, fontsize=7, ha='center', va='center', fontweight='bold')

        # Line separator
        ax.plot([x, x + w], [y + h - 0.3, y + h - 0.3], color='#000000', lw=0.8)

        # Members
        mem_y = y + h - 0.45
        for m in members:
            ax.text(x + 0.05, mem_y, m, fontsize=5.8, va='center')
            mem_y -= 0.16

    # Relationships
    # DBSimulation -> DBIncident (1 to 0..1)
    ax.annotate("", xy=(1.83, 2.9), xytext=(1.55, 2.9),
                arrowprops=dict(arrowstyle="->", lw=0.8, color='#000000'))
    ax.text(1.69, 2.96, "creates >", fontsize=5.8, ha='center')

    # RiskEngine -> AgentResponsePayload (uses)
    ax.annotate("", xy=(1.83, 1.0), xytext=(1.55, 1.0),
                arrowprops=dict(arrowstyle="->", lw=0.8, color='#000000'))
    ax.text(1.69, 1.06, "processes >", fontsize=5.8, ha='center')

    # RiskEngine -> DBSimulation (evaluates)
    ax.annotate("", xy=(0.825, 2.2), xytext=(0.825, 1.7),
                arrowprops=dict(arrowstyle="->", lw=0.8, color='#000000'))
    ax.text(0.88, 1.95, "scores", fontsize=5.8)

    save_fig(fig, "fig5_class_diagram")

# ==========================================
# FIGURE 6: Activity Diagram
# ==========================================
def create_figure6():
    fig, ax = plt.subplots(figsize=(3.38, 4.0))
    ax.axis('off')
    ax.set_xlim(0, 3.38)
    ax.set_ylim(0, 4.0)

    # Initial Node (Filled black circle)
    ax.plot([1.69], [3.85], 'o', ms=9, color='#000000')

    activities = [
        ("Validate Simulation Request", 3.4),
        ("Select Behavioral System Prompt", 2.9),
        ("Stream Reasoning via Gemini LLM", 2.4),
        ("Extract [VULNERABLE] or [SAFE] Tag", 1.9),
        ("Calculate Composite Risk Score", 1.4),
        ("Create Incident & Broadcast WS", 0.9),
        ("Persist Record in SQLite Datastore", 0.4),
    ]

    for title, y in activities:
        box = patches.FancyBboxPatch(
            (0.44, y - 0.15), 2.5, 0.3,
            boxstyle="round,pad=0.02,rounding_size=0.08",
            linewidth=0.8, edgecolor='#000000', facecolor='#F8F9FA'
        )
        ax.add_patch(box)
        ax.text(1.69, y, title, fontsize=6.5, ha='center', va='center')

    # Connecting Arrows
    ax.annotate("", xy=(1.69, 3.55), xytext=(1.69, 3.8), arrowprops=dict(arrowstyle="->", lw=0.8, color='#000000'))
    ax.annotate("", xy=(1.69, 3.05), xytext=(1.69, 3.25), arrowprops=dict(arrowstyle="->", lw=0.8, color='#000000'))
    ax.annotate("", xy=(1.69, 2.55), xytext=(1.69, 2.75), arrowprops=dict(arrowstyle="->", lw=0.8, color='#000000'))
    ax.annotate("", xy=(1.69, 2.05), xytext=(1.69, 2.25), arrowprops=dict(arrowstyle="->", lw=0.8, color='#000000'))
    ax.annotate("", xy=(1.69, 1.55), xytext=(1.69, 1.75), arrowprops=dict(arrowstyle="->", lw=0.8, color='#000000'))
    ax.annotate("", xy=(1.69, 1.05), xytext=(1.69, 1.25), arrowprops=dict(arrowstyle="->", lw=0.8, color='#000000'))
    ax.annotate("", xy=(1.69, 0.55), xytext=(1.69, 0.75), arrowprops=dict(arrowstyle="->", lw=0.8, color='#000000'))

    # Final Node (Circled black dot)
    ax.plot([1.69], [0.15], 'o', ms=9, color='#000000', mfc='none', mew=1.2)
    ax.plot([1.69], [0.15], 'o', ms=5, color='#000000')
    ax.annotate("", xy=(1.69, 0.22), xytext=(1.69, 0.25), arrowprops=dict(arrowstyle="->", lw=0.8, color='#000000'))

    save_fig(fig, "fig6_activity_diagram")

if __name__ == "__main__":
    create_figure1()
    create_figure2()
    create_figure3()
    create_figure4()
    create_figure5()
    create_figure6()
    print("All 6 diagrams generated successfully!")
