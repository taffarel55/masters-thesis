[← Back to Qualification](../README.md)

# 2. Screening Process

This step documents the **screening phase** of the Systematic Literature Review. Following the PRISMA methodology, the raw search results obtained in Step 1 were evaluated based on title, abstract, and keywords to determine their relevance to the research questions.

The primary goal was to filter out entries that did not meet the specific intersection of **Radar**, **AI**, and **UAV/Aviation** contexts.

### 📂 File Structure

- **`screened.bib`**: The filtered BibTeX file containing only the studies that passed the screening criteria and will proceed to the full-text review or extraction phase.
- **`reasons_removed.txt`**: A raw log of specific reasons and topics excluded during the manual review.

### 🛑 Exclusion Criteria

Records were excluded if they failed to meet the guiding questions: _Does it use Radar? Does it use AI? Is it in an Aeronautical context?_

Major reasons for exclusion included:

#### 1. Out of Scope (Domain)

- **Marine/Maritime:** Ship detection, sea targets.
- **Space:** Satellite operations, space debris, space-borne radars.
- **Environmental/Urban:** Deforestation, oil spill detection, building damage assessment, urban modeling.

#### 2. Technology Mismatch

- **Non-Radar:** Approaches relying solely on Optical/RGB Cameras, Infrared Thermography, or Lidar (unless fused with Radar).
- **Non-AI:** Purely deterministic or traditional signal processing methods without Machine Learning/Deep Learning components.

#### 3. Application Mismatch

- **Path/Trajectory Planning:** Papers focused solely on path optimization without the active detection component.
- **Counter-UAS:** Systems designed for _security_ (detecting intruding drones from ground) rather than _safety_ (onboard collision avoidance).
- **Cooperative Systems:** Approaches relying on communication between vehicles rather than active sensing.
- **Search and Rescue:** Focus on finding ground targets/victims rather than aerial obstacle avoidance.

> **Note:** Some articles were excluded because, despite containing relevant keywords (e.g., "target detection"), their actual application context was distinct (e.g., detecting landmines or ground monitoring).
