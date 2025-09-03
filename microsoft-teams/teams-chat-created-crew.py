from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task


@CrewBase
class MicrosoftTeamsChatCreatedTrigger:
    """MicrosoftTeamsChatCreatedTrigger crew for chat creation events"""

    @agent
    def chat_creation_analyzer(self) -> Agent:
        return Agent(
            role="Microsoft Teams Chat Creation Analyzer",
            goal="Parse Microsoft Teams chat creation payload data to extract chat details, participants, and analyze team communication patterns",
            backstory="You're an expert at parsing Microsoft Graph API payload structures for Teams chat creation events. You excel at analyzing chat types (oneOnOne, group, meeting), understanding team collaboration patterns, and assessing the business impact of new communication channels being established.",
            verbose=True
        )

    @agent
    def chat_creation_summarizer(self) -> Agent:
        return Agent(
            role="Teams Chat Creation Summarization Specialist",
            goal="Create clear summaries of chat creation events that highlight communication patterns, team collaboration, and business context",
            backstory="You're skilled at analyzing Teams chat data and providing insights into team communication patterns, collaboration effectiveness, and organizational dynamics based on chat creation activities.",
            verbose=True
        )

    @task
    def chat_creation_analysis_task(self) -> Task:
        return Task(
            description="""
            The payload contains a Microsoft Teams chat creation event with the following structure:
            - result.id: Chat ID
            - result.chatType: Type of chat (oneOnOne, group, meeting)
            - result.createdDateTime: When the chat was created
            - result.lastUpdatedDateTime: Last activity timestamp
            - result.topic: Chat topic/subject (null for oneOnOne chats)
            - result.tenantId: Organization tenant identifier
            - result.webUrl: Direct link to the chat
            - result.isHiddenForAllMembers: Visibility setting
            - result.viewpoint: User-specific view information
            - result.onlineMeetingInfo: Associated meeting data (if any)

            IMPORTANT: Extract the following information from the payload structure:

            1. Chat Identity:
               - Chat ID and web URL
               - Chat type (oneOnOne, group, meeting)
               - Creation timestamp
               - Topic/subject (if available)

            2. Organizational Context:
               - Tenant ID for organization identification
               - Chat visibility and privacy settings
               - Associated meeting information

            3. Communication Analysis:
               - Type of collaboration initiated
               - Communication channel purpose
               - Team interaction patterns
               - Business context implications

            4. Activity Assessment:
               - Chat creation timing
               - Last update information
               - User engagement indicators
               - Collaboration effectiveness potential
            """,
            expected_output="""
            A structured analysis containing:
            - Chat Information:
              * Chat ID: [Teams chat identifier]
              * Chat Type: [oneOnOne/group/meeting]
              * Created: [Creation timestamp]
              * Last Updated: [Last activity time]
              * Topic: [Chat subject if available]
            - Organization Context:
              * Tenant ID: [Organization identifier]
              * Web URL: [Direct chat access link]
              * Visibility: [Privacy and access settings]
              * Meeting Info: [Associated meeting data]
            - Communication Analysis:
              * Collaboration Type: [Direct/group/meeting-based]
              * Purpose: [Inferred chat purpose]
              * Business Context: [Organizational relevance]
              * Team Dynamics: [Communication pattern implications]
            - Engagement Assessment:
              * Activity Level: [Based on timing and updates]
              * Collaboration Potential: [Expected interaction value]
              * Business Impact: [Organizational communication effect]
            """,
            agent=self.chat_creation_analyzer
        )

    @task
    def chat_creation_summarization_task(self) -> Task:
        return Task(
            description="""
            Based on the chat creation analysis from the parsed Teams payload, create a comprehensive summary that includes:
            - The chat type and participants (inferred from type)
            - The timing and organizational context
            - Communication and collaboration insights
            - Business impact and team dynamics assessment

            IMPORTANT: Ensure the chat type and creation context are displayed prominently at the top
            of your summary as these are critical for understanding team communication patterns.
            """,
            expected_output="""
            A Teams chat creation summary in markdown format containing:
            - **Chat ID**: Teams chat identifier
            - **Chat Type**: Type of communication channel (1:1, group, meeting-based)
            - **Created**: When the chat was established
            - **Organization**: Tenant/organization context
            - **Topic**: Chat subject or purpose (if available)
            - **Access**: Web URL and visibility settings
            - **Last Activity**: Most recent update timestamp
            - **Communication Purpose**: Inferred reason for chat creation
            - **Collaboration Type**:
              - **One-on-One**: Direct communication between two team members
              - **Group Chat**: Multi-participant team discussion
              - **Meeting Chat**: Associated with scheduled meeting
            - **Business Context**: Organizational communication impact
            - **Team Dynamics**: Collaboration pattern analysis
            - **Engagement Potential**: Expected interaction value
            - **Recommended Monitoring**:
              - Track message frequency and participation
              - Monitor for important decisions or action items
              - Assess collaboration effectiveness over time

            Ensure the Chat Type and Communication Purpose are prominently displayed at the top.
            """,
            agent=self.chat_creation_summarizer,
            output_file='teams_chat_created_summary.md'
        )

    @crew
    def crew(self) -> Crew:
        """Creates the MicrosoftTeamsChatCreatedTrigger crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
        )

if __name__ == "__main__":
    crew = MicrosoftTeamsChatCreatedTrigger().crew()
    # Example payload from chat-created.json
    crewai_trigger_payload = """{
        "result": {
            "chatType": "oneOnOne",
            "createdDateTime": "2025-07-17T18:15:41.055Z",
            "id": "[REDACTED]",
            "isHiddenForAllMembers": false,
            "lastUpdatedDateTime": "2025-07-17T18:15:41.457Z",
            "onlineMeetingInfo": null,
            "tenantId": "[REDACTED]",
            "topic": null,
            "viewpoint": {
                "isHidden": false,
                "lastMessageReadDateTime": "0001-01-01T00:00:00Z"
            },
            "webUrl": "[REDACTED]"
        }
    }"""
    crew.kickoff({'crewai_trigger_payload': crewai_trigger_payload})
