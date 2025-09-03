from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task


@CrewBase
class HubSpotRecordTrigger:
    """HubSpotRecordTrigger crew"""

    @agent
    def hubspot_record_analyzer(self) -> Agent:
        return Agent(
            role="HubSpot Record Payload Parser and Analyzer",
            goal="Parse HubSpot record payload data to extract contact, company, or deal information and analyze CRM data for business insights",
            backstory="You're an expert at parsing HubSpot API payload structures and CRM data formats. You excel at navigating complex JSON structures to extract record information including properties, timestamps, associations, and lifecycle stages. You understand different record types (contacts, companies, deals), property mappings, and HubSpot's data model for sales, marketing, and customer success operations.",
            verbose=True
        )

    @agent
    def hubspot_record_summarizer(self) -> Agent:
        return Agent(
            role="HubSpot CRM Data Summarization Specialist",
            goal="Create clear, concise summaries that prominently display record type, name/title, and operation, then capture essential business context and insights",
            backstory="You're a skilled business analyst who specializes in distilling complex CRM data into clear, actionable summaries. You excel at organizing information with record identification and operation type prominently displayed at the top, followed by comprehensive business analysis. You understand that record type, primary identifier, and operation are the most critical pieces of information for quick CRM record identification.",
            verbose=True
        )

    @task
    def hubspot_record_analysis_task(self) -> Task:
        return Task(
            description="""
            The payload contains a HubSpot record operation with the following structure:
            - result.id: Record ID
            - result.properties: Object containing all record properties
            - result.createdAt: Record creation timestamp
            - result.updatedAt: Last update timestamp
            - result.archived: Archive status
            - result.associations: Related records (if included)

            IMPORTANT: Extract the following information from the payload structure:

            1. Record Basic Information:
               - Record ID (result.id)
               - Record type (contact, company, deal - inferred from properties)
               - Primary identifier (name, email, deal name, company name)
               - Archive status (result.archived)

            2. Key Properties Analysis:
               For Contacts: firstname, lastname, email, company, jobtitle, phone, lifecyclestage
               For Companies: name, domain, industry, city, state, country, annualrevenue
               For Deals: dealname, amount, dealstage, closedate, pipeline

            3. Timeline Information:
               - Creation date (result.createdAt)
               - Last update (result.updatedAt)
               - Lifecycle progression (from properties)

            4. Business Context:
               - Lead scoring and qualification data
               - Revenue and business metrics
               - Engagement history and touchpoints
               - Geographic and demographic data

            5. Analyze the record for:
               - Type of operation (new record, update, archive)
               - Business significance and priority
               - Sales/marketing qualified status
               - Revenue impact potential
               - Next steps and action items
            """,
            expected_output="""
            A structured analysis containing:
            - Record Information:
              * Record ID: [HubSpot record ID]
              * Type: [contact/company/deal]
              * Primary ID: [name/email/deal name]
              * Status: [active/archived]
            - Key Properties:
              * Name/Title: [primary identifier]
              * Contact Info: [email, phone, location]
              * Business Data: [company, revenue, stage]
              * Qualification: [lifecycle stage, scores]
            - Timeline:
              * Created: [creation timestamp]
              * Updated: [last update timestamp]
              * Operation: [type of record operation detected]
            - Business Context:
              * Industry/Market: [business classification]
              * Revenue Potential: [deal value, company size]
              * Engagement Level: [interaction history]
              * Geographic Data: [location information]
            - Analysis:
              * Operation type and significance
              * Business priority and potential
              * Sales readiness assessment
              * Marketing qualification status
              * Recommended next actions
            """,
            agent=self.hubspot_record_analyzer
        )

    @task
    def hubspot_record_summarization_task(self) -> Task:
        return Task(
            description="""
            Based on the HubSpot record analysis from the parsed payload, create a comprehensive summary that includes:
            - The record type and primary identifier from the properties
            - The operation type and business significance from the analysis
            - Key business metrics and qualification data
            - Important context for sales, marketing, or customer success teams
            - Assessment of priority and recommended actions

            IMPORTANT: Ensure the record type and primary identifier (name/email/deal name)
            are displayed prominently at the top of your summary. These are critical pieces of
            information that must be clearly visible for quick record identification.
            """,
            expected_output="""
            A well-structured HubSpot record summary in markdown format containing:
            - **Record ID**: HubSpot record ID (from result.id in payload)
            - **Record Type**: Contact/Company/Deal (inferred from properties)
            - **Primary Identifier**: Name, email, or deal name (from properties)
            - **Operation**: Type of record operation (new, update, archive)
            - **Status**: Lifecycle stage and current status
            - **Contact Information**: Email, phone, location (if applicable)
            - **Business Data**: Company, industry, revenue, deal value
            - **Qualification**: Lead scores, lifecycle progression
            - **Timeline**: Creation and last update timestamps
            - **Engagement**: Interaction history and touchpoints
            - **Summary**: Concise overview of record significance
            - **Business Context**: Revenue potential and market context
            - **Priority Assessment**: Business importance and urgency
            - **Recommended Actions**: Next steps for sales/marketing teams

            Ensure the Record Type and Primary Identifier fields are prominently displayed at the top and
            formatted as clean markdown without code blocks.
            """,
            agent=self.hubspot_record_summarizer,
            output_file='hubspot_record_summary.md'
        )

    @crew
    def crew(self) -> Crew:
        """Creates the HubSpotRecordTrigger crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
        )

if __name__ == "__main__":
    crew = HubSpotRecordTrigger().crew()
    crewai_trigger_payload = "PUT YOUR TRIGGER PAYLOAD HERE"
    crew.kickoff({'crewai_trigger_payload': crewai_trigger_payload})
