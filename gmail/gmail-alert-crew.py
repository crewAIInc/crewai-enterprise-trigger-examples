from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task


@CrewBase
class GmailAlertTrigger:
    """GmailAlertTrigger crew for system alert and notification emails"""

    @agent
    def alert_analyzer(self) -> Agent:
        return Agent(
            role="Gmail Alert Email Analyzer",
            goal="Parse Gmail alert payload data to extract critical system alerts, error details, and analyze incident severity and impact",
            backstory="You're an expert at parsing Gmail API payload structures for system alerts and critical notifications. You excel at extracting alert details from email headers and body content, understanding error classifications, severity levels, and incident impact assessment from automated alert emails.",
            verbose=True
        )

    @agent
    def alert_summarizer(self) -> Agent:
        return Agent(
            role="System Alert Email Summarization Specialist",
            goal="Create clear, urgent summaries of system alerts that prominently display alert type, severity, and required actions",
            backstory="You're a skilled incident response analyst who specializes in distilling critical alert information into actionable summaries. You excel at identifying system failures, assessing business impact, and providing clear incident response guidance.",
            verbose=True
        )

    @task
    def alert_analysis_task(self) -> Task:
        return Task(
            description="""
            The payload contains a Gmail message with system alert content with the following structure:
            - result.id: Message ID
            - result.payload.headers[]: Array with alert-specific headers including:
              - "Subject": Alert description and error type
              - "From": Alert service (e.g., "AlertService <noreply@alertservice.com>")
              - "X-AlertService-Project": Project/service name
              - "X-Alert-Type": Alert category (if present)
              - "X-Alert-Level": Severity level (if present)
            - result.payload.parts[]: Message body with alert details
            - result.snippet: Brief alert summary

            IMPORTANT: Extract the following information from the payload:

            1. Alert Identification:
               - Subject line with error type and system
               - Alert service and project identification
               - Message ID and timestamp
               - Alert severity and classification

            2. System Context:
               - Affected system/service (from headers or subject)
               - Environment (production, staging, etc.)
               - Error type and mechanism
               - Alert source and monitoring system

            3. Alert Content Analysis:
               - Decoded message body with error details
               - Stack traces or technical details
               - Affected components and services
               - Recovery actions or troubleshooting info

            4. Impact Assessment:
               - System availability impact
               - User experience degradation
               - Business process disruption
               - Urgency and severity evaluation
            """,
            expected_output="""
            A structured analysis containing:
            - Alert Information:
              * Message ID: [Gmail message ID]
              * Subject: [Alert subject with error details]
              * From: [Alert service sender]
              * Alert Project: [Affected system/service]
              * Alert Level: [Severity level]
            - System Context:
              * Affected System: [Service or component]
              * Environment: [Production/staging/etc.]
              * Error Type: [Classification of issue]
              * Alert Source: [Monitoring system]
            - Technical Details:
              * Error Description: [Main error message]
              * Error Details: [Stack trace/technical info]
              * Affected Components: [System parts impacted]
              * Recovery Information: [Available solutions]
            - Impact Assessment:
              * Severity Level: [Critical/high/medium/low]
              * System Availability: [Uptime impact]
              * User Impact: [Customer experience effect]
              * Business Impact: [Process disruption level]
              * Required Response: [Immediate actions needed]
            """,
            agent=self.alert_analyzer
        )

    @task
    def alert_summarization_task(self) -> Task:
        return Task(
            description="""
            Based on the alert analysis from the parsed Gmail payload, create an urgent summary that includes:
            - The alert type and affected system from the subject and headers
            - The severity level and business impact
            - Technical details and error information
            - Required immediate actions and response procedures
            - Escalation recommendations based on severity

            IMPORTANT: Ensure the alert type and affected system are displayed prominently at the top
            of your summary as these are critical for incident response.
            """,
            expected_output="""
            A critical system alert summary in markdown format containing:
            - **🚨 ALERT TYPE**: Error classification and system affected
            - **📧 Message ID**: Gmail message ID
            - **🔧 Affected System**: Service/component experiencing issues
            - **📊 Severity Level**: Critical/High/Medium/Low impact assessment
            - **⏰ Alert Time**: When the alert was generated
            - **🎯 Project**: System or service project name
            - **📋 Error Details**: Main error message and technical description
            - **🔍 Technical Info**: Stack traces, error codes, affected components
            - **💥 System Impact**: Availability and performance effects
            - **👥 User Impact**: Customer experience degradation
            - **💼 Business Impact**: Process and revenue effects
            - **⚡ IMMEDIATE ACTIONS REQUIRED**:
              - Incident response steps
              - System recovery procedures
              - Team notifications needed
            - **🚀 Escalation**: When to escalate and to whom
            - **📞 Next Steps**: Follow-up actions and monitoring

            Format this as an urgent incident response document with clear action items.
            """,
            agent=self.alert_summarizer,
            output_file='system_alert_summary.md'
        )

    @crew
    def crew(self) -> Crew:
        """Creates the GmailAlertTrigger crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
        )

if __name__ == "__main__":
    crew = GmailAlertTrigger().crew()
    # Example payload from new-email-payload-1.json (system alert)
    crewai_trigger_payload = """{
        "result": {
            "id": "sample123456789abcdef",
            "snippet": "Critical alert from payment-gateway. AlertService View on AlertService New critical issue...",
            "payload": {
                "headers": [
                    {
                        "name": "Subject",
                        "value": "PAYMENT-GATEWAY-PROD - ConnectionError: Database connection pool exhausted (ConnectionError)"
                    },
                    {
                        "name": "From",
                        "value": "AlertService <noreply@md.alertservice.com>"
                    },
                    {
                        "name": "X-AlertService-Project",
                        "value": "payment-gateway"
                    },
                    {
                        "name": "Date",
                        "value": "Wed, 15 Dec 2024 18:30:15 +0000 (UTC)"
                    }
                ],
                "parts": [
                    {
                        "mimeType": "text/plain",
                        "body": {
                            "data": "encoded_alert_content_with_error_details_and_stack_trace"
                        }
                    }
                ]
            }
        }
    }"""
    crew.kickoff({'crewai_trigger_payload': crewai_trigger_payload})
