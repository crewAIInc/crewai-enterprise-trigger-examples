from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task


@CrewBase
class GoogleCalendarMeetingTrigger:
    """GoogleCalendarMeetingTrigger crew for meeting events with attendees and conference data"""

    @agent
    def meeting_analyzer(self) -> Agent:
        return Agent(
            role="Google Calendar Meeting Event Analyzer",
            goal="Parse Google Calendar meeting payload data to extract attendee information, conference details, and analyze meeting collaboration patterns",
            backstory="You're an expert at parsing Google Calendar meeting events with complex attendee lists and conference data. You excel at analyzing meeting patterns, attendee response statuses, conference integrations (Zoom, Teams), and understanding team collaboration dynamics from meeting data.",
            verbose=True
        )

    @agent
    def meeting_summarizer(self) -> Agent:
        return Agent(
            role="Meeting Event Summarization Specialist",
            goal="Create clear summaries of meeting events that highlight attendee participation, conference details, and collaboration insights",
            backstory="You're skilled at analyzing meeting data and providing insights into team collaboration, meeting effectiveness, and participation patterns based on attendee responses and meeting structure.",
            verbose=True
        )

    @task
    def meeting_analysis_task(self) -> Task:
        return Task(
            description="""
            The payload contains a Google Calendar meeting event with the following structure:
            - result.id: Event ID
            - result.summary: Meeting title
            - result.description: Meeting agenda/description (may contain HTML)
            - result.start.dateTime: Meeting start time with timezone
            - result.end.dateTime: Meeting end time with timezone
            - result.attendees[]: Array of attendee objects with:
              - email: Attendee email
              - responseStatus: accepted/declined/needsAction
              - organizer: true if organizer
              - displayName: Attendee name (optional)
            - result.conferenceData: Conference/video call information:
              - conferenceSolution.name: Platform name (e.g., "Zoom Meeting")
              - entryPoints[]: Array of access methods (video, phone, etc.)
            - result.organizer: Meeting organizer information
            - result.recurringEventId: If part of recurring series

            IMPORTANT: Extract the following information:

            1. Meeting Basic Information:
               - Event ID, title, description
               - Date/time with timezone
               - Organizer information

            2. Attendee Analysis:
               - Total attendee count
               - Response status breakdown (accepted/declined/pending)
               - Organizer identification
               - Key participants

            3. Conference Details:
               - Platform type (Zoom, Teams, etc.)
               - Access methods available
               - Meeting codes/links

            4. Collaboration Insights:
               - Meeting engagement level
               - Response rate analysis
               - Team participation patterns
            """,
            expected_output="""
            A structured analysis containing:
            - Meeting Information:
              * Event ID: [Calendar event ID]
              * Title: [Meeting title]
              * Date/Time: [Start to end time with timezone]
              * Duration: [Calculated meeting length]
            - Organizer & Attendees:
              * Organizer: [Organizer name and email]
              * Total Attendees: [Count of attendees]
              * Responses: [Breakdown by status]
              * Key Participants: [Notable attendees]
            - Conference Details:
              * Platform: [Zoom/Teams/etc.]
              * Access Methods: [Video, phone, etc.]
              * Entry Points: [Meeting links/codes]
            - Collaboration Analysis:
              * Engagement Level: [Based on response rates]
              * Participation: [Team involvement assessment]
              * Meeting Type: [Recurring, one-time, etc.]
            """,
            agent=self.meeting_analyzer
        )

    @task
    def meeting_summarization_task(self) -> Task:
        return Task(
            description="""
            Create a comprehensive summary of the meeting event that includes attendee participation,
            conference details, and insights into team collaboration and meeting effectiveness.
            """,
            expected_output="""
            A meeting event summary in markdown format:
            - **Event ID**: Calendar event ID
            - **Meeting Title**: Meeting subject/title
            - **Date & Time**: Start and end times with timezone
            - **Duration**: Meeting length
            - **Organizer**: Meeting organizer name and email
            - **Attendees**: Total count and key participants
            - **Response Status**: Breakdown of accepted/declined/pending
            - **Conference Platform**: Video conferencing platform used
            - **Access Information**: Meeting links and dial-in details
            - **Agenda**: Meeting description/agenda (if provided)
            - **Summary**: Overview of meeting purpose and scope
            - **Engagement Analysis**: Attendee response and participation insights
            - **Collaboration Notes**: Team dynamics and meeting effectiveness assessment
            """,
            agent=self.meeting_summarizer,
            output_file='meeting_summary.md'
        )

    @crew
    def crew(self) -> Crew:
        """Creates the GoogleCalendarMeetingTrigger crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
        )

if __name__ == "__main__":
    crew = GoogleCalendarMeetingTrigger().crew()
    # Example payload from event-ended.json
    crewai_trigger_payload = """{
        "result": {
            "attendees": [
                {
                    "email": "user1@example.com",
                    "responseStatus": "accepted"
                },
                {
                    "email": "user2@example.com",
                    "organizer": true,
                    "responseStatus": "accepted"
                }
            ],
            "conferenceData": {
                "conferenceSolution": {
                    "name": "Zoom Meeting"
                },
                "entryPoints": [
                    {
                        "entryPointType": "video",
                        "uri": "https://zoom.us/j/123456789"
                    }
                ]
            },
            "created": "2024-11-06T14:14:40.000Z",
            "description": "Weekly sync meeting agenda",
            "end": {
                "dateTime": "2025-02-14T16:00:00-03:00",
                "timeZone": "America/Los_Angeles"
            },
            "id": "meeting123",
            "summary": "GTM and Product & Engineering Demo + Sync",
            "start": {
                "dateTime": "2025-02-14T15:00:00-03:00",
                "timeZone": "America/Los_Angeles"
            },
            "status": "confirmed"
        }
    }"""
    crew.kickoff({'crewai_trigger_payload': crewai_trigger_payload})
