from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task


@CrewBase
class HubSpotContactTrigger:
    """HubSpotContactTrigger crew for contact record operations"""

    @agent
    def contact_analyzer(self) -> Agent:
        return Agent(
            role="HubSpot Contact Record Analyzer",
            goal="Parse HubSpot contact payload data to extract lead information, qualification data, and analyze sales/marketing potential",
            backstory="You're an expert at parsing HubSpot contact records and understanding lead qualification processes. You excel at analyzing contact properties, lead scores, lifecycle stages, email engagement, and understanding the sales pipeline progression for individual prospects.",
            verbose=True
        )

    @agent
    def contact_summarizer(self) -> Agent:
        return Agent(
            role="HubSpot Contact Summarization Specialist",
            goal="Create clear summaries of contact records that highlight sales readiness, marketing qualification, and next action priorities",
            backstory="You're skilled at analyzing contact data and providing actionable insights for sales and marketing teams, including lead scoring, engagement levels, and recommended follow-up actions.",
            verbose=True
        )

    @task
    def contact_analysis_task(self) -> Task:
        return Task(
            description="""
            The payload contains a HubSpot contact record with the following structure:
            - result.id: Contact ID
            - result.properties: Object with contact-specific fields including:
              - firstname, lastname, email: Basic contact info
              - company, jobtitle: Professional details
              - phone, city, state, country: Contact information
              - lifecyclestage: Current stage (lead, marketingqualifiedlead, etc.)
              - createdate, lastmodifieddate: Timeline information
              - lead_score_*: Lead scoring data
              - hs_email_*: Email engagement metrics
              - associatedcompanyid: Linked company
              - Various HubSpot tracking fields

            IMPORTANT: Extract the following information:

            1. Contact Identity:
               - Full name (firstname + lastname)
               - Email address and contact information
               - Company and job title
               - Geographic location

            2. Lead Qualification:
               - Lifecycle stage progression
               - Lead scores and thresholds
               - Email engagement metrics
               - Conversion events and dates

            3. Engagement History:
               - Email open/click rates
               - Website interaction data
               - Form submissions and conversions
               - Last activity timestamps

            4. Sales Readiness:
               - Qualification level assessment
               - Company association and size
               - Technology usage and needs
               - Revenue potential indicators
            """,
            expected_output="""
            A structured analysis containing:
            - Contact Information:
              * Contact ID: [HubSpot contact ID]
              * Name: [Full name]
              * Email: [Email address]
              * Company: [Company name and title]
              * Location: [City, state, country]
            - Qualification Status:
              * Lifecycle Stage: [Current stage]
              * Lead Score: [Score and threshold]
              * Company Association: [Associated company ID]
              * Creation Date: [When contact was created]
            - Engagement Metrics:
              * Email Performance: [Opens, clicks, deliveries]
              * Website Activity: [Page views, visits]
              * Conversion Events: [Form submissions, etc.]
              * Last Activity: [Most recent engagement]
            - Sales Assessment:
              * Readiness Level: [Sales qualification status]
              * Company Context: [Business potential]
              * Technology Profile: [Technical sophistication]
              * Revenue Opportunity: [Business value potential]
            """,
            agent=self.contact_analyzer
        )

    @task
    def contact_summarization_task(self) -> Task:
        return Task(
            description="""
            Create a comprehensive summary of the contact record that includes lead qualification status,
            engagement levels, and actionable recommendations for sales and marketing teams.
            """,
            expected_output="""
            A contact record summary in markdown format:
            - **Contact ID**: HubSpot contact ID
            - **Name**: Full contact name
            - **Email**: Primary email address
            - **Company**: Company name and job title
            - **Location**: Geographic location
            - **Lifecycle Stage**: Current qualification level
            - **Lead Score**: Score and qualification threshold
            - **Created**: Contact creation date
            - **Last Updated**: Most recent modification
            - **Email Engagement**: Open/click rates and performance
            - **Website Activity**: Page views and visit patterns
            - **Conversion History**: Form submissions and key events
            - **Company Context**: Associated business and revenue potential
            - **Technology Profile**: Technical sophistication and needs
            - **Sales Readiness**: Qualification assessment and priority level
            - **Recommended Actions**:
              - Next steps for sales outreach
              - Marketing nurturing recommendations
              - Priority level for follow-up
            - **Notes**: Additional context and opportunities
            """,
            agent=self.contact_summarizer,
            output_file='contact_summary.md'
        )

    @crew
    def crew(self) -> Crew:
        """Creates the HubSpotContactTrigger crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
        )

if __name__ == "__main__":
    crew = HubSpotContactTrigger().crew()
    # Example payload from record-created-contact.json
    crewai_trigger_payload = """{
        "result": {
            "id": "12345678901",
            "properties": {
                "firstname": "Alex",
                "lastname": "Thompson",
                "email": "alex.thompson@zenithtech-sample.com",
                "company": "ZenithTech Innovations",
                "jobtitle": "VP of Engineering",
                "phone": "+1 (303) 555-1234",
                "city": "Denver",
                "state": "Colorado",
                "country": "United States",
                "lifecyclestage": "lead",
                "createdate": "2024-09-12T11:45:30.789Z",
                "lastmodifieddate": "2024-12-22T13:20:45.567Z",
                "lead_score_06_11_2025": "82",
                "lead_score_06_11_2025_threshold": "Low",
                "hs_email_open": "5",
                "hs_email_delivered": "8",
                "annualrevenue": "8500000",
                "associatedcompanyid": "67890123456"
            },
            "createdAt": "2024-09-12T11:45:30.789Z",
            "updatedAt": "2024-12-22T13:20:45.567Z",
            "archived": false
        }
    }"""
    crew.kickoff({'crewai_trigger_payload': crewai_trigger_payload})
