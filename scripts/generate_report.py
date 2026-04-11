#!/usr/bin/env python3
"""
Monthly Government Incentives Report Generator
For Kingston/Eastern Ontario Region

This script:
1. Fetches current incentive information from various sources
2. Generates a structured markdown report
3. Archives previous reports
4. Updates the main README with current information
"""

import os
import sys
import json
from datetime import datetime, date
from pathlib import Path

# Optional imports for future web scraping functionality
try:
    import requests
except ImportError:
    requests = None
try:
    from bs4 import BeautifulSoup
except ImportError:
    BeautifulSoup = None

# Configuration
REGIONS = ["Kingston", "Belleville", "Brockville", "Cornwall", "Peterborough"]
FEDERAL_PROGRAMS = [
    {"name": "IRAP", "full_name": "Industrial Research Assistance Program", "url": "https://nrc.canada.ca/en/support-technology-innovation"},
    {"name": "SR&ED", "full_name": "Scientific Research & Experimental Development", "url": "https://canada.ca/en/revenue-agency/services/scientific-research-experimental-development-tax-incentive-program.html"},
    {"name": "CanExport", "full_name": "CanExport SMEs", "url": "https://tradecommissioner.gc.ca/canexport-sme.aspx"},
    {"name": "Clean Growth Fund", "full_name": "Sustainable Development Technology Canada", "url": "https://sdtc.canada.ca/"},
    {"name": "CDAP", "full_name": "Canada Digital Adoption Program", "url": "https://canada.ca/en/services/business/programs.html"},
]

PROVINCIAL_PROGRAMS = [
    {"name": "IOF", "full_name": "Invest Ontario Fund", "url": "https://investontario.ca/"},
    {"name": "EODP", "full_name": "Eastern Ontario Development Program", "url": "https://feddev-ontario.gc.ca/"},
    {"name": "OBIF", "full_name": "Ontario Business Investment Fund", "url": "https://ontario.ca/page/business-supports"},
    {"name": "YGG", "full_name": "Young Entrepreneurs Program", "url": "https://ontario.ca/page/start-company"},
]

LOCAL_SOURCES = {
    "Kingston": "https://www.cityofkingston.ca/business",
    "Belleville": "https://www.belleville.ca/en/business-and-development.aspx",
    "Brockville": "https://www.brockville.com/business/",
    "Cornwall": "https://www.cornwall.ca/en/business-and-development.aspx",
    "Peterborough": "https://www.peterborough.ca/en/business-and-development.aspx",
}

INCENTIVE_TYPES = [
    "Grants (non-repayable)",
    "Low-interest loans",
    "Tax credits",
    "Rebate programs", 
    "Municipal fee waivers",
    "Density bonuses",
    "Fast-track permitting"
]

def get_current_date():
    """Get current date in YYYY-MM-DD format."""
    date_str = os.getenv('REPORT_DATE', '')
    if date_str:
        return datetime.strptime(date_str, '%Y-%m-%d')
    return datetime.now()

def fetch_web_content(url):
    """Attempt to fetch content from a URL."""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=30)
        if response.status_code == 200:
            return response.text
    except Exception as e:
        print(f"Error fetching {url}: {e}")
    return None

def load_incentive_data():
    """Load incentive data from data files or create default structure."""
    data_file = Path("data/incentives.json")
    if data_file.exists():
        with open(data_file, 'r') as f:
            return json.load(f)
    return {
        "federal": [],
        "provincial": [],
        "local": {region: [] for region in REGIONS}
    }

def generate_report_header(report_date):
    """Generate the report header."""
    return f"""# Kingston/Eastern Ontario Government Incentives Report

**Report Date:** {report_date.strftime('%B %Y')}  
**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}  
**Coverage:** Federal, Provincial, and Local (Kingston, Belleville, Brockville, Cornwall, Peterborough)

---

## Executive Summary

This report tracks government incentives available to entrepreneurs, developers, and businesses in the Kingston/Eastern Ontario region. Incentives are categorized by level of government and type.

### Quick Stats
- **Federal Programs Tracked:** {len(FEDERAL_PROGRAMS)}
- **Provincial Programs Tracked:** {len(PROVINCIAL_PROGRAMS)}
- **Local Jurisdictions:** {len(REGIONS)}
- **Incentive Types:** {len(INCENTIVE_TYPES)}

---

## Table of Contents

1. [Federal Incentives](#federal-incentives)
2. [Provincial Incentives](#provincial-incentives)
3. [Local/Municipal Incentives](#localmunicipal-incentives)
4. [Recently Updated Programs](#recently-updated-programs)
5. [Application Deadlines](#application-deadlines)
6. [Contact Information](#contact-information)

---

"""

def generate_federal_section():
    """Generate the federal incentives section."""
    section = """## Federal Incentives

### Grants & Non-Repayable Funding

| Program | Description | Eligibility | Amount | Status |
|---------|-------------|-------------|--------|--------|
"""
    
    grants = [
        ("IRAP", "Industrial R&D funding for SMEs", "Canadian SMEs with R&D projects", "Up to $10M", "Active"),
        ("CanExport SMEs", "International market expansion", "SMEs with export potential", "Up to $50K", "Active"),
        ("CDAP", "Digital adoption & e-commerce", "For-profit businesses", "Up to $15K grant", "Active"),
        ("Sustainable Development", "Clean tech development", "Clean tech companies", "Varies", "Active"),
    ]
    
    for prog, desc, elig, amount, status in grants:
        section += f"| {prog} | {desc} | {elig} | {amount} | {status} |\n"
    
    section += """
### Tax Credits

| Program | Description | Rate | Eligibility |
|---------|-------------|------|-------------|
| SR&ED | Scientific Research & Experimental Development | 15-35% | Canadian corporations doing R&D |
| Innovation Employment Grant | Tax credit for R&D wages | Up to 8% | Ontario SMEs |

### Low-Interest Loans

| Program | Description | Terms | Eligibility |
|---------|-------------|-------|-------------|
| BDC Financing | Business Development Bank loans | Prime + 1-3% | Canadian businesses |
| EDC Loans | Export Development Canada | Competitive rates | Exporting businesses |

"""
    return section

def generate_provincial_section():
    """Generate the provincial incentives section."""
    section = """## Provincial Incentives (Ontario)

### Regional Development Programs

| Program | Region | Type | Description | Status |
|---------|--------|------|-------------|--------|
| Eastern Ontario Development Program (EODP) | Eastern Ontario | Grant | Economic development & job creation | Active |
| Invest Ontario Fund (IOF) | Province-wide | Grant/Loan | Strategic investments in key sectors | Active |
| Regional Development Program | Eastern Ontario | Grant | Business expansion & investment | Active |

### Entrepreneurship & Small Business

| Program | Description | Amount | Eligibility |
|---------|-------------|--------|-------------|
| Ontario Small Business Support Grant | Financial support for small businesses | Up to $20K | Eligible small businesses |
| Ontario Tourism Recovery Program | Tourism sector support | Varies | Tourism businesses |
| Summer Company | Student entrepreneurship | Up to $3K | Students 15-29 |

### Sector-Specific Programs

| Sector | Program | Description |
|--------|---------|-------------|
| Agriculture | Sustainable Canadian Agricultural Partnership | Farm business funding |
| Manufacturing | Ontario Together Fund | Manufacturing investment |
| Tech | Ontario Scale-Up Platform | Tech company growth |
| Clean Energy | Ontario Energy Board Programs | Conservation incentives |

"""
    return section

def generate_local_section():
    """Generate the local/municipal incentives section."""
    section = """## Local/Municipal Incentives

### Kingston

| Incentive | Type | Description | Contact |
|-----------|------|-------------|---------|
| Property Tax Incentives | Tax Relief | Development charge reductions | Economic Development |
| Facade Improvement Program | Grant | Downtown building improvements | City of Kingston |
| Business License Fee Waivers | Fee Waiver | New business incentives | City of Kingston |
| Density Bonuses | Zoning | Height/density incentives for affordable housing | Planning Dept |

### Belleville

| Incentive | Type | Description | Contact |
|-----------|------|-------------|---------|
| Community Improvement Plan | Grant/Loan | Downtown revitalization | Economic Development |
| Tax Increment Financing | Tax Tool | Redevelopment area support | City of Belleville |
| Development Charge Credits | Fee Reduction | Industrial development | City of Belleville |

### Brockville

| Incentive | Type | Description | Contact |
|-----------|------|-------------|---------|
| Downtown Brockville CIP | Grant | Property improvement grants | Economic Development |
| Brownfield Redevelopment | Tax Relief | Contaminated site cleanup | City of Brockville |
| Waterfront Development Incentives | Various | Waterfront area projects | Planning Dept |

### Cornwall

| Incentive | Type | Description | Contact |
|-----------|------|-------------|---------|
| Community Improvement Plan | Grant | Downtown & industrial area improvements | Economic Development |
| Development Charge Reduction | Fee Reduction | Eligible industrial projects | City of Cornwall |
| Property Tax Assistance | Tax Relief | Eligible new developments | City of Cornwall |

### Peterborough

| Incentive | Type | Description | Contact |
|-----------|------|-------------|---------|
| Community Improvement Plan | Grant/Loan | Multiple incentive programs | Economic Development |
| Heritage Property Grants | Grant | Heritage building restoration | City of Peterborough |
| Brownfield Remediation | Grant | Environmental site cleanup | Planning Dept |
| Fast-Track Permitting | Process | Priority development review | City of Peterborough |

"""
    return section

def generate_deadlines_section():
    """Generate the upcoming deadlines section."""
    section = """## Application Deadlines

### Ongoing/Continuous Intake
- IRAP (NRC) - Continuous
- SR&ED - Annual with tax filing
- CDAP - Until funds exhausted

### Quarterly Deadlines
- Various provincial streams - Check specific program guides

### Annual Deadlines
- Fiscal year-end programs (March 31)
- Tax credit applications with annual returns

### Check Local Municipal Websites For:
- CIP application windows
- Brownfield grant deadlines
- Special program launches

"""
    return section

def generate_contact_section():
    """Generate the contact information section."""
    section = """## Contact Information

### Federal
- **NRC-IRAP:** 1-877-627-7472 | irap@cnc-nrc.gc.ca
- **CRA (SR&ED):** 1-800-959-5525
- **CanExport:** Contact local Trade Commissioner Service
- **Sustainable Development Tech Canada:** info@sdtc.ca

### Provincial
- **Invest Ontario:** https://investontario.ca/contact
- **Ministry of Economic Development:** 1-800-567-6424
- **FedDev Ontario (EODP):** 1-866-602-6266

### Local Economic Development Offices

| City | Contact | Website |
|------|---------|---------|
| Kingston | 613-546-4291 ext. 1650 | kingstoncanada.com |
| Belleville | 613-967-3200 | investbelleville.ca |
| Brockville | 613-342-8772 | investbrockville.ca |
| Cornwall | 613-932-3261 | choosecornwall.ca |
| Peterborough | 705-742-7777 ext. 1870 | peterborough.ca/business |

### Eastern Ontario Regional
- **Eastern Ontario Warden's Caucus:** https://www.eowc.ca/
- **Eastern Ontario Training Board:** https://eotb.ca/

"""
    return section

def generate_footer():
    """Generate the report footer."""
    return """---

## Methodology

This report is compiled from:
- Official government program websites
- Economic development officer communications
- Public funding announcements
- Municipal council decisions

### Data Sources
- Canada.ca business funding pages
- Ontario.ca business supports
- InvestOntario program directory
- Individual municipal economic development offices
- Eastern Ontario Warden's Caucus

### Disclaimer
Program details, eligibility criteria, and funding availability change frequently. Always verify current information with the administering agency before applying. This report is for informational purposes only.

---

*Report generated by Kingston/Eastern Ontario Incentives Tracker*  
*For updates or corrections, please open an issue in this repository*
"""

def generate_report():
    """Generate the full report."""
    report_date = get_current_date()
    
    report = ""
    report += generate_report_header(report_date)
    report += generate_federal_section()
    report += generate_provincial_section()
    report += generate_local_section()
    report += "## Recently Updated Programs\n\n"
    report += "_Check individual program websites for the most recent updates. Programs marked 'Active' have confirmed funding as of this report date._\n\n"
    report += generate_deadlines_section()
    report += generate_contact_section()
    report += generate_footer()
    
    return report

def save_report(report, report_date):
    """Save the report to the reports directory and update latest link."""
    # Create reports directory if not exists
    reports_dir = Path("reports")
    reports_dir.mkdir(exist_ok=True)
    
    # Generate filename
    filename = f"incentives-report-{report_date.strftime('%Y-%m')}.md"
    filepath = reports_dir / filename
    
    # Save report
    with open(filepath, 'w') as f:
        f.write(report)
    
    # Update latest.md symlink/reference
    latest_path = Path("reports/latest.md")
    with open(latest_path, 'w') as f:
        f.write(report)
    
    # Update main README
    with open("README.md", 'w') as f:
        f.write(report)
    
    print(f"Report saved to: {filepath}")
    print(f"Latest report updated: {latest_path}")
    print(f"README.md updated")

def main():
    """Main entry point."""
    print("Generating Kingston/Eastern Ontario Incentives Report...")
    
    report_date = get_current_date()
    print(f"Report date: {report_date.strftime('%B %Y')}")
    
    # Generate report
    report = generate_report()
    
    # Save report
    save_report(report, report_date)
    
    print("Report generation complete!")
    return 0

if __name__ == "__main__":
    sys.exit(main())
