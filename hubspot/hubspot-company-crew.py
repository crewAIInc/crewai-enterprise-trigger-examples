from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task


@CrewBase
class HubSpotCompanyTrigger:
    """HubSpotCompanyTrigger crew for company record operations"""

    @agent
    def company_analyzer(self) -> Agent:
        return Agent(
            role="HubSpot Company Record Analyzer",
            goal="Parse HubSpot company payload data to extract business information, market data, and analyze enterprise sales potential",
            backstory="You're an expert at parsing HubSpot company records and understanding enterprise sales processes. You excel at analyzing company properties, business metrics, market segments, technology stacks, and understanding the enterprise sales pipeline for B2B prospects.",
            verbose=True
        )

    @agent
    def company_summarizer(self) -> Agent:
        return Agent(
            role="HubSpot Company Summarization Specialist",
            goal="Create clear summaries of company records that highlight enterprise sales potential, market fit, and strategic account value",
            backstory="You're skilled at analyzing company data and providing strategic insights for enterprise sales teams, including market positioning, revenue potential, and account development recommendations.",
            verbose=True
        )

    @task
    def company_analysis_task(self) -> Task:
        return Task(
            description="""
            The payload contains a HubSpot company record with the following structure:
            - result.id: Company ID
            - result.properties: Object with company-specific fields including:
              - name: Company name
              - domain, website: Company web presence
              - industry: Business sector
              - annualrevenue: Company revenue
              - numberofemployees: Company size
              - country, city: Location information
              - founded_year: Company age
              - lifecyclestage: Current stage (lead, customer, etc.)
              - hs_num_* fields: Associated records counts
              - web_technologies: Technology stack
              - market_segment: Business segment classification

            IMPORTANT: Extract the following information:

            1. Company Identity:
               - Company name and domain
               - Industry and business sector
               - Geographic location and headquarters
               - Company founding and age

            2. Business Metrics:
               - Annual revenue and size
               - Number of employees
               - Market segment classification
               - Growth indicators

            3. Technology Profile:
               - Technology stack in use
               - Digital presence and web technologies
               - Technical sophistication level

            4. Sales Potential:
               - Enterprise readiness assessment
               - Revenue opportunity size
               - Associated contacts and deals
               - Strategic account value
            """,
            expected_output="""
            A structured analysis containing:
            - Company Information:
              * Company ID: [HubSpot company ID]
              * Name: [Company name]
              * Domain: [Website domain]
              * Industry: [Business sector]
              * Location: [Headquarters location]
            - Business Profile:
              * Annual Revenue: [Revenue figures]
              * Employee Count: [Company size]
              * Founded: [Founding year and age]
              * Market Segment: [SMB/Mid-market/Enterprise]
              * Lifecycle Stage: [Current sales stage]
            - Technology Stack:
              * Web Technologies: [Tech stack analysis]
              * Digital Presence: [Website and tools]
              * Technical Maturity: [Sophistication level]
            - Sales Assessment:
              * Enterprise Potential: [Account value assessment]
              * Revenue Opportunity: [Deal size potential]
              * Associated Records: [Contacts, deals counts]
              * Strategic Value: [Account importance level]
            """,
            agent=self.company_analyzer
        )

    @task
    def company_summarization_task(self) -> Task:
        return Task(
            description="""
            Create a comprehensive summary of the company record that includes enterprise sales potential,
            market positioning, and strategic account development recommendations.
            """,
            expected_output="""
            A company record summary in markdown format:
            - **Company ID**: HubSpot company ID
            - **Company Name**: Full company name
            - **Domain**: Primary website domain
            - **Industry**: Business sector and classification
            - **Location**: Headquarters and key locations
            - **Annual Revenue**: Revenue figures and growth indicators
            - **Employee Count**: Company size and scale
            - **Founded**: Founding year and company maturity
            - **Market Segment**: SMB/Mid-market/Enterprise classification
            - **Lifecycle Stage**: Current sales pipeline position
            - **Technology Stack**: Web technologies and digital tools in use
            - **Digital Presence**: Website sophistication and online footprint
            - **Associated Records**: Connected contacts, deals, and activities
            - **Business Context**: Market position and competitive landscape
            - **Sales Potential**: Revenue opportunity and deal size assessment
            - **Strategic Value**: Account importance and prioritization
            - **Recommended Actions**:
              - Enterprise sales approach strategy
              - Account development priorities
              - Technology positioning opportunities
            - **Notes**: Key insights and growth opportunities
            """,
            agent=self.company_summarizer,
            output_file='company_summary.md'
        )

    @crew
    def crew(self) -> Crew:
        """Creates the HubSpotCompanyTrigger crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
        )

if __name__ == "__main__":
    crew = HubSpotCompanyTrigger().crew()
    # Example payload from record-created-company.json
    crewai_trigger_payload = """{
        "result": {
            "id": "78924563147",
            "properties": {
                "name": "VelocityWorks Inc - VWI",
                "domain": "velocityworks-sample.com",
                "website": "velocityworks-sample.com",
                "industry": "COMPUTER_SOFTWARE",
                "annualrevenue": "2500000",
                "numberofemployees": "75",
                "country": "United States",
                "founded_year": "2018",
                "lifecyclestage": "marketingqualifiedlead",
                "market_segment": "SMB",
                "web_technologies": "react;aws;docker;kubernetes;stripe;google_analytics;hubspot;salesforce",
                "createdate": "2024-11-22T14:25:33.156Z",
                "hs_lastmodifieddate": "2024-12-21T09:32:15.234Z",
                "hs_num_open_deals": "1",
                "num_associated_contacts": "5"
            },
            "createdAt": "2024-11-22T14:25:33.156Z",
            "updatedAt": "2024-12-21T09:32:15.234Z",
            "archived": false
        }
    }"""
    crew.kickoff({'crewai_trigger_payload': crewai_trigger_payload})
