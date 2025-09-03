from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task


@CrewBase
class OutlookMessageTrigger:
    """OutlookMessageTrigger crew"""

    @agent
    def outlook_message_analyzer(self) -> Agent:
        return Agent(
            role="Outlook Message Payload Parser and Analyzer",
            goal="Parse Outlook message payload data to extract email details (sender, subject, recipients, content) and analyze message information for insights",
            backstory="You're an expert at parsing Microsoft Graph API payload structures and Outlook message data formats. You excel at navigating complex JSON structures to extract message information including from/sender, subject, toRecipients, body content, attachments, and message metadata. You understand different message types, importance levels, and Outlook-specific properties like conversation threading and categories.",
            verbose=True
        )

    @agent
    def outlook_message_summarizer(self) -> Agent:
        return Agent(
            role="Outlook Message Summarization Specialist",
            goal="Create clear, concise summaries that prominently display sender, subject, and recipients, then capture essential message content and context",
            backstory="You're a skilled communicator who specializes in distilling complex email data into clear, actionable summaries. You excel at organizing information with sender and subject details prominently displayed at the top, followed by comprehensive message analysis. You understand that sender, subject, and recipients are the most critical pieces of information for quick message identification and prioritization.",
            verbose=True
        )

    @task
    def outlook_message_analysis_task(self) -> Task:
        return Task(
            description="""
            The payload contains an Outlook message with the following structure:
            - result.id: Message ID
            - result.subject: Email subject line
            - result.from.emailAddress: Sender information (name and address)
            - result.sender.emailAddress: Actual sender information
            - result.toRecipients[]: Array of recipient objects
            - result.ccRecipients[]: Array of CC recipient objects
            - result.bccRecipients[]: Array of BCC recipient objects
            - result.body: Message body content and type
            - result.bodyPreview: Preview text of the message
            - result.receivedDateTime: When message was received
            - result.sentDateTime: When message was sent
            - result.importance: Message importance level
            - result.hasAttachments: Whether message has attachments
            - result.conversationId: Conversation thread ID

            IMPORTANT: Extract the following information from the payload structure:

            1. Message Basic Information:
               - Message ID (result.id)
               - Subject (result.subject)
               - Conversation ID (result.conversationId)
               - Importance level (result.importance)

            2. Sender and Recipients:
               - From/Sender (result.from.emailAddress and result.sender.emailAddress)
               - To Recipients (result.toRecipients)
               - CC Recipients (result.ccRecipients)
               - BCC Recipients (result.bccRecipients)

            3. Message Content:
               - Body content (result.body.content)
               - Body type (result.body.contentType - html/text)
               - Body preview (result.bodyPreview)
               - Attachments indicator (result.hasAttachments)

            4. Timing and Metadata:
               - Sent timestamp (result.sentDateTime)
               - Received timestamp (result.receivedDateTime)
               - Read status (result.isRead)
               - Flag status (result.flag)

            5. Analyze the message for:
               - Message purpose and intent
               - Priority and urgency assessment
               - Action items or requests
               - Communication context and thread relevance
               - Business impact and next steps needed
            """,
            expected_output="""
            A structured analysis containing:
            - Message Information:
              * Message ID: [Outlook message ID]
              * Subject: [email subject line]
              * Conversation ID: [thread identifier]
              * Importance: [message importance level]
            - Communication Details:
              * From: [sender name and email address]
              * To: [recipient list with names and emails]
              * CC: [carbon copy recipients if any]
              * BCC: [blind carbon copy recipients if any]
            - Content Analysis:
              * Body Type: [HTML/text format]
              * Body Preview: [message preview text]
              * Full Content: [complete message body]
              * Attachments: [attachment status]
            - Timeline:
              * Sent: [sent timestamp]
              * Received: [received timestamp]
              * Read Status: [read/unread status]
              * Flag Status: [flagged status]
            - Analysis:
              * Message purpose and context
              * Priority and urgency level
              * Action items identified
              * Communication thread relevance
              * Business impact assessment
            """,
            agent=self.outlook_message_analyzer
        )

    @task
    def outlook_message_summarization_task(self) -> Task:
        return Task(
            description="""
            Based on the message analysis from the parsed Outlook payload, create a comprehensive summary that includes:
            - The sender information extracted from the "from" field in the payload
            - The subject line extracted from the "subject" field
            - The recipient information from the "toRecipients" field
            - The message content and context from the analysis
            - Key insights and action items identified
            - Assessment of message priority and business impact

            IMPORTANT: Ensure the sender (from "from" field) and subject (from "subject" field)
            are displayed prominently at the top of your summary. These are critical pieces of
            information that must be clearly visible for quick message identification.
            """,
            expected_output="""
            A well-structured Outlook message summary in markdown format containing:
            - **Message ID**: Outlook message ID (from result.id in payload)
            - **From**: Sender name and email (extracted from "from" field)
            - **Subject**: Email subject line (extracted from "subject" field)
            - **To**: Recipient list (extracted from "toRecipients" field)
            - **CC/BCC**: Carbon copy recipients (if any)
            - **Sent**: Message sent timestamp
            - **Received**: Message received timestamp
            - **Importance**: Message importance level
            - **Conversation**: Thread/conversation context
            - **Message Content**: Body preview and key content
            - **Attachments**: Attachment status and details
            - **Summary**: Concise overview of the message
            - **Key Points**: Important information and requests
            - **Action Items**: Tasks or follow-ups identified
            - **Priority**: Assessment of urgency and importance
            - **Business Impact**: Relevance and next steps

            Ensure the From and Subject fields are prominently displayed at the top and
            formatted as clean markdown without code blocks.
            """,
            agent=self.outlook_message_summarizer,
            output_file='outlook_message_summary.md'
        )

    @crew
    def crew(self) -> Crew:
        """Creates the OutlookMessageTrigger crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
        )

if __name__ == "__main__":
    crew = OutlookMessageTrigger().crew()
    crewai_trigger_payload = "PUT YOUR TRIGGER PAYLOAD HERE"
    crew.kickoff({'crewai_trigger_payload': crewai_trigger_payload})
