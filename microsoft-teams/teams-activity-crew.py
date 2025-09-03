from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task


@CrewBase
class MicrosoftTeamsActivityTrigger:
    """MicrosoftTeamsActivityTrigger crew"""

    @agent
    def teams_activity_analyzer(self) -> Agent:
        return Agent(
            role="Microsoft Teams Activity Payload Parser and Analyzer",
            goal="Parse Microsoft Teams activity payload data to extract conversation, message, meeting, or channel activity details and analyze team collaboration patterns",
            backstory="You're an expert at parsing Microsoft Graph API payload structures and Teams activity data formats. You excel at navigating complex JSON structures to extract activity information including messages, meetings, channel activities, member changes, and file sharing. You understand different activity types, team structures, and Teams collaboration patterns for business communication analysis.",
            verbose=True
        )

    @agent
    def teams_activity_summarizer(self) -> Agent:
        return Agent(
            role="Teams Activity Summarization Specialist",
            goal="Create clear, concise summaries that prominently display activity type, participants, and context, then capture essential collaboration insights and business impact",
            backstory="You're a skilled collaboration analyst who specializes in distilling complex Teams activity data into clear, actionable summaries. You excel at organizing information with activity type and key participants prominently displayed at the top, followed by comprehensive collaboration analysis. You understand that activity type, participants, and context are the most critical pieces of information for quick Teams activity identification and business impact assessment.",
            verbose=True
        )

    @task
    def teams_activity_analysis_task(self) -> Task:
        return Task(
            description="""
            The payload contains a Microsoft Teams activity with the following potential structure:
            - result.id: Activity ID
            - result.activityType: Type of activity (message, meeting, memberAdded, etc.)
            - result.teamId: Team identifier
            - result.channelId: Channel identifier (if applicable)
            - result.from: User who initiated the activity
            - result.recipient: Activity recipient or target
            - result.summary: Activity summary
            - result.body: Activity content or message body
            - result.createdDateTime: Activity timestamp
            - result.webUrl: Link to the activity in Teams
            - result.participants: List of activity participants
            - result.attachments: Any file attachments or shared content

            IMPORTANT: Extract the following information from the payload structure:

            1. Activity Basic Information:
               - Activity ID (result.id)
               - Activity type (result.activityType)
               - Team and channel context (result.teamId, result.channelId)
               - Activity timestamp (result.createdDateTime)

            2. Participants and Communication:
               - Initiator/From user (result.from)
               - Recipients or targets (result.recipient)
               - All participants (result.participants)
               - User roles and permissions

            3. Content and Context:
               - Activity summary (result.summary)
               - Message or content body (result.body)
               - Attachments or shared files (result.attachments)
               - Web URL for access (result.webUrl)

            4. Team and Channel Context:
               - Team information and structure
               - Channel type and purpose
               - Access levels and membership

            5. Analyze the activity for:
               - Type of collaboration (communication, meeting, file sharing)
               - Business context and relevance
               - Team productivity and engagement patterns
               - Information sharing and knowledge transfer
               - Action items or follow-up requirements
            """,
            expected_output="""
            A structured analysis containing:
            - Activity Information:
              * Activity ID: [Teams activity ID]
              * Type: [activity type - message, meeting, etc.]
              * Team: [team identifier and context]
              * Channel: [channel identifier and purpose]
            - Participants:
              * Initiator: [user who started the activity]
              * Recipients: [target users or audience]
              * All Participants: [complete participant list]
              * Roles: [user roles and permissions]
            - Content Analysis:
              * Summary: [activity summary or title]
              * Content: [message body or activity details]
              * Attachments: [shared files or resources]
              * Access: [web URL and access method]
            - Context:
              * Team Structure: [team organization and purpose]
              * Channel Type: [channel classification and use]
              * Timestamp: [activity timing]
            - Analysis:
              * Collaboration type and purpose
              * Business relevance and impact
              * Team engagement patterns
              * Knowledge sharing effectiveness
              * Required follow-up actions
            """,
            agent=self.teams_activity_analyzer
        )

    @task
    def teams_activity_summarization_task(self) -> Task:
        return Task(
            description="""
            Based on the Teams activity analysis from the parsed payload, create a comprehensive summary that includes:
            - The activity type and context from the payload
            - The participants and team/channel information
            - The content and business relevance from the analysis
            - Key collaboration insights and patterns
            - Assessment of team productivity and engagement impact

            IMPORTANT: Ensure the activity type and key participants
            are displayed prominently at the top of your summary. These are critical pieces of
            information that must be clearly visible for quick Teams activity identification.
            """,
            expected_output="""
            A well-structured Microsoft Teams activity summary in markdown format containing:
            - **Activity ID**: Teams activity ID (from result.id in payload)
            - **Activity Type**: Type of activity (message, meeting, file share, etc.)
            - **Initiator**: User who initiated the activity
            - **Team**: Team name and identifier
            - **Channel**: Channel name and type (if applicable)
            - **Participants**: All participants involved in the activity
            - **Timestamp**: When the activity occurred
            - **Summary**: Brief description of the activity
            - **Content**: Message content or activity details
            - **Attachments**: Shared files or resources (if any)
            - **Web Access**: Direct link to the activity in Teams
            - **Business Context**: Relevance and impact on team goals
            - **Collaboration Insights**: Team interaction patterns
            - **Engagement Level**: Assessment of participant involvement
            - **Knowledge Sharing**: Information transfer effectiveness
            - **Action Items**: Follow-up tasks or requirements
            - **Team Productivity**: Impact on overall team efficiency

            Ensure the Activity Type and Initiator fields are prominently displayed at the top and
            formatted as clean markdown without code blocks.
            """,
            agent=self.teams_activity_summarizer,
            output_file='teams_activity_summary.md'
        )

    @crew
    def crew(self) -> Crew:
        """Creates the MicrosoftTeamsActivityTrigger crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
        )

if __name__ == "__main__":
    crew = MicrosoftTeamsActivityTrigger().crew()
    crewai_trigger_payload = "PUT YOUR TRIGGER PAYLOAD HERE"
    crew.kickoff({'crewai_trigger_payload': crewai_trigger_payload})
