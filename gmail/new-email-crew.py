from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task


@CrewBase
class GmailNewThreadTrigger:
    """GmailNewThreadTrigger crew"""

    @agent
    def email_analyzer(self) -> Agent:
        return Agent(
            role="Gmail Payload Parser and Analyzer",
            goal="Parse Gmail payload data to extract header information (sender from 'From' header, subject from 'Subject' header) and decode message body content for analysis",
            backstory="You're an expert at parsing Gmail API payload structures and email data formats. You excel at navigating complex JSON structures to extract header information from the headers array, decoding base64 encoded message bodies, and understanding different MIME types. You can distinguish between plain text and HTML content and extract meaningful information from both header fields and message body parts.",
            verbose=True
        )

    @agent
    def email_summarizer(self) -> Agent:
        return Agent(
            role="Email Summarization Specialist",
            goal="Create clear, concise summaries that prominently display sender and subject information, then capture the essential message and key details",
            backstory="You're a skilled communicator who specializes in distilling complex email conversations into clear, actionable summaries. You excel at organizing information with sender and subject details prominently displayed at the top, followed by comprehensive content analysis. You understand that sender and subject are the most critical pieces of information for quick email identification.",
            verbose=True
        )

    @task
    def email_analysis_task(self) -> Task:
        return Task(
            description="""
            The payload contains a Gmail message with the following structure:
            - result.id: Message ID
            - result.payload.headers[]: Array of email headers with name/value pairs
            - result.payload.parts[]: Array of message body parts (text/plain, text/html)

            IMPORTANT: Extract the following information from the payload structure:

            1. From the headers array (result.payload.headers), find headers with these names:
               - "From": sender email address and name
               - "Subject": email subject line
               - "To": recipient information
               - "Date": email timestamp
               - "Message-ID": unique message identifier

            2. From the parts array (result.payload.parts), extract and decode message body:
               - Find parts with mimeType "text/plain" or "text/html"
               - Decode the base64 encoded body.data content to readable text
               - Prefer text/plain over text/html for readability

            3. Analyze the decoded message content for:
               - Main purpose/intent of the email
               - Key information and important details from the message
               - Any action items or requests mentioned
               - Tone and urgency level
               - Important dates, numbers, or references

            Make sure to clearly distinguish between header information and decoded message body content.
            """,
            expected_output="""
            A structured analysis containing:
            - Email Headers:
              * Message ID (from result.id): [Gmail message ID]
              * From (from "From" header): [sender email address and name]
              * Subject (from "Subject" header): [email subject line]
              * To (from "To" header): [recipient information]
              * Date (from "Date" header): [email timestamp]
            - Decoded Message Body: [full decoded email text from parts array]
            - Main purpose/intent of the email
            - Key information extracted from the content
            - Action items identified
            - Tone and urgency assessment
            - Important details (dates, numbers, references)
            """,
            agent=self.email_analyzer
        )

    @task
    def email_summarization_task(self) -> Task:
        return Task(
            description="""
            Based on the email analysis from the parsed Gmail payload, create a comprehensive summary that includes:
            - The sender information extracted from the "From" header in the payload
            - The subject line extracted from the "Subject" header in the payload
            - The decoded and analyzed message content from the email body parts
            - Key points and important information from the analysis
            - Any action items or next steps identified
            - Assessment of priority/urgency

            IMPORTANT: Ensure the sender (from "From" header) and subject (from "Subject" header)
            are displayed prominently at the top of your summary. These are critical pieces of
            information that must be clearly visible for quick email identification.
            """,
            expected_output="""
            A well-structured email summary in markdown format containing:
            - **Message ID**: Gmail message ID (from result.id in payload)
            - **From**: Sender email address and name (extracted from "From" header)
            - **Subject**: The email subject line (extracted from "Subject" header)
            - **To**: Recipient information (extracted from "To" header)
            - **Date**: Email timestamp (extracted from "Date" header)
            - **Message Content**: The full decoded email message body
            - **Summary**: Concise overview of the main message
            - **Key Points**: Bullet points of important information
            - **Action Items**: Any tasks or requests mentioned
            - **Priority**: Assessment of urgency/importance

            Ensure the From and Subject fields are prominently displayed at the top and
            formatted as clean markdown without code blocks.
            """,
            agent=self.email_summarizer,
            output_file='email_summary.md'
        )

    @crew
    def crew(self) -> Crew:
        """Creates the GmailNewThreadTrigger crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
        )

if __name__ == "__main__":
    crew = GmailNewThreadTrigger().crew()
    crewai_trigger_payload = "PUT YOUR TRIGGER PAYLOAD HERE"
    crew.kickoff({'crewai_trigger_payload': crewai_trigger_payload})
