import os


def parse_custom_ini(filepath="config.ini"):
    """Reads a simple .ini file (without values) and transforms it into a dictionary of lists."""
    config_dict = {}
    current_section = None
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if line.startswith("[") and line.endswith("]"):
                    current_section = line[1:-1]
                    config_dict[current_section] = []
                elif current_section:
                    config_dict[current_section].append(line)
        return config_dict
    except FileNotFoundError:
        print(
            f"❌ ERROR: File '{filepath}' not found. Create the configuration file before running the script."
        )
        return None


def build_or_group(terms, field_code=""):
    """
    Creates a group of terms (OR), automatically adding quotation marks to phrases or terms containing hyphens.
    """
    if not terms:
        return ""

    formatted_terms = []
    for term in terms:
        term = term.strip()
        # Ensure quotes for terms with spaces or hyphens
        term_to_use = f'"{term}"' if " " in term or "-" in term else term
        formatted_terms.append(term_to_use)

    or_clause = " OR ".join(formatted_terms)

    if field_code:
        return f"{field_code}({or_clause})"
    else:
        return f"({or_clause})"


def generate_queries(config):
    """Main function that generates all queries based on the configuration."""

    # Load all terms from the configuration dictionary
    # NOTE: Ensure your config.ini headers match these keys
    problem_terms = config.get("PROBLEM_CONCEPTS", [])
    tech_terms = config.get("TECHNOLOGY_CONCEPTS", [])
    ai_terms = config.get("AI_CONCEPTS", [])
    domain_terms = config.get("DOMAIN_CONCEPTS", [])
    metadata_exclusion_terms = config.get("METADATA_EXCLUSION", [])
    title_exclusion_terms = config.get("TITLE_EXCLUSION", [])

    combined_exclusion = metadata_exclusion_terms + title_exclusion_terms

    queries = {}

    # --- 1. Query for IEEE Xplore ---
    # IEEE syntax is special and works better with repeated field codes
    def build_ieee_or_group(terms, field_code):
        formatted_terms = []
        for term in terms:
            term = term.strip()
            # Ensure quotes for terms with spaces or hyphens
            term_to_use = f'"{term}"' if " " in term or "-" in term else term
            formatted_terms.append(f"{field_code}{term_to_use}")
        return " OR ".join(formatted_terms)

    ieee_prob = build_ieee_or_group(problem_terms, '"All Metadata":')
    ieee_tech = build_ieee_or_group(tech_terms, '"All Metadata":')
    ieee_ai = build_ieee_or_group(ai_terms, '"All Metadata":')
    ieee_dom = build_ieee_or_group(domain_terms, '"All Metadata":')
    ieee_ex_meta = build_ieee_or_group(metadata_exclusion_terms, '"All Metadata":')
    ieee_ex_title = build_ieee_or_group(title_exclusion_terms, '"Document Title":')

    queries["IEEE.query"] = (
        f"(({ieee_prob}) AND ({ieee_tech}) AND ({ieee_ai}) AND ({ieee_dom})) NOT (({ieee_ex_meta}) OR ({ieee_ex_title}))"
    )

    # --- 2. Query for ACM Digital Library ---
    acm_prob = build_or_group(problem_terms, "fulltext:")
    acm_tech = build_or_group(tech_terms, "fulltext:")
    acm_ai = build_or_group(ai_terms, "fulltext:")
    acm_dom = build_or_group(domain_terms, "fulltext:")
    acm_ex_meta = build_or_group(metadata_exclusion_terms, "fulltext:")
    acm_ex_title = build_or_group(title_exclusion_terms, "acmdlTitle:")

    queries["ACM.query"] = (
        f"({acm_prob} AND {acm_tech} AND {acm_ai} AND {acm_dom}) NOT ({acm_ex_meta} OR {acm_ex_title})"
    )

    # --- 3. Query for Scopus ---
    scopus_prob = build_or_group(problem_terms, "TITLE-ABS-KEY")
    scopus_tech = build_or_group(tech_terms, "TITLE-ABS-KEY")
    scopus_ai = build_or_group(ai_terms, "TITLE-ABS-KEY")
    scopus_dom = build_or_group(domain_terms, "TITLE-ABS-KEY")
    scopus_ex_meta = build_or_group(metadata_exclusion_terms, "TITLE-ABS-KEY")
    scopus_ex_title = build_or_group(title_exclusion_terms, "TITLE")

    queries["SCOPUS.query"] = (
        f"{scopus_prob} AND {scopus_tech} AND {scopus_ai} AND {scopus_dom} AND NOT ({scopus_ex_meta} OR {scopus_ex_title})"
    )

    # --- 4. Query for Web of Science ---
    wos_prob = build_or_group(problem_terms, "TS=")
    wos_tech = build_or_group(tech_terms, "TS=")
    wos_ai = build_or_group(ai_terms, "TS=")
    wos_dom = build_or_group(domain_terms, "TS=")
    wos_ex_meta = build_or_group(metadata_exclusion_terms, "TS=")
    wos_ex_title = build_or_group(title_exclusion_terms, "TI=")

    queries["WOS.query"] = (
        f"{wos_prob} AND {wos_tech} AND {wos_ai} AND {wos_dom} NOT ({wos_ex_meta} OR {wos_ex_title})"
    )

    # --- 5. Query for AIAA ARC ---
    aiaa_prob = build_or_group(problem_terms)
    aiaa_tech = build_or_group(tech_terms)
    aiaa_ai = build_or_group(ai_terms)
    aiaa_dom = build_or_group(domain_terms)
    aiaa_ex = build_or_group(combined_exclusion)

    queries["AIAA.query"] = (
        f"{aiaa_prob} AND {aiaa_tech} AND {aiaa_ai} AND {aiaa_dom} NOT {aiaa_ex}"
    )

    # --- 6. Queries for NASA NTRL ---
    nasa_query1 = '"collision avoidance" AND radar'
    nasa_query2 = '"collision avoidance" AND UAV'
    queries["NASA.query"] = (
        f"# Run the searches below separately:\n\n# Search 1:\n{nasa_query1}\n\n# Search 2:\n{nasa_query2}"
    )

    # --- Save queries to files ---
    output_dir = "generated_queries"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for filename, query_string in queries.items():
        # Clean whitespace for most queries, but preserve structure for NASA instructions
        clean_query = (
            " ".join(query_string.split()) if "NASA" not in filename else query_string
        )
        filepath = os.path.join(output_dir, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(clean_query)
        print(f"✅ Query saved to: {filepath}")


if __name__ == "__main__":
    config_data = parse_custom_ini()
    if config_data:
        generate_queries(config_data)
